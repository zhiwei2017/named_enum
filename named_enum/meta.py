# -*- coding: utf-8 -*-
"""Module for the rewriting EnumMeta class. It contains 2 classes:
`NamedEnumMeta`, `_NamedEnumDict`."""
# mypy: ignore-errors
import sys as _sys
from collections import namedtuple, OrderedDict
from collections.abc import Sequence
from enum import Enum, EnumMeta, _EnumDict
from functools import partial
from typing import (
    Any, ClassVar, Dict, Generator, List, NamedTuple, Optional, Set, Tuple, Union, Type
)

__all__ = ['NamedEnumMeta']


class _NamedEnumDict(_EnumDict):
    """Customizes _EnumDict, such that it allows setting the value for the keyword
    '_field_names_' and provides the functions for cleaning itself and
    converting the collection type value (except str) to NamedTuple type.
    """

    def __setitem__(self, key: str, value: Any) -> None:
        """Makes an exception for the single underscore name '_field_names_'.

        Args:
            key (str): variable or function names defined in class.
            value (Any): values or functions.
        """
        if key == '_field_names_':
            dict.__setitem__(self, key, value)
        else:
            super().__setitem__(key, value)

    def _clean(self) -> None:
        """Removes all the items, and set the variables '_member_names' and
        '_last_values' to empty."""
        # for dictionary, that's the only way to _clean it
        for name in self._member_names:
            del self[name]
        # _clean the variables as well
        self._member_names, self._last_values = [], []

    def _convert(self, tuple_cls: Type[NamedTuple]) -> None:
        """Uses the given tuple class to _convert the items.

        Args:
            tuple_cls (Type[NamedTuple]): using namedtuple generated tuple class.
        """
        if tuple_cls is tuple or not issubclass(tuple_cls, tuple):
            raise ValueError("'tuple_cls' must be a customized tuple class "
                             "using namedtuple generated class instead.")
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
    def __prepare__(mcs, cls: str, bases: Tuple) -> _NamedEnumDict:
        """Namespace hook, uses _NamedEnumDict as the type of namespace instead
        of _EnumDict.

        Args:
            cls (str): name of the class to create.
            bases (Tuple): parent classes of the class to create.

        Returns:
            _NamedEnumDict: namespace dictionary.
        """
        # create the namespace dict
        enum_dict = _NamedEnumDict()
        enum_dict._cls_name = cls
        # inherit previous flags and _generate_next_value_ function
        if _sys.version_info >= (3, 8, 6):
            # inherit previous flags and _generate_next_value_ function
            member_type, first_enum = mcs._get_mixins_(cls, bases)
        else:
            member_type, first_enum = mcs._get_mixins_(bases)
        if first_enum is not None:
            enum_dict['_generate_next_value_'] = getattr(
                first_enum, '_generate_next_value_', None)
        return enum_dict

    def __new__(mcs, name: str, bases: Tuple, namespace: _NamedEnumDict) -> ClassVar:
        """Besides the class creation, this function also intends to create a
        named tuple data type depending on the given value of '_field_names_'
        variable to be the data type of the value of enumeration iem and add
        those extra functions to the class.

        Args:
            name (str): name of the instance class.
            bases (Tuple): base classes, its instance class inherits from.
            namespace (_NamedEnumDict): contains the attributes and functions of the
             instance class.

        Returns:
            ClassVar: class object
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

    def __contains__(cls, member: Union[str, Enum]) -> bool:
        """verrides the magic method in Enum class, which doesn't support
        member name search from python 3.8.

        Args:
            member (Union[str, Enum]):

        Returns:
            bool: if the member is contained in the enumeration.
        """
        if isinstance(member, str):
            return member in cls._member_map_
        return isinstance(member, cls) and member._name_ in cls._member_map_

    def _fields(cls) -> Tuple:
        """Returns the defined field names as a `tuple` for the enumeration
        class.

        Note:
            If the variable `_field_names_` is `None` or empty value, then
            returns an empty `tuple`.

        Returns:
            Tuple: tuple of field names.

        Examples:
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
    def _field_values(mcs, cls: Enum, field_name: str,
                      as_tuple: Optional[bool] = True) -> Union[Tuple, Generator]:
        """Base function returns a `tuple`/`generator` containing just the
        value of the given field_name of all the elements from the cls.

        Note:
            It's used to generate the particular function with name format
            `<field_name>s` for each `field_name`.

        Args:
            cls (Enum): subclass of NamedEnum class.
            field_name (str): attribute's name.
            as_tuple (Optional[bool]): returns a tuple of the values if True;
             otherwise returns a generator. Default value is True.

        Returns:
            Union[Tuple, Generator]: corresponding values of the field name in
            all enumeration items
        """
        g = (getattr(item.value, field_name)
             for item in cls.gen(name_value_pair=False))
        return tuple(g) if as_tuple else g

    @classmethod
    def _from_field(mcs, cls: Enum, field_name: str, field_value: Any,
                    as_tuple: Optional[bool] = True) -> Union[Tuple, Generator]:
        """Base function returns a `tuple` of the defined enumeration items
        regarding to the given `field_value` of field with `field_name`, if
        `as_tuple` is True; otherwise returns a generator.

        Args:
            cls (Enum): subclass of NamedEnum class.
            field_name (str): attribute's name.
            field_value (Any): key to search for.
            as_tuple (Optional[bool]): returns a tuple of the values if True;
             otherwise returns a generator. Default value is True.

        Returns:
            Union[Tuple, Generator]: collection of enumeration items matching
            the condition.
        """
        g = (item for item in cls.gen(name_value_pair=False)
             if getattr(item.value, field_name) == field_value)
        return tuple(g) if as_tuple else g

    @classmethod
    def _has_field(mcs, cls: Enum, field_name: str, field_value: Any) -> bool:
        """Base function returns a boolean value which indicates if there is at
        least one enumeration item in which the value of the field `field_name`
        corresponding value matches the given `field_value`.

        Note:
            It's used to generate the particular function with name format
            `has_<field_name>` for each `field_name`.

        Args:
            cls (Enum): subclass of NamedEnum class.
            field_name (str): attribute's name.
            field_value (Any): key to search for

        Returns:
            bool: True, if has at least one matching; otherwise False.
        """
        gen_field_values = mcs._field_values(cls, field_name, as_tuple=False)
        return field_value in gen_field_values

    def gen(cls, name_value_pair: Optional[bool] = True) -> Generator:
        """Returns a generator of pairs consisting of each enumeration item's
        name and value, if name_value_pair is True; otherwise a generator of the
        enumeration items.

        Args:
            name_value_pair (Optional[bool]): controls the return result. If true,
             returns the generator of name-value pair; if False, returns the
             generator of the enumeration items. Default value is True.

        Returns:
            Generator: a generator which iterates all the enumeration items.

        Examples:
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

    def _as_data_type(cls, data_type: Union[dict, list, set, tuple, OrderedDict])\
            -> Union[Dict, List, Set, Tuple, OrderedDict]:
        """ase function converts the enumeration class to the given data type
        value.

        Note:
            It's used for generating the functions like `as_dict`, `as_tuple`,
            `as_set`, `as_list`, `as_ordereddict`.

        Args:
            data_type (Union[dict, list, set, tuple, OrderedDict]): desired data
             type for the output.

        Returns:
            Union[Dict, List, Set, Tuple, OrderedDict]: converted value
            depending on the given data type.
        """
        return data_type(cls.gen(name_value_pair=True))

    def as_dict(cls) -> Dict:
        """Converts the enumeration to a `dict`, in which the key is the name
        of the enumeration item and value is its value.

        Returns:
            Dict: a dictionary containing name-value-pairs of the enumeration.

        Examples:
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

    def as_tuple(cls) -> Tuple:
        """Converts the enumerations to a `tuple`, in which each item is a tuple
        of the enumeration item's name and value.

        Returns:
            Tuple: a tuple containing name-value-pairs of the enumeration.

        Examples:
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

    def as_set(cls) -> Set:
        """Converts the enumerations to a `set`, in which each item is a tuple of
        the enumeration item's name and value.

        Returns:
            Set: a set containing name-value-pairs of the enumeration.

        Examples:
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

    def as_list(cls) -> List:
        """Converts the enumerations to a `list`, in which each item is a tuple of
        the enumeration item's name and value.

        Returns:
            List: a list containing name-value-pairs of the enumeration.

        Examples:
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

    def as_ordereddict(cls) -> OrderedDict:
        """Converts the enumerations to an `OrderedDict`, in which each item is a
        tuple of the enumeration item's name and value.

        Returns:
            OrderedDict: an OrderedDict containing name-value-pairs of the
             enumeration.

        Examples:
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

    def __repr__(cls) -> str:
        """Overrides the __repr__ function from EnumMeta class.

        Returns:
            str: string represents the class.
        """
        return "<named enum %r>" % cls.__name__

    def describe(cls) -> None:
        """Prints in the console a table showing the content of the enumeration.

        Examples:
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

    def names(cls, as_tuple: Optional[bool] = True) -> Union[Tuple, Generator]:
        """Returns the names of all the enumeration items as a `tuple`, if
        parameter `as_tuple` is `True`; otherwise returns a generator.

        Args:
            as_tuple (bool): returns a tuple if True; otherwise returns a
             generator.

        Returns:
            Union[Tuple, Generator]: names of all the enumeration items inside
            the class in a specific form.

        Examples:
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

    def values(cls, as_tuple: Optional[bool] = True) -> Union[Tuple, Generator]:
        """Returns the values of all the enumeration items as a tuple, if
        parameter `as_tuple` is `True`, otherwise returns a generator.

        Args:
            as_tuple (Optional[bool]): returns a tuple if True; otherwise
             returns a generator. Default value is True.

        Returns:
            Union[Tuple, Generator]: values of all the enumeration items inside
            the class in a specific form.

        Examples:
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
