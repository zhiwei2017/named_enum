import types
import pytest
from unittest import mock


def generator_tester(generator_to_test, expected_values):
    assert isinstance(generator_to_test, types.GeneratorType)
    range_index = 0
    for actual in generator_to_test:
        assert range_index + 1 <= len(expected_values)
        assert expected_values[range_index] == actual
        range_index += 1
    assert range_index == len(expected_values)


def spy(obj, name):
    method = getattr(obj, name)
    return mock.patch.object(obj, name, side_effect=method,
                             autospec=True)


class CommonEnumTest:
    enum_cls = None

    def test___contains__(self, checked_member, expected):
        assert (checked_member in self.enum_cls) == expected

    def test__fields(self, expected_normal_output):
        assert self.enum_cls._fields() == expected_normal_output

        with mock.patch.object(self.enum_cls, '_field_names_',
                               new_callable=mock.PropertyMock(return_value=None)) \
                as mocked__field_names_:
            assert self.enum_cls._fields() == tuple()

    def test_gen(self, name_value_pair, expected_result):
        result = self.enum_cls.gen(name_value_pair)
        generator_tester(result, expected_result)

    def test__as_data_type(self, data_type, expected):
        with spy(self.enum_cls, 'gen') as mocked_gen:
            result = self.enum_cls._as_data_type(data_type)
            assert result == expected
            mocked_gen.assert_called_once_with(name_value_pair=True)

    def test_as_x(self, func_name, expected):
        with spy(self.enum_cls, '_as_data_type') as mocked__as_data_type:
            result = getattr(self.enum_cls, func_name)()
            assert result == expected
            mocked__as_data_type.assert_called_once_with(type(expected))

    def test___repr__(self, expected):
        with spy(type(self.enum_cls), "__repr__") as mocked_repr:
            assert repr(self.enum_cls) == expected
            assert mocked_repr.call_count == 1
            assert str(self.enum_cls) == expected
            assert mocked_repr.call_count == 2

    def test___str__(self, obj, expected):
        with spy(self.enum_cls, "__str__") as mocked_str:
            result = str(obj)
            assert result == expected
            assert mocked_str.call_count == 1

    def test_describe(self, capsys, expected):
        self.enum_cls.describe()
        out, err = capsys.readouterr()
        assert out == expected

    def test_names_values(self, func_name, as_tuple, expected_result):
        result = getattr(self.enum_cls, func_name)(as_tuple)
        if as_tuple:
            assert result == expected_result
        else:
            generator_tester(result, expected_result)


class ExtraEnumTest:
    enum_cls = None

    def test__field_values(self, func_name, as_tuple, expected):
        with spy(self.enum_cls, 'gen') as mocked_gen:
            result = getattr(self.enum_cls, func_name)(as_tuple)
            if as_tuple:
                assert result == expected
            else:
                generator_tester(result, expected)
            mocked_gen.assert_called_once_with(name_value_pair=False)

    def test__from_field(self, func_name, value, as_tuple, expected):
        with spy(self.enum_cls, 'gen') as mocked_gen:
            result = getattr(self.enum_cls, func_name)(value, as_tuple)
            if as_tuple:
                assert result == expected
            else:
                generator_tester(result, expected)
            mocked_gen.assert_called_once_with(name_value_pair=False)

    def test__has_field(self, func_name, value, expected):
        with spy(self.enum_cls, 'gen') as mocked_gen:
            result = getattr(self.enum_cls, func_name)(value)
            assert result == expected
            mocked_gen.assert_called_once_with(name_value_pair=False)

    def test__func_fail(self, func_name, func_param, error_type):
        with pytest.raises(error_type, match=func_name):
            getattr(self.enum_cls, func_name)(*func_param)

    def test___getattr___success(self, obj, func_name, expected):
        result = getattr(obj, func_name)
        assert result == expected

    def test___getattr___fail(self, obj, func_name, err_msg):
        with pytest.raises(AttributeError, match=err_msg):
            getattr(obj, func_name)
