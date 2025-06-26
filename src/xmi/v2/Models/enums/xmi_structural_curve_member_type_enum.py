from enum import unique
from ..bases.xmi_base_enum import XmiBaseEnum

@unique
class XmiStructuralCurveMemberTypeEnum(XmiBaseEnum):
    BEAM = "Beam"
    COLUMN = "Column"
    BRACING = "Bracing"
    OTHER = "Other"
