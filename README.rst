NamedEnum
=========

Efficient, Pythonic named enumeration implementation and related functionality.
The named enumeration means that the value of each item inside the enumeration
class is the type of named tuple.

This package is inspired by `Cristian <https://github.com/cagonza6/>`_.

Status
------
.. image:: https://readthedocs.org/projects/named-enum/badge/?version=latest
    :target: https://named-enum.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Installation
------------

``pip install named_enum``


Quick Start
-----------

Enumeration Creation
````````````````````

1. create a new enumeration class

    + using inheritance from class ``NamedEnum``

    .. code-block:: python

        >>> from named_enum import NamedEnum

        >>> class ExtendedEnum(NamedEnum):
        ...     """
        ...     normal Enum class with extra functions
        ...     """
        ...     pass

        >>> class TripleEnum(NamedEnum):
        ...     """
        ...     using a sequence of strings to define the field names
        ...     """
        ...     _field_names_ = ("first", "second", "third")

        >>> class LabelEnum(NamedEnum):
        ...     """
        ...     using a comma/space separated string to define the field names
        ...     """
        ...     _field_names_ = "key, label"


    + using function ``namedenum``

    .. code-block:: python

        >>> from named_enum import namedenum

        >>> # normal Enum class with extra functions
        >>> ExtendedEnum = namedenum("ExtendedEnum")

        >>> # using a sequence of strings to define the field names
        >>> TripleEnum = namedenum("TripleEnum", ("first", "second", "third"))

        >>> # using a comma/space separated string to define the field names
        >>> LabelEnum = namedenum("LabelEnum", "key, label")

2. create enumerations using the customized enumeration class in step **1**.

    .. code-block:: python

        >>> class TVCouple(ExtendedEnum):
        ...     GALLAGHERS = ("FRANK", "MONICA")
        ...     MIKE_AND_MOLLY = ("Mike", "Molly")

        >>> class AnimationFamily(TripleEnum):
        ...     SIMPSONS = ("Homer", "Bart", "Marge")
        ...     DUCKS = ("Huey", "Dewey", "Louie")

        >>> class NBALegendary(LabelEnum):
        ...     JOHNSON = ("Johnson", "Magic Johnson")
        ...     Jordan = ("Jordan", "Air Jordan")

Or you can directly use the class ``PairEnum``, which has two fields: ``first``
and ``second``.

    .. code-block:: python

        >>> from named_enum import PairEnum
        >>> class Pair(PairEnum):
        ...     TOM_AND_JERRY = ("Tom", "Jerry")
        ...     BULLS = ("Micheal", "Pippen")

Usages
``````
+ ``names(as_tuple=True)``
    ``as_tuple=True``: returns the names of all enumeration items as a tuple.

    .. code-block:: python

        >>> TVCouple.names()
        ('GALLAGHERS', 'MIKE_AND_MOLLY')

        >>> AnimationFamily.names()
        ('SIMPSONS', 'DUCKS')

        >>> NBALegendary.names()
        ('JOHNSON', 'Jordan')

        >>> Pair.names()
        ('TOM_AND_JERRY', 'BULLS')

    ``as_tuple=False``: returns a generator of the names of all enumeration items.

    .. code-block:: python

        >>> from types import GeneratorType
        >>> isinstance(TVCouple.names(as_tuple=False), GeneratorType)
        True

        >>> isinstance(AnimationFamily.names(as_tuple=False), GeneratorType)
        True

        >>> isinstance(NBALegendary.names(as_tuple=False), GeneratorType)
        True

        >>> isinstance(Pair.names(as_tuple=False), GeneratorType)
        True

+ ``values(as_tuple=True)``
    ``as_tuple=True``: returns the values of all enumeration items as a tuple.

    .. code-block:: python

        >>> TVCouple.values()
        (('FRANK', 'MONICA'), ('Mike', 'Molly'))

        >>> AnimationFamily.values()
        (NamedTuple(first='Homer', second='Bart', third='Marge'), NamedTuple(first='Huey', second='Dewey', third='Louie'))

        >>> NBALegendary.values()
        (NamedTuple(key='Johnson', label='Magic Johnson'), NamedTuple(key='Jordan', label='Air Jordan'))

        >>> Pair.values()
        (NamedTuple(first='Tom', second='Jerry'), NamedTuple(first='Micheal', second='Pippen'))

    ``as_tuple=False``: returns a generator of the values of all enumeration items.

    .. code-block:: python

        >>> import types
        >>> isinstance(TVCouple.values(as_tuple=False), GeneratorType)
        True

        >>> isinstance(AnimationFamily.values(as_tuple=False), GeneratorType)
        True

        >>> isinstance(NBALegendary.values(as_tuple=False), GeneratorType)
        True

        >>> isinstance(Pair.values(as_tuple=False), GeneratorType)
        True

+ ``describe()``
    displays the enumeration as a table.

    .. code-block:: python

        >>> TVCouple.describe()
        Class: TVCouple
                  Name |               Value
        ------------------------------------
            GALLAGHERS | ('FRANK', 'MONICA')
        MIKE_AND_MOLLY |   ('Mike', 'Molly')
        <BLANKLINE>

        >>> AnimationFamily.describe()
        Class: AnimationFamily
            Name | First | Second | Third
        ---------------------------------
        SIMPSONS | Homer |   Bart | Marge
           DUCKS |  Huey |  Dewey | Louie
        <BLANKLINE>


        >>> NBALegendary.describe()
        Class: NBALegendary
           Name |     Key |         Label
        ---------------------------------
        JOHNSON | Johnson | Magic Johnson
         Jordan |  Jordan |    Air Jordan
        <BLANKLINE>

        >>> Pair.describe()
        Class: Pair
                 Name |   First | Second
        --------------------------------
        TOM_AND_JERRY |     Tom |  Jerry
                BULLS | Micheal | Pippen
        <BLANKLINE>

+ ``gen(name_value_pair=True)``
    ``name_value_pair=True``: returns a generator comprised of name-value pair of each enumeration item

    .. code-block:: python

        >>> tuple(TVCouple.gen())
        (('GALLAGHERS', ('FRANK', 'MONICA')), ('MIKE_AND_MOLLY', ('Mike', 'Molly')))

        >>> tuple(AnimationFamily.gen())
        (('SIMPSONS', NamedTuple(first='Homer', second='Bart', third='Marge')), ('DUCKS', NamedTuple(first='Huey', second='Dewey', third='Louie')))

        >>> tuple(NBALegendary.gen())
        (('JOHNSON', NamedTuple(key='Johnson', label='Magic Johnson')), ('Jordan', NamedTuple(key='Jordan', label='Air Jordan')))

        >>> tuple(Pair.gen())
        (('TOM_AND_JERRY', NamedTuple(first='Tom', second='Jerry')), ('BULLS', NamedTuple(first='Micheal', second='Pippen')))

    ``name_value_pair=False``: returns a generator of enumeration items

    .. code-block:: python

        >>> tuple(TVCouple.gen(name_value_pair=False))
        (<TVCouple.GALLAGHERS: ('FRANK', 'MONICA')>, <TVCouple.MIKE_AND_MOLLY: ('Mike', 'Molly')>)

        >>> tuple(AnimationFamily.gen(name_value_pair=False))
        (<AnimationFamily.SIMPSONS: NamedTuple(first='Homer', second='Bart', third='Marge')>, <AnimationFamily.DUCKS: NamedTuple(first='Huey', second='Dewey', third='Louie')>)

        >>> tuple(NBALegendary.gen(name_value_pair=False))
        (<NBALegendary.JOHNSON: NamedTuple(key='Johnson', label='Magic Johnson')>, <NBALegendary.Jordan: NamedTuple(key='Jordan', label='Air Jordan')>)

        >>> tuple(Pair.gen(name_value_pair=False))
        (<Pair.TOM_AND_JERRY: NamedTuple(first='Tom', second='Jerry')>, <Pair.BULLS: NamedTuple(first='Micheal', second='Pippen')>)

+ ``as_dict()``
    returns a dictionary, in which the key is the enumeration item's name and the value is the item's value

    .. code-block:: python

        >>> TVCouple.as_dict()
        {'GALLAGHERS': ('FRANK', 'MONICA'), 'MIKE_AND_MOLLY': ('Mike', 'Molly')}

        >>> AnimationFamily.as_dict()
        {'SIMPSONS': NamedTuple(first='Homer', second='Bart', third='Marge'), 'DUCKS': NamedTuple(first='Huey', second='Dewey', third='Louie')}

        >>> NBALegendary.as_dict()
        {'JOHNSON': NamedTuple(key='Johnson', label='Magic Johnson'), 'Jordan': NamedTuple(key='Jordan', label='Air Jordan')}

        >>> Pair.as_dict()
        {'TOM_AND_JERRY': NamedTuple(first='Tom', second='Jerry'), 'BULLS': NamedTuple(first='Micheal', second='Pippen')}

+ ``as_set()``
    returns a set of tuples containing the enumeration item's name and value

    .. code-block:: python

        >>> TVCouple.as_set()
        {('GALLAGHERS', ('FRANK', 'MONICA')), ('MIKE_AND_MOLLY', ('Mike', 'Molly'))}

        >>> AnimationFamily.as_set()
        {('SIMPSONS', NamedTuple(first='Homer', second='Bart', third='Marge')), ('DUCKS', NamedTuple(first='Huey', second='Dewey', third='Louie'))}

        >>> NBALegendary.as_set()
        {('JOHNSON', NamedTuple(key='Johnson', label='Magic Johnson')), ('Jordan', NamedTuple(key='Jordan', label='Air Jordan'))}

        >>> Pair.as_set()
        {('TOM_AND_JERRY', NamedTuple(first='Tom', second='Jerry')), ('BULLS', NamedTuple(first='Micheal', second='Pippen'))}

+ ``as_tuple()``
    returns a tuple of tuples containing the enumeration item's name and value

    .. code-block:: python

        >>> TVCouple.as_tuple()
        (('GALLAGHERS', ('FRANK', 'MONICA')), ('MIKE_AND_MOLLY', ('Mike', 'Molly')))

        >>> AnimationFamily.as_tuple()
        (('SIMPSONS', NamedTuple(first='Homer', second='Bart', third='Marge')), ('DUCKS', NamedTuple(first='Huey', second='Dewey', third='Louie')))

        >>> NBALegendary.as_tuple()
        (('JOHNSON', NamedTuple(key='Johnson', label='Magic Johnson')), ('Jordan', NamedTuple(key='Jordan', label='Air Jordan')))

        >>> Pair.as_tuple()
        (('TOM_AND_JERRY', NamedTuple(first='Tom', second='Jerry')), ('BULLS', NamedTuple(first='Micheal', second='Pippen')))

+ ``as_list()``
    returns a list of tuples containing the enumeration item's name and value

    .. code-block:: python

        >>> TVCouple.as_list()
        [('GALLAGHERS', ('FRANK', 'MONICA')), ('MIKE_AND_MOLLY', ('Mike', 'Molly'))]

        >>> AnimationFamily.as_list()
        [('SIMPSONS', NamedTuple(first='Homer', second='Bart', third='Marge')), ('DUCKS', NamedTuple(first='Huey', second='Dewey', third='Louie'))]

        >>> NBALegendary.as_list()
        [('JOHNSON', NamedTuple(key='Johnson', label='Magic Johnson')), ('Jordan', NamedTuple(key='Jordan', label='Air Jordan'))]

        >>> Pair.as_list()
        [('TOM_AND_JERRY', NamedTuple(first='Tom', second='Jerry')), ('BULLS', NamedTuple(first='Micheal', second='Pippen'))]

+ ``as_ordereddict()``
    returns an ordered dict, in which the key is the enumeration item's name and the value is the item's value

    .. code-block:: python

        >>> TVCouple.as_ordereddict()
        OrderedDict([('GALLAGHERS', ('FRANK', 'MONICA')), ('MIKE_AND_MOLLY', ('Mike', 'Molly'))])

        >>> AnimationFamily.as_ordereddict()
        OrderedDict([('SIMPSONS', NamedTuple(first='Homer', second='Bart', third='Marge')), ('DUCKS', NamedTuple(first='Huey', second='Dewey', third='Louie'))])

        >>> NBALegendary.as_ordereddict()
        OrderedDict([('JOHNSON', NamedTuple(key='Johnson', label='Magic Johnson')), ('Jordan', NamedTuple(key='Jordan', label='Air Jordan'))])

        >>> Pair.as_ordereddict()
        OrderedDict([('TOM_AND_JERRY', NamedTuple(first='Tom', second='Jerry')), ('BULLS', NamedTuple(first='Micheal', second='Pippen'))])


If you define the enumeration class with ``field_names``, then for each field name there are 3 corresponding functions:

    - ``<field_name>s(as_tuple=True)``
        ``as_tuple=True``: returns a tuple containing all corresponding values of the field in enumeration items

        .. code-block:: python

            >>> AnimationFamily.firsts()
            ('Homer', 'Huey')
            >>> AnimationFamily.seconds()
            ('Bart', 'Dewey')
            >>> AnimationFamily.thirds()
            ('Marge', 'Louie')

            >>> NBALegendary.keys()
            ('Johnson', 'Jordan')
            >>> NBALegendary.labels()
            ('Magic Johnson', 'Air Jordan')

        ``as_tuple=False``: returns a generator of all corresponding values of the field in enumeration items

        .. code-block:: python

            >>> isinstance(AnimationFamily.firsts(as_tuple=False), GeneratorType)
            True
            >>> isinstance(AnimationFamily.seconds(as_tuple=False), GeneratorType)
            True
            >>> isinstance(AnimationFamily.thirds(as_tuple=False), GeneratorType)
            True

            >>> isinstance(NBALegendary.keys(as_tuple=False), GeneratorType)
            True
            >>> isinstance(NBALegendary.labels(as_tuple=False), GeneratorType)
            True

    - ``from_<field_name>(field_value, as_tuple=True)``
        ``as_tuple=True``: returns a tuple containing **all enumeration items** which has the given ``field_value`` in corresponding field

        .. code-block:: python

            >>> AnimationFamily.from_first('Homer')
            (<AnimationFamily.SIMPSONS: NamedTuple(first='Homer', second='Bart', third='Marge')>,)
            >>> AnimationFamily.from_first('Huey')
            (<AnimationFamily.DUCKS: NamedTuple(first='Huey', second='Dewey', third='Louie')>,)

            >>> AnimationFamily.from_second('Bart')
            (<AnimationFamily.SIMPSONS: NamedTuple(first='Homer', second='Bart', third='Marge')>,)
            >>> AnimationFamily.from_second('Dewey')
            (<AnimationFamily.DUCKS: NamedTuple(first='Huey', second='Dewey', third='Louie')>,)

            >>> AnimationFamily.from_third('Marge')
            (<AnimationFamily.SIMPSONS: NamedTuple(first='Homer', second='Bart', third='Marge')>,)
            >>> AnimationFamily.from_third('Louie')
            (<AnimationFamily.DUCKS: NamedTuple(first='Huey', second='Dewey', third='Louie')>,)


            >>> NBALegendary.from_key('Johnson')
            (<NBALegendary.JOHNSON: NamedTuple(key='Johnson', label='Magic Johnson')>,)
            >>> NBALegendary.from_key('Jordan')
            (<NBALegendary.Jordan: NamedTuple(key='Jordan', label='Air Jordan')>,)

            >>> NBALegendary.from_label('Magic Johnson')
            (<NBALegendary.JOHNSON: NamedTuple(key='Johnson', label='Magic Johnson')>,)
            >>> NBALegendary.from_label('Air Jordan')
            (<NBALegendary.Jordan: NamedTuple(key='Jordan', label='Air Jordan')>,)

        ``as_tuple=False``: returns a generator of **all enumeration items** which has the given ``field_value`` in corresponding field

        .. code-block:: python

            >>> isinstance(AnimationFamily.from_first('Homer', as_tuple=False), GeneratorType)
            True
            >>> isinstance(AnimationFamily.from_first('Huey', as_tuple=False), GeneratorType)
            True

            >>> isinstance(AnimationFamily.from_second('Bart', as_tuple=False), GeneratorType)
            True
            >>> isinstance(AnimationFamily.from_second('Dewey', as_tuple=False), GeneratorType)
            True

            >>> isinstance(AnimationFamily.from_third('Marge', as_tuple=False), GeneratorType)
            True
            >>> isinstance(AnimationFamily.from_third('Louie', as_tuple=False), GeneratorType)
            True


            >>> isinstance(NBALegendary.from_key('Johnson', as_tuple=False), GeneratorType)
            True
            >>> isinstance(NBALegendary.from_key('Jordan', as_tuple=False), GeneratorType)
            True

            >>> isinstance(NBALegendary.from_label('Magic Johnson', as_tuple=False), GeneratorType)
            True
            >>> isinstance(NBALegendary.from_label('Air Jordan', as_tuple=False), GeneratorType)
            True

    - ``has_<field_name>(field_value)``
        returns a boolean value to indicate whether there is at least one enumeration item has the given ``field_value`` in corresponding field

        .. code-block:: python

            >>> AnimationFamily.has_first('Homer')
            True
            >>> AnimationFamily.has_first('Holmes')
            False
            >>> AnimationFamily.has_first('Huey')
            True
            >>> AnimationFamily.has_first('Huth')
            False

            >>> AnimationFamily.has_second('Bart')
            True
            >>> AnimationFamily.has_second('Ben')
            False
            >>> AnimationFamily.has_second('Dewey')
            True
            >>> AnimationFamily.has_second('David')
            False

            >>> AnimationFamily.has_third('Marge')
            True
            >>> AnimationFamily.has_third('Mary')
            False
            >>> AnimationFamily.has_third('Louie')
            True
            >>> AnimationFamily.has_third('Louis')
            False


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