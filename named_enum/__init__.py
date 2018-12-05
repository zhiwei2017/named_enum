# -*- coding: utf-8 -*-
"""
Module for the classes extending the default Enum class. It contains 3 classes
(ExtendedEnumMeta, ExtendedEnum, PairEnum) and one method namedenum.
"""
import sys as _sys
from collections import namedtuple, abc
from enum import Enum, EnumMeta, _EnumDict
from functools import partial
from collections import OrderedDict

__all__ = [
    'NamedEnumMeta', 'NamedEnum', 'PairEnum', 'namedenum'
]


class _NamedEnumDict(_EnumDict):
    """
    Customizes _EnumDict, such that it allows setting the value for the keyword
    '_field_names_' and provides the functions for cleaning itself and
    converting the collection type value (except str) to NamedTuple type.
    """

    def __setitem__(self, key, value):
        """
        Makes an exception for the single underscore name '_field_names_'.

        :param key: str: variable or function names defined in class
        :param value: different types: values or functions
        :return: None
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
        # converting the type of the value in customized tuple
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
    Extends the EnumMeta class for three purposes:

    1.  uses the _NamedEnumDict as the data type of the namespace parameter for
    __new__ function, such that we can use the namedtuple as the data type of
    the value of each enumeration item.

    2.  provides extra functions, which is independent from the value of the
    variable '_field_names_' in the NamedEnum class and its subclasses, such
    as 'names', 'values', 'as_dict', 'as_list', 'as_set',
    'as_tuple', 'as_ordereddict', 'describe', 'gen'. The aim is extending the
    Enum class for complicated use cases in software development.

    3.  provides functions for each field_name defined in '_field_names_' in the
    NamedEnum class and its subclasses, for example 'key' is included in
    '_field_names_', then the functions for this field_name are:
    'keys', 'from_key', 'has_key'.
    """
    @classmethod
    def __prepare__(mcs, cls, bases):
        """
        Namespace hook, uses _NamedEnumDict as the type of namespace instead of
        _EnumDict.

        :param cls: str: name of the class to create
        :param bases: tuple: parent classes of the class to create
        :return: namespace dictionary
        """
        # create the namespace dict
        enum_dict = _NamedEnumDict()
        # inherit previous flags and _generate_next_value_ function
        member_type, first_enum = mcs._get_mixins_(bases)
        if first_enum is not None:
            enum_dict['_generate_next_value_'] = getattr(
                first_enum, '_generate_next_value_', None)
        return enum_dict

    def __new__(mcs, name, bases, namespace):
        """
        Besides the class creation, this function also intends to create a named
        tuple data type depending on the given value of '_field_names_' variable
        to be the data type of the value of enumeration iem and add those extra
        functions to the class.

        :param name: str: name of the instance class
        :param bases: tuple: base classes, its instance class inherits from
        :param namespace: dict: contains the attributes and functions of the
          instance class
        :return: class object
        """
        # if the _field_names_ not defined in the class, get it from its parent
        # class; otherwise uses the defined one.
        if '_field_names_' not in namespace:
            _field_names_ = bases[0].__dict__.get('_field_names_', None)
        else:
            _field_names_ = namespace['_field_names_']
        # if the _field_names_ is not defined, then switch back to the normal
        # enum but with extended functions
        if _field_names_:
            # created the customized tuple class with the defined _field_names_
            _tuple_cls = namedtuple("NamedTuple", _field_names_)
            if {"name", "value"}.issubset(_tuple_cls._fields):
                raise AttributeError("name or value cannot be attributes")
            # _convert the type of the item in namespace dictionary to the named
            # tuple type
            namespace._convert(_tuple_cls)
            # create the class and define a class variable to hold the
            # customized tuple class. It's needed to return the field names.
            cls = super().__new__(mcs, name, bases, namespace)
            cls._tuple_cls = _tuple_cls
            # the function name formats, docstring formats and bases functions
            func_factory_mapping = [
                ("%ss",
                 "Collective function to return the values of the attribute %s "
                 "from all the enumerations in the Enum class.",
                 mcs._field_values),
                ("from_%s",
                 "Returns the corresponding enumeration(s) according to the "
                 "given value of the attribute %s.",
                 mcs._from_field),
                ("has_%s",
                 "Returns if the corresponding enumeration(s) exists according "
                 "to the given value of the attribute %s.",
                 mcs._has_field)
            ]
            # function creation factory: create functions for each field_name
            for field_name in cls._fields():
                for name, docstring, mcs_func in func_factory_mapping:
                    func_name = name % field_name
                    func_docstring = docstring % field_name
                    setattr(cls, func_name, partial(mcs_func, cls, field_name))
                    # override the docstring of the partial function
                    getattr(cls, func_name).__doc__ = func_docstring
        else:
            cls = super().__new__(mcs, name, bases, namespace)
        return cls

    def _fields(cls):
        """
        Returns the defined field names for the enumeration class. Since the
        customized tuple class contains the field names, just render it in
        enumeration level. If the _field_names_ is None or empty value, then
        return an empty list, since it's a kind of default Enum class

        :return: list of field names
        """
        if cls._field_names_:
            return cls._tuple_cls._fields
        return tuple()

    @classmethod
    def _field_values(mcs, cls, field_name, as_tuple=True):
        """
        Base function returns a tuple/generator containing just the value of the
        given field_name of all the elements from the cls.
        It's used to generate the particular function with name format
        <field_name>s for each field_name.

        :param cls: Enum class: subclass of NamedEnum class
        :param field_name: str: attribute's name
        :param as_tuple: bool: returns a tuple of the values if True; otherwise
          returns a generator
        :return: tuple of different types/ generator
        """
        g = (getattr(item.value, field_name)
             for item in cls.gen(name_value_pair=False))
        return tuple(g) if as_tuple else g

    @classmethod
    def _from_field(mcs, cls, field_name, field_value, as_tuple=True):
        """
        Base function returns a tuple of the defined enumeration item(s)
        regarding to the given field's name and value, or None if not found for
        the given cls.
        It's used to generate the particular function with name format
        from_<field_name> for each field_name.

        :param cls: Enum class: subclass of NamedEnum class
        :param field_name: str: attribute's name
        :param field_value: different values: key to search for
        :param as_tuple: bool: returns a tuple of the value if True; otherwise
          returns a generator
        :return: tuple of enumeration items matching the condition/ generator
        """
        g = (item for item in cls.gen(name_value_pair=False)
             if getattr(item.value, field_name) == field_value)
        return tuple(g) if as_tuple else g

    @classmethod
    def _has_field(mcs, cls, field_name, field_value):
        """
        Base function returns a boolean value which identifies if there is at
        least one enumeration item whose field_name's corresponding value
        matches the given field_value.
        It's used to generate the particular function with name format
        has_<field_name> for each field_name.

        :param cls: Enum class: subclass of NamedEnum class
        :param field_name: str: attribute's name
        :param field_value: different values: key to search for
        :return: boolean
        """
        gen_field_values = mcs._field_values(cls, field_name, as_tuple=False)
        return field_value in gen_field_values

    def gen(cls, name_value_pair=True):
        """
        Generates a generator for the tuple of each enumeration item's name and
        value, if name_value_pair is True; otherwise a generator of the
        enumeration items.

        :param name_value_pair: bool: controls the return result. If true,
          returns the generator of name-value pair; if False, returns the
          generator of the enumeration items.
        :return: generator
        """
        if name_value_pair:
            return ((name, item.value) for name, item in cls._member_map_.items())
        return (item for name, item in cls._member_map_.items())

    def _as_data_type(cls, data_type):
        """
        Base function converts the enumeration class to the given data type
        value.
        It's used to generate the functions like as_dict, as_tuple, as_set,
        as_list, as_ordereddict.

        :param cls: Enum class: subclass of NamedEnum class
        :param data_type: different data type: dict, list, set, tuple,
          OrderedDict
        :return: converted value depending on the given data type
        """
        return data_type(cls.gen())

    def as_dict(cls):
        """
        Converts the enumerations to a dictionary, in which the key is the name
        of the enumeration item and value is the corresponding enumeration
        item's value

        :return: dict
        """
        return cls._as_data_type(dict)

    def as_tuple(cls):
        """
        Converts the enumerations to a tuple, in which each item is a tuple of
        the enumeration item's name and value

        :return: tuple
        """
        return cls._as_data_type(tuple)

    def as_set(cls):
        """
        Converts the enumerations to a set, in which each item is a tuple of
        the enumeration item's name and value

        :return: set
        """
        return cls._as_data_type(set)

    def as_list(cls):
        """
        Converts the enumerations to a list, in which each item is a tuple of
        the enumeration item's name and value

        :return: list
        """
        return cls._as_data_type(list)

    def as_ordereddict(cls):
        """
        Converts the enumerations to an OrderedDict, in which each item is a
        tuple of the enumeration item's name and value

        :return: OrderedDict
        """
        return cls._as_data_type(OrderedDict)

    def __repr__(cls):
        """
        Overrides the __repr__ function from EnumMeta class.

        :return: str
        """
        return "<named enum %r>" % cls.__name__

    def describe(cls):
        """
        Prints in the console a table showing all the fields for all the
        definitions inside the class together with the enumeration names

        :return: None
        """
        name = "name"
        max_lengths, headers = [], []
        fields = cls._fields() if cls._fields() else ("value",)
        row_format = ["{:>%d}"] * (len(fields) + 1)
        names = [name] + list(cls.names())
        max_lengths.append(max(list(map(len, names))))
        headers.append(name.capitalize())
        for attr_name in fields:
            attr_func = "%ss" % attr_name
            attr_list = list(map(str, getattr(cls, attr_func)()))
            max_lengths.append(max(list(map(len, [attr_name] + attr_list))))
            headers.append(attr_name.capitalize())
        row_format = " | ".join(row_format) % tuple(max_lengths)
        header_line = row_format.format(*headers)
        output = "Class: %s\n" % cls.__name__
        output += header_line + "\n"
        output += "-" * (len(header_line)) + "\n"
        if cls._fields():
            for name, value in cls.gen():
                output += row_format.format(name, *value) + "\n"
        else:
            for name, value in cls.gen():
                output += row_format.format(name, str(value)) + "\n"
        print(output)

    def names(cls, as_tuple=True):
        """
        Returns the names of the enumeration items as a tuple, if as_tuple is
        True, otherwise returns a generator.

        :return: tuple
        """
        g = (name for name in cls._member_map_.keys())
        return tuple(g) if as_tuple else g

    def values(cls, as_tuple=True):
        """
        Returns the values of the enumeration items as a tuple, if as_tuple is
        True, otherwise returns a generator.

        :return: tuple
        """
        g = (item.value for item in cls._member_map_.values())
        return tuple(g) if as_tuple else g


class NamedEnum(Enum, metaclass=NamedEnumMeta):
    """
    Through the value of variable '_field_names_' to control its subclass for
    different use cases:

    1.  value of '_field_names_' is None or empty value. In this case, its
    subclass works like an extended Enum class with extra function:
    'names', 'values', 'as_dict', 'as_list', 'as_set', 'as_tuple',
    'as_ordereddict', 'describe'.

    2.  value of '_field_names_' is neither None or empty. In this case, its
    subclass keeps the extra functions in 1. mentioned, gives each element
    in the enumeration item's value a name and provides functions for each
    attribute/field name, like '<field_name>s', 'from_<field_name>',
    'has_<field_name>'.

    Instead of the setting the attributes to the enumeration instance, it uses
    the function __getattr__ to achieve it.

    >>> class TripleEnum(NamedEnum):
    ...     _field_names_ = ("first", "second", "third")
    >>> class Triangle(TripleEnum):
    ...     EQUILATERAL = (6, 6, 6)
    ...     RIGHT = (3, 4, 5)
    >>> Triangle._fields()
    ('first', 'second', 'third')
    >>> Triangle.names()
    ('EQUILATERAL', 'RIGHT')
    >>> Triangle.values()
    (NamedTuple(first=6, second=6, third=6), NamedTuple(first=3, second=4, third=5))
    >>> Triangle.describe()
    Class: Triangle
           Name | First | Second | Third
    ------------------------------------
    EQUILATERAL |     6 |      6 |     6
          RIGHT |     3 |      4 |     5
    <BLANKLINE>
    >>> Triangle.as_dict()
    {'EQUILATERAL': NamedTuple(first=6, second=6, third=6), 'RIGHT': NamedTuple(first=3, second=4, third=5)}
    >>> Triangle.as_list()
    [('EQUILATERAL', NamedTuple(first=6, second=6, third=6)), ('RIGHT', NamedTuple(first=3, second=4, third=5))]
    >>> from collections import namedtuple
    >>> NamedTuple = namedtuple("NamedTuple", "first, second, third")
    >>> Triangle.as_set() == {('RIGHT', NamedTuple(first=3, second=4, third=5)), ('EQUILATERAL', NamedTuple(first=6, second=6, third=6))}
    True
    >>> Triangle.as_tuple()
    (('EQUILATERAL', NamedTuple(first=6, second=6, third=6)), ('RIGHT', NamedTuple(first=3, second=4, third=5)))
    >>> Triangle.as_ordereddict()
    OrderedDict([('EQUILATERAL', NamedTuple(first=6, second=6, third=6)), ('RIGHT', NamedTuple(first=3, second=4, third=5))])
    >>> Triangle.firsts()
    (6, 3)
    >>> Triangle.seconds()
    (6, 4)
    >>> Triangle.thirds()
    (6, 5)
    >>> Triangle.from_first(6)
    (<Triangle.EQUILATERAL: NamedTuple(first=6, second=6, third=6)>,)
    >>> Triangle.from_first(66)
    ()
    >>> Triangle.from_second(6)
    (<Triangle.EQUILATERAL: NamedTuple(first=6, second=6, third=6)>,)
    >>> Triangle.from_second(66)
    ()
    >>> Triangle.from_third(6)
    (<Triangle.EQUILATERAL: NamedTuple(first=6, second=6, third=6)>,)
    >>> Triangle.from_third(66)
    ()
    >>> Triangle.has_first(6)
    True
    >>> Triangle.has_first(66)
    False
    >>> Triangle.has_second(6)
    True
    >>> Triangle.has_second(66)
    False
    >>> Triangle.has_third(6)
    True
    >>> Triangle.has_third(66)
    False
    >>> Triangle.RIGHT
    <Triangle.RIGHT: NamedTuple(first=3, second=4, third=5)>
    >>> Triangle.RIGHT.first
    3
    >>> Triangle.RIGHT.second
    4
    >>> Triangle.RIGHT.third
    5
    >>> Triangle.RIGHT.name
    'RIGHT'
    >>> Triangle.RIGHT.value
    NamedTuple(first=3, second=4, third=5)
    >>> print(Triangle.RIGHT)
    Triangle.RIGHT: NamedTuple(first=3, second=4, third=5)
    """
    _field_names_ = None
    """
    The place to define the field names of the enumeration class. It accepts the 
    same format as the parameter 'field_names' in function namedtuple from 
    collection package. 
    It's used in the NamedEnumMeta class's '__new__' function to generate the 
    corresponding functions for each field.
    If it's value is None or empty, then the enumeration class behaves like a 
    normal Enum class, but with some extended functions to simplify the usages 
    of enumerations.

    Attention: this variable should not be used to get the field_names, to do
    so you can use the class method '_fields'. Because it also accept the comma 
    separated string.
    """

    def __getattr__(self, item):
        """
        Hijacks the default __getattr__ function, such that every time when the
        user wants to get the value of a field in an enumeration item, it
        returns the corresponding field's value from the value of enumeration.

        :param item: str: name of the field or attribute
        :return: different types
        """
        if item in self.__class__._fields():
            return getattr(self._value_, item)
        return super().__getattribute__(item)

    def __str__(self):
        """
        Displays the value as well.

        :return: str
        """
        return "%s.%s: %r" % (
            self.__class__.__name__, self._name_, self._value_)


class PairEnum(NamedEnum):
    """
    Enumeration with two attributes "first", "second", the idea comes from the
    C++'s pair container.
    """
    _field_names_ = ("first", "second")


_class_template = """\
from named_enum import NamedEnum


class {typename}(NamedEnum):

    _field_names_ = {field_names!r}

"""


def namedenum(typename, field_names=None, *, verbose=False, module=None):
    """
    Creates an named enum class with the given typename as class name and
    field_names as the _field_names_ in named enum class. The implementation is
    similar to the namedtuple function.

    :param typename: str: name of the create class
    :param field_names: Sequence: field names for the named enum class
    :param verbose: bool: displays the code for the named enum class creation,
      if True
    :param module: None/str: which module, the new created enum class belongs to
    :return: subclass of NamedEnum

    >>> TripleEnum = namedenum("TripleEnum", ("first", "second", "third"))
    >>> TripleEnum
    <named enum 'TripleEnum'>
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
