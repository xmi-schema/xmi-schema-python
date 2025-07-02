from enum import unique
from ..bases.xmi_base_enum import XmiBaseEnum

@unique
class XmiStructuralSurfaceMemberSpanTypeEnum(XmiBaseEnum):
    ONE_WAY = "One Way"
    TWO_WAY = "Two Way"
    UNKNOWN = "Unknown"
