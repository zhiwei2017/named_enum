import pytest
from pytest_mock import mocker
from enum import Enum
from collections import OrderedDict, namedtuple
from unittest.mock import Mock
from named_enum import NamedEnumMeta, _NamedEnumDict
from .helper import generator_tester


class Color(Enum):
    red = 1
    blue = 2


class MockColor(Enum):
    red = Mock(a=1)
    blue = Mock(a=2)


class TestNamedEnumMeta:

    def test___prepare__(self, mocker):
        mocker.patch.object(NamedEnumMeta, '_get_mixins_')
        NamedEnumMeta._get_mixins_.return_value = (None, None)
        result = NamedEnumMeta.__prepare__("dummy", ())
        expected_result = _NamedEnumDict()
        assert isinstance(result, _NamedEnumDict)
        assert result == expected_result
        NamedEnumMeta._get_mixins_.assert_called_with(tuple())

        first_enum = Mock(spec=[])
        NamedEnumMeta._get_mixins_.return_value = (None, first_enum)
        result = NamedEnumMeta.__prepare__("dummy", ())

        expected_result['_generate_next_value_'] = None
        assert isinstance(result, _NamedEnumDict)
        assert result == expected_result
        NamedEnumMeta._get_mixins_.assert_called_with(tuple())

        first_enum = Mock(spec=['_generate_next_value_'],
                          _generate_next_value_=1)
        NamedEnumMeta._get_mixins_.return_value =(None, first_enum)
        result = NamedEnumMeta.__prepare__("dummy", ())
        expected_result['_generate_next_value_'] = 1
        assert isinstance(result, _NamedEnumDict)
        assert result == expected_result
        NamedEnumMeta._get_mixins_.assert_called_with(tuple())

    @pytest.mark.parametrize('_field_names_, expected',
                             [(None, tuple()), ("ha", ('key', 'value'))])
    def test__fields(self, mocker, _field_names_, expected):
        mocker.patch.object(NamedEnumMeta, '_tuple_cls', create=True)
        NamedEnumMeta._tuple_cls = namedtuple("nt", "key, value")
        mocker.patch.object(NamedEnumMeta, '_field_names_', create=True)
        NamedEnumMeta._field_names_ = _field_names_

        result = NamedEnumMeta._fields(NamedEnumMeta)
        assert result == expected

    @pytest.mark.parametrize('params, expected',
                             [((True, ), [('red', 1), ('blue', 2)]),
                              ((False, ), [Color.red, Color.blue])])
    def test_gen(self, mocker, params, expected):
        mocker.patch.object(NamedEnumMeta, '_member_map_', create=True)
        NamedEnumMeta._member_map_ = Color._member_map_

        result = NamedEnumMeta.gen(NamedEnumMeta, *params)
        generator_tester(result, expected)

    def test__field_values(self, mocker):
        mocker.patch.object(NamedEnumMeta, 'gen')
        NamedEnumMeta.gen.return_value = (item for item in MockColor)
        result = NamedEnumMeta._field_values(NamedEnumMeta, 'a', True)
        expected = (1, 2)
        assert result == expected
        NamedEnumMeta.gen.assert_called_with(name_value_pair=False)

        NamedEnumMeta.gen.return_value = (item for item in MockColor)
        result = NamedEnumMeta._field_values(NamedEnumMeta, 'a', False)
        generator_tester(result, expected)
        NamedEnumMeta.gen.assert_called_with(name_value_pair=False)

    @pytest.mark.parametrize('params, expected',
                             [(('a', 1), (MockColor.red, )),
                              (('a', 3), tuple())])
    def test__from_field(self, mocker, params, expected):
        mocker.patch.object(NamedEnumMeta, 'gen')
        NamedEnumMeta.gen.return_value = (item for item in MockColor)
        result = NamedEnumMeta._from_field(NamedEnumMeta, *params, True)
        assert result == expected
        NamedEnumMeta.gen.assert_called_with(name_value_pair=False)

        NamedEnumMeta.gen.return_value = (item for item in MockColor)
        result = NamedEnumMeta._from_field(NamedEnumMeta, *params, False)
        generator_tester(result, expected)
        NamedEnumMeta.gen.assert_called_with(name_value_pair=False)

    @pytest.mark.parametrize('params, expected',
                             [(('a', 1), True),
                              (('a', 3), False)])
    def test__has_field(self, mocker, params, expected):
        mocker.patch.object(NamedEnumMeta, 'gen')
        NamedEnumMeta.gen.return_value = (item for item in MockColor)
        result = NamedEnumMeta._has_field(NamedEnumMeta, *params)
        assert result == expected
        NamedEnumMeta.gen.assert_called_with(name_value_pair=False)

    @pytest.mark.parametrize("data_type, expected",
                             [(dict, {'red': 1, 'blue': 2}),
                              (list, [('red', 1), ('blue', 2)]),
                              (set, {('red', 1), ('blue', 2)}),
                              (tuple, (('red', 1), ('blue', 2))),
                              (OrderedDict, OrderedDict([('red', 1), ('blue', 2)]))])
    def test__as_data_type(self, mocker, data_type, expected):
        mocker.patch.object(NamedEnumMeta, 'gen')
        NamedEnumMeta.gen.return_value = ((item.name, item.value)
                                          for item in Color)
        result = NamedEnumMeta._as_data_type(NamedEnumMeta, data_type)
        assert result == expected
        NamedEnumMeta.gen.assert_called_with()

    @pytest.mark.parametrize("func_name, expected",
                             [("as_dict", {'red': 1, 'blue': 2}),
                              ("as_list", [('red', 1), ('blue', 2)]),
                              ("as_set", {('red', 1), ('blue', 2)}),
                              ("as_tuple", (('red', 1), ('blue', 2))),
                              ("as_ordereddict", OrderedDict([('red', 1), ('blue', 2)]))])
    def test_as_x(self, mocker, func_name, expected):
        mocker.patch.object(NamedEnumMeta, '_as_data_type')
        NamedEnumMeta._as_data_type.side_effect = lambda data_type: \
            data_type((item.name, item.value) for item in Color)
        result = getattr(NamedEnumMeta, func_name)(NamedEnumMeta)
        assert result == expected
        NamedEnumMeta._as_data_type.assert_called_with(type(expected))

    def test___repr__(self):
        result = NamedEnumMeta.__repr__(NamedEnumMeta)
        assert result == "<named enum 'NamedEnumMeta'>"

    def test_names(self, mocker):
        mocker.patch.object(NamedEnumMeta, '_member_map_', create=True)
        NamedEnumMeta._member_map_ = Color._member_map_

        result = NamedEnumMeta.names(NamedEnumMeta, True)
        assert result == ('red', 'blue')

        result = NamedEnumMeta.names(NamedEnumMeta, False)
        generator_tester(result, ('red', 'blue'))

    def test_values(self, mocker):
        mocker.patch.object(NamedEnumMeta, '_member_map_', create=True)
        NamedEnumMeta._member_map_ = Color._member_map_

        result = NamedEnumMeta.values(NamedEnumMeta, True)
        assert result == (1, 2)

        result = NamedEnumMeta.values(NamedEnumMeta, False)
        generator_tester(result, (1, 2))
