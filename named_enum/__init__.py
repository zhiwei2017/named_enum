# -*- coding: utf-8 -*-
"""
Module for the classes extending the default `Enum` class. It contains 5 classes:
`ExtendedEnumMeta`, `ExtendedEnum`, `ExtendedEnum`, `LabeledEnum`, `PairEnum`
and one method `namedenum`.
"""
import sys as _sys
from collections import namedtuple
from collections.abc import Sequence
from enum import Enum, EnumMeta, _EnumDict
from functools import partial
from collections import OrderedDict

__all__ = [
    'NamedEnumMeta', 'NamedEnum', 'ExtendedEnum', 'LabeledEnum', 'PairEnum',
    'namedenum'
]


class _NamedEnumDict(_EnumDict):
    """Customizes _EnumDict, such that it allows setting the value for the keyword
    '_field_names_' and provides the functions for cleaning itself and
    converting the collection type value (except str) to NamedTuple type.
    """

    def __setitem__(self, key, value):
        """
        Makes an exception for the single underscore name '_field_names_'.

        :param key: variable or function names defined in class
        :type key: str
        :param value: values or functions
        :type value: int, str, object, ...
        """
        if key == '_field_names_':
            dict.__setitem__(self, key, value)
        else:
            super().__setitem__(key, value)

    def _clean(self):
        """Removes all the items, and set the variables '_member_names' and
        '_last_values' to empty.
        """
        # for dictionary, that's the only way to _clean it
        for name in self._member_names:
            del self[name]
        # _clean the variables as well
        self._member_names, self._last_values = [], []

    def _convert(self, tuple_cls):
        """Uses the given tuple class to _convert the items.

        :param tuple_cls: using namedtuple generated
          tuple class
        :type tuple_cls: customized tuple class
        """
        if tuple_cls is tuple or not issubclass(tuple_cls, tuple):
            raise ValueError("'tuple_cls' must be a customized tuple class "
                             "using namedtuple generated.")
        _member_names = self._member_names
        _last_values = []
        feature_num = len(getattr(tuple_cls, '_fields'))

        if feature_num == 1:
            # converting the type of the value in customized tuple
            for value in self._last_values:
                _last_values.append(tuple_cls(value))
        else:
            # converting the type of the value in customized tuple
            for value in self._last_values:
                if not isinstance(value, Sequence):
                    raise ValueError("unable to unpack the value for the fields.")
                elif isinstance(value, str):
                    _last_values.append(tuple_cls(value))
                else:
                    _last_values.append(tuple_cls(*value))
        self._clean()

        # put the converted items back, the __setitem__ function in _EnumDict
        # will fill the variables, like '_member_names' and '_last_values'
        for i, name in enumerate(_member_names):
            self[name] = _last_values[i]


class NamedEnumMeta(EnumMeta):
    """Extends the `EnumMeta` class for three purposes:

    1.  uses the `_NamedEnumDict` as the data type of the `namespace` parameter
    for `__new__` function, such that we can use the `namedtuple` as the data
    type of the value of each enumeration item.

    2.  provides extra functions, which is independent of the variable
    `_field_names_`, such as `names`, `values`, `as_dict`, `as_list`, `as_set`,
    `as_tuple`, `as_ordereddict`, `describe`, `gen`. The aim is extending the
    Enum class for complicated use cases in software development.

    3.  provides functions for each field name defined in class variable
    `_field_names_` in the NamedEnum class and its subclasses, for example:

    assuming `'key'` is included in `_field_names_`, then the functions for this
    field name are: `keys`, `from_key`, `has_key`.
    """
    @classmethod
    def __prepare__(mcs, cls, bases):
        """Namespace hook, uses _NamedEnumDict as the type of namespace instead of
        _EnumDict.

        :param cls: name of the class to create
        :type cls: str
        :param bases: parent classes of the class to create
        :type bases: tuple
        :return: namespace dictionary
        :rtype: _NamedEnumDict
        """
        # create the namespace dict
        enum_dict = _NamedEnumDict()
        # inherit previous flags and _generate_next_value_ function
        if _sys.version_info >= (3, 8):
            enum_dict._cls_name = cls
            # inherit previous flags and _generate_next_value_ function
            member_type, first_enum = mcs._get_mixins_(cls, bases)
        else:
            member_type, first_enum = mcs._get_mixins_(bases)
        if first_enum is not None:
            enum_dict['_generate_next_value_'] = getattr(
                first_enum, '_generate_next_value_', None)
        return enum_dict

    def __new__(mcs, name, bases, namespace):
        """Besides the class creation, this function also intends to create a named
        tuple data type depending on the given value of '_field_names_' variable
        to be the data type of the value of enumeration iem and add those extra
        functions to the class.

        :param name: name of the instance class
        :type name: str
        :param bases: base classes, its instance class inherits from
        :type bases: tuple
        :param namespace: contains the attributes and functions of the
          instance class
        :type namespace: dict
        :return: class object
        :rtype: object
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
                raise AttributeError("'name' or 'value' cannot be attributes")
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
                 "Collective method to return the values of the attribute `%s` "
                 "from all the enumeration items.",
                 mcs._field_values),
                ("from_%s",
                 "Returns a tuple of the defined enumeration items regarding to "
                 "the given `field_value` of field `%s`, if `as_tuple` is True; "
                 "otherwise returns a generator.",
                 mcs._from_field),
                ("has_%s",
                 "Returns a boolean value which indicates if there is at least "
                 "one enumeration item in which the value of the field `%s` "
                 "matches the given field_value.",
                 mcs._has_field)
            ]
            # function creation factory: create functions for each field_name
            for field_name in cls._fields():
                for name, docstring, mcs_func in func_factory_mapping:
                    func_name = name % field_name
                    func_docstring = docstring % field_name
                    setattr(cls, func_name, partial(mcs_func, cls, field_name))
                    # override the docstring of the partial function
                    par_func = getattr(cls, func_name)
                    par_func.__doc__ = func_docstring
                    par_func.__name__ = func_name
            cls._tuple_cls = _tuple_cls
        else:
            cls = super().__new__(mcs, name, bases, namespace)
        return cls

    def __contains__(cls, member):
        """Overrides the magic method in Enum class, which doesn't support
        member name search from python 3.8.

        :param member: the lookup value
        :type member: str | Enum class
        :return: if the member is contained in the enumeration.
        :rtype: bool
        """
        if isinstance(member, str):
            return member in cls._member_map_
        return isinstance(member, cls) and member._name_ in cls._member_map_

    def _fields(cls):
        """Returns the defined field names as a `tuple` for the enumeration class.

        If the variable `_field_names_` is `None` or empty value, then
        returns an empty `tuple`.

        :return: tuple of field names
        :rtype: tuple

        >>> class TripleEnum(NamedEnum):
        ...     _field_names_ = ("first", "second", "third")
        >>> TripleEnum._fields()
        ('first', 'second', 'third')
        >>> class Triangle(TripleEnum):
        ...     EQUILATERAL = (6, 6, 6)
        ...     RIGHT = (3, 4, 5)
        >>> Triangle._fields()
        ('first', 'second', 'third')
        """
        if cls._field_names_:
            return cls._tuple_cls._fields
        return tuple()

    @classmethod
    def _field_values(mcs, cls, field_name, as_tuple=True):
        """Base function returns a `tuple`/`generator` containing just the value of the
        given field_name of all the elements from the cls.

        It's used to generate the particular function with name format
        `<field_name>s` for each `field_name`.

        :param cls: subclass of NamedEnum class
        :type cls: Enum class
        :param field_name: attribute's name
        :type field_name: str
        :param as_tuple: returns a tuple of the values if True; otherwise
          returns a generator
        :type as_tuple: bool
        :return: corresponding values of the field name in all enumeration items
        :rtype: tuple_, Generator_
        """
        g = (getattr(item.value, field_name)
             for item in cls.gen(name_value_pair=False))
        return tuple(g) if as_tuple else g

    @classmethod
    def _from_field(mcs, cls, field_name, field_value, as_tuple=True):
        """Base function returns a `tuple` of the defined enumeration items
        regarding to the given `field_value` of field with `field_name`, if
        `as_tuple` is True; otherwise returns a generator.

        It's used to generate the particular function with name format
        `from_<field_name>` for each `field_name`.

        :param cls: subclass of NamedEnum class
        :type cls: Enum class
        :param field_name: attribute's name
        :type field_name: str
        :param field_value: key to search for
        :type field_value: int, str, object, ...
        :param as_tuple: returns a tuple of the values if True; otherwise
          returns a generator
        :type as_tuple: bool
        :return: collection of enumeration items matching the condition
        :rtype: tuple_, Generator_
        """
        g = (item for item in cls.gen(name_value_pair=False)
             if getattr(item.value, field_name) == field_value)
        return tuple(g) if as_tuple else g

    @classmethod
    def _has_field(mcs, cls, field_name, field_value):
        """Base function returns a boolean value which indicates if there is at
        least one enumeration item in which the value of the field `field_name`
        corresponding value matches the given `field_value`.

        It's used to generate the particular function with name format
        `has_<field_name>` for each `field_name`.

        :param cls: subclass of NamedEnum class
        :type cls: Enum class
        :param field_name: attribute's name
        :type field_name: str
        :param field_value: key to search for
        :type field_value: int, str, object, ...
        :return: True, if has at least one matching; otherwise False.
        :rtype: bool
        """
        gen_field_values = mcs._field_values(cls, field_name, as_tuple=False)
        return field_value in gen_field_values

    def gen(cls, name_value_pair=True):
        """Returns a generator of pairs consisting of each enumeration item's name
        and value, if name_value_pair is True; otherwise a generator of the
        enumeration items.

        :param name_value_pair: controls the return result. If true,
          returns the generator of name-value pair; if False, returns the
          generator of the enumeration items.
        :type name_value_pair: bool
        :return: a generator which iterates all the enumeration items
        :rtype: Generator_

        >>> from types import GeneratorType
        >>> class TripleEnum(NamedEnum):
        ...     _field_names_ = ("first", "second", "third")
        >>> class Triangle(TripleEnum):
        ...     EQUILATERAL = (6, 6, 6)
        ...     RIGHT = (3, 4, 5)
        >>> isinstance(TripleEnum.gen(), GeneratorType)
        True
        >>> list(TripleEnum.gen())
        []
        >>> isinstance(TripleEnum.gen(name_value_pair=False), GeneratorType)
        True
        >>> list(TripleEnum.gen(name_value_pair=False))
        []
        >>> isinstance(Triangle.gen(), GeneratorType)
        True
        >>> list(Triangle.gen())
        [('EQUILATERAL', NamedTuple(first=6, second=6, third=6)), ('RIGHT', NamedTuple(first=3, second=4, third=5))]
        >>> isinstance(Triangle.gen(name_value_pair=False), GeneratorType)
        True
        >>> list(Triangle.gen(name_value_pair=False))
        [<Triangle.EQUILATERAL: NamedTuple(first=6, second=6, third=6)>, <Triangle.RIGHT: NamedTuple(first=3, second=4, third=5)>]
        """
        if name_value_pair:
            return ((name, item.value) for name, item in cls._member_map_.items())
        return (item for name, item in cls._member_map_.items())

    def _as_data_type(cls, data_type):
        """Base function converts the enumeration class to the given data type
        value.

        It's used for generating the functions like `as_dict`, `as_tuple`,
        `as_set`, `as_list`, `as_ordereddict`.

        :param cls: subclass of NamedEnum class
        :type cls: Enum class
        :param data_type: desired data type for the output
        :type data_type: dict, list, set, tuple, OrderedDict_
        :return: converted value depending on the given data type
        :rtype: dict, list, set, tuple, OrderedDict_
        """
        return data_type(cls.gen(name_value_pair=True))

    def as_dict(cls):
        """Converts the enumeration to a `dict`, in which the key is the name
        of the enumeration item and value is its value.

        :return: a dictionary containing name-value-pairs of the enumeration
        :rtype: dict

        >>> class TripleEnum(NamedEnum):
        ...     _field_names_ = ("first", "second", "third")
        >>> class Triangle(TripleEnum):
        ...     EQUILATERAL = (6, 6, 6)
        ...     RIGHT = (3, 4, 5)
        >>> TripleEnum.as_dict()
        {}
        >>> Triangle.as_dict()
        {'EQUILATERAL': NamedTuple(first=6, second=6, third=6), 'RIGHT': NamedTuple(first=3, second=4, third=5)}
        """
        return cls._as_data_type(dict)

    def as_tuple(cls):
        """
        Converts the enumerations to a `tuple`, in which each item is a tuple of
        the enumeration item's name and value.

        :return: a tuple containing name-value-pairs of the enumeration
        :rtype: tuple

        >>> class TripleEnum(NamedEnum):
        ...     _field_names_ = ("first", "second", "third")
        >>> class Triangle(TripleEnum):
        ...     EQUILATERAL = (6, 6, 6)
        ...     RIGHT = (3, 4, 5)
        >>> TripleEnum.as_tuple()
        ()
        >>> Triangle.as_tuple()
        (('EQUILATERAL', NamedTuple(first=6, second=6, third=6)), ('RIGHT', NamedTuple(first=3, second=4, third=5)))
        """
        return cls._as_data_type(tuple)

    def as_set(cls):
        """
        Converts the enumerations to a `set`, in which each item is a tuple of
        the enumeration item's name and value.

        :return: a set containing name-value-pairs of the enumeration
        :rtype: set

        >>> class TripleEnum(NamedEnum):
        ...     _field_names_ = ("first", "second", "third")
        >>> class Triangle(TripleEnum):
        ...     EQUILATERAL = (6, 6, 6)
        ...     RIGHT = (3, 4, 5)
        >>> TripleEnum.as_set() == set()
        True
        >>> isinstance(Triangle.as_set(), set)
        True
        >>> dict(Triangle.as_set()) == Triangle.as_dict()
        True
        """
        return cls._as_data_type(set)

    def as_list(cls):
        """
        Converts the enumerations to a `list`, in which each item is a tuple of
        the enumeration item's name and value.

        :return: a list containing name-value-pairs of the enumeration
        :rtype: list

        >>> class TripleEnum(NamedEnum):
        ...     _field_names_ = ("first", "second", "third")
        >>> class Triangle(TripleEnum):
        ...     EQUILATERAL = (6, 6, 6)
        ...     RIGHT = (3, 4, 5)
        >>> TripleEnum.as_list()
        []
        >>> Triangle.as_list()
        [('EQUILATERAL', NamedTuple(first=6, second=6, third=6)), ('RIGHT', NamedTuple(first=3, second=4, third=5))]
        """
        return cls._as_data_type(list)

    def as_ordereddict(cls):
        """
        Converts the enumerations to an `OrderedDict`, in which each item is a
        tuple of the enumeration item's name and value.

        :return: an OrderedDict containing name-value-pairs of the enumeration
        :rtype: OrderedDict_

        >>> class TripleEnum(NamedEnum):
        ...     _field_names_ = ("first", "second", "third")
        >>> class Triangle(TripleEnum):
        ...     EQUILATERAL = (6, 6, 6)
        ...     RIGHT = (3, 4, 5)
        >>> TripleEnum.as_ordereddict()
        OrderedDict()
        >>> Triangle.as_ordereddict()
        OrderedDict([('EQUILATERAL', NamedTuple(first=6, second=6, third=6)), ('RIGHT', NamedTuple(first=3, second=4, third=5))])
        """
        return cls._as_data_type(OrderedDict)

    def __repr__(cls):
        """
        Overrides the __repr__ function from EnumMeta class.

        :return: string represents the class
        :rtype: str
        """
        return "<named enum %r>" % cls.__name__

    def describe(cls):
        """
        Prints in the console a table showing the content of the enumeration.

        >>> class TripleEnum(NamedEnum):
        ...     _field_names_ = ("first", "second", "third")
        >>> class Triangle(TripleEnum):
        ...     EQUILATERAL = (6, 6, 6)
        ...     RIGHT = (3, 4, 5)
        >>> TripleEnum.describe()
        Class: TripleEnum
        Name | First | Second | Third
        -----------------------------
        <BLANKLINE>
        >>> Triangle.describe()
        Class: Triangle
               Name | First | Second | Third
        ------------------------------------
        EQUILATERAL |     6 |      6 |     6
              RIGHT |     3 |      4 |     5
        <BLANKLINE>
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
        Returns the names of all the enumeration items as a `tuple`, if
        parameter `as_tuple` is `True`; otherwise returns a generator.

        :param as_tuple: returns a tuple if True; otherwise returns a generator.
        :type as_tuple: bool
        :return: names of all the enumeration items inside the class in a
          specific form
        :rtype: tuple_, Generator_

        >>> from types import GeneratorType
        >>> class TripleEnum(NamedEnum):
        ...     _field_names_ = ("first", "second", "third")
        >>> class Triangle(TripleEnum):
        ...     EQUILATERAL = (6, 6, 6)
        ...     RIGHT = (3, 4, 5)
        >>> TripleEnum.names()
        ()
        >>> isinstance(TripleEnum.names(as_tuple=False), GeneratorType)
        True
        >>> list(TripleEnum.names(as_tuple=False))
        []
        >>> Triangle.names()
        ('EQUILATERAL', 'RIGHT')
        >>> isinstance(Triangle.names(as_tuple=False), GeneratorType)
        True
        >>> list(Triangle.names(as_tuple=False))
        ['EQUILATERAL', 'RIGHT']
        """
        g = (name for name in cls._member_map_.keys())
        return tuple(g) if as_tuple else g

    def values(cls, as_tuple=True):
        """
        Returns the values of all the enumeration items as a tuple, if
        parameter `as_tuple` is `True`, otherwise returns a generator.

        :param as_tuple: returns a tuple if True; otherwise returns a generator
        :type as_tuple: bool
        :return: values of all the enumeration items inside the class in a
          specific form
        :rtype: tuple_, Generator_

        >>> from types import GeneratorType
        >>> class TripleEnum(NamedEnum):
        ...     _field_names_ = ("first", "second", "third")
        >>> class Triangle(TripleEnum):
        ...     EQUILATERAL = (6, 6, 6)
        ...     RIGHT = (3, 4, 5)
        >>> TripleEnum.values()
        ()
        >>> isinstance(TripleEnum.values(as_tuple=False), GeneratorType)
        True
        >>> list(TripleEnum.values(as_tuple=False))
        []
        >>> Triangle.values()
        (NamedTuple(first=6, second=6, third=6), NamedTuple(first=3, second=4, third=5))
        >>> isinstance(Triangle.values(as_tuple=False), GeneratorType)
        True
        >>> list(Triangle.values(as_tuple=False))
        [NamedTuple(first=6, second=6, third=6), NamedTuple(first=3, second=4, third=5)]
        """
        g = (item.value for item in cls._member_map_.values())
        return tuple(g) if as_tuple else g


class NamedEnum(Enum, metaclass=NamedEnumMeta):
    """
    Through the value of variable `_field_names_` to control its subclass for
    different use cases:

    1.  value of `_field_names_` is `None` or empty. In this case, its
    subclass works like an extended Enum class with extra function:
    `names`, `values`, `as_dict`, `as_list`, `as_set`, `as_tuple`,
    `as_ordereddict`, `describe`.

    2.  value of `_field_names_` is neither `None` or empty. In this case, its
    subclass keeps the extra functions mentioned in **1**, and gives each
    element in the enumeration item's value a name and provides functions for
    each attribute/field, like: `<field_name>s`, `from_<field_name>`,
    `has_<field_name>`.

    Instead of the setting the attributes to the enumeration instance, it uses
    the function `__getattr__` to achieve it.

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
    >>> Triangle.as_set() == {('RIGHT', Triangle._tuple_cls(first=3, second=4, third=5)), ('EQUILATERAL', Triangle._tuple_cls(first=6, second=6, third=6))}
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
    same format as the parameter `field_names` in function `namedtuple` from 
    `collections` package. 
    It's used in the NamedEnumMeta class's `__new__` function to generate the 
    corresponding functions for each field.
    If it's value is `None` or empty, then the enumeration class behaves like a 
    normal `Enum` class, but with some extended functions to simplify the usages 
    of enumerations.

    **Attention**: this variable should not be used to get the field_names, to 
    do so you can use the class method `_fields`. Because it also accept the 
    comma separated string.
    """
    def __getattr__(self, item):
        """
        Hijacks the default __getattr__ function, such that every time when the
        user wants to get the value of a field in an enumeration item, it
        returns the corresponding field's value from the value of enumeration.

        :param item: name of the field or attribute
        :type item: str
        :return: corresponding value
        :rtype: int, str, object, ...
        """
        if item in self.__class__._fields():
            return getattr(self._value_, item)
        return super().__getattribute__(item)

    def __str__(self):
        """
        Displays the value as well.

        :return: string represents the enumeration item
        :rtype: str
        """
        return "%s.%s: %r" % (
            self.__class__.__name__, self._name_, self._value_)


class ExtendedEnum(NamedEnum):
    """
    An alias for the class `NamedEnum`.

    The goal is explicit directly providing
    the users an Enum class with extra functions.

    >>> from types import GeneratorType
    >>> class TVCouple(ExtendedEnum):
    ...     GALLAGHERS = ("FRANK", "MONICA")
    ...     MIKE_AND_MOLLY = ("Mike", "Molly")
    >>> TVCouple.names()
    ('GALLAGHERS', 'MIKE_AND_MOLLY')
    >>> isinstance(TVCouple.names(as_tuple=False), GeneratorType)
    True
    >>> list(TVCouple.names(as_tuple=False))
    ['GALLAGHERS', 'MIKE_AND_MOLLY']
    >>> TVCouple.values()
    (('FRANK', 'MONICA'), ('Mike', 'Molly'))
    >>> isinstance(TVCouple.values(as_tuple=False), GeneratorType)
    True
    >>> list(TVCouple.values(as_tuple=False))
    [('FRANK', 'MONICA'), ('Mike', 'Molly')]
    >>> TVCouple.describe()
    Class: TVCouple
              Name |               Value
    ------------------------------------
        GALLAGHERS | ('FRANK', 'MONICA')
    MIKE_AND_MOLLY |   ('Mike', 'Molly')
    <BLANKLINE>
    >>> isinstance(TVCouple.gen(), GeneratorType)
    True
    >>> tuple(TVCouple.gen())
    (('GALLAGHERS', ('FRANK', 'MONICA')), ('MIKE_AND_MOLLY', ('Mike', 'Molly')))
    >>> isinstance(TVCouple.gen(name_value_pair=False), GeneratorType)
    True
    >>> tuple(TVCouple.gen(name_value_pair=False))
    (<TVCouple.GALLAGHERS: ('FRANK', 'MONICA')>, <TVCouple.MIKE_AND_MOLLY: ('Mike', 'Molly')>)
    >>> TVCouple.as_dict()
    {'GALLAGHERS': ('FRANK', 'MONICA'), 'MIKE_AND_MOLLY': ('Mike', 'Molly')}
    >>> isinstance(TVCouple.as_set(), set)
    True
    >>> sorted(list(TVCouple.as_set()))
    [('GALLAGHERS', ('FRANK', 'MONICA')), ('MIKE_AND_MOLLY', ('Mike', 'Molly'))]
    >>> TVCouple.as_tuple()
    (('GALLAGHERS', ('FRANK', 'MONICA')), ('MIKE_AND_MOLLY', ('Mike', 'Molly')))
    >>> TVCouple.as_list()
    [('GALLAGHERS', ('FRANK', 'MONICA')), ('MIKE_AND_MOLLY', ('Mike', 'Molly'))]
    >>> TVCouple.as_ordereddict()
    OrderedDict([('GALLAGHERS', ('FRANK', 'MONICA')), ('MIKE_AND_MOLLY', ('Mike', 'Molly'))])
    """
    pass


class LabeledEnum(NamedEnum):
    """
    An enumeration class with two attributes `key` and `label`.

    It can be used in the Django project as the choices of a field in model or
    form.

    >>> from types import GeneratorType
    >>> class NBALegendary(LabeledEnum):
    ...     JOHNSON = ("Johnson", "Magic Johnson")
    ...     Jordan = ("Jordan", "Air Jordan")
    >>> NBALegendary.names()
    ('JOHNSON', 'Jordan')
    >>> isinstance(NBALegendary.names(as_tuple=False), GeneratorType)
    True
    >>> list(NBALegendary.names(as_tuple=False))
    ['JOHNSON', 'Jordan']
    >>> NBALegendary.values()
    (NamedTuple(key='Johnson', label='Magic Johnson'), NamedTuple(key='Jordan', label='Air Jordan'))
    >>> isinstance(NBALegendary.values(as_tuple=False), GeneratorType)
    True
    >>> list(NBALegendary.values(as_tuple=False))
    [NamedTuple(key='Johnson', label='Magic Johnson'), NamedTuple(key='Jordan', label='Air Jordan')]
    >>> NBALegendary.describe()
    Class: NBALegendary
       Name |     Key |         Label
    ---------------------------------
    JOHNSON | Johnson | Magic Johnson
     Jordan |  Jordan |    Air Jordan
    <BLANKLINE>
    >>> isinstance(NBALegendary.gen(), GeneratorType)
    True
    >>> tuple(NBALegendary.gen())
    (('JOHNSON', NamedTuple(key='Johnson', label='Magic Johnson')), ('Jordan', NamedTuple(key='Jordan', label='Air Jordan')))
    >>> isinstance(NBALegendary.gen(name_value_pair=False), GeneratorType)
    True
    >>> tuple(NBALegendary.gen(name_value_pair=False))
    (<NBALegendary.JOHNSON: NamedTuple(key='Johnson', label='Magic Johnson')>, <NBALegendary.Jordan: NamedTuple(key='Jordan', label='Air Jordan')>)
    >>> NBALegendary.as_dict()
    {'JOHNSON': NamedTuple(key='Johnson', label='Magic Johnson'), 'Jordan': NamedTuple(key='Jordan', label='Air Jordan')}
    >>> isinstance(NBALegendary.as_set(), set)
    True
    >>> sorted(list(NBALegendary.as_set()))
    [('JOHNSON', NamedTuple(key='Johnson', label='Magic Johnson')), ('Jordan', NamedTuple(key='Jordan', label='Air Jordan'))]
    >>> NBALegendary.as_tuple()
    (('JOHNSON', NamedTuple(key='Johnson', label='Magic Johnson')), ('Jordan', NamedTuple(key='Jordan', label='Air Jordan')))
    >>> NBALegendary.as_list()
    [('JOHNSON', NamedTuple(key='Johnson', label='Magic Johnson')), ('Jordan', NamedTuple(key='Jordan', label='Air Jordan'))]
    >>> NBALegendary.as_ordereddict()
    OrderedDict([('JOHNSON', NamedTuple(key='Johnson', label='Magic Johnson')), ('Jordan', NamedTuple(key='Jordan', label='Air Jordan'))])
    >>> NBALegendary.keys()
    ('Johnson', 'Jordan')
    >>> NBALegendary.labels()
    ('Magic Johnson', 'Air Jordan')
    >>> isinstance(NBALegendary.keys(as_tuple=False), GeneratorType)
    True
    >>> list(NBALegendary.keys(as_tuple=False))
    ['Johnson', 'Jordan']
    >>> isinstance(NBALegendary.labels(as_tuple=False), GeneratorType)
    True
    >>> list(NBALegendary.labels(as_tuple=False))
    ['Magic Johnson', 'Air Jordan']
    >>> NBALegendary.from_key('Johnson')
    (<NBALegendary.JOHNSON: NamedTuple(key='Johnson', label='Magic Johnson')>,)
    >>> NBALegendary.from_key('Jordan')
    (<NBALegendary.Jordan: NamedTuple(key='Jordan', label='Air Jordan')>,)
    >>> NBALegendary.from_label('Magic Johnson')
    (<NBALegendary.JOHNSON: NamedTuple(key='Johnson', label='Magic Johnson')>,)
    >>> NBALegendary.from_label('Air Jordan')
    (<NBALegendary.Jordan: NamedTuple(key='Jordan', label='Air Jordan')>,)
    >>> isinstance(NBALegendary.from_key('Johnson', as_tuple=False), GeneratorType)
    True
    >>> list(NBALegendary.from_key('Johnson', as_tuple=False))
    [<NBALegendary.JOHNSON: NamedTuple(key='Johnson', label='Magic Johnson')>]
    >>> isinstance(NBALegendary.from_key('Jordan', as_tuple=False), GeneratorType)
    True
    >>> list(NBALegendary.from_key('Jordan', as_tuple=False))
    [<NBALegendary.Jordan: NamedTuple(key='Jordan', label='Air Jordan')>]
    >>> isinstance(NBALegendary.from_label('Magic Johnson', as_tuple=False), GeneratorType)
    True
    >>> list(NBALegendary.from_label('Magic Johnson', as_tuple=False))
    [<NBALegendary.JOHNSON: NamedTuple(key='Johnson', label='Magic Johnson')>]
    >>> isinstance(NBALegendary.from_label('Air Jordan', as_tuple=False), GeneratorType)
    True
    >>> list(NBALegendary.from_label('Air Jordan', as_tuple=False))
    [<NBALegendary.Jordan: NamedTuple(key='Jordan', label='Air Jordan')>]
    >>> NBALegendary.has_key('Johnson')
    True
    >>> NBALegendary.has_key('John')
    False
    >>> NBALegendary.has_key('Jordan')
    True
    >>> NBALegendary.has_key('George')
    False
    >>> NBALegendary.has_label('Magic Johnson')
    True
    >>> NBALegendary.has_label('King James')
    False
    >>> NBALegendary.has_label('Air Jordan')
    True
    >>> NBALegendary.has_label('The Black Mamba')
    False
    """
    _field_names_ = ("key", "label")
    """Each enumeration of LabeledEnum has two attributes: `key`, `label`"""


class PairEnum(NamedEnum):
    """
    Enumeration with two attributes `first`, `second`, the idea comes from the
    C++'s pair container.

    >>> from types import GeneratorType
    >>> class Pair(PairEnum):
    ...     TOM_AND_JERRY = ("Tom", "Jerry")
    ...     BULLS = ("Micheal", "Pippen")
    >>> Pair.names()
    ('TOM_AND_JERRY', 'BULLS')
    >>> isinstance(Pair.names(as_tuple=False), GeneratorType)
    True
    >>> list(Pair.names(as_tuple=False))
    ['TOM_AND_JERRY', 'BULLS']
    >>> Pair.values()
    (NamedTuple(first='Tom', second='Jerry'), NamedTuple(first='Micheal', second='Pippen'))
    >>> isinstance(Pair.values(as_tuple=False), GeneratorType)
    True
    >>> list(Pair.values(as_tuple=False))
    [NamedTuple(first='Tom', second='Jerry'), NamedTuple(first='Micheal', second='Pippen')]
    >>> Pair.describe()
    Class: Pair
             Name |   First | Second
    --------------------------------
    TOM_AND_JERRY |     Tom |  Jerry
            BULLS | Micheal | Pippen
    <BLANKLINE>
    >>> isinstance(Pair.gen(), GeneratorType)
    True
    >>> tuple(Pair.gen())
    (('TOM_AND_JERRY', NamedTuple(first='Tom', second='Jerry')), ('BULLS', NamedTuple(first='Micheal', second='Pippen')))
    >>> isinstance(Pair.gen(name_value_pair=False), GeneratorType)
    True
    >>> tuple(Pair.gen(name_value_pair=False))
    (<Pair.TOM_AND_JERRY: NamedTuple(first='Tom', second='Jerry')>, <Pair.BULLS: NamedTuple(first='Micheal', second='Pippen')>)
    >>> Pair.as_dict()
    {'TOM_AND_JERRY': NamedTuple(first='Tom', second='Jerry'), 'BULLS': NamedTuple(first='Micheal', second='Pippen')}
    >>> isinstance(Pair.as_set(), set)
    True
    >>> sorted(list(Pair.as_set()))
    [('BULLS', NamedTuple(first='Micheal', second='Pippen')), ('TOM_AND_JERRY', NamedTuple(first='Tom', second='Jerry'))]
    >>> Pair.as_tuple()
    (('TOM_AND_JERRY', NamedTuple(first='Tom', second='Jerry')), ('BULLS', NamedTuple(first='Micheal', second='Pippen')))
    >>> Pair.as_list()
    [('TOM_AND_JERRY', NamedTuple(first='Tom', second='Jerry')), ('BULLS', NamedTuple(first='Micheal', second='Pippen'))]
    >>> Pair.as_ordereddict()
    OrderedDict([('TOM_AND_JERRY', NamedTuple(first='Tom', second='Jerry')), ('BULLS', NamedTuple(first='Micheal', second='Pippen'))])
    >>> Pair.firsts()
    ('Tom', 'Micheal')
    >>> Pair.seconds()
    ('Jerry', 'Pippen')
    >>> isinstance(Pair.firsts(as_tuple=False), GeneratorType)
    True
    >>> list(Pair.firsts(as_tuple=False))
    ['Tom', 'Micheal']
    >>> isinstance(Pair.seconds(as_tuple=False), GeneratorType)
    True
    >>> list(Pair.seconds(as_tuple=False))
    ['Jerry', 'Pippen']
    >>> Pair.from_first("Tom")
    (<Pair.TOM_AND_JERRY: NamedTuple(first='Tom', second='Jerry')>,)
    >>> Pair.from_first("Micheal")
    (<Pair.BULLS: NamedTuple(first='Micheal', second='Pippen')>,)
    >>> Pair.from_second("Jerry")
    (<Pair.TOM_AND_JERRY: NamedTuple(first='Tom', second='Jerry')>,)
    >>> Pair.from_second("Pippen")
    (<Pair.BULLS: NamedTuple(first='Micheal', second='Pippen')>,)
    >>> isinstance(Pair.from_first("Tom", as_tuple=False), GeneratorType)
    True
    >>> list(Pair.from_first("Tom", as_tuple=False))
    [<Pair.TOM_AND_JERRY: NamedTuple(first='Tom', second='Jerry')>]
    >>> isinstance(Pair.from_first("Micheal", as_tuple=False), GeneratorType)
    True
    >>> list(Pair.from_first("Micheal", as_tuple=False))
    [<Pair.BULLS: NamedTuple(first='Micheal', second='Pippen')>]
    >>> isinstance(Pair.from_second("Jerry", as_tuple=False), GeneratorType)
    True
    >>> list(Pair.from_second("Jerry", as_tuple=False))
    [<Pair.TOM_AND_JERRY: NamedTuple(first='Tom', second='Jerry')>]
    >>> isinstance(Pair.from_second("Pippen", as_tuple=False), GeneratorType)
    True
    >>> list(Pair.from_second("Pippen", as_tuple=False))
    [<Pair.BULLS: NamedTuple(first='Micheal', second='Pippen')>]
    >>> Pair.has_first('Tom')
    True
    >>> Pair.has_first('Tommy')
    False
    >>> Pair.has_first('Micheal')
    True
    >>> Pair.has_first('Mike')
    False
    >>> Pair.has_second('Jerry')
    True
    >>> Pair.has_second('Jeremy')
    False
    >>> Pair.has_second('Pippen')
    True
    >>> Pair.has_second('Pepe')
    False
    """
    _field_names_ = ("first", "second")
    """Each enumeration of PairEnum has two attributes: first, second"""


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

    :param typename: name for the created class
    :type typename: str
    :param field_names: field names for the named enum class
    :type field_names: Sequence_
    :param verbose: displays the code for the named enum class creation,
      if True
    :type verbose: bool
    :param module: which module the new created enum class belongs to
    :type module: None, str
    :return: subclass of NamedEnum
    :rtype: object

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
