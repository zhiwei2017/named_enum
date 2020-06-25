from collections import OrderedDict
from named_enum import PairEnum
from .helper import CommonEnumTest, ExtraEnumTest


class Pair(PairEnum):
    TOM_AND_JERRY = ("Tom", "Jerry")
    MIKE_AND_MOLLY = ("Mike", "Molly")


class TestPairEnum(CommonEnumTest, ExtraEnumTest):
    # an enum class for the test methods
    enum_cls = Pair
    # a map specifying multiple argument sets for a test method
    params = {
        "test___contains__": [
            dict(checked_member="TOM_AND_JERRY", expected=True),
            dict(checked_member="MIKE_AND_MOLLY", expected=True),
            dict(checked_member="GALLAGHERS", expected=False),
            dict(checked_member=Pair.TOM_AND_JERRY, expected=True),
            dict(checked_member=Pair.MIKE_AND_MOLLY, expected=True),
            dict(checked_member=Pair, expected=False),
            dict(checked_member=PairEnum, expected=False)],
        "test__fields": [dict(expected_normal_output=('first', 'second'))],
        "test_gen": [
            dict(name_value_pair=True,
                 expected_result=[
                     ('TOM_AND_JERRY', Pair._tuple_cls(first="Tom",
                                                       second="Jerry")),
                     ('MIKE_AND_MOLLY', Pair._tuple_cls(first="Mike",
                                                        second="Molly"))]),
            dict(name_value_pair=False,
                 expected_result=[Pair.TOM_AND_JERRY, Pair.MIKE_AND_MOLLY])],
        "test__field_values": [
            dict(func_name='firsts', as_tuple=True, expected=("Tom", "Mike")),
            dict(func_name='firsts', as_tuple=False, expected=("Tom", "Mike")),
            dict(func_name='seconds', as_tuple=True, expected=("Jerry", "Molly")),
            dict(func_name='seconds', as_tuple=False, expected=("Jerry", "Molly"))],
        "test__from_field": [
            dict(func_name='from_first', value="Tom", as_tuple=True, expected=(Pair.TOM_AND_JERRY,)),
            dict(func_name='from_first', value="Tom", as_tuple=False, expected=(Pair.TOM_AND_JERRY,)),
            dict(func_name='from_first', value="Mike", as_tuple=True, expected=(Pair.MIKE_AND_MOLLY,)),
            dict(func_name='from_first', value="Mike", as_tuple=False, expected=(Pair.MIKE_AND_MOLLY,)),
            dict(func_name='from_first', value="Tommy", as_tuple=True, expected=tuple()),
            dict(func_name='from_first', value="Tommy", as_tuple=False, expected=tuple()),
            dict(func_name='from_second', value="Jerry", as_tuple=True, expected=(Pair.TOM_AND_JERRY,)),
            dict(func_name='from_second', value="Jerry", as_tuple=False, expected=(Pair.TOM_AND_JERRY,)),
            dict(func_name='from_second', value="Molly", as_tuple=True, expected=(Pair.MIKE_AND_MOLLY,)),
            dict(func_name='from_second', value="Molly", as_tuple=False, expected=(Pair.MIKE_AND_MOLLY,)),
            dict(func_name='from_second', value="Micheal", as_tuple=True, expected=tuple()),
            dict(func_name='from_second', value="Micheal", as_tuple=False, expected=tuple())],
        "test__has_field": [
            dict(func_name='has_first', value="Tom", expected=True),
            dict(func_name='has_first', value="Mike", expected=True),
            dict(func_name='has_first', value="Tommy", expected=False),
            dict(func_name='has_second', value="Jerry", expected=True),
            dict(func_name='has_second', value="Molly", expected=True),
            dict(func_name='has_second', value="Micheal", expected=False)],
        "test__func_fail": [
            dict(func_name='forths', func_param=(True,), error_type=AttributeError),
            dict(func_name='forths', func_param=(False,), error_type=AttributeError),
            dict(func_name='from_forth', func_param=("Tom", True), error_type=AttributeError),
            dict(func_name='from_forth', func_param=("Tom", False), error_type=AttributeError),
            dict(func_name='has_forth', func_param=("Tom", True), error_type=AttributeError),
            dict(func_name='has_forth', func_param=("Tom", False), error_type=AttributeError)],
        "test__as_data_type": [
            dict(data_type=dict,
                 expected={'TOM_AND_JERRY': Pair._tuple_cls(first="Tom", second="Jerry"),
                           'MIKE_AND_MOLLY': Pair._tuple_cls(first="Mike", second="Molly")}),
            dict(data_type=list,
                 expected=[('TOM_AND_JERRY', Pair._tuple_cls(first="Tom", second="Jerry")),
                           ('MIKE_AND_MOLLY', Pair._tuple_cls(first="Mike", second="Molly"))]),
            dict(data_type=set,
                 expected={('TOM_AND_JERRY', Pair._tuple_cls(first="Tom", second="Jerry")),
                           ('MIKE_AND_MOLLY', Pair._tuple_cls(first="Mike", second="Molly"))}),
            dict(data_type=tuple,
                 expected=(('TOM_AND_JERRY', Pair._tuple_cls(first="Tom", second="Jerry")),
                           ('MIKE_AND_MOLLY', Pair._tuple_cls(first="Mike", second="Molly")))),
            dict(data_type=OrderedDict,
                 expected=OrderedDict([
                     ('TOM_AND_JERRY', Pair._tuple_cls(first="Tom", second="Jerry")),
                     ('MIKE_AND_MOLLY', Pair._tuple_cls(first="Mike", second="Molly"))]))],
        "test_as_x": [
            dict(func_name="as_dict",
                 expected={'TOM_AND_JERRY': Pair._tuple_cls(first="Tom", second="Jerry"),
                           'MIKE_AND_MOLLY': Pair._tuple_cls(first="Mike", second="Molly")}),
            dict(func_name="as_list",
                 expected=[('TOM_AND_JERRY', Pair._tuple_cls(first="Tom", second="Jerry")),
                           ('MIKE_AND_MOLLY', Pair._tuple_cls(first="Mike", second="Molly"))]),
            dict(func_name="as_set",
                 expected={('TOM_AND_JERRY', Pair._tuple_cls(first="Tom", second="Jerry")),
                           ('MIKE_AND_MOLLY', Pair._tuple_cls(first="Mike", second="Molly"))}),
            dict(func_name="as_tuple",
                 expected=(('TOM_AND_JERRY', Pair._tuple_cls(first="Tom", second="Jerry")),
                           ('MIKE_AND_MOLLY', Pair._tuple_cls(first="Mike", second="Molly")))),
            dict(func_name="as_ordereddict",
                 expected=OrderedDict([
                     ('TOM_AND_JERRY', Pair._tuple_cls(first="Tom", second="Jerry")),
                     ('MIKE_AND_MOLLY', Pair._tuple_cls(first="Mike", second="Molly"))]))],
        "test___repr__": [dict(expected="<named enum 'Pair'>")],
        "test___str__": [
            dict(obj=Pair.MIKE_AND_MOLLY,
                 expected="Pair.MIKE_AND_MOLLY: NamedTuple(first='Mike', second='Molly')"),
            dict(obj=Pair.TOM_AND_JERRY,
                 expected="Pair.TOM_AND_JERRY: NamedTuple(first='Tom', second='Jerry')")],
        "test_describe": [dict(expected="Class: Pair\n          Name | First | "
                                        "Second\n------------------------------"
                                        "-\n TOM_AND_JERRY |   Tom |  Jerry\n"
                                        "MIKE_AND_MOLLY |  Mike |  Molly\n\n")],
        "test_names_values": [
            dict(func_name="names", as_tuple=True,
                 expected_result=('TOM_AND_JERRY', 'MIKE_AND_MOLLY')),
            dict(func_name="names", as_tuple=False,
                 expected_result=('TOM_AND_JERRY', 'MIKE_AND_MOLLY')),
            dict(func_name="values", as_tuple=True,
                 expected_result=(Pair._tuple_cls(first="Tom", second="Jerry"),
                                  Pair._tuple_cls(first="Mike", second="Molly"))),
            dict(func_name="values", as_tuple=False,
                 expected_result=(Pair._tuple_cls(first="Tom", second="Jerry"),
                                  Pair._tuple_cls(first="Mike", second="Molly")))],
        "test___getattr___success": [
            dict(obj=Pair.MIKE_AND_MOLLY, func_name="first", expected='Mike'),
            dict(obj=Pair.MIKE_AND_MOLLY, func_name="name", expected='MIKE_AND_MOLLY')],
        "test___getattr___fail": [
            dict(obj=Pair.MIKE_AND_MOLLY, func_name='key',
                 err_msg="'Pair' object has no attribute 'key'")]
    }
