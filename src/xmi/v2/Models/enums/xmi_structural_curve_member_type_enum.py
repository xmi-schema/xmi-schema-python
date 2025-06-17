from enum import unique
from ..bases.xmi_base_enum import XmiBaseEnum

@unique
class XmiStructuralCurveMemberTypeEnum(XmiBaseEnum):
    BEAM = "Beam"
    COLUMN = "Column"
    BRACING = "Bracing"
    OTHER = "Other"


# Testing run python -m src.xmi.v2.models.enums.xmi_structural_curve_member_type_enum

print(XmiStructuralCurveMemberTypeEnum.BRACING.value)
print(XmiStructuralCurveMemberTypeEnum.COLUMN.name)