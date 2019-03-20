import pytest
from pytest_mock import mocker
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
            class TripleFakeEnum(NamedEnum):
                _field_names_ = ("name, value, key")
        assert "'name' or 'value' cannot be attributes" == str(exe_info.value)

    def test__fields(self, mocker):
        assert Triangle._fields() == ('first', 'second', 'third')

        mocker.patch.object(Triangle, '_field_names_')
        Triangle._field_names_ = None
        assert Triangle._fields() == tuple()

    def test_gen(self, mocker):
        mocker.spy(Triangle._member_map_, 'items')
        result = Triangle.gen(True)
        expected_result = [
            ('EQUILATERAL', Triangle._tuple_cls(first=6, second=6, third=6)),
            ('RIGHT', Triangle._tuple_cls(first=3, second=4, third=5))]
        generator_tester(result, expected_result)
        assert Triangle._member_map_.items.call_count == 1

        result = Triangle.gen(False)
        expected_result = [Triangle.EQUILATERAL, Triangle.RIGHT]
        generator_tester(result, expected_result)
        assert Triangle._member_map_.items.call_count == 2

    @pytest.mark.parametrize('func_name, expected',
                             [('firsts', (6, 3)),
                              ('seconds', (6, 4)),
                              ('thirds', (6, 5))])
    def test__field_values(self, mocker, func_name, expected):
        mocker.spy(Triangle, 'gen')
        result = getattr(Triangle, func_name)(True)
        assert result == expected
        assert Triangle.gen.call_count == 1
        Triangle.gen.assert_called_with(name_value_pair=False)

        result = getattr(Triangle, func_name)(False)
        generator_tester(result, expected)
        assert Triangle.gen.call_count == 2
        Triangle.gen.assert_called_with(name_value_pair=False)

    @pytest.mark.parametrize('func_name, value, expected',
                             [('from_first', 6, (Triangle.EQUILATERAL, )),
                              ('from_first', 3, (Triangle.RIGHT, )),
                              ('from_first', 63, tuple()),
                              ('from_second', 6, (Triangle.EQUILATERAL, )),
                              ('from_second', 4, (Triangle.RIGHT, )),
                              ('from_second', 64, tuple()),
                              ('from_third', 6, (Triangle.EQUILATERAL, )),
                              ('from_third', 5, (Triangle.RIGHT, )),
                              ('from_third', 65, tuple())])
    def test__from_field(self, mocker, func_name, value, expected):
        mocker.spy(Triangle, 'gen')
        result = getattr(Triangle, func_name)(value, True)
        assert result == expected
        assert Triangle.gen.call_count == 1
        Triangle.gen.assert_called_with(name_value_pair=False)

        result = getattr(Triangle, func_name)(value, False)
        generator_tester(result, expected)
        assert Triangle.gen.call_count == 2
        Triangle.gen.assert_called_with(name_value_pair=False)

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
    def test__has_field(self, mocker, func_name, value, expected):
        mocker.spy(Triangle, 'gen')
        result = getattr(Triangle, func_name)(value)
        assert result == expected
        assert Triangle.gen.call_count == 1
        Triangle.gen.assert_called_with(name_value_pair=False)

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
                             [(dict, {'EQUILATERAL': Triangle._tuple_cls(first=6, second=6, third=6), 'RIGHT': Triangle._tuple_cls(first=3, second=4, third=5)}),
                              (list, [('EQUILATERAL', Triangle._tuple_cls(first=6, second=6, third=6)), ('RIGHT', Triangle._tuple_cls(first=3, second=4, third=5))]),
                              (set, {('EQUILATERAL', Triangle._tuple_cls(first=6, second=6, third=6)), ('RIGHT', Triangle._tuple_cls(first=3, second=4, third=5))}),
                              (tuple, (('EQUILATERAL', Triangle._tuple_cls(first=6, second=6, third=6)), ('RIGHT', Triangle._tuple_cls(first=3, second=4, third=5)))),
                              (OrderedDict, OrderedDict([('EQUILATERAL', Triangle._tuple_cls(first=6, second=6, third=6)), ('RIGHT', Triangle._tuple_cls(first=3, second=4, third=5))]))])
    def test__as_data_type(self, mocker, data_type, expected):
        mocker.spy(Triangle, 'gen')
        result = Triangle._as_data_type(data_type)
        assert result == expected
        assert Triangle.gen.call_count == 1
        Triangle.gen.assert_called_with()

    @pytest.mark.parametrize("func_name, expected",
                             [("as_dict", {'EQUILATERAL': Triangle._tuple_cls(first=6, second=6, third=6), 'RIGHT': Triangle._tuple_cls(first=3, second=4, third=5)}),
                              ("as_list", [('EQUILATERAL', Triangle._tuple_cls(first=6, second=6, third=6)), ('RIGHT', Triangle._tuple_cls(first=3, second=4, third=5))]),
                              ("as_set", {('EQUILATERAL', Triangle._tuple_cls(first=6, second=6, third=6)), ('RIGHT', Triangle._tuple_cls(first=3, second=4, third=5))}),
                              ("as_tuple", (('EQUILATERAL', Triangle._tuple_cls(first=6, second=6, third=6)), ('RIGHT', Triangle._tuple_cls(first=3, second=4, third=5)))),
                              ("as_ordereddict", OrderedDict([('EQUILATERAL', Triangle._tuple_cls(first=6, second=6, third=6)), ('RIGHT', Triangle._tuple_cls(first=3, second=4, third=5))]))])
    def test_as_x(self, mocker, func_name, expected):
        mocker.spy(Triangle, '_as_data_type')
        result = getattr(Triangle, func_name)()
        assert result == expected
        assert Triangle._as_data_type.call_count == 1
        Triangle._as_data_type.assert_called_with(type(expected))

    def test___repr__(self, mocker):
        mocker.spy(type(Triangle), '__repr__')
        assert repr(Triangle) == "<named enum 'Triangle'>"
        assert type(Triangle).__repr__.call_count == 1
        assert str(Triangle) == "<named enum 'Triangle'>"
        assert type(Triangle).__repr__.call_count == 2

    def test___str__(self, mocker):
        mocker.spy(Triangle, '__str__')
        result = str(Triangle.RIGHT)
        assert result == "Triangle.RIGHT: NamedTuple(first=3, second=4, " \
                         "third=5)"
        assert Triangle.__str__.call_count == 1

        result = str(Triangle.EQUILATERAL)
        assert result == "Triangle.EQUILATERAL: NamedTuple(first=6, second=6, " \
                         "third=6)"
        assert Triangle.__str__.call_count == 2

    def test_describe(self, capsys):
        Triangle.describe()
        out, err = capsys.readouterr()
        assert out == "Class: Triangle\n       Name | First | Second | Third" \
                      "\n------------------------------------\nEQUILATERAL | " \
                      "    6 |      6 |     6\n      RIGHT |     3 |      4 |" \
                      "     5\n\n"

    def test_names(self, mocker):
        mocker.spy(Triangle._member_map_, 'keys')
        result = Triangle.names(True)
        assert result == ('EQUILATERAL', 'RIGHT')
        assert Triangle._member_map_.keys.call_count == 1

        result = Triangle.names(False)
        generator_tester(result, ('EQUILATERAL', 'RIGHT'))
        assert Triangle._member_map_.keys.call_count == 2

    def test_values(self, mocker):
        mocker.spy(Triangle._member_map_, 'values')
        expected = (Triangle._tuple_cls(first=6, second=6, third=6),
                    Triangle._tuple_cls(first=3, second=4, third=5))
        result = Triangle.values(True)
        assert result == expected
        assert Triangle._member_map_.values.call_count == 1

        result = Triangle.values(False)
        generator_tester(result, expected)
        assert Triangle._member_map_.values.call_count == 2

    def test___getattr__(self):
        result = getattr(Triangle.RIGHT, 'first')
        assert result == 3

        result = getattr(Triangle.RIGHT, 'name')
        assert result == 'RIGHT'

        with pytest.raises(AttributeError) as exe_infg:
            getattr(Triangle.RIGHT, 'key')
        assert "'Triangle' object has no attribute 'key'" == str(exe_infg.value)
