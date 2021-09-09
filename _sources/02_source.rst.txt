Source
======

named_enum.meta
---------------

.. automodule:: named_enum.meta
    :members:

    .. autoclass:: NamedEnumMeta
        :members: _fields, describe, gen, names, values, as_dict, as_list, as_set, as_tuple, as_ordereddict


named_enum.enum
---------------

.. automodule:: named_enum.enum
    :members: namedenum

    .. autoclass:: NamedEnum
        :members: _field_names_

    .. autoclass:: ExtendedEnum

    .. autoclass:: LabeledEnum
        :members: _field_names_, keys, labels, from_key, from_label, has_key, has_label

    .. autoclass:: PairEnum
        :members: _field_names_, firsts, seconds, from_first, from_second, has_first. has_second