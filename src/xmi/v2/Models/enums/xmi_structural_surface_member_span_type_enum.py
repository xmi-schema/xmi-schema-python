from enum import unique
from ..bases.xmi_base_enum import XmiBaseEnum

@unique
class XmiStructuralSurfaceMemberSpanTypeEnum(XmiBaseEnum):
    ONE_WAY = "One Way"
    TWO_WAY = "Two Way"


# Testing run python -m src.xmi.v2.models.enums.xmi_structural_surface_member_span_type_enum

print(XmiStructuralSurfaceMemberSpanTypeEnum.ONE_WAY.value)
print(XmiStructuralSurfaceMemberSpanTypeEnum.TWO_WAY.name)