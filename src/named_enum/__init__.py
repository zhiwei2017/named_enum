# -*- coding: utf-8 -*-
"""
Module for the classes extending the default Enum class. It contains 3 classes:
ExtendedEnumMeta, ExtendedEnum, TripleEnum.
"""
import sys as _sys
from collections import namedtuple, abc
from enum import Enum, EnumMeta, _EnumDict
from functools import partial

__all__ = [
    'NamedEnumMeta', 'NamedEnum', 'PairEnum', 'namedenum'
]


class _NamedEnumDict(_EnumDict):
    """
    Customizes _EnumDict, such that it will accept the '_field_names_'.
    """

    def __setitem__(self, key, value):
        """
        Makes an exception for the single underscore name '_field_names_'.
        """
        if key == '_field_names_':
            dict.__setitem__(self, key, value)
        else:
            super().__setitem__(key, value)

    def _clean(self):
        """
        Removes all the items, and set the variables '_member_names' and
        '_last_values' to empty.

        :return: None
        """
        # for dictionary, that's the only way to _clean it
        for name in self._member_names:
            del self[name]
        # _clean the variables as well
        self._member_names, self._last_values = [], []

    def _convert(self, tuple_cls):
        """
        Uses the given tuple class to _convert the items.

        :param tuple_cls: customized tuple class: using namedtuple generated
          tuple class
        :return: None
        """
        _member_names = self._member_names
        _last_values = []
        for value in self._last_values:
            if isinstance(value, abc.Collection) and not isinstance(value, str):
                _last_values.append(tuple_cls(*value))
            else:
                _last_values.append(tuple_cls(value))
        self._clean()

        # put the converted items back, the __setitem__ function in _EnumDict
        # will fill the variables, like '_member_names' and '_last_values'
        for i, name in enumerate(_member_names):
            self[name] = _last_values[i]


class NamedEnumMeta(EnumMeta):
    """
    Extends the EnumMeta class with several functions according to the value of
    class variable '_field_names_' in Enumeration class.
    It will create two kinds of functions for each field name:
    1. one returns the collective results of the same field name from all
       enumerations of the same Enumeration class
    2. the other one returns the enumeration according to the given value of the
       specific field_name
    """

    @classmethod
    def __prepare__(mcs, cls, bases):
        """
        Namespace hook, uses _NamedEnumDict as the type of namespace

        :param cls: str: name of the class to create
        :param bases: tuple: parent classes of the class to create
        :return: namespace dictionary
        """
        # create the namespace dict
        enum_dict = _NamedEnumDict()
        # inherit previous flags and _generate_next_value_ function
        member_type, first_enum = mcs._get_mixins_(bases)
        if first_enum is not None:
            enum_dict['_generate_next_value_'] = getattr(first_enum, '_generate_next_value_', None)
        return enum_dict

    def __new__(mcs, name, bases, namespace):
        """
        Intends to create the functions with name formats:
        <field_name>s and from_<field_name>
        for each field_name defined in the class variable _field_names_.

        :param name: str: name of the instance class
        :param bases: tuple: base classes, its instance class inherits from
        :param namespace: dict: contains the attributes and functions of the
          instance class
        :return: class object
        """
        # if the _field_names_ not defined in the class, get it from its parent
        # class; otherwise uses the one defined inside.
        if '_field_names_' not in namespace:
            _field_names_ = bases[0].__dict__['_field_names_']
        else:
            _field_names_ = namespace['_field_names_']
        # created the customized tuple class with the defined field_names
        _tuple_cls = namedtuple("NamedTuple", _field_names_)
        # _convert the type of the item in namespace dictionary
        namespace._convert(_tuple_cls)
        # declare teh class and assign the customized tuple class as a variable
        # in it
        cls = super().__new__(mcs, name, bases, namespace)
        cls._tuple_cls = _tuple_cls
        # the function name formats, docstring formats and bases functions
        func_name_and_doc = [
            ("%ss",
             "Collective function to return the values of the attribute %s from"
             " all the enumerations in the Enum class.",
             mcs._field_values),
            ("from_%s",
             "Returns the corresponding enumeration according to the given "
             "value of the attribute %s.",
             mcs._from_field)
        ]
        # function creation factory.
        for field_name in cls._fields():
            for name, docstring, meta_func in func_name_and_doc:
                func_name = name % field_name
                func_docstring = docstring % field_name
                setattr(cls, func_name, partial(meta_func, cls, field_name))
                # override the docstring of the partial function
                getattr(cls, func_name).__doc__ = func_docstring
        return cls

    @classmethod
    def _field_values(mcs, cls, field_name):
        """
        Returns a tuple containing just the value of the given field_name of all
        the elements from the cls.

        :return: tuple of different types
        """
        return tuple(map(lambda x: getattr(x, field_name), list(cls)))

    @classmethod
    def _from_field(mcs, cls, field_name, field_value):
        """
        Returns the first defined enumeration item regarding to the given
        field's name and value, or None if not found for the given cls

        :param field_name: str: attribute's name
        :param field_value: different values: key to search for
        :return: Enumeration Item
        """
        return next(iter(filter(lambda x: getattr(x, field_name) == field_value,
                                list(cls))), None)

    def __repr__(cls):
        """
        Overrides the __repr__ function from EnumMeta class.

        :return:
        """
        return "<named enum %r>" % cls.__name__

    def tuples(cls):
        """
        Returns a tuple formed by fields for all the elements inside the class.

        :return: tuple of n-elements-tuples
        """
        return tuple(cls._value2member_map_.keys())

    def _fields(cls):
        """
        Returns the defined field names for each enumeration item. Since the
        customized tuple class contains the field names, just render it in
        enumeration level.

        :return: list of field names
        """
        return cls._tuple_cls._fields

    def describe(cls):
        """
        Prints in the console a table showing all the fields for all the
        definitions inside the class

        :return: None
        """
        max_lengths = []
        headers = []
        row_format = ["{:>%d}"] * len(cls._fields())
        for attr_name in cls._fields():
            attr_func = "%ss" % attr_name
            attr_list = list(map(str, getattr(cls, attr_func)())) + [attr_name]
            max_lengths.append(max(list(map(len, attr_list))))
            headers.append(attr_name.capitalize())
        row_format = " | ".join(row_format) % tuple(max_lengths)
        header_line = row_format.format(*headers)
        output = "Class: %s\n" % cls.__name__
        output += header_line + "\n"
        output += "-" * (len(header_line)) + "\n"
        for item in cls:
            enum_val = item._value_
            output += row_format.format(*enum_val) + "\n"
        print(output)


class NamedEnum(Enum, metaclass=NamedEnumMeta):
    """
    Abstract class with ("key", ) as the default value of _field_names_,
    functions like 'tuples', '_fields', 'describe' are defined directly for the
    subclasses.
    Instead of the setting the attributes to the class instance, it uses the
    function __getattr__ to achieve it.

    >>> class TripleEnum(NamedEnum):
    ...     _field_names_ = ("first", "second", "third")
    >>> class Triangle(TripleEnum):
    ...     EQUILATERAL = (6, 6, 6)
    ...     RIGHT = (3, 4, 5)
    >>> Triangle._fields()
    ('first', 'second', 'third')
    >>> Triangle.tuples()
    (NamedTuple(first=6, second=6, third=6), NamedTuple(first=3, second=4, third=5))
    >>> Triangle.firsts()
    (6, 3)
    >>> Triangle.seconds()
    (6, 4)
    >>> Triangle.thirds()
    (6, 5)
    >>> Triangle.from_first(6)
    <Triangle.EQUILATERAL: NamedTuple(first=6, second=6, third=6)>
    >>> Triangle.from_second(6)
    <Triangle.EQUILATERAL: NamedTuple(first=6, second=6, third=6)>
    >>> Triangle.from_third(6)
    <Triangle.EQUILATERAL: NamedTuple(first=6, second=6, third=6)>
    >>> Triangle.RIGHT
    <Triangle.RIGHT: NamedTuple(first=3, second=4, third=5)>
    >>> Triangle.RIGHT.first
    3
    >>> Triangle.RIGHT.second
    4
    >>> Triangle.RIGHT.third
    5
    >>> Triangle.describe()
    Class: Triangle
    First | Second | Third
    ----------------------
        6 |      6 |     6
        3 |      4 |     5
    <BLANKLINE>
    >>> Triangle.RIGHT.value
    NamedTuple(first=3, second=4, third=5)
    >>> Triangle.RIGHT.name
    'RIGHT'

    """
    _field_names_ = ("key",)
    """
    The place to define the field names of the enumeration item. It accepts the 
    same format as the parameter 'field_names' in function namedtuple. 
    It's used in the NamedEnumMeta class's __new__function to generate the 
    corresponding functions for each field.

    Attention: this variable should not be used to get the field_names, to do
    so you can use the class method '_fields'. Because it also accept the comma 
    separated string.
    """

    def __getattr__(self, item):
        """
        Hijacks the default __getattr__ function, such that every time when the
        user wants to get the value of a field in an enumeration, it returns the
        value from the customized tuple class.

        :param item: str: name of the field or attribute
        :return: different types
        """
        if item in self.__class__._fields():
            return getattr(self._value_, item)
        return super().__getattr__(item)

    def __str__(self):
        """
        Displays the value as well.

        :return:
        """
        return "%s.%s: %r" % (
            self.__class__.__name__, self._name_, self._value_)


class PairEnum(NamedEnum):
    """
    Enumeration with two attributes "first", "second", the idea comes from the
    C++'s pair container.

    >>> class Couple(PairEnum):
    ...     SMITHS = ("John", "Jane")
    ...     BIEBERS = ("Justin", "Hailey")
    >>> Couple._fields()
    ('first', 'second')
    >>> Couple.tuples()
    (NamedTuple(first='John', second='Jane'), NamedTuple(first='Justin', second='Hailey'))
    >>> Couple.firsts()
    ('John', 'Justin')
    >>> Couple.seconds()
    ('Jane', 'Hailey')
    >>> Couple.from_first("John")
    <Couple.SMITHS: NamedTuple(first='John', second='Jane')>
    >>> Couple.from_second("Jane")
    <Couple.SMITHS: NamedTuple(first='John', second='Jane')>
    >>> Couple.BIEBERS
    <Couple.BIEBERS: NamedTuple(first='Justin', second='Hailey')>
    >>> Couple.BIEBERS.first
    'Justin'
    >>> Couple.BIEBERS.second
    'Hailey'
    >>> Couple.describe()
    Class: Couple
     First | Second
    ---------------
      John |   Jane
    Justin | Hailey
    <BLANKLINE>
    >>> Couple.BIEBERS.value
    NamedTuple(first='Justin', second='Hailey')
    >>> Couple.BIEBERS.name
    'BIEBERS'
    """
    _field_names_ = ("first", "second")


_class_template = """\
from named_enum import NamedEnum


class {typename}(NamedEnum):
    '''
    {typename} is a named enumeration, which provides the normal functions 
    "tuples", "describe" and special functions like <field_name>s, 
    from_<field_name> for each field name defined in variable '_field_names_'.
    '''
    _field_names_ = {field_names!r}

"""


def namedenum(typename, field_names, *, verbose=False, module=None):
    """
    Creates an named enum class with the given typename as class name and
    field_names as the _field_names_ in named enum class.

    :param typename: str: name of the create class
    :param field_names: Sequence: field names for the named enum class
    :param verbose: bool: displays the code for the named enum class creation,
      if True
    :param module: None/str: which module, the new created enum class belongs to
    :return: subclass of NamedEnum

    >>> TripleEnum = namedenum("TripleEnum", ("first", "second", "third"))
    >>> class Triangle(TripleEnum):
    ...     EQUILATERAL = (6, 6, 6)
    ...     RIGHT = (3, 4, 5)
    >>> Triangle._fields()
    ('first', 'second', 'third')
    >>> Triangle.tuples()
    (NamedTuple(first=6, second=6, third=6), NamedTuple(first=3, second=4, third=5))
    >>> Triangle.firsts()
    (6, 3)
    >>> Triangle.seconds()
    (6, 4)
    >>> Triangle.thirds()
    (6, 5)
    >>> Triangle.from_first(6)
    <Triangle.EQUILATERAL: NamedTuple(first=6, second=6, third=6)>
    >>> Triangle.from_second(6)
    <Triangle.EQUILATERAL: NamedTuple(first=6, second=6, third=6)>
    >>> Triangle.from_third(6)
    <Triangle.EQUILATERAL: NamedTuple(first=6, second=6, third=6)>
    >>> Triangle.RIGHT
    <Triangle.RIGHT: NamedTuple(first=3, second=4, third=5)>
    >>> Triangle.RIGHT.first
    3
    >>> Triangle.RIGHT.second
    4
    >>> Triangle.RIGHT.third
    5
    >>> Triangle.describe()
    Class: Triangle
    First | Second | Third
    ----------------------
        6 |      6 |     6
        3 |      4 |     5
    <BLANKLINE>
    >>> Triangle.RIGHT.value
    NamedTuple(first=3, second=4, third=5)
    >>> Triangle.RIGHT.name
    'RIGHT'
    """
    # Fill-in the class template
    class_definition = _class_template.format(
        typename=typename,
        field_names=field_names
    )

    # Execute the template string in a temporary namespace and support
    # tracing utilities by setting a value for frame.f_globals['__name__']
    namespace = dict(__name__='%s' % typename)
    exec(class_definition, namespace)
    result = namespace[typename]
    result._source = class_definition
    if verbose:
        print(result._source)

    # For pickling to work, the __module__ variable needs to be set to the frame
    # where the named tuple is created.  Bypass this step in environments where
    # sys._getframe is not defined (Jython for example) or sys._getframe is not
    # defined for arguments greater than 0 (IronPython), or where the user has
    # specified a particular module.
    if module is None:
        try:
            module = _sys._getframe(1).f_globals.get('__name__', '__main__')
        except (AttributeError, ValueError):
            pass
    if module is not None:
        result.__module__ = module

    return result
