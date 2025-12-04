from enum import unique
from ..bases.xmi_base_enum import XmiBaseEnum

@unique
class XmiStructuralSurfaceMemberSystemPlaneEnum(XmiBaseEnum):
    """
    Enumeration of reference planes (system planes) for surface members.

    This enum defines which plane of a surface member (slab, wall) is used as
    the reference for positioning and thickness measurement. The system plane
    determines how thickness is applied from the reference geometry.

    Attributes:
        BOTTOM: Bottom face of the surface (typical for slabs - soffit reference)
        TOP: Top face of the surface (top surface reference)
        MIDDLE: Middle plane of the surface (centerline - analytical modeling)
        LEFT: Left edge of the surface (typical for walls)
        RIGHT: Right edge of the surface (walls)
        UNKNOWN: System plane not specified

    Examples:
        >>> from xmi.v2.models.enums.xmi_structural_surface_member_system_plane_enum import XmiStructuralSurfaceMemberSystemPlaneEnum
        >>> # Direct access
        >>> plane = XmiStructuralSurfaceMemberSystemPlaneEnum.BOTTOM
        >>> print(plane.value)  # "Bottom"
        >>>
        >>> # Case-insensitive lookup
        >>> plane = XmiStructuralSurfaceMemberSystemPlaneEnum("middle")  # Returns MIDDLE
        >>>
        >>> # Use in surface member
        >>> from xmi.v2.models.entities.structural_analytical.xmi_structural_surface_member import XmiStructuralSurfaceMember
        >>> slab = XmiStructuralSurfaceMember(
        ...     name="SLAB_L1",
        ...     system_plane=XmiStructuralSurfaceMemberSystemPlaneEnum.BOTTOM,
        ...     thickness=200  # mm, applied upward from bottom
        ... )

    Note:
        For slabs, BOTTOM reference is common in construction (soffit level),
        while MIDDLE is common in analytical models (centerline).
    """
    BOTTOM = "Bottom"
    TOP = "Top"
    MIDDLE = "Middle"
    LEFT = "Left"
    RIGHT = "Right"
    UNKNOWN = "Unknown"