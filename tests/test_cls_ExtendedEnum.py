import pytest
from unittest import mock
from collections import OrderedDict
from named_enum import ExtendedEnum
from .helper import generator_tester


class TVCouple(ExtendedEnum):
    GALLAGHERS = ("FRANK", "MONICA")
    MIKE_AND_MOLLY = ("Mike", "Molly")


class TestExtendedEnum:
    def test__fields(self):
        assert TVCouple._fields() == tuple()

    @pytest.mark.parametrize("name_value_pair, expected_result",
                             [(True, [('GALLAGHERS', ("FRANK", "MONICA")),
                                      ('MIKE_AND_MOLLY', ("Mike", "Molly"))]),
                              (False, [TVCouple.GALLAGHERS, TVCouple.MIKE_AND_MOLLY])])
    def test_gen(self, name_value_pair, expected_result):
        result = TVCouple.gen(name_value_pair)
        generator_tester(result, expected_result)

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
    @mock.patch.object(TVCouple, 'gen', side_effect=TVCouple.gen)
    def test__as_data_type(self, mocked_gen, data_type, expected):
        result = TVCouple._as_data_type(data_type)
        assert result == expected
        mocked_gen.assert_called_once_with(name_value_pair=True)

    @pytest.mark.parametrize("func_name, expected",
                             [("as_dict", {'GALLAGHERS': ("FRANK", "MONICA"), 'MIKE_AND_MOLLY': ("Mike", "Molly")}),
                              ("as_list", [('GALLAGHERS', ("FRANK", "MONICA")), ('MIKE_AND_MOLLY', ("Mike", "Molly"))]),
                              ("as_set", {('GALLAGHERS', ("FRANK", "MONICA")), ('MIKE_AND_MOLLY', ("Mike", "Molly"))}),
                              ("as_tuple", (('GALLAGHERS', ("FRANK", "MONICA")), ('MIKE_AND_MOLLY', ("Mike", "Molly")))),
                              ("as_ordereddict", OrderedDict([('GALLAGHERS', ("FRANK", "MONICA")), ('MIKE_AND_MOLLY', ("Mike", "Molly"))]))])
    @mock.patch.object(TVCouple, '_as_data_type', side_effect=TVCouple._as_data_type)
    def test_as_x(self, mocked__as_data_type, func_name, expected):
        result = getattr(TVCouple, func_name)()
        assert result == expected
        mocked__as_data_type.assert_called_once_with(type(expected))

    @mock.patch.object(type(TVCouple), "__repr__",
                       side_effect=type(TVCouple).__repr__, autospec=True)
    def test___repr__(self, mocked_repr):
        assert repr(TVCouple) == "<named enum 'TVCouple'>"
        assert mocked_repr.call_count == 1
        assert str(TVCouple) == "<named enum 'TVCouple'>"
        assert mocked_repr.call_count == 2

    @mock.patch.object(TVCouple, "__str__", side_effect=TVCouple.__str__,
                       autospec=True)
    def test___str__(self, mocked_str):
        result = str(TVCouple.MIKE_AND_MOLLY)
        assert result == "TVCouple.MIKE_AND_MOLLY: ('Mike', 'Molly')"
        assert mocked_str.call_count == 1

        result = str(TVCouple.GALLAGHERS)
        assert result == "TVCouple.GALLAGHERS: ('FRANK', 'MONICA')"
        assert mocked_str.call_count == 2

    def test_describe(self, capsys):
        TVCouple.describe()
        out, err = capsys.readouterr()
        assert out == "Class: TVCouple\n          Name |               Value" \
                      "\n------------------------------------\n " \
                      "   GALLAGHERS | ('FRANK', 'MONICA')\n" \
                      "MIKE_AND_MOLLY |   ('Mike', 'Molly')\n\n"

    @pytest.mark.parametrize("as_tuple", [True, False])
    def test_names(self, as_tuple):
        expected_result = ('GALLAGHERS', 'MIKE_AND_MOLLY')
        result = TVCouple.names(as_tuple)
        if as_tuple:
            assert result == expected_result
        else:
            generator_tester(result, expected_result)

    @pytest.mark.parametrize("as_tuple", [True, False])
    def test_values(self, as_tuple):
        expected_result = (('FRANK', 'MONICA'), ('Mike', 'Molly'))
        result = TVCouple.values(as_tuple)
        if as_tuple:
            assert result == expected_result
        else:
            generator_tester(result, expected_result)
