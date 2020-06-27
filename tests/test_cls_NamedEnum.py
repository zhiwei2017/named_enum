import pytest
from unittest import mock
from collections import OrderedDict
from named_enum import NamedEnum
from .helper import generator_tester


class TripleEnum(NamedEnum):
    _field_names_ = ("first", "second", "third")


class Triangle(TripleEnum):
    EQUILATERAL = (6, 6, 6)
    RIGHT = (3, 4, 5)


class TestNamedEnum:
    def test___new__(self):
        with pytest.raises(AttributeError) as exe_info:
            type("TripleFakeEnum", (NamedEnum, ),
                 {'_field_names_': ("name, value, key")})
        assert "'name' or 'value' cannot be attributes" == str(exe_info.value)

    def test__fields(self):
        assert Triangle._fields() == ('first', 'second', 'third')

        with mock.patch.object(Triangle, '_field_names_',
                               new_callable=mock.PropertyMock(return_value=None)) \
                as mocked__field_names_:
            assert Triangle._fields() == tuple()

    @pytest.mark.parametrize("name_value_pair, expected_result",
                             [(True, [('EQUILATERAL',
                                       Triangle._tuple_cls(first=6, second=6, third=6)),
                                      ('RIGHT',
                                       Triangle._tuple_cls(first=3, second=4, third=5))]),
                              (False, [Triangle.EQUILATERAL, Triangle.RIGHT])])
    def test_gen(self, name_value_pair, expected_result):
        result = Triangle.gen(name_value_pair)
        generator_tester(result, expected_result)

    @pytest.mark.parametrize('func_name, as_tuple, expected',
                             [('firsts', True, (6, 3)),
                              ('firsts', False, (6, 3)),
                              ('seconds', True, (6, 4)),
                              ('seconds', False, (6, 4)),
                              ('thirds', True, (6, 5)),
                              ('thirds', False, (6, 5))])
    @mock.patch.object(Triangle, 'gen', side_effect=Triangle.gen)
    def test__field_values(self, mocked_gen, func_name, as_tuple, expected):
        result = getattr(Triangle, func_name)(as_tuple)
        if as_tuple:
            assert result == expected
        else:
            generator_tester(result, expected)
        mocked_gen.assert_called_once_with(name_value_pair=False)

    @pytest.mark.parametrize('func_name, value, as_tuple, expected',
                             [('from_first', 6, True, (Triangle.EQUILATERAL, )),
                              ('from_first', 6, False, (Triangle.EQUILATERAL,)),
                              ('from_first', 3, True, (Triangle.RIGHT, )),
                              ('from_first', 3, False, (Triangle.RIGHT,)),
                              ('from_first', 63, True, tuple()),
                              ('from_first', 63, False, tuple()),
                              ('from_second', 6, True, (Triangle.EQUILATERAL, )),
                              ('from_second', 6, False, (Triangle.EQUILATERAL,)),
                              ('from_second', 4, True, (Triangle.RIGHT, )),
                              ('from_second', 4, False, (Triangle.RIGHT, )),
                              ('from_second', 64, True, tuple()),
                              ('from_second', 64, False, tuple()),
                              ('from_third', 6, True, (Triangle.EQUILATERAL, )),
                              ('from_third', 6, False, (Triangle.EQUILATERAL, )),
                              ('from_third', 5, True, (Triangle.RIGHT, )),
                              ('from_third', 5, False, (Triangle.RIGHT, )),
                              ('from_third', 65, True, tuple()),
                              ('from_third', 65, False, tuple())])
    @mock.patch.object(Triangle, 'gen', side_effect=Triangle.gen)
    def test__from_field(self, mocked_gen, func_name, value, as_tuple, expected):
        result = getattr(Triangle, func_name)(value, as_tuple)
        if as_tuple:
            assert result == expected
        else:
            generator_tester(result, expected)
        mocked_gen.assert_called_once_with(name_value_pair=False)

    @pytest.mark.parametrize('func_name, value, expected',
                             [('has_first', 6, True),
                              ('has_first', 3, True),
                              ('has_first', 63, False),
                              ('has_second', 6, True),
                              ('has_second', 4, True),
                              ('has_second', 64, False),
                              ('has_third', 6, True),
                              ('has_third', 5, True),
                              ('has_third', 65, False)])
    @mock.patch.object(Triangle, 'gen', side_effect=Triangle.gen)
    def test__has_field(self, mocked_gen, func_name, value, expected):
        result = getattr(Triangle, func_name)(value)
        assert result == expected
        mocked_gen.assert_called_once_with(name_value_pair=False)

    @pytest.mark.parametrize('func_name, func_param, error_type',
                             [('forths', (True, ), AttributeError),
                              ('forths', (False, ), AttributeError),
                              ('from_forth', (6, True), AttributeError),
                              ('from_forth', (6, False), AttributeError),
                              ('has_forth', (6, True), AttributeError),
                              ('has_forth', (6, False), AttributeError),
                              ])
    def test__func_fail(self, func_name, func_param, error_type):
        with pytest.raises(error_type) as excinfo:
            getattr(Triangle, func_name)(*func_param)
        assert func_name == str(excinfo.value)

    @pytest.mark.parametrize("data_type, expected",
                             [(dict, {'EQUILATERAL': Triangle._tuple_cls(first=6, second=6, third=6),
                                      'RIGHT': Triangle._tuple_cls(first=3, second=4, third=5)}),
                              (list, [('EQUILATERAL', Triangle._tuple_cls(first=6, second=6, third=6)),
                                      ('RIGHT', Triangle._tuple_cls(first=3, second=4, third=5))]),
                              (set, {('EQUILATERAL', Triangle._tuple_cls(first=6, second=6, third=6)),
                                     ('RIGHT', Triangle._tuple_cls(first=3, second=4, third=5))}),
                              (tuple, (('EQUILATERAL', Triangle._tuple_cls(first=6, second=6, third=6)),
                                       ('RIGHT', Triangle._tuple_cls(first=3, second=4, third=5)))),
                              (OrderedDict, OrderedDict([
                                  ('EQUILATERAL', Triangle._tuple_cls(first=6, second=6, third=6)),
                                  ('RIGHT', Triangle._tuple_cls(first=3, second=4, third=5))]))])
    @mock.patch.object(Triangle, 'gen', side_effect=Triangle.gen)
    def test__as_data_type(self, mocked_gen, data_type, expected):
        result = Triangle._as_data_type(data_type)
        assert result == expected
        mocked_gen.assert_called_once_with(name_value_pair=True)

    @pytest.mark.parametrize("func_name, expected",
                             [("as_dict", {'EQUILATERAL': Triangle._tuple_cls(first=6, second=6, third=6),
                                           'RIGHT': Triangle._tuple_cls(first=3, second=4, third=5)}),
                              ("as_list", [('EQUILATERAL', Triangle._tuple_cls(first=6, second=6, third=6)),
                                           ('RIGHT', Triangle._tuple_cls(first=3, second=4, third=5))]),
                              ("as_set", {('EQUILATERAL', Triangle._tuple_cls(first=6, second=6, third=6)),
                                          ('RIGHT', Triangle._tuple_cls(first=3, second=4, third=5))}),
                              ("as_tuple", (('EQUILATERAL', Triangle._tuple_cls(first=6, second=6, third=6)),
                                            ('RIGHT', Triangle._tuple_cls(first=3, second=4, third=5)))),
                              ("as_ordereddict", OrderedDict([
                                  ('EQUILATERAL', Triangle._tuple_cls(first=6, second=6, third=6)),
                                  ('RIGHT', Triangle._tuple_cls(first=3, second=4, third=5))]))])
    @mock.patch.object(Triangle, '_as_data_type', side_effect=Triangle._as_data_type)
    def test_as_x(self, mocked__as_data_type, func_name, expected):
        result = getattr(Triangle, func_name)()
        assert result == expected
        mocked__as_data_type.assert_called_once_with(type(expected))

    @mock.patch.object(type(Triangle), "__repr__",
                       side_effect=type(Triangle).__repr__, autospec=True)
    def test___repr__(self, mocked_repr):
        assert repr(Triangle) == "<named enum 'Triangle'>"
        assert mocked_repr.call_count == 1
        assert str(Triangle) == "<named enum 'Triangle'>"
        assert mocked_repr.call_count == 2

    @mock.patch.object(Triangle, "__str__", side_effect=Triangle.__str__,
                       autospec=True)
    def test___str__(self, mocked_str):
        result = str(Triangle.RIGHT)
        assert result == "Triangle.RIGHT: NamedTuple(first=3, second=4, " \
                         "third=5)"
        assert mocked_str.call_count == 1

        result = str(Triangle.EQUILATERAL)
        assert result == "Triangle.EQUILATERAL: NamedTuple(first=6, second=6, " \
                         "third=6)"
        assert mocked_str.call_count == 2

    def test_describe(self, capsys):
        Triangle.describe()
        out, err = capsys.readouterr()
        assert out == "Class: Triangle\n       Name | First | Second | Third" \
                      "\n------------------------------------\nEQUILATERAL | " \
                      "    6 |      6 |     6\n      RIGHT |     3 |      4 |" \
                      "     5\n\n"

    @pytest.mark.parametrize("as_tuple", [True, False])
    def test_names(self, as_tuple):
        expected_result = ('EQUILATERAL', 'RIGHT')
        result = Triangle.names(as_tuple)
        if as_tuple:
            assert result == expected_result
        else:
            generator_tester(result, expected_result)

    @pytest.mark.parametrize("as_tuple", [True, False])
    def test_values(self, as_tuple):
        expected_result = (Triangle._tuple_cls(first=6, second=6, third=6),
                           Triangle._tuple_cls(first=3, second=4, third=5))
        result = Triangle.values(as_tuple)
        if as_tuple:
            assert result == expected_result
        else:
            generator_tester(result, expected_result)

    def test___getattr__(self):
        result = getattr(Triangle.RIGHT, 'first')
        assert result == 3

        result = getattr(Triangle.RIGHT, 'name')
        assert result == 'RIGHT'

        with pytest.raises(AttributeError) as exe_infg:
            getattr(Triangle.RIGHT, 'key')
        assert "'Triangle' object has no attribute 'key'" == str(exe_infg.value)
