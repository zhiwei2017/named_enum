import sys as _sys
from unittest import mock
from named_enum import namedenum
from collections import OrderedDict
from .helper import CommonEnumTest, ExtraEnumTest


TripleEnum = namedenum("TripleEnum", ["first", "second", "third"],
                       verbose=False)


class Triangle(TripleEnum):
    EQUILATERAL = (6, 6, 6)
    RIGHT = (3, 4, 5)


class TestNamedEnumFunc(CommonEnumTest, ExtraEnumTest):
    # an enum class for the test methods
    enum_cls = Triangle
    # a map specifying multiple argument sets for a test method
    params = {
        "test___contains__": [
            dict(checked_member="EQUILATERAL", expected=True),
            dict(checked_member="RIGHT", expected=True),
            dict(checked_member="TOM_AND_JERRY", expected=False),
            dict(checked_member=Triangle.EQUILATERAL, expected=True),
            dict(checked_member=Triangle.RIGHT, expected=True),
            dict(checked_member=Triangle, expected=False),
            dict(checked_member=TripleEnum, expected=False)],
        "test__fields": [dict(expected_normal_output=('first', 'second', 'third'))],
        "test_gen": [
            dict(name_value_pair=True,
                 expected_result=[
                     ('EQUILATERAL', Triangle._tuple_cls(first=6, second=6, third=6)),
                     ('RIGHT', Triangle._tuple_cls(first=3, second=4, third=5))]),
            dict(name_value_pair=False,
                 expected_result=[Triangle.EQUILATERAL, Triangle.RIGHT])],
        "test__field_values": [
            dict(func_name='firsts', as_tuple=True, expected=(6, 3)),
            dict(func_name='firsts', as_tuple=False, expected=(6, 3)),
            dict(func_name='seconds', as_tuple=True, expected=(6, 4)),
            dict(func_name='seconds', as_tuple=False, expected=(6, 4)),
            dict(func_name='thirds', as_tuple=True, expected=(6, 5)),
            dict(func_name='thirds', as_tuple=False, expected=(6, 5))],
        "test__from_field": [
            dict(func_name='from_first', value=6, as_tuple=True, expected=(Triangle.EQUILATERAL,)),
            dict(func_name='from_first', value=6, as_tuple=False, expected=(Triangle.EQUILATERAL,)),
            dict(func_name='from_first', value=3, as_tuple=True, expected=(Triangle.RIGHT,)),
            dict(func_name='from_first', value=3, as_tuple=False, expected=(Triangle.RIGHT,)),
            dict(func_name='from_first', value=63, as_tuple=True, expected=tuple()),
            dict(func_name='from_first', value=63, as_tuple=False, expected=tuple()),
            dict(func_name='from_second', value=6, as_tuple=True, expected=(Triangle.EQUILATERAL,)),
            dict(func_name='from_second', value=6, as_tuple=False, expected=(Triangle.EQUILATERAL,)),
            dict(func_name='from_second', value=4, as_tuple=True, expected=(Triangle.RIGHT,)),
            dict(func_name='from_second', value=4, as_tuple=False, expected=(Triangle.RIGHT,)),
            dict(func_name='from_second', value=64, as_tuple=True, expected=tuple()),
            dict(func_name='from_second', value=64, as_tuple=False, expected=tuple()),
            dict(func_name='from_third', value=6, as_tuple=True, expected=(Triangle.EQUILATERAL,)),
            dict(func_name='from_third', value=6, as_tuple=False, expected=(Triangle.EQUILATERAL,)),
            dict(func_name='from_third', value=5, as_tuple=True, expected=(Triangle.RIGHT,)),
            dict(func_name='from_third', value=5, as_tuple=False, expected=(Triangle.RIGHT,)),
            dict(func_name='from_third', value=65, as_tuple=True, expected=tuple()),
            dict(func_name='from_third', value=65, as_tuple=False, expected=tuple())],
        "test__has_field": [
            dict(func_name='has_first', value=6, expected=True),
            dict(func_name='has_first', value=3, expected=True),
            dict(func_name='has_first', value=63, expected=False),
            dict(func_name='has_second', value=6, expected=True),
            dict(func_name='has_second', value=4, expected=True),
            dict(func_name='has_second', value=64, expected=False),
            dict(func_name='has_third', value=6, expected=True),
            dict(func_name='has_third', value=5, expected=True),
            dict(func_name='has_third', value=65, expected=False)],
        "test__func_fail": [
            dict(func_name='forths', func_param=(True,), error_type=AttributeError),
            dict(func_name='forths', func_param=(False,), error_type=AttributeError),
            dict(func_name='from_forth', func_param=(6, True), error_type=AttributeError),
            dict(func_name='from_forth', func_param=(6, False), error_type=AttributeError),
            dict(func_name='has_forth', func_param=(6, True), error_type=AttributeError),
            dict(func_name='has_forth', func_param=(6, False), error_type=AttributeError)],
        "test__as_data_type": [
            dict(data_type=dict,
                 expected={'EQUILATERAL': Triangle._tuple_cls(first=6, second=6, third=6),
                           'RIGHT': Triangle._tuple_cls(first=3, second=4, third=5)}),
            dict(data_type=list,
                 expected=[('EQUILATERAL', Triangle._tuple_cls(first=6, second=6, third=6)),
                           ('RIGHT', Triangle._tuple_cls(first=3, second=4, third=5))]),
            dict(data_type=set,
                 expected={('EQUILATERAL', Triangle._tuple_cls(first=6, second=6, third=6)),
                           ('RIGHT', Triangle._tuple_cls(first=3, second=4, third=5))}),
            dict(data_type=tuple,
                 expected=(('EQUILATERAL', Triangle._tuple_cls(first=6, second=6, third=6)),
                           ('RIGHT', Triangle._tuple_cls(first=3, second=4, third=5)))),
            dict(data_type=OrderedDict,
                 expected=OrderedDict([
                     ('EQUILATERAL', Triangle._tuple_cls(first=6, second=6, third=6)),
                     ('RIGHT', Triangle._tuple_cls(first=3, second=4, third=5))]))],
        "test_as_x": [
            dict(func_name="as_dict",
                 expected={'EQUILATERAL': Triangle._tuple_cls(first=6, second=6, third=6),
                           'RIGHT': Triangle._tuple_cls(first=3, second=4, third=5)}),
            dict(func_name="as_list",
                 expected=[('EQUILATERAL', Triangle._tuple_cls(first=6, second=6, third=6)),
                           ('RIGHT', Triangle._tuple_cls(first=3, second=4, third=5))]),
            dict(func_name="as_set",
                 expected={('EQUILATERAL', Triangle._tuple_cls(first=6, second=6, third=6)),
                           ('RIGHT', Triangle._tuple_cls(first=3, second=4, third=5))}),
            dict(func_name="as_tuple",
                 expected=(('EQUILATERAL', Triangle._tuple_cls(first=6, second=6, third=6)),
                           ('RIGHT', Triangle._tuple_cls(first=3, second=4, third=5)))),
            dict(func_name="as_ordereddict",
                 expected=OrderedDict([
                     ('EQUILATERAL', Triangle._tuple_cls(first=6, second=6, third=6)),
                     ('RIGHT', Triangle._tuple_cls(first=3, second=4, third=5))]))],
        "test___repr__": [dict(expected="<named enum 'Triangle'>")],
        "test___str__": [
            dict(obj=Triangle.RIGHT,
                 expected="Triangle.RIGHT: NamedTuple(first=3, second=4, third=5)"),
            dict(obj=Triangle.EQUILATERAL,
                 expected="Triangle.EQUILATERAL: NamedTuple(first=6, second=6, third=6)")],
        "test_describe": [dict(expected="Class: Triangle\n       Name | First |"
                                        " Second | Third\n---------------------"
                                        "---------------\nEQUILATERAL |     6 |"
                                        "      6 |     6\n      RIGHT |     3 |"
                                        "      4 |     5\n\n")],
        "test_names_values": [
            dict(func_name="names", as_tuple=True,
                 expected_result=('EQUILATERAL', 'RIGHT')),
            dict(func_name="names", as_tuple=False,
                 expected_result=('EQUILATERAL', 'RIGHT')),
            dict(func_name="values", as_tuple=True,
                 expected_result=(Triangle._tuple_cls(first=6, second=6, third=6),
                                  Triangle._tuple_cls(first=3, second=4, third=5))),
            dict(func_name="values", as_tuple=False,
                 expected_result=(Triangle._tuple_cls(first=6, second=6, third=6),
                                  Triangle._tuple_cls(first=3, second=4, third=5)))],
        "test___getattr___success": [
            dict(obj=Triangle.RIGHT, func_name="first", expected=3),
            dict(obj=Triangle.RIGHT, func_name="name", expected='RIGHT')],
        "test___getattr___fail": [
            dict(obj=Triangle.RIGHT, func_name='key',
                 err_msg="'Triangle' object has no attribute 'key'")]
    }

    @mock.patch.object(_sys, '_getframe', side_effect=AttributeError)
    def test_error(self, mocked__getframe):
        TripleFakeEnum = namedenum('TripleFakeEnum',
                                   ("first", "second", "third"), module=None)
        assert TripleFakeEnum.__module__ == 'TripleFakeEnum'
        mocked__getframe.assert_called_with(1)
