import types


def generator_tester(generator_to_test, expected_values):
    assert isinstance(generator_to_test, types.GeneratorType)
    range_index = 0
    for actual in generator_to_test:
        assert range_index + 1 <= len(expected_values)
        assert expected_values[range_index] == actual
        range_index += 1
    assert range_index == len(expected_values)
