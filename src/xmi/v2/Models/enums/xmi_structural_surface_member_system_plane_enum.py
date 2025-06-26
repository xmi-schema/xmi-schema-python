from enum import unique
from ..bases.xmi_base_enum import XmiBaseEnum

@unique
class XmiStructuralSurfaceMemberSystemPlaneEnum(XmiBaseEnum):
    BOTTOM = "Bottom"
    TOP = "Top"
    MIDDLE = "Middle"
    LEFT = "Left"
    RIGHT = "Right"
