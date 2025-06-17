from enum import unique
from ..bases.xmi_base_enum import XmiBaseEnum

@unique
class XmiStructuralCurveMemberSystemLineEnum(XmiBaseEnum):
    TOP_LEFT = "Top Left"
    TOP_MIDDLE = "Top Middle"
    TOP_RIGHT = "Top Right"
    MIDDLE_LEFT = "Middle Left"
    MIDDLE_MIDDLE = "Middle Middle"
    MIDDLE_RIGHT = "Middle Right"
    BOTTOM_LEFT = "Bottom Left"
    BOTTOM_MIDDLE = "Bottom Middle"
    BOTTOM_RIGHT = "Bottom Right"
    UNKNOWN = "Unknown"


# Testing run python -m src.xmi.v2.models.enums.xmi_structural_curve_member_system_line_enum

print(XmiStructuralCurveMemberSystemLineEnum.BOTTOM_MIDDLE.value)
print(XmiStructuralCurveMemberSystemLineEnum.TOP_LEFT.name)