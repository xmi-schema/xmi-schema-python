from xmi.v2.models.enums.xmi_unit_enum import XmiUnitEnum

def test_xmi_unit_enum_values():
    assert XmiUnitEnum.METER3.value == "m^3"
    assert XmiUnitEnum.METER2.value == "m^2"
    assert XmiUnitEnum.METER.value == "m"
    assert XmiUnitEnum.METER4.value == "m^4"
    assert XmiUnitEnum.MILLIMETER4.value == "mm^4"
    assert XmiUnitEnum.MILLIMETER.value == "mm"
    assert XmiUnitEnum.CENTIMETER.value == "cm"
    assert XmiUnitEnum.MILLIMETER3.value == "mm^3"
    assert XmiUnitEnum.MILLIMETER2.value == "mm^2"
    assert XmiUnitEnum.SECOND.value == "sec"


# .venv/bin/python -m pytest tests/xmi/v2/test_enums/test_xmi_unit_enum.py