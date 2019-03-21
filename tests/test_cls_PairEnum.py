import pytest
from pytest_mock import mocker
from collections import OrderedDict
from named_enum import PairEnum
from .helper import generator_tester


class Pair(PairEnum):
    TOM_AND_JERRY = ("Tom", "Jerry")
    MIKE_AND_MOLLY = ("Mike", "Molly")


class TestPairEnum:
    def test__fields(self, mocker):
        assert Pair._fields() == ('first', 'second')

        mocker.patch.object(Pair, '_field_names_')
        Pair._field_names_ = None
        assert Pair._fields() == tuple()

    def test_gen(self, mocker):
        mocker.spy(Pair._member_map_, 'items')
        result = Pair.gen(True)
        expected_result = [
            ('TOM_AND_JERRY', Pair._tuple_cls(first="Tom", second="Jerry")),
            ('MIKE_AND_MOLLY', Pair._tuple_cls(first="Mike", second="Molly"))]
        generator_tester(result, expected_result)
        assert Pair._member_map_.items.call_count == 1

        result = Pair.gen(False)
        expected_result = [Pair.TOM_AND_JERRY, Pair.MIKE_AND_MOLLY]
        generator_tester(result, expected_result)
        assert Pair._member_map_.items.call_count == 2

    @pytest.mark.parametrize('func_name, expected',
                             [('firsts', ("Tom", "Mike")),
                              ('seconds', ("Jerry", "Molly"))])
    def test__field_values(self, mocker, func_name, expected):
        mocker.spy(Pair, 'gen')
        result = getattr(Pair, func_name)(True)
        assert result == expected
        assert Pair.gen.call_count == 1
        Pair.gen.assert_called_with(name_value_pair=False)

        result = getattr(Pair, func_name)(False)
        generator_tester(result, expected)
        assert Pair.gen.call_count == 2
        Pair.gen.assert_called_with(name_value_pair=False)

    @pytest.mark.parametrize('func_name, value, expected',
                             [('from_first', "Tom", (Pair.TOM_AND_JERRY, )),
                              ('from_first', "Mike", (Pair.MIKE_AND_MOLLY, )),
                              ('from_first', "Tommy", tuple()),
                              ('from_second', "Jerry", (Pair.TOM_AND_JERRY, )),
                              ('from_second', "Molly", (Pair.MIKE_AND_MOLLY, )),
                              ('from_second', "Micheal", tuple())])
    def test__from_field(self, mocker, func_name, value, expected):
        mocker.spy(Pair, 'gen')
        result = getattr(Pair, func_name)(value, True)
        assert result == expected
        assert Pair.gen.call_count == 1
        Pair.gen.assert_called_with(name_value_pair=False)

        result = getattr(Pair, func_name)(value, False)
        generator_tester(result, expected)
        assert Pair.gen.call_count == 2
        Pair.gen.assert_called_with(name_value_pair=False)

    @pytest.mark.parametrize('func_name, value, expected',
                             [('has_first', "Tom", True),
                              ('has_first', "Mike", True),
                              ('has_first', "Tommy", False),
                              ('has_second', "Jerry", True),
                              ('has_second', "Molly", True),
                              ('has_second', "Micheal", False)])
    def test__has_field(self, mocker, func_name, value, expected):
        mocker.spy(Pair, 'gen')
        result = getattr(Pair, func_name)(value)
        assert result == expected
        assert Pair.gen.call_count == 1
        Pair.gen.assert_called_with(name_value_pair=False)

    @pytest.mark.parametrize('func_name, func_param, error_type',
                             [('forths', (True, ), AttributeError),
                              ('forths', (False, ), AttributeError),
                              ('from_forth', ("Tom", True), AttributeError),
                              ('from_forth', ("Tom", False), AttributeError),
                              ('has_forth', ("Tom", True), AttributeError),
                              ('has_forth', ("Tom", False), AttributeError),
                              ])
    def test__func_fail(self, func_name, func_param, error_type):
        with pytest.raises(error_type) as excinfo:
            getattr(Pair, func_name)(*func_param)
        assert func_name == str(excinfo.value)

    @pytest.mark.parametrize("data_type, expected",
                             [(dict, {'TOM_AND_JERRY': Pair._tuple_cls(first="Tom", second="Jerry"), 'MIKE_AND_MOLLY': Pair._tuple_cls(first="Mike", second="Molly")}),
                              (list, [('TOM_AND_JERRY', Pair._tuple_cls(first="Tom", second="Jerry")), ('MIKE_AND_MOLLY', Pair._tuple_cls(first="Mike", second="Molly"))]),
                              (set, {('TOM_AND_JERRY', Pair._tuple_cls(first="Tom", second="Jerry")), ('MIKE_AND_MOLLY', Pair._tuple_cls(first="Mike", second="Molly"))}),
                              (tuple, (('TOM_AND_JERRY', Pair._tuple_cls(first="Tom", second="Jerry")), ('MIKE_AND_MOLLY', Pair._tuple_cls(first="Mike", second="Molly")))),
                              (OrderedDict, OrderedDict([('TOM_AND_JERRY', Pair._tuple_cls(first="Tom", second="Jerry")), ('MIKE_AND_MOLLY', Pair._tuple_cls(first="Mike", second="Molly"))]))])
    def test__as_data_type(self, mocker, data_type, expected):
        mocker.spy(Pair, 'gen')
        result = Pair._as_data_type(data_type)
        assert result == expected
        assert Pair.gen.call_count == 1
        Pair.gen.assert_called_with()

    @pytest.mark.parametrize("func_name, expected",
                             [("as_dict", {'TOM_AND_JERRY': Pair._tuple_cls(first="Tom", second="Jerry"), 'MIKE_AND_MOLLY': Pair._tuple_cls(first="Mike", second="Molly")}),
                              ("as_list", [('TOM_AND_JERRY', Pair._tuple_cls(first="Tom", second="Jerry")), ('MIKE_AND_MOLLY', Pair._tuple_cls(first="Mike", second="Molly"))]),
                              ("as_set", {('TOM_AND_JERRY', Pair._tuple_cls(first="Tom", second="Jerry")), ('MIKE_AND_MOLLY', Pair._tuple_cls(first="Mike", second="Molly"))}),
                              ("as_tuple", (('TOM_AND_JERRY', Pair._tuple_cls(first="Tom", second="Jerry")), ('MIKE_AND_MOLLY', Pair._tuple_cls(first="Mike", second="Molly")))),
                              ("as_ordereddict", OrderedDict([('TOM_AND_JERRY', Pair._tuple_cls(first="Tom", second="Jerry")), ('MIKE_AND_MOLLY', Pair._tuple_cls(first="Mike", second="Molly"))]))])
    def test_as_x(self, mocker, func_name, expected):
        mocker.spy(Pair, '_as_data_type')
        result = getattr(Pair, func_name)()
        assert result == expected
        assert Pair._as_data_type.call_count == 1
        Pair._as_data_type.assert_called_with(type(expected))

    def test___repr__(self, mocker):
        mocker.spy(type(Pair), '__repr__')
        assert repr(Pair) == "<named enum 'Pair'>"
        assert type(Pair).__repr__.call_count == 1
        assert str(Pair) == "<named enum 'Pair'>"
        assert type(Pair).__repr__.call_count == 2

    def test___str__(self, mocker):
        mocker.spy(Pair, '__str__')
        result = str(Pair.MIKE_AND_MOLLY)
        assert result == "Pair.MIKE_AND_MOLLY: NamedTuple(first='Mike', " \
                         "second='Molly')"
        assert Pair.__str__.call_count == 1

        result = str(Pair.TOM_AND_JERRY)
        assert result == "Pair.TOM_AND_JERRY: NamedTuple(first='Tom', " \
                         "second='Jerry')"
        assert Pair.__str__.call_count == 2

    def test_describe(self, capsys):
        Pair.describe()
        out, err = capsys.readouterr()
        assert out == "Class: Pair\n          Name | First | Second" \
                      "\n-------------------------------\n " \
                      "TOM_AND_JERRY |   Tom |  Jerry\n" \
                      "MIKE_AND_MOLLY |  Mike |  Molly\n\n"

    def test_names(self, mocker):
        mocker.spy(Pair._member_map_, 'keys')
        result = Pair.names(True)
        assert result == ('TOM_AND_JERRY', 'MIKE_AND_MOLLY')
        assert Pair._member_map_.keys.call_count == 1

        result = Pair.names(False)
        generator_tester(result, ('TOM_AND_JERRY', 'MIKE_AND_MOLLY'))
        assert Pair._member_map_.keys.call_count == 2

    def test_values(self, mocker):
        mocker.spy(Pair._member_map_, 'values')
        expected = (Pair._tuple_cls(first="Tom", second="Jerry"),
                    Pair._tuple_cls(first="Mike", second="Molly"))
        result = Pair.values(True)
        assert result == expected
        assert Pair._member_map_.values.call_count == 1

        result = Pair.values(False)
        generator_tester(result, expected)
        assert Pair._member_map_.values.call_count == 2

    def test___getattr__(self):
        result = getattr(Pair.MIKE_AND_MOLLY, 'first')
        assert result == "Mike"

        result = getattr(Pair.MIKE_AND_MOLLY, 'name')
        assert result == 'MIKE_AND_MOLLY'

        with pytest.raises(AttributeError) as exe_infg:
            getattr(Pair.MIKE_AND_MOLLY, 'key')
        assert "'Pair' object has no attribute 'key'" == str(exe_infg.value)
