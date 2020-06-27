import pytest
from pytest_mock import mocker
from collections import OrderedDict
from named_enum import LabeledEnum
from .helper import generator_tester


class NBALegendary(LabeledEnum):
    JOHNSON = ("Johnson", "Magic Johnson")
    Jordan = ("Jordan", "Air Jordan")


class TestLabeledEnum:
    def test__fields(self, mocker):
        assert NBALegendary._fields() == ('key', 'label')

        mocker.patch.object(NBALegendary, '_field_names_')
        NBALegendary._field_names_ = None
        assert NBALegendary._fields() == tuple()

    def test_gen(self, mocker):
        result = NBALegendary.gen(True)
        expected_result = [
            ('JOHNSON', NBALegendary._tuple_cls(key="Johnson", label="Magic Johnson")),
            ('Jordan', NBALegendary._tuple_cls(key="Jordan", label="Air Jordan"))]
        generator_tester(result, expected_result)

        result = NBALegendary.gen(False)
        expected_result = [NBALegendary.JOHNSON, NBALegendary.Jordan]
        generator_tester(result, expected_result)

    @pytest.mark.parametrize('func_name, expected',
                             [('keys', ("Johnson", "Jordan")),
                              ('labels', ("Magic Johnson", "Air Jordan"))])
    def test__field_values(self, mocker, func_name, expected):
        mocker.spy(NBALegendary, 'gen')
        result = getattr(NBALegendary, func_name)(True)
        assert result == expected
        assert NBALegendary.gen.call_count == 1
        NBALegendary.gen.assert_called_with(name_value_pair=False)

        result = getattr(NBALegendary, func_name)(False)
        generator_tester(result, expected)
        assert NBALegendary.gen.call_count == 2
        NBALegendary.gen.assert_called_with(name_value_pair=False)

    @pytest.mark.parametrize('func_name, value, expected',
                             [('from_key', "Johnson", (NBALegendary.JOHNSON, )),
                              ('from_key', "Jordan", (NBALegendary.Jordan, )),
                              ('from_key', "Johnsonmy", tuple()),
                              ('from_label', "Magic Johnson", (NBALegendary.JOHNSON, )),
                              ('from_label', "Air Jordan", (NBALegendary.Jordan, )),
                              ('from_label', "Micheal", tuple())])
    def test__from_field(self, mocker, func_name, value, expected):
        mocker.spy(NBALegendary, 'gen')
        result = getattr(NBALegendary, func_name)(value, True)
        assert result == expected
        assert NBALegendary.gen.call_count == 1
        NBALegendary.gen.assert_called_with(name_value_pair=False)

        result = getattr(NBALegendary, func_name)(value, False)
        generator_tester(result, expected)
        assert NBALegendary.gen.call_count == 2
        NBALegendary.gen.assert_called_with(name_value_pair=False)

    @pytest.mark.parametrize('func_name, value, expected',
                             [('has_key', "Johnson", True),
                              ('has_key', "Jordan", True),
                              ('has_key', "Johnsonmy", False),
                              ('has_label', "Magic Johnson", True),
                              ('has_label', "Air Jordan", True),
                              ('has_label', "Micheal", False)])
    def test__has_field(self, mocker, func_name, value, expected):
        mocker.spy(NBALegendary, 'gen')
        result = getattr(NBALegendary, func_name)(value)
        assert result == expected
        assert NBALegendary.gen.call_count == 1
        NBALegendary.gen.assert_called_with(name_value_pair=False)

    @pytest.mark.parametrize('func_name, func_param, error_type',
                             [('forths', (True, ), AttributeError),
                              ('forths', (False, ), AttributeError),
                              ('from_forth', ("Johnson", True), AttributeError),
                              ('from_forth', ("Johnson", False), AttributeError),
                              ('has_forth', ("Johnson", True), AttributeError),
                              ('has_forth', ("Johnson", False), AttributeError),
                              ])
    def test__func_fail(self, func_name, func_param, error_type):
        with pytest.raises(error_type) as excinfo:
            getattr(NBALegendary, func_name)(*func_param)
        assert func_name == str(excinfo.value)

    @pytest.mark.parametrize("data_type, expected",
                             [(dict, {'JOHNSON': NBALegendary._tuple_cls(key="Johnson", label="Magic Johnson"), 'Jordan': NBALegendary._tuple_cls(key="Jordan", label="Air Jordan")}),
                              (list, [('JOHNSON', NBALegendary._tuple_cls(key="Johnson", label="Magic Johnson")), ('Jordan', NBALegendary._tuple_cls(key="Jordan", label="Air Jordan"))]),
                              (set, {('JOHNSON', NBALegendary._tuple_cls(key="Johnson", label="Magic Johnson")), ('Jordan', NBALegendary._tuple_cls(key="Jordan", label="Air Jordan"))}),
                              (tuple, (('JOHNSON', NBALegendary._tuple_cls(key="Johnson", label="Magic Johnson")), ('Jordan', NBALegendary._tuple_cls(key="Jordan", label="Air Jordan")))),
                              (OrderedDict, OrderedDict([('JOHNSON', NBALegendary._tuple_cls(key="Johnson", label="Magic Johnson")), ('Jordan', NBALegendary._tuple_cls(key="Jordan", label="Air Jordan"))]))])
    def test__as_data_type(self, mocker, data_type, expected):
        mocker.spy(NBALegendary, 'gen')
        result = NBALegendary._as_data_type(data_type)
        assert result == expected
        assert NBALegendary.gen.call_count == 1
        NBALegendary.gen.assert_called_with()

    @pytest.mark.parametrize("func_name, expected",
                             [("as_dict", {'JOHNSON': NBALegendary._tuple_cls(key="Johnson", label="Magic Johnson"), 'Jordan': NBALegendary._tuple_cls(key="Jordan", label="Air Jordan")}),
                              ("as_list", [('JOHNSON', NBALegendary._tuple_cls(key="Johnson", label="Magic Johnson")), ('Jordan', NBALegendary._tuple_cls(key="Jordan", label="Air Jordan"))]),
                              ("as_set", {('JOHNSON', NBALegendary._tuple_cls(key="Johnson", label="Magic Johnson")), ('Jordan', NBALegendary._tuple_cls(key="Jordan", label="Air Jordan"))}),
                              ("as_tuple", (('JOHNSON', NBALegendary._tuple_cls(key="Johnson", label="Magic Johnson")), ('Jordan', NBALegendary._tuple_cls(key="Jordan", label="Air Jordan")))),
                              ("as_ordereddict", OrderedDict([('JOHNSON', NBALegendary._tuple_cls(key="Johnson", label="Magic Johnson")), ('Jordan', NBALegendary._tuple_cls(key="Jordan", label="Air Jordan"))]))])
    def test_as_x(self, mocker, func_name, expected):
        mocker.spy(NBALegendary, '_as_data_type')
        result = getattr(NBALegendary, func_name)()
        assert result == expected
        assert NBALegendary._as_data_type.call_count == 1
        NBALegendary._as_data_type.assert_called_with(type(expected))

    def test___repr__(self, mocker):
        mocker.spy(type(NBALegendary), '__repr__')
        assert repr(NBALegendary) == "<named enum 'NBALegendary'>"
        assert type(NBALegendary).__repr__.call_count == 1
        assert str(NBALegendary) == "<named enum 'NBALegendary'>"
        assert type(NBALegendary).__repr__.call_count == 2

    def test___str__(self, mocker):
        mocker.spy(NBALegendary, '__str__')
        result = str(NBALegendary.Jordan)
        assert result == "NBALegendary.Jordan: NamedTuple(key='Jordan', " \
                         "label='Air Jordan')"
        assert NBALegendary.__str__.call_count == 1

        result = str(NBALegendary.JOHNSON)
        assert result == "NBALegendary.JOHNSON: NamedTuple(key='Johnson', " \
                         "label='Magic Johnson')"
        assert NBALegendary.__str__.call_count == 2

    def test_describe(self, capsys):
        NBALegendary.describe()
        out, err = capsys.readouterr()
        assert out == "Class: NBALegendary\n   Name |     Key |         Label" \
                      "\n---------------------------------\n" \
                      "JOHNSON | Johnson | Magic Johnson\n" \
                      " Jordan |  Jordan |    Air Jordan\n\n"

    def test_names(self, mocker):
        result = NBALegendary.names(True)
        assert result == ('JOHNSON', 'Jordan')

        result = NBALegendary.names(False)
        generator_tester(result, ('JOHNSON', 'Jordan'))

    def test_values(self, mocker):
        expected = (NBALegendary._tuple_cls(key="Johnson", label="Magic Johnson"),
                    NBALegendary._tuple_cls(key="Jordan", label="Air Jordan"))
        result = NBALegendary.values(True)
        assert result == expected

        result = NBALegendary.values(False)
        generator_tester(result, expected)

    def test___getattr__(self):
        result = getattr(NBALegendary.Jordan, 'key')
        assert result == "Jordan"

        result = getattr(NBALegendary.Jordan, 'name')
        assert result == 'Jordan'

        with pytest.raises(AttributeError) as exe_infg:
            getattr(NBALegendary.Jordan, 'nickname')
        assert "'NBALegendary' object has no attribute 'nickname'" == str(exe_infg.value)
