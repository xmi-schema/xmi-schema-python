from enum import unique
from ..bases.xmi_base_enum import XmiBaseEnum

@unique
class XmiUnitEnum(XmiBaseEnum):
    METER3 = "m^3"
    METER2 = "m^2"
    METER = "m"
    METER4 = "m^4"
    MILLIMETER4 = "mm^4"
    MILLIMETER = "mm"
    CENTIMETER = "cm"
    MILLIMETER3 = "mm^3"
    MILLIMETER2 = "mm^2"
    SECOND = "sec"


# Testing run python -m src.xmi.v2.models.enums.xmi_unit_enum

print(XmiUnitEnum.MILLIMETER.value)
print(XmiUnitEnum.METER2.name)