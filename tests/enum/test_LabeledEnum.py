from collections import OrderedDict
from named_enum import LabeledEnum
from ..helper import CommonEnumTest, ExtraEnumTest


class NBALegendary(LabeledEnum):
    JOHNSON = ("Johnson", "Magic Johnson")
    Jordan = ("Jordan", "Air Jordan")


class TestLabeledEnum(CommonEnumTest, ExtraEnumTest):
    # an enum class for the test methods
    enum_cls = NBALegendary
    # a map specifying multiple argument sets for a test method
    params = {
        "test___contains__": [
            dict(checked_member="JOHNSON", expected=True),
            dict(checked_member="Jordan", expected=True),
            dict(checked_member="TOM_AND_JERRY", expected=False),
            dict(checked_member=NBALegendary.JOHNSON, expected=True),
            dict(checked_member=NBALegendary.Jordan, expected=True),
            dict(checked_member=NBALegendary, expected=False),
            dict(checked_member=LabeledEnum, expected=False)],
        "test__fields": [dict(expected_normal_output=('key', 'label'))],
        "test_gen": [
            dict(name_value_pair=True,
                 expected_result=[
                     ('JOHNSON', NBALegendary._tuple_cls(key="Johnson",
                                                         label="Magic Johnson")),
                     ('Jordan', NBALegendary._tuple_cls(key="Jordan",
                                                        label="Air Jordan"))]),
            dict(name_value_pair=False,
                 expected_result=[NBALegendary.JOHNSON, NBALegendary.Jordan])],
        "test__field_values": [
            dict(func_name='keys', as_tuple=True, expected=("Johnson", "Jordan")),
            dict(func_name='keys', as_tuple=False, expected=("Johnson", "Jordan")),
            dict(func_name='labels', as_tuple=True, expected=("Magic Johnson", "Air Jordan")),
            dict(func_name='labels', as_tuple=False, expected=("Magic Johnson", "Air Jordan"))],
        "test__from_field": [
            dict(func_name='from_key', value="Johnson", as_tuple=True, expected=(NBALegendary.JOHNSON, )),
            dict(func_name='from_key', value="Johnson", as_tuple=False, expected=(NBALegendary.JOHNSON, )),
            dict(func_name='from_key', value="Jordan", as_tuple=True, expected=(NBALegendary.Jordan, )),
            dict(func_name='from_key', value="Jordan", as_tuple=False, expected=(NBALegendary.Jordan, )),
            dict(func_name='from_key', value="Johnsonmy", as_tuple=True, expected=tuple()),
            dict(func_name='from_key', value="Johnsonmy", as_tuple=False, expected=tuple()),
            dict(func_name='from_label', value="Magic Johnson", as_tuple=True, expected=(NBALegendary.JOHNSON, )),
            dict(func_name='from_label', value="Magic Johnson", as_tuple=False, expected=(NBALegendary.JOHNSON, )),
            dict(func_name='from_label', value="Air Jordan", as_tuple=True, expected=(NBALegendary.Jordan, )),
            dict(func_name='from_label', value="Air Jordan", as_tuple=False, expected=(NBALegendary.Jordan, )),
            dict(func_name='from_label', value="Micheal", as_tuple=True, expected=tuple()),
            dict(func_name='from_label', value="Micheal", as_tuple=False, expected=tuple())],
        "test__has_field": [
            dict(func_name='has_key', value="Johnson", expected=True),
            dict(func_name='has_key', value="Jordan", expected=True),
            dict(func_name='has_key', value="Johnsonmy", expected=False),
            dict(func_name='has_label', value="Magic Johnson", expected=True),
            dict(func_name='has_label', value="Air Jordan", expected=True),
            dict(func_name='has_label', value="Micheal", expected=False)],
        "test__func_fail": [
            dict(func_name='forths', func_param=(True,), error_type=AttributeError),
            dict(func_name='forths', func_param=(False,), error_type=AttributeError),
            dict(func_name='from_forth', func_param=("Johnson", True), error_type=AttributeError),
            dict(func_name='from_forth', func_param=("Johnson", False), error_type=AttributeError),
            dict(func_name='has_forth', func_param=("Johnson", True), error_type=AttributeError),
            dict(func_name='has_forth', func_param=("Johnson", False), error_type=AttributeError)],
        "test__as_data_type": [
            dict(data_type=dict,
                 expected={
                     'JOHNSON': NBALegendary._tuple_cls(key="Johnson",
                                                        label="Magic Johnson"),
                     'Jordan': NBALegendary._tuple_cls(key="Jordan",
                                                       label="Air Jordan")}),
            dict(data_type=list,
                 expected=[
                     ('JOHNSON', NBALegendary._tuple_cls(key="Johnson",
                                                         label="Magic Johnson")),
                     ('Jordan', NBALegendary._tuple_cls(key="Jordan",
                                                        label="Air Jordan"))]),
            dict(data_type=set,
                 expected={
                     ('JOHNSON', NBALegendary._tuple_cls(key="Johnson",
                                                         label="Magic Johnson")),
                     ('Jordan', NBALegendary._tuple_cls(key="Jordan",
                                                        label="Air Jordan"))}),
            dict(data_type=tuple,
                 expected=(
                     ('JOHNSON', NBALegendary._tuple_cls(key="Johnson",
                                                         label="Magic Johnson")),
                     ('Jordan', NBALegendary._tuple_cls(key="Jordan",
                                                        label="Air Jordan")))),
            dict(data_type=OrderedDict,
                 expected=OrderedDict([
                     ('JOHNSON', NBALegendary._tuple_cls(key="Johnson",
                                                         label="Magic Johnson")),
                     ('Jordan', NBALegendary._tuple_cls(key="Jordan",
                                                        label="Air Jordan"))]))],
        "test_as_x": [
            dict(func_name="as_dict",
                 expected={
                     'JOHNSON': NBALegendary._tuple_cls(key="Johnson",
                                                        label="Magic Johnson"),
                     'Jordan': NBALegendary._tuple_cls(key="Jordan",
                                                       label="Air Jordan")}),
            dict(func_name="as_list",
                 expected=[
                     ('JOHNSON', NBALegendary._tuple_cls(key="Johnson",
                                                         label="Magic Johnson")),
                     ('Jordan', NBALegendary._tuple_cls(key="Jordan",
                                                        label="Air Jordan"))]),
            dict(func_name="as_set",
                 expected={
                     ('JOHNSON', NBALegendary._tuple_cls(key="Johnson",
                                                         label="Magic Johnson")),
                     ('Jordan', NBALegendary._tuple_cls(key="Jordan",
                                                        label="Air Jordan"))}),
            dict(func_name="as_tuple",
                 expected=(
                     ('JOHNSON', NBALegendary._tuple_cls(key="Johnson",
                                                         label="Magic Johnson")),
                     ('Jordan', NBALegendary._tuple_cls(key="Jordan",
                                                        label="Air Jordan")))),
            dict(func_name="as_ordereddict",
                 expected=OrderedDict([
                     ('JOHNSON', NBALegendary._tuple_cls(key="Johnson",
                                                         label="Magic Johnson")),
                     ('Jordan', NBALegendary._tuple_cls(key="Jordan",
                                                        label="Air Jordan"))]))],
        "test___repr__": [dict(expected="<named enum 'NBALegendary'>")],
        "test___str__": [
            dict(obj=NBALegendary.Jordan,
                 expected="NBALegendary.Jordan: NamedTuple(key='Jordan', "
                          "label='Air Jordan')"),
            dict(obj=NBALegendary.JOHNSON,
                 expected="NBALegendary.JOHNSON: NamedTuple(key='Johnson', "
                          "label='Magic Johnson')")],
        "test_describe": [dict(expected="Class: NBALegendary\n   Name |     Key"
                                        " |         Label\n--------------------"
                                        "-------------\nJOHNSON | Johnson | Mag"
                                        "ic Johnson\n Jordan |  Jordan |    Air"
                                        " Jordan\n\n")],
        "test_names_values": [
            dict(func_name="names", as_tuple=True,
                 expected_result=('JOHNSON', 'Jordan')),
            dict(func_name="names", as_tuple=False,
                 expected_result=('JOHNSON', 'Jordan')),
            dict(func_name="values", as_tuple=True,
                 expected_result=(NBALegendary._tuple_cls(key="Johnson",
                                                          label="Magic Johnson"),
                                  NBALegendary._tuple_cls(key="Jordan",
                                                          label="Air Jordan"))),
            dict(func_name="values", as_tuple=False,
                 expected_result=(NBALegendary._tuple_cls(key="Johnson",
                                                          label="Magic Johnson"),
                                  NBALegendary._tuple_cls(key="Jordan",
                                                          label="Air Jordan")))],
        "test___getattr___success": [
            dict(obj=NBALegendary.Jordan, func_name="key", expected='Jordan'),
            dict(obj=NBALegendary.Jordan, func_name="name", expected='Jordan')],
        "test___getattr___fail": [
            dict(obj=NBALegendary.Jordan, func_name='nickname',
                 err_msg="'NBALegendary' object has no attribute 'nickname'")]
    }
