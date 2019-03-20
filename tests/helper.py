def generator_tester(generator_iterator_to_test, expected_values):
    range_index = 0
    for actual in generator_iterator_to_test:
        assert range_index + 1 <= len(expected_values)
        assert expected_values[range_index] == actual
        range_index += 1
    assert range_index == len(expected_values)
