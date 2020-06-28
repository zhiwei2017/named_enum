import pytest
from collections import OrderedDict
from named_enum import ExtendedEnum
from .helper import CommonEnumTest


class TVCouple(ExtendedEnum):
    GALLAGHERS = ("FRANK", "MONICA")
    MIKE_AND_MOLLY = ("Mike", "Molly")


class TestExtendedEnum(CommonEnumTest):
    # an enum class for the test methods
    enum_cls = TVCouple
    # a map specifying multiple argument sets for a test method
    params = {
        "test__fields": [dict(expected_normal_output=tuple())],
        "test_gen": [
            dict(name_value_pair=True,
                 expected_result=[('GALLAGHERS', ("FRANK", "MONICA")),
                                  ('MIKE_AND_MOLLY', ("Mike", "Molly"))]),
            dict(name_value_pair=False,
                 expected_result=[TVCouple.GALLAGHERS,
                                  TVCouple.MIKE_AND_MOLLY])],
        "test__as_data_type": [
            dict(data_type=dict,
                 expected={'GALLAGHERS': ("FRANK", "MONICA"),
                           'MIKE_AND_MOLLY': ("Mike", "Molly")}),
            dict(data_type=list,
                 expected=[('GALLAGHERS', ("FRANK", "MONICA")),
                           ('MIKE_AND_MOLLY', ("Mike", "Molly"))]),
            dict(data_type=set,
                 expected={('GALLAGHERS', ("FRANK", "MONICA")),
                           ('MIKE_AND_MOLLY', ("Mike", "Molly"))}),
            dict(data_type=tuple,
                 expected=(('GALLAGHERS', ("FRANK", "MONICA")),
                           ('MIKE_AND_MOLLY', ("Mike", "Molly")))),
            dict(data_type=OrderedDict,
                 expected=OrderedDict([('GALLAGHERS', ("FRANK", "MONICA")),
                                       ('MIKE_AND_MOLLY', ("Mike", "Molly"))]))],
        "test_as_x": [
            dict(func_name="as_dict",
                 expected={'GALLAGHERS': ("FRANK", "MONICA"),
                           'MIKE_AND_MOLLY': ("Mike", "Molly")}),
            dict(func_name="as_list",
                 expected=[('GALLAGHERS', ("FRANK", "MONICA")),
                           ('MIKE_AND_MOLLY', ("Mike", "Molly"))]),
            dict(func_name="as_set",
                 expected={('GALLAGHERS', ("FRANK", "MONICA")),
                           ('MIKE_AND_MOLLY', ("Mike", "Molly"))}),
            dict(func_name="as_tuple",
                 expected=(('GALLAGHERS', ("FRANK", "MONICA")),
                           ('MIKE_AND_MOLLY', ("Mike", "Molly")))),
            dict(func_name="as_ordereddict",
                 expected=OrderedDict([('GALLAGHERS', ("FRANK", "MONICA")),
                                       ('MIKE_AND_MOLLY', ("Mike", "Molly"))]))],
        "test___repr__": [dict(expected="<named enum 'TVCouple'>")],
        "test___str__": [
            dict(obj=TVCouple.MIKE_AND_MOLLY,
                 expected="TVCouple.MIKE_AND_MOLLY: ('Mike', 'Molly')"),
            dict(obj=TVCouple.GALLAGHERS,
                 expected="TVCouple.GALLAGHERS: ('FRANK', 'MONICA')")],
        "test_describe": [dict(expected="Class: TVCouple\n          Name |     "
                                        "          Value\n---------------------"
                                        "---------------\n    GALLAGHERS | ('FR"
                                        "ANK', 'MONICA')\nMIKE_AND_MOLLY |   ('"
                                        "Mike', 'Molly')\n\n")],
        "test_names_values": [
            dict(func_name="names", as_tuple=True,
                 expected_result=('GALLAGHERS', 'MIKE_AND_MOLLY')),
            dict(func_name="names", as_tuple=False,
                 expected_result=('GALLAGHERS', 'MIKE_AND_MOLLY')),
            dict(func_name="values", as_tuple=True,
                 expected_result=(('FRANK', 'MONICA'), ('Mike', 'Molly'))),
            dict(func_name="values", as_tuple=False,
                 expected_result=(('FRANK', 'MONICA'), ('Mike', 'Molly')))],
    }

    @pytest.mark.parametrize('func_name, value',
                             [('firsts', True),
                              ('seconds', True),
                              ('from_first', "FRANK"),
                              ('from_first', "Mike"),
                              ('from_first', "Tommy"),
                              ('from_second', "MONICA"),
                              ('from_second', "Molly"),
                              ('from_second', "Micheal"),
                              ('has_first', "Tom"),
                              ('has_first', "Mike"),
                              ('has_first', "Tommy"),
                              ('has_second', "Jerry"),
                              ('has_second', "Molly"),
                              ('has_second', "Micheal")])
    def test_nonexistent_method(self, func_name, value):
        with pytest.raises(AttributeError):
            getattr(TVCouple, func_name)(value)
