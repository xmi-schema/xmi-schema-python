from enum import unique
from ..bases.xmi_base_enum import XmiBaseEnum

@unique
class XmiStructuralSurfaceMemberSystemPlaneEnum(XmiBaseEnum):
    BOTTOM = "Bottom"
    TOP = "Top"
    MIDDLE = "Middle"
    LEFT = "Left"
    RIGHT = "Right"


# Testing run python -m src.xmi.v2.models.enums.xmi_structural_surface_member_system_plane_enum

print(XmiStructuralSurfaceMemberSystemPlaneEnum.RIGHT.value)
print(XmiStructuralSurfaceMemberSystemPlaneEnum.TOP.name)