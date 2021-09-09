# -*- coding: utf-8 -*-
"""Module for the classes extending the default `Enum` class. It contains four
classes:
`ExtendedEnum`, `ExtendedEnum`, `LabeledEnum`, `PairEnum` and one function
`namedenum`.
"""
import sys as _sys
from enum import Enum
from typing import (
    Any, Optional, Sequence, Tuple, Union
)
from .meta import NamedEnumMeta

__all__ = [
    'NamedEnum', 'ExtendedEnum', 'LabeledEnum', 'PairEnum', 'namedenum'
]


class NamedEnum(Enum, metaclass=NamedEnumMeta):
    """Through the value of variable `_field_names_` to control its subclass for
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

    Examples:
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
        >>> Triangle.as_set() == {('RIGHT', Triangle._tuple_cls(first=3, second=4, third=5)),
        ... ('EQUILATERAL', Triangle._tuple_cls(first=6, second=6, third=6))}
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
    _field_names_: Union[Tuple[str], None] = None

    """The place to define the field names of the enumeration class. It accepts
    the same format as the parameter `field_names` in function `namedtuple` from
    `collections` package.
    It's used in the NamedEnumMeta class's `__new__` function to generate the
    corresponding functions for each field.
    If it's value is `None` or empty, then the enumeration class behaves like a
    normal `Enum` class, but with some extended functions to simplify the usages
    of enumerations.

    **Attention**: this variable should not be used to get the field_names, to
    do so you can use the class method `_fields`. Because it also accept the
    comma separated string."""
    def __getattr__(self, item: str) -> Any:
        """Hijacks the default `__getattr__` function, such that every time when the
        user wants to get the value of a field in an enumeration item, it
        returns the corresponding field's value from the value of enumeration.

        Args:
            item (str): name of the field or attribute.

        Returns:
            Any: corresponding value.
        """
        if item in self.__class__._fields():
            return getattr(self._value_, item)
        return super().__getattribute__(item)

    def __str__(self) -> str:
        """Displays the value as well.

        Returns:
            str: string represents the enumeration item.
        """
        return "%s.%s: %r" % (
            self.__class__.__name__, self._name_, self._value_)


class ExtendedEnum(NamedEnum):
    """An alias for the class `NamedEnum`.

    The goal is explicit directly providing
    the users an Enum class with extra functions.

    Examples:
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
    """An enumeration class with two attributes `key` and `label`.

    It can be used in the Django project as the choices of a field in model or
    form.

    Examples:
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
    _field_names_ = ("key", "label")  # type: ignore
    """Each enumeration of LabeledEnum has two attributes: `key`, `label`"""


class PairEnum(NamedEnum):
    """Enumeration with two attributes `first`, `second`, the idea comes from the
    C++'s pair container.

    Examples:
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
    _field_names_ = ("first", "second")  # type: ignore
    """Each enumeration of PairEnum has two attributes: first, second"""


_class_template = """\
from named_enum import NamedEnum


class {typename}(NamedEnum):

    _field_names_ = {field_names!r}

"""


def namedenum(typename: str, field_names: Optional[Sequence] = None, *,
              verbose: Optional[bool] = False, module: Optional[str] = None) -> object:
    """Creates an named enum class with the given typename as class name and
    field_names as the _field_names_ in named enum class. The implementation is
    similar to the namedtuple function.

    Args:
        typename (str): name for the created class.
        field_names (Optional[Sequence]): field names for the named enum class.
        verbose (Optional[bool]): displays the code for the named enum class
         creation, if True.
        module (Optional[str]): which module the new created enum class belongs to.

    Returns:
        object: subclass of NamedEnum

    Examples:
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
    exec(class_definition, namespace)  # nosec
    result = namespace[typename]
    result._source = class_definition  # type: ignore
    if verbose:
        print(result._source)  # type: ignore

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
