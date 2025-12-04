from enum import unique
from ..bases.xmi_base_enum import XmiBaseEnum

@unique
class XmiStructuralSurfaceMemberTypeEnum(XmiBaseEnum):
    """
    Enumeration of structural surface member types (2D elements).

    This enum defines the structural function/role of surface members in the
    building system, which affects design requirements and load behavior.

    Attributes:
        SLAB: Horizontal floor or roof slab
        WALL: Vertical wall element (load-bearing or shear wall)
        PAD_FOOTING: Individual column footing
        STRIP_FOOTING: Continuous wall footing
        PILECAP: Cap connecting pile group (may be deprecated in future)
        ROOF_PANEL: Architectural roof panel (may be deprecated in future)
        WALL_PANEL: Architectural wall panel (may be deprecated in future)
        RAFT: Raft foundation / mat foundation
        UNKNOWN: Surface type not specified

    Examples:
        >>> from xmi.v2.models.enums.xmi_structural_surface_member_type_enum import XmiStructuralSurfaceMemberTypeEnum
        >>> # Direct access
        >>> surface_type = XmiStructuralSurfaceMemberTypeEnum.SLAB
        >>> print(surface_type.value)  # "Slab"
        >>>
        >>> # Case-insensitive lookup
        >>> surface_type = XmiStructuralSurfaceMemberTypeEnum("wall")  # Returns WALL
        >>>
        >>> # Use in surface member
        >>> from xmi.v2.models.entities.structural_analytical.xmi_structural_surface_member import XmiStructuralSurfaceMember
        >>> slab = XmiStructuralSurfaceMember(
        ...     name="SLAB_L2",
        ...     member_type=XmiStructuralSurfaceMemberTypeEnum.SLAB,
        ...     thickness=200
        ... )

    Note:
        Some values (PILECAP, ROOF_PANEL, WALL_PANEL) are marked for potential
        removal in future versions. RAFT may be moved to foundation-specific elements.
    """
    SLAB = "Slab"
    WALL = "Wall"
    PAD_FOOTING = "Pad Footing"
    STRIP_FOOTING = "Strip Footing"
    PILECAP = "Pilecap"  # i think this shouldn't be here
    ROOF_PANEL = "Roof Panel"  # this sounds like archi. should not be here
    WALL_PANEL = "Wall Panel"  # this sounds like archi. should not be here
    # For future changes to be shifted to foundation type elements
    RAFT = "Raft"
    UNKNOWN = "Unknown"