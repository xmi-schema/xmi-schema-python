from enum import unique
from ..bases.xmi_base_enum import XmiBaseEnum

@unique
class XmiStructuralSurfaceMemberTypeEnum(XmiBaseEnum):
    SLAB = "Slab"
    WALL = "Wall"
    PAD_FOOTING = "Pad Footing"
    STRIP_FOOTING = "Strip Footing"
    PILECAP = "Pilecap"  # i think this shouldn't be here
    ROOF_PANEL = "Roof Panel"  # this sounds like archi. should not be here
    WALL_PANEL = "Wall Panel"  # this sounds like archi. should not be here
    # For future changes to be shifted to foundation type elements
    RAFT = "Raft"


# Testing run python -m src.xmi.v2.models.enums.xmi_structural_surface_member_type_enum

print(XmiStructuralSurfaceMemberTypeEnum.STRIP_FOOTING.value)
print(XmiStructuralSurfaceMemberTypeEnum.SLAB.name)