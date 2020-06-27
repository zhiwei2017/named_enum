import pytest
from unittest import mock
from collections import OrderedDict
from named_enum import PairEnum
from .helper import generator_tester


class Pair(PairEnum):
    TOM_AND_JERRY = ("Tom", "Jerry")
    MIKE_AND_MOLLY = ("Mike", "Molly")


class TestPairEnum:
    def test__fields(self):
        assert Pair._fields() == ('first', 'second')

        with mock.patch.object(Pair, '_field_names_',
                               new_callable=mock.PropertyMock(return_value=None)) \
                as mocked__field_names_:
            assert Pair._fields() == tuple()

    @pytest.mark.parametrize("name_value_pair, expected_result",
                             [(True, [
                                 ('TOM_AND_JERRY', Pair._tuple_cls(first="Tom",
                                                                   second="Jerry")),
                                 ('MIKE_AND_MOLLY', Pair._tuple_cls(first="Mike",
                                                                    second="Molly"))]),
                              (False, [Pair.TOM_AND_JERRY, Pair.MIKE_AND_MOLLY])])
    def test_gen(self, name_value_pair, expected_result):
        result = Pair.gen(name_value_pair)
        generator_tester(result, expected_result)

    @pytest.mark.parametrize('func_name, as_tuple, expected',
                             [('firsts', True, ("Tom", "Mike")),
                              ('firsts', False, ("Tom", "Mike")),
                              ('seconds', True, ("Jerry", "Molly")),
                              ('seconds', False, ("Jerry", "Molly"))])
    @mock.patch.object(Pair, 'gen', side_effect=Pair.gen)
    def test__field_values(self, mocked_gen, func_name, as_tuple, expected):
        result = getattr(Pair, func_name)(as_tuple)
        if as_tuple:
            assert result == expected
        else:
            generator_tester(result, expected)
        mocked_gen.assert_called_once_with(name_value_pair=False)

    @pytest.mark.parametrize('func_name, value, as_tuple, expected',
                             [('from_first', "Tom", True, (Pair.TOM_AND_JERRY, )),
                              ('from_first', "Tom", False, (Pair.TOM_AND_JERRY,)),
                              ('from_first', "Mike", True, (Pair.MIKE_AND_MOLLY, )),
                              ('from_first', "Mike", False, (Pair.MIKE_AND_MOLLY, )),
                              ('from_first', "Tommy", True, tuple()),
                              ('from_first', "Tommy", False, tuple()),
                              ('from_second', "Jerry", True, (Pair.TOM_AND_JERRY, )),
                              ('from_second', "Jerry", False, (Pair.TOM_AND_JERRY, )),
                              ('from_second', "Molly", True, (Pair.MIKE_AND_MOLLY, )),
                              ('from_second', "Molly", False, (Pair.MIKE_AND_MOLLY, )),
                              ('from_second', "Micheal", True, tuple()),
                              ('from_second', "Micheal", False, tuple())])
    @mock.patch.object(Pair, 'gen', side_effect=Pair.gen)
    def test__from_field(self, mocked_gen, func_name, value, as_tuple, expected):
        result = getattr(Pair, func_name)(value, as_tuple)
        if as_tuple:
            assert result == expected
        else:
            generator_tester(result, expected)
        mocked_gen.assert_called_once_with(name_value_pair=False)

    @pytest.mark.parametrize('func_name, value, expected',
                             [('has_first', "Tom", True),
                              ('has_first', "Mike", True),
                              ('has_first', "Tommy", False),
                              ('has_second', "Jerry", True),
                              ('has_second', "Molly", True),
                              ('has_second', "Micheal", False)])
    @mock.patch.object(Pair, 'gen', side_effect=Pair.gen)
    def test__has_field(self, mocked_gen, func_name, value, expected):
        result = getattr(Pair, func_name)(value)
        assert result == expected
        mocked_gen.assert_called_with(name_value_pair=False)

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
                             [(dict, {'TOM_AND_JERRY': Pair._tuple_cls(first="Tom", second="Jerry"),
                                      'MIKE_AND_MOLLY': Pair._tuple_cls(first="Mike", second="Molly")}),
                              (list, [('TOM_AND_JERRY', Pair._tuple_cls(first="Tom", second="Jerry")),
                                      ('MIKE_AND_MOLLY', Pair._tuple_cls(first="Mike", second="Molly"))]),
                              (set, {('TOM_AND_JERRY', Pair._tuple_cls(first="Tom", second="Jerry")),
                                     ('MIKE_AND_MOLLY', Pair._tuple_cls(first="Mike", second="Molly"))}),
                              (tuple, (('TOM_AND_JERRY', Pair._tuple_cls(first="Tom", second="Jerry")),
                                       ('MIKE_AND_MOLLY', Pair._tuple_cls(first="Mike", second="Molly")))),
                              (OrderedDict, OrderedDict([
                                  ('TOM_AND_JERRY', Pair._tuple_cls(first="Tom", second="Jerry")),
                                  ('MIKE_AND_MOLLY', Pair._tuple_cls(first="Mike", second="Molly"))]))])
    @mock.patch.object(Pair, 'gen', side_effect=Pair.gen)
    def test__as_data_type(self, mocked_gen, data_type, expected):
        result = Pair._as_data_type(data_type)
        assert result == expected
        mocked_gen.assert_called_once_with(name_value_pair=True)

    @pytest.mark.parametrize("func_name, expected",
                             [("as_dict", {'TOM_AND_JERRY': Pair._tuple_cls(first="Tom", second="Jerry"),
                                           'MIKE_AND_MOLLY': Pair._tuple_cls(first="Mike", second="Molly")}),
                              ("as_list", [('TOM_AND_JERRY', Pair._tuple_cls(first="Tom", second="Jerry")),
                                           ('MIKE_AND_MOLLY', Pair._tuple_cls(first="Mike", second="Molly"))]),
                              ("as_set", {('TOM_AND_JERRY', Pair._tuple_cls(first="Tom", second="Jerry")),
                                          ('MIKE_AND_MOLLY', Pair._tuple_cls(first="Mike", second="Molly"))}),
                              ("as_tuple", (('TOM_AND_JERRY', Pair._tuple_cls(first="Tom", second="Jerry")),
                                            ('MIKE_AND_MOLLY', Pair._tuple_cls(first="Mike", second="Molly")))),
                              ("as_ordereddict", OrderedDict([
                                  ('TOM_AND_JERRY', Pair._tuple_cls(first="Tom", second="Jerry")),
                                  ('MIKE_AND_MOLLY', Pair._tuple_cls(first="Mike", second="Molly"))]))])
    @mock.patch.object(Pair, '_as_data_type', side_effect=Pair._as_data_type)
    def test_as_x(self, mocked__as_data_type, func_name, expected):
        result = getattr(Pair, func_name)()
        assert result == expected
        mocked__as_data_type.assert_called_once_with(type(expected))

    @mock.patch.object(type(Pair), "__repr__", side_effect=type(Pair).__repr__,
                       autospec=True)
    def test___repr__(self, mocked_repr):
        assert repr(Pair) == "<named enum 'Pair'>"
        assert mocked_repr.call_count == 1
        assert str(Pair) == "<named enum 'Pair'>"
        assert mocked_repr.call_count == 2

    @mock.patch.object(Pair, "__str__", side_effect=Pair.__str__,
                       autospec=True)
    def test___str__(self, mocked_str):
        result = str(Pair.MIKE_AND_MOLLY)
        assert result == "Pair.MIKE_AND_MOLLY: NamedTuple(first='Mike', " \
                         "second='Molly')"
        assert mocked_str.call_count == 1

        result = str(Pair.TOM_AND_JERRY)
        assert result == "Pair.TOM_AND_JERRY: NamedTuple(first='Tom', " \
                         "second='Jerry')"
        assert mocked_str.call_count == 2

    def test_describe(self, capsys):
        Pair.describe()
        out, err = capsys.readouterr()
        assert out == "Class: Pair\n          Name | First | Second" \
                      "\n-------------------------------\n " \
                      "TOM_AND_JERRY |   Tom |  Jerry\n" \
                      "MIKE_AND_MOLLY |  Mike |  Molly\n\n"

    @pytest.mark.parametrize("as_tuple", [True, False])
    def test_names(self, as_tuple):
        expected_result = ('TOM_AND_JERRY', 'MIKE_AND_MOLLY')
        result = Pair.names(as_tuple)
        if as_tuple:
            assert result == expected_result
        else:
            generator_tester(result, expected_result)

    @pytest.mark.parametrize("as_tuple", [True, False])
    def test_values(self, as_tuple):
        expected_result = (Pair._tuple_cls(first="Tom", second="Jerry"),
                    Pair._tuple_cls(first="Mike", second="Molly"))
        result = Pair.values(as_tuple)
        if as_tuple:
            assert result == expected_result
        else:
            generator_tester(result, expected_result)

    def test___getattr__(self):
        result = getattr(Pair.MIKE_AND_MOLLY, 'first')
        assert result == "Mike"

        result = getattr(Pair.MIKE_AND_MOLLY, 'name')
        assert result == 'MIKE_AND_MOLLY'

        with pytest.raises(AttributeError) as exe_infg:
            getattr(Pair.MIKE_AND_MOLLY, 'key')
        assert "'Pair' object has no attribute 'key'" == str(exe_infg.value)
