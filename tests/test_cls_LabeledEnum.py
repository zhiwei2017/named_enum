import pytest
from unittest import mock
from collections import OrderedDict
from named_enum import LabeledEnum
from .helper import generator_tester


class NBALegendary(LabeledEnum):
    JOHNSON = ("Johnson", "Magic Johnson")
    Jordan = ("Jordan", "Air Jordan")


class TestLabeledEnum:
    def test__fields(self):
        assert NBALegendary._fields() == ('key', 'label')

        with mock.patch.object(NBALegendary, '_field_names_',
                               new_callable=mock.PropertyMock(return_value=None)) \
                as mocked__field_names_:
            assert NBALegendary._fields() == tuple()

    @pytest.mark.parametrize("name_value_pair, expected_result",
                             [(True, [('JOHNSON', NBALegendary._tuple_cls(key="Johnson",
                                                                          label="Magic Johnson")),
                                      ('Jordan', NBALegendary._tuple_cls(key="Jordan",
                                                                         label="Air Jordan"))]),
                              (False, [NBALegendary.JOHNSON, NBALegendary.Jordan])])
    def test_gen(self, name_value_pair, expected_result):
        result = NBALegendary.gen(name_value_pair)
        generator_tester(result, expected_result)

    @pytest.mark.parametrize('func_name, as_tuple, expected',
                             [('keys', True, ("Johnson", "Jordan")),
                              ('keys', False, ("Johnson", "Jordan")),
                              ('labels', True, ("Magic Johnson", "Air Jordan")),
                              ('labels', False, ("Magic Johnson", "Air Jordan"))])
    @mock.patch.object(NBALegendary, 'gen', side_effect=NBALegendary.gen)
    def test__field_values(self, mocked_gen, func_name, as_tuple, expected):
        result = getattr(NBALegendary, func_name)(as_tuple)
        if as_tuple:
            assert result == expected
        else:
            generator_tester(result, expected)
        mocked_gen.assert_called_once_with(name_value_pair=False)

    @pytest.mark.parametrize('func_name, value, as_tuple, expected',
                             [('from_key', "Johnson", True, (NBALegendary.JOHNSON, )),
                              ('from_key', "Johnson", False, (NBALegendary.JOHNSON,)),
                              ('from_key', "Jordan", True, (NBALegendary.Jordan, )),
                              ('from_key', "Jordan", False, (NBALegendary.Jordan, )),
                              ('from_key', "Johnsonmy", True, tuple()),
                              ('from_key', "Johnsonmy", False, tuple()),
                              ('from_label', "Magic Johnson", True, (NBALegendary.JOHNSON, )),
                              ('from_label', "Magic Johnson", False, (NBALegendary.JOHNSON, )),
                              ('from_label', "Air Jordan", True, (NBALegendary.Jordan, )),
                              ('from_label', "Air Jordan", False, (NBALegendary.Jordan, )),
                              ('from_label', "Micheal", True, tuple()),
                              ('from_label', "Micheal", False, tuple())])
    @mock.patch.object(NBALegendary, 'gen', side_effect=NBALegendary.gen)
    def test__from_field(self, mocked_gen, func_name, value, as_tuple, expected):
        result = getattr(NBALegendary, func_name)(value, as_tuple)
        if as_tuple:
            assert result == expected
        else:
            generator_tester(result, expected)
        mocked_gen.assert_called_once_with(name_value_pair=False)

    @pytest.mark.parametrize('func_name, value, expected',
                             [('has_key', "Johnson", True),
                              ('has_key', "Jordan", True),
                              ('has_key', "Johnsonmy", False),
                              ('has_label', "Magic Johnson", True),
                              ('has_label', "Air Jordan", True),
                              ('has_label', "Micheal", False)])
    @mock.patch.object(NBALegendary, 'gen', side_effect=NBALegendary.gen)
    def test__has_field(self, mocked_gen, func_name, value, expected):
        result = getattr(NBALegendary, func_name)(value)
        assert result == expected
        mocked_gen.assert_called_once_with(name_value_pair=False)

    @pytest.mark.parametrize('func_name, func_param, error_type',
                             [('forths', (True, ), AttributeError),
                              ('forths', (False, ), AttributeError),
                              ('from_forth', ("Johnson", True), AttributeError),
                              ('from_forth', ("Johnson", False), AttributeError),
                              ('has_forth', ("Johnson", True), AttributeError),
                              ('has_forth', ("Johnson", False), AttributeError)])
    def test__func_fail(self, func_name, func_param, error_type):
        with pytest.raises(error_type) as excinfo:
            getattr(NBALegendary, func_name)(*func_param)
        assert func_name == str(excinfo.value)

    @pytest.mark.parametrize("data_type, expected",
                             [(dict, {'JOHNSON': NBALegendary._tuple_cls(key="Johnson",
                                                                         label="Magic Johnson"),
                                      'Jordan': NBALegendary._tuple_cls(key="Jordan",
                                                                        label="Air Jordan")}),
                              (list, [('JOHNSON', NBALegendary._tuple_cls(key="Johnson",
                                                                          label="Magic Johnson")),
                                      ('Jordan', NBALegendary._tuple_cls(key="Jordan",
                                                                         label="Air Jordan"))]),
                              (set, {('JOHNSON', NBALegendary._tuple_cls(key="Johnson",
                                                                         label="Magic Johnson")),
                                     ('Jordan', NBALegendary._tuple_cls(key="Jordan",
                                                                        label="Air Jordan"))}),
                              (tuple, (('JOHNSON', NBALegendary._tuple_cls(key="Johnson",
                                                                           label="Magic Johnson")),
                                       ('Jordan', NBALegendary._tuple_cls(key="Jordan",
                                                                          label="Air Jordan")))),
                              (OrderedDict, OrderedDict([
                                  ('JOHNSON', NBALegendary._tuple_cls(key="Johnson",
                                                                      label="Magic Johnson")),
                                  ('Jordan', NBALegendary._tuple_cls(key="Jordan",
                                                                     label="Air Jordan"))]))])
    @mock.patch.object(NBALegendary, 'gen', side_effect=NBALegendary.gen)
    def test__as_data_type(self, mocked_gen, data_type, expected):
        result = NBALegendary._as_data_type(data_type)
        assert result == expected
        mocked_gen.assert_called_once_with(name_value_pair=True)

    @pytest.mark.parametrize("func_name, expected",
                             [("as_dict", {'JOHNSON': NBALegendary._tuple_cls(key="Johnson",
                                                                              label="Magic Johnson"),
                                           'Jordan': NBALegendary._tuple_cls(key="Jordan",
                                                                             label="Air Jordan")}),
                              ("as_list", [('JOHNSON', NBALegendary._tuple_cls(key="Johnson",
                                                                               label="Magic Johnson")),
                                           ('Jordan', NBALegendary._tuple_cls(key="Jordan",
                                                                              label="Air Jordan"))]),
                              ("as_set", {('JOHNSON', NBALegendary._tuple_cls(key="Johnson",
                                                                              label="Magic Johnson")),
                                          ('Jordan', NBALegendary._tuple_cls(key="Jordan",
                                                                             label="Air Jordan"))}),
                              ("as_tuple", (('JOHNSON', NBALegendary._tuple_cls(key="Johnson",
                                                                                label="Magic Johnson")),
                                            ('Jordan', NBALegendary._tuple_cls(key="Jordan",
                                                                               label="Air Jordan")))),
                              ("as_ordereddict", OrderedDict([
                                  ('JOHNSON', NBALegendary._tuple_cls(key="Johnson",
                                                                      label="Magic Johnson")),
                                  ('Jordan', NBALegendary._tuple_cls(key="Jordan",
                                                                     label="Air Jordan"))]))])
    @mock.patch.object(NBALegendary, '_as_data_type', side_effect=NBALegendary._as_data_type)
    def test_as_x(self, mocked__as_data_type, func_name, expected):
        result = getattr(NBALegendary, func_name)()
        assert result == expected
        mocked__as_data_type.assert_called_once_with(type(expected))

    @mock.patch.object(type(NBALegendary), "__repr__",
                       side_effect=type(NBALegendary).__repr__, autospec=True)
    def test___repr__(self, mocked_repr):
        assert repr(NBALegendary) == "<named enum 'NBALegendary'>"
        assert mocked_repr.call_count == 1
        assert str(NBALegendary) == "<named enum 'NBALegendary'>"
        assert mocked_repr.call_count == 2

    @mock.patch.object(NBALegendary, "__str__", side_effect=NBALegendary.__str__,
                       autospec=True)
    def test___str__(self, mocked_str):
        result = str(NBALegendary.Jordan)
        assert result == "NBALegendary.Jordan: NamedTuple(key='Jordan', " \
                         "label='Air Jordan')"
        assert mocked_str.call_count == 1

        result = str(NBALegendary.JOHNSON)
        assert result == "NBALegendary.JOHNSON: NamedTuple(key='Johnson', " \
                         "label='Magic Johnson')"
        assert mocked_str.call_count == 2

    def test_describe(self, capsys):
        NBALegendary.describe()
        out, err = capsys.readouterr()
        assert out == "Class: NBALegendary\n   Name |     Key |         Label" \
                      "\n---------------------------------\n" \
                      "JOHNSON | Johnson | Magic Johnson\n" \
                      " Jordan |  Jordan |    Air Jordan\n\n"

    @pytest.mark.parametrize("as_tuple", [True, False])
    def test_names(self, as_tuple):
        expected_result = ('JOHNSON', 'Jordan')
        result = NBALegendary.names(as_tuple)
        if as_tuple:
            assert result == expected_result
        else:
            generator_tester(result, expected_result)

    @pytest.mark.parametrize("as_tuple", [True, False])
    def test_values(self, as_tuple):
        expected_result = (NBALegendary._tuple_cls(key="Johnson",
                                                   label="Magic Johnson"),
                           NBALegendary._tuple_cls(key="Jordan",
                                                   label="Air Jordan"))
        result = NBALegendary.values(as_tuple)
        if as_tuple:
            assert result == expected_result
        else:
            generator_tester(result, expected_result)

    def test___getattr__(self):
        result = getattr(NBALegendary.Jordan, 'key')
        assert result == "Jordan"

        result = getattr(NBALegendary.Jordan, 'name')
        assert result == 'Jordan'

        with pytest.raises(AttributeError) as exe_infg:
            getattr(NBALegendary.Jordan, 'nickname')
        assert "'NBALegendary' object has no attribute 'nickname'" == str(exe_infg.value)
