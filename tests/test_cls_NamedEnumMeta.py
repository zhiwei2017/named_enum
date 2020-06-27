import pytest
from unittest import mock
from enum import Enum
from collections import OrderedDict, namedtuple
from named_enum import NamedEnumMeta, _NamedEnumDict
from .helper import generator_tester


class Color(Enum):
    red = 1
    blue = 2


class MockColor(Enum):
    red = mock.Mock(a=1)
    blue = mock.Mock(a=2)


class TestNamedEnumMeta:

    @mock.patch.object(NamedEnumMeta, '_get_mixins_')
    def test___prepare__(self, mocked__get_mixins_):
        mocked__get_mixins_.return_value = (None, None)

        result = NamedEnumMeta.__prepare__("dummy", ())
        expected_result = _NamedEnumDict()
        assert isinstance(result, _NamedEnumDict)
        assert result == expected_result
        mocked__get_mixins_.assert_called_once_with(tuple())

        mocked__get_mixins_.reset_mock()

        first_enum = mock.Mock(spec=[])
        mocked__get_mixins_.return_value = (None, first_enum)

        result = NamedEnumMeta.__prepare__("dummy", ())
        expected_result['_generate_next_value_'] = None
        assert isinstance(result, _NamedEnumDict)
        assert result == expected_result
        mocked__get_mixins_.assert_called_once_with(tuple())

        mocked__get_mixins_.reset_mock()

        first_enum = mock.Mock(spec=['_generate_next_value_'],
                               _generate_next_value_=1)
        mocked__get_mixins_.return_value =(None, first_enum)

        result = NamedEnumMeta.__prepare__("dummy", ())
        expected_result['_generate_next_value_'] = 1
        assert isinstance(result, _NamedEnumDict)
        assert result == expected_result
        mocked__get_mixins_.assert_called_once_with(tuple())

    @pytest.mark.parametrize('_field_names_, expected',
                             [(None, tuple()),
                              ("ha", ('key', 'value'))])
    @mock.patch.object(NamedEnumMeta, '_tuple_cls', create=True)
    @mock.patch.object(NamedEnumMeta, '_field_names_', create=True)
    def test__fields(self, mocked__field_names_, mocked__tuple_cls,
                     _field_names_, expected):
        NamedEnumMeta._tuple_cls = namedtuple("nt", "key, value")
        NamedEnumMeta._field_names_ = _field_names_

        result = NamedEnumMeta._fields(NamedEnumMeta)
        assert result == expected

    @pytest.mark.parametrize('params, expected',
                             [((True, ), [('red', 1), ('blue', 2)]),
                              ((False, ), [Color.red, Color.blue])])
    @mock.patch.object(NamedEnumMeta, '_member_map_', create=True,
                       new_callable=mock.PropertyMock(return_value=Color._member_map_))
    def test_gen(self, mocked__member_map_, params, expected):
        result = NamedEnumMeta.gen(NamedEnumMeta, *params)
        generator_tester(result, expected)

    @mock.patch.object(NamedEnumMeta, 'gen')
    def test__field_values(self, mocked_gen):
        mocked_gen.return_value = (item for item in MockColor)
        result = NamedEnumMeta._field_values(NamedEnumMeta, 'a', True)
        expected = (1, 2)
        assert result == expected
        mocked_gen.assert_called_once_with(name_value_pair=False)

        mocked_gen.reset_mock()

        mocked_gen.return_value = (item for item in MockColor)
        result = NamedEnumMeta._field_values(NamedEnumMeta, 'a', False)
        generator_tester(result, expected)
        mocked_gen.assert_called_once_with(name_value_pair=False)

    @pytest.mark.parametrize('params, expected',
                             [(dict(field_name='a', field_value=1, as_tuple=True), (MockColor.red, )),
                              (dict(field_name='a', field_value=1, as_tuple=False), (MockColor.red,)),
                              (dict(field_name='a', field_value=3, as_tuple=True), tuple()),
                              (dict(field_name='a', field_value=3, as_tuple=False), tuple())])
    @mock.patch.object(NamedEnumMeta, 'gen',
                       side_effect=lambda name_value_pair: (item for item in MockColor))
    def test__from_field(self, mocked_gen, params, expected):
        result = NamedEnumMeta._from_field(NamedEnumMeta, **params)
        if params["as_tuple"]:
            assert result == expected
        else:
            generator_tester(result, expected)
        mocked_gen.assert_called_with(name_value_pair=False)

    @pytest.mark.parametrize('params, expected',
                             [(('a', 1), True),
                              (('a', 3), False)])
    @mock.patch.object(NamedEnumMeta, 'gen',
                       return_value=(item for item in MockColor))
    def test__has_field(self, mocked_gen, params, expected):
        result = NamedEnumMeta._has_field(NamedEnumMeta, *params)
        assert result == expected
        mocked_gen.assert_called_once_with(name_value_pair=False)

    @pytest.mark.parametrize("data_type, expected",
                             [(dict, {'red': 1, 'blue': 2}),
                              (list, [('red', 1), ('blue', 2)]),
                              (set, {('red', 1), ('blue', 2)}),
                              (tuple, (('red', 1), ('blue', 2))),
                              (OrderedDict, OrderedDict([('red', 1), ('blue', 2)]))])
    @mock.patch.object(NamedEnumMeta, 'gen',
                       side_effect=lambda name_value_pair: ((item.name, item.value) for item in Color))
    def test__as_data_type(self, mocked_gen, data_type, expected):
        result = NamedEnumMeta._as_data_type(NamedEnumMeta, data_type)
        assert result == expected
        mocked_gen.assert_called_once_with(name_value_pair=True)

    @pytest.mark.parametrize("func_name, expected",
                             [("as_dict", {'red': 1, 'blue': 2}),
                              ("as_list", [('red', 1), ('blue', 2)]),
                              ("as_set", {('red', 1), ('blue', 2)}),
                              ("as_tuple", (('red', 1), ('blue', 2))),
                              ("as_ordereddict", OrderedDict([('red', 1), ('blue', 2)]))])
    @mock.patch.object(NamedEnumMeta, '_as_data_type',
                       side_effect=lambda data_type: data_type((item.name, item.value) for item in Color))
    def test_as_x(self, mocked__as_data_type, func_name, expected):
        result = getattr(NamedEnumMeta, func_name)(NamedEnumMeta)
        assert result == expected
        mocked__as_data_type.assert_called_once_with(type(expected))

    def test___repr__(self):
        result = NamedEnumMeta.__repr__(NamedEnumMeta)
        assert result == "<named enum 'NamedEnumMeta'>"

    @pytest.mark.parametrize("as_tuple", [True, False])
    @mock.patch.object(NamedEnumMeta, '_member_map_', create=True,
                       new_callable=mock.PropertyMock(return_value=Color._member_map_))
    def test_names(self, mocked__member_map_, as_tuple):
        expected_result = ('red', 'blue')
        result = NamedEnumMeta.names(NamedEnumMeta, as_tuple)
        if as_tuple:
            assert result == expected_result
        else:
            generator_tester(result, expected_result)

    @pytest.mark.parametrize("as_tuple", [True, False])
    @mock.patch.object(NamedEnumMeta, '_member_map_', create=True,
                       new_callable=mock.PropertyMock(return_value=Color._member_map_))
    def test_values(self, mocked__member_map_, as_tuple):
        expected_result = (1, 2)
        result = NamedEnumMeta.values(NamedEnumMeta, as_tuple)
        if as_tuple:
            assert result == expected_result
        else:
            generator_tester(result, expected_result)
