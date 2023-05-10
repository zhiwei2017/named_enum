import pytest
import sys as _sys
from enum import _EnumDict
from named_enum.meta import _NamedEnumDict
from collections import namedtuple


class TestNamedEnumDict:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.dict = _NamedEnumDict()
        self.dict._cls_name = "Dummy"

    @pytest.fixture
    def fill(self):
        """
        Fill the _NamedEnumDict dictionary with different kinds of value names.
        """
        # that's the only allowed underline surrounded name, but it's not
        # included in the member_names feature
        self.dict["_field_names_"] = "b"
        # normal case
        self.dict["a"] = ["a", "b"]
        # with one underline is ok
        self.dict["_a"] = "a"
        # double underline names are not included in the member_names feature
        self.dict["__a__"] = "a"

        self.dict["b"] = 1

        assert self.dict == {"_field_names_": "b", "a": ["a", "b"],
                             "_a": "a", "__a__": "a", "b": 1}
        assert self.dict._last_values == [["a", "b"], "a", 1]
        if _sys.version_info < (3, 11):
            assert self.dict._member_names == ["a", "_a", "b"]
        else:
            assert self.dict._member_names == {'_a': None, 'a': None, 'b': None}

    def test___setitem__(self):
        """
        Try to setup the value in the dictionary, the special case is that
        setting a key with underline surround and not '_field_names_', it
        should raise the ValueError.
        """
        self.dict["_field_names_"] = "b"
        assert self.dict["_field_names_"] == "b"

        self.dict["a"] = "a"
        assert self.dict["a"] == "a"

        self.dict["_a"] = "a"
        assert self.dict["_a"] == "a"

        self.dict["__a__"] = "a"
        assert self.dict["__a__"] == "a"

        with pytest.raises(ValueError) as excinfo:
            self.dict["_a_"] = "a"
        if _sys.version_info < (3, 11):
            # inherit previous flags and _generate_next_value_ function
            assert '_names_ are reserved for future Enum use' in str(excinfo.value)
        else:
            assert "_sunder_ names, such as '_a_', are reserved for future Enum use" in str(excinfo.value)

    def test__clean(self, fill):
        """
        Test the clean method, which cleans the _last_values, _member_names,
        and the keys without underline or double underline surround.
        """
        self.dict._clean()

        assert self.dict == {"_field_names_": "b", "__a__": 'a'}
        tmp = _EnumDict()
        assert self.dict._last_values == tmp._last_values
        assert self.dict._member_names == tmp._member_names

    def test__convert_fail(self, fill):
        """Test the _convert function in failure case."""
        # if the tuple_cls is tuple, it should raise an error
        with pytest.raises(ValueError) as excinfo:
            self.dict._convert(tuple)
        assert "'tuple_cls' must be a customized tuple class using namedtuple" \
               " generated class instead." in str(excinfo.value)

        tuple_cls = namedtuple("NamedTuple", ["key", "value"])
        self.dict._clean()
        self.dict['b'] = 1
        with pytest.raises(ValueError) as exe_info:
            self.dict._convert(tuple_cls)
        assert "Unable to unpack the value '1' as NamedTuple for the fields." in str(exe_info.value)

        self.dict._clean()
        self.dict['b'] = "1,2"
        with pytest.raises(ValueError) as exe_info:
            self.dict._convert(tuple_cls)
        assert "Unable to unpack the value '1,2' as NamedTuple for the fields." in str(exe_info.value)

    def test__convert_success_one_feature(self, fill):
        """Test the _convert function in success case."""
        # create a named tuple and call the _convert, everything should be fine.
        tuple_cls = namedtuple("NamedTuple", ["key"])
        self.dict._convert(tuple_cls)

        assert self.dict == {"_field_names_": "b",
                             "a": tuple_cls(key=['a', 'b']),
                             "_a": tuple_cls(key='a'),
                             "__a__": "a",
                             'b': tuple_cls(key=1)}
        assert self.dict._last_values == [tuple_cls(key=['a', 'b']),
                                          tuple_cls(key='a'),
                                          tuple_cls(key=1)]
        if _sys.version_info < (3, 11):
            assert self.dict._member_names == ["a", "_a", "b"]
        else:
            assert self.dict._member_names == {'_a': None, 'a': None, 'b': None}

    def test__convert_success_more_feature(self, fill):
        """Test the _convert function in success case."""
        # create a named tuple and call the _convert, everything should be fine.
        tuple_cls = namedtuple("NamedTuple", ["key", "value"])
        self.dict._clean()
        self.dict['b'] = [111, 222]
        self.dict._convert(tuple_cls)

        assert self.dict == {"_field_names_": "b",
                             '__a__': 'a',
                             'b': tuple_cls(key=111, value=222)}
        assert self.dict._last_values == [tuple_cls(key=111, value=222)]
        if _sys.version_info < (3, 11):
            assert self.dict._member_names == ["b"]
        else:
            assert self.dict._member_names == {'b': None}
