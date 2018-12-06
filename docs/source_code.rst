===========
Source Code
===========
.. automodule:: __init__
    :members: namedenum

    .. autoclass:: NamedEnumMeta
        :members: _fields, describe, gen, names, values, as_dict, as_list, as_set, as_tuple, as_ordereddict

    .. autoclass:: NamedEnum
        :members: _field_names_

    .. autoclass:: ExtendedEnum

    .. autoclass:: LabeledEnum

        .. autoattribute:: _field_names_

        .. method:: keys(as_tuple=True)

            Collective method to return the values of the attribute `key` from
            all the enumeration items.

            :param as_tuple: bool: returns a tuple of the values if True; otherwise returns a generator
            :return: tuple of different types/ generator

            .. code-block:: python

                >>> NBALegendary.keys()
                ('Johnson', 'Jordan')
                >>> isinstance(NBALegendary.keys(as_tuple=False), GeneratorType)
                True
                >>> list(NBALegendary.keys(as_tuple=False))
                ['Johnson', 'Jordan']

        .. method:: labels(as_tuple=True)

            Collective method to return the values of the attribute `label` from
            all the enumeration items.

            :param as_tuple: bool: returns a tuple of the values if True; otherwise returns a generator
            :return: tuple of different types/ generator

            .. code-block:: python

                >>> NBALegendary.labels()
                ('Magic Johnson', 'Air Jordan')
                >>> isinstance(NBALegendary.labels(as_tuple=False), GeneratorType)
                True
                >>> list(NBALegendary.labels(as_tuple=False))
                ['Magic Johnson', 'Air Jordan']

        .. method:: from_key(field_value, as_tuple=True)

            Returns a tuple of the defined enumeration items regarding to the
            given `field_value` of field `key`, if `as_tuple` is True; otherwise
            returns a generator.

            :param field_value: different values: key to search for
            :param as_tuple: bool: returns a tuple of the values if True; otherwise returns a generator
            :return: tuple of different types/ generator

            .. code-block:: python

                >>> NBALegendary.from_key('Johnson')
                (<NBALegendary.JOHNSON: NamedTuple(key='Johnson', label='Magic Johnson')>,)
                >>> NBALegendary.from_key('Jordan')
                (<NBALegendary.Jordan: NamedTuple(key='Jordan', label='Air Jordan')>,)
                >>> isinstance(NBALegendary.from_key('Johnson', as_tuple=False), GeneratorType)
                True
                >>> list(NBALegendary.from_key('Johnson', as_tuple=False))
                [<NBALegendary.JOHNSON: NamedTuple(key='Johnson', label='Magic Johnson')>]
                >>> isinstance(NBALegendary.from_key('Jordan', as_tuple=False), GeneratorType)
                True
                >>> list(NBALegendary.from_key('Jordan', as_tuple=False))
                [<NBALegendary.Jordan: NamedTuple(key='Jordan', label='Air Jordan')>]

        .. method:: from_label(field_value, as_tuple=True)

            Returns a tuple of the defined enumeration items regarding to the
            given `field_value` of field `label`, if `as_tuple` is True; otherwise
            returns a generator.

            :param field_value: different values: key to search for
            :param as_tuple: bool: returns a tuple of the values if True; otherwise returns a generator
            :return: tuple of different types/ generator

            .. code-block:: python

                >>> NBALegendary.from_label('Magic Johnson')
                (<NBALegendary.JOHNSON: NamedTuple(key='Johnson', label='Magic Johnson')>,)
                >>> NBALegendary.from_label('Air Jordan')
                (<NBALegendary.Jordan: NamedTuple(key='Jordan', label='Air Jordan')>,)
                >>> isinstance(NBALegendary.from_label('Magic Johnson', as_tuple=False), GeneratorType)
                True
                >>> list(NBALegendary.from_label('Magic Johnson', as_tuple=False))
                [<NBALegendary.JOHNSON: NamedTuple(key='Johnson', label='Magic Johnson')>]
                >>> isinstance(NBALegendary.from_label('Air Jordan', as_tuple=False), GeneratorType)
                True
                >>> list(NBALegendary.from_label('Air Jordan', as_tuple=False))
                [<NBALegendary.Jordan: NamedTuple(key='Jordan', label='Air Jordan')>]

        .. method:: has_key(field_value)

            Returns a boolean value which indicates if there is at least one
            enumeration item in which the value of the field `key` matches
            the given `field_value`.

            :param field_value: different values: key to search for
            :return: True, if has at least one matching; otherwise False.

            .. code-block:: python

                >>> NBALegendary.has_key('Johnson')
                True
                >>> NBALegendary.has_key('John')
                False
                >>> NBALegendary.has_key('Jordan')
                True
                >>> NBALegendary.has_key('George')
                False

        .. method:: has_label(field_value)

            Returns a boolean value which indicates if there is at least one
            enumeration item in which the value of the field `label` matches
            the given `field_value`.

            :param field_value: different values: key to search for
            :return: True, if has at least one matching; otherwise False.

            .. code-block:: python

                >>> NBALegendary.has_label('Magic Johnson')
                True
                >>> NBALegendary.has_label('King James')
                False
                >>> NBALegendary.has_label('Air Jordan')
                True
                >>> NBALegendary.has_label('The Black Mamba')
                False

    .. autoclass:: PairEnum

        .. autoattribute:: _field_names_

        .. method:: firsts(as_tuple=True)

            Collective method to return the values of the attribute `first` from
            all the enumeration items.

            :param as_tuple: bool: returns a tuple of the values if True; otherwise returns a generator
            :return: tuple of different types/ generator

            .. code-block:: python

                >>> Pair.firsts()
                ('Tom', 'Micheal')
                >>> isinstance(Pair.firsts(as_tuple=False), GeneratorType)
                True
                >>> list(Pair.firsts(as_tuple=False))
                ['Tom', 'Micheal']

        .. method:: seconds(as_tuple=True)

            Collective method to return the values of the attribute `second` from
            all the enumeration items.

            :param as_tuple: bool: returns a tuple of the values if True; otherwise returns a generator
            :return: tuple of different types/ generator

            .. code-block:: python

                >>> Pair.seconds()
                ('Jerry', 'Pippen')
                >>> isinstance(Pair.seconds(as_tuple=False), GeneratorType)
                True
                >>> list(Pair.seconds(as_tuple=False))
                ['Jerry', 'Pippen']

        .. method:: from_first(field_value, as_tuple=True)

            Returns a tuple of the defined enumeration items regarding to the
            given `field_value` of field `first`, if `as_tuple` is True; otherwise
            returns a generator.

            :param field_value: different values: key to search for
            :param as_tuple: bool: returns a tuple of the values if True; otherwise returns a generator
            :return: tuple of different types/ generator

            .. code-block:: python

                >>> Pair.from_first("Tom")
                (<Pair.TOM_AND_JERRY: NamedTuple(first='Tom', second='Jerry')>,)
                >>> Pair.from_first("Micheal")
                (<Pair.BULLS: NamedTuple(first='Micheal', second='Pippen')>,)
                >>> isinstance(Pair.from_first("Tom", as_tuple=False), GeneratorType)
                True
                >>> list(Pair.from_first("Tom", as_tuple=False))
                [<Pair.TOM_AND_JERRY: NamedTuple(first='Tom', second='Jerry')>]
                >>> isinstance(Pair.from_first("Micheal", as_tuple=False), GeneratorType)
                True
                >>> list(Pair.from_first("Micheal", as_tuple=False))
                [<Pair.BULLS: NamedTuple(first='Micheal', second='Pippen')>]

        .. method:: from_second(field_value, as_tuple=True)

            Returns a tuple of the defined enumeration items regarding to the
            given `field_value` of field `second`, if `as_tuple` is True; otherwise
            returns a generator.

            :param field_value: different values: key to search for
            :param as_tuple: bool: returns a tuple of the values if True; otherwise returns a generator
            :return: tuple of different types/ generator

            .. code-block:: python

                >>> Pair.from_second("Jerry")
                (<Pair.TOM_AND_JERRY: NamedTuple(first='Tom', second='Jerry')>,)
                >>> Pair.from_second("Pippen")
                (<Pair.BULLS: NamedTuple(first='Micheal', second='Pippen')>,)
                >>> isinstance(Pair.from_second("Jerry", as_tuple=False), GeneratorType)
                True
                >>> list(Pair.from_second("Jerry", as_tuple=False))
                [<Pair.TOM_AND_JERRY: NamedTuple(first='Tom', second='Jerry')>]
                >>> isinstance(Pair.from_second("Pippen", as_tuple=False), GeneratorType)
                True
                >>> list(Pair.from_second("Pippen", as_tuple=False))
                [<Pair.BULLS: NamedTuple(first='Micheal', second='Pippen')>]

        .. method:: has_first(field_value)

            Returns a boolean value which indicates if there is at least one
            enumeration item in which the value of the field `first` matches
            the given `field_value`.

            :param field_value: different values: key to search for
            :return: True, if has at least one matching; otherwise False.

            .. code-block:: python

                >>> Pair.has_first('Tom')
                True
                >>> Pair.has_first('Tommy')
                False
                >>> Pair.has_first('Micheal')
                True
                >>> Pair.has_first('Mike')
                False

        .. method:: has_second(field_value)

            Returns a boolean value which indicates if there is at least one
            enumeration item in which the value of the field `second` matches
            the given `field_value`.

            :param field_value: different values: key to search for
            :return: True, if has at least one matching; otherwise False.

            .. code-block:: python

                >>> Pair.has_second('Jerry')
                True
                >>> Pair.has_second('Jeremy')
                False
                >>> Pair.has_second('Pippen')
                True
                >>> Pair.has_second('Pepe')
                False