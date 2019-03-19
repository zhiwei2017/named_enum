import pytest
from pytest_mock import mocker
from collections import OrderedDict
from named_enum import ExtendedEnum
from .helper import generator_tester


class TVCouple(ExtendedEnum):
    GALLAGHERS = ("FRANK", "MONICA")
    MIKE_AND_MOLLY = ("Mike", "Molly")


class TestExtendedEnum:
    def test__fields(self):
        assert TVCouple._fields() == tuple()

    def test_gen(self, mocker):
        mocker.spy(TVCouple._member_map_, 'items')
        result = TVCouple.gen(True)
        expected_result = [
            ('GALLAGHERS', ("FRANK", "MONICA")),
            ('MIKE_AND_MOLLY', ("Mike", "Molly"))]
        generator_tester(result, expected_result)
        assert TVCouple._member_map_.items.call_count == 1

        result = TVCouple.gen(False)
        expected_result = [TVCouple.GALLAGHERS, TVCouple.MIKE_AND_MOLLY]
        generator_tester(result, expected_result)
        assert TVCouple._member_map_.items.call_count == 2

    @pytest.mark.parametrize('func_name, value',
                             [('firsts', True),
                              ('seconds', True),
                              ('from_first', "FRANK"),
                              ('from_first', "Mike"),
                              ('from_first', "Tommy"),
                              ('from_second', "MONICA"),
                              ('from_second', "Molly"),
                              ('from_second', "Micheal"),
                              ('has_first', "Tom"),
                              ('has_first', "Mike"),
                              ('has_first', "Tommy"),
                              ('has_second', "Jerry"),
                              ('has_second', "Molly"),
                              ('has_second', "Micheal")])
    def test_nonexistent_method(self, func_name, value):
        with pytest.raises(AttributeError):
            getattr(TVCouple, func_name)(value)

    @pytest.mark.parametrize("data_type, expected",
                             [(dict, {'GALLAGHERS': ("FRANK", "MONICA"), 'MIKE_AND_MOLLY': ("Mike", "Molly")}),
                              (list, [('GALLAGHERS', ("FRANK", "MONICA")), ('MIKE_AND_MOLLY', ("Mike", "Molly"))]),
                              (set, {('GALLAGHERS', ("FRANK", "MONICA")), ('MIKE_AND_MOLLY', ("Mike", "Molly"))}),
                              (tuple, (('GALLAGHERS', ("FRANK", "MONICA")), ('MIKE_AND_MOLLY', ("Mike", "Molly")))),
                              (OrderedDict, OrderedDict([('GALLAGHERS', ("FRANK", "MONICA")), ('MIKE_AND_MOLLY', ("Mike", "Molly"))]))])
    def test__as_data_type(self, mocker, data_type, expected):
        mocker.spy(TVCouple, 'gen')
        result = TVCouple._as_data_type(data_type)
        assert result == expected
        assert TVCouple.gen.call_count == 1
        TVCouple.gen.assert_called_with()

    @pytest.mark.parametrize("func_name, expected",
                             [("as_dict", {'GALLAGHERS': ("FRANK", "MONICA"), 'MIKE_AND_MOLLY': ("Mike", "Molly")}),
                              ("as_list", [('GALLAGHERS', ("FRANK", "MONICA")), ('MIKE_AND_MOLLY', ("Mike", "Molly"))]),
                              ("as_set", {('GALLAGHERS', ("FRANK", "MONICA")), ('MIKE_AND_MOLLY', ("Mike", "Molly"))}),
                              ("as_tuple", (('GALLAGHERS', ("FRANK", "MONICA")), ('MIKE_AND_MOLLY', ("Mike", "Molly")))),
                              ("as_ordereddict", OrderedDict([('GALLAGHERS', ("FRANK", "MONICA")), ('MIKE_AND_MOLLY', ("Mike", "Molly"))]))])
    def test_as_x(self, mocker, func_name, expected):
        mocker.spy(TVCouple, '_as_data_type')
        result = getattr(TVCouple, func_name)()
        assert result == expected
        assert TVCouple._as_data_type.call_count == 1
        TVCouple._as_data_type.assert_called_with(type(expected))

    def test___repr__(self, mocker):
        mocker.spy(type(TVCouple), '__repr__')
        assert repr(TVCouple) == "<named enum 'TVCouple'>"
        assert type(TVCouple).__repr__.call_count == 1
        assert str(TVCouple) == "<named enum 'TVCouple'>"
        assert type(TVCouple).__repr__.call_count == 2

    def test___str__(self, mocker):
        mocker.spy(TVCouple, '__str__')
        result = str(TVCouple.MIKE_AND_MOLLY)
        assert result == "TVCouple.MIKE_AND_MOLLY: ('Mike', 'Molly')"
        assert TVCouple.__str__.call_count == 1

        result = str(TVCouple.GALLAGHERS)
        assert result == "TVCouple.GALLAGHERS: ('FRANK', 'MONICA')"
        assert TVCouple.__str__.call_count == 2

    def test_describe(self, capsys):
        TVCouple.describe()
        out, err = capsys.readouterr()
        assert out == "Class: TVCouple\n          Name |               Value" \
                      "\n------------------------------------\n " \
                      "   GALLAGHERS | ('FRANK', 'MONICA')\n" \
                      "MIKE_AND_MOLLY |   ('Mike', 'Molly')\n\n"

    def test_names(self, mocker):
        mocker.spy(TVCouple._member_map_, 'keys')
        result = TVCouple.names(True)
        assert result == ('GALLAGHERS', 'MIKE_AND_MOLLY')
        assert TVCouple._member_map_.keys.call_count == 1

        result = TVCouple.names(False)
        generator_tester(result, ('GALLAGHERS', 'MIKE_AND_MOLLY'))
        assert TVCouple._member_map_.keys.call_count == 2

    def test_values(self, mocker):
        mocker.spy(TVCouple._member_map_, 'values')
        expected = (('FRANK', 'MONICA'), ('Mike', 'Molly'))
        result = TVCouple.values(True)
        assert result == expected
        assert TVCouple._member_map_.values.call_count == 1

        result = TVCouple.values(False)
        generator_tester(result, expected)
        assert TVCouple._member_map_.values.call_count == 2
