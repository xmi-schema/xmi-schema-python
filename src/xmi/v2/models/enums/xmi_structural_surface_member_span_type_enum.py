from enum import unique
from ..bases.xmi_base_enum import XmiBaseEnum

@unique
class XmiStructuralSurfaceMemberSpanTypeEnum(XmiBaseEnum):
    """
    Enumeration of spanning behavior for surface members (slabs, walls).

    This enum defines how load is distributed and carried by surface elements,
    which affects structural analysis and reinforcement design.

    Attributes:
        ONE_WAY: Surface spans primarily in one direction (length/width > 2)
        TWO_WAY: Surface spans in two orthogonal directions (square or nearly square)
        UNKNOWN: Span type not specified

    Examples:
        >>> from xmi.v2.models.enums.xmi_structural_surface_member_span_type_enum import XmiStructuralSurfaceMemberSpanTypeEnum
        >>> # Direct access
        >>> span_type = XmiStructuralSurfaceMemberSpanTypeEnum.TWO_WAY
        >>> print(span_type.value)  # "Two Way"
        >>>
        >>> # Case-insensitive lookup
        >>> span_type = XmiStructuralSurfaceMemberSpanTypeEnum("one way")  # Returns ONE_WAY
        >>>
        >>> # Use in surface member
        >>> from xmi.v2.models.entities.structural_analytical.xmi_structural_surface_member import XmiStructuralSurfaceMember
        >>> slab = XmiStructuralSurfaceMember(
        ...     name="SLAB_2W",
        ...     span_type=XmiStructuralSurfaceMemberSpanTypeEnum.TWO_WAY,
        ...     thickness=200
        ... )

    Note:
        One-way slabs use beam theory (simpler analysis), while two-way slabs
        use plate theory (more complex). Reinforcement is required in both
        directions for two-way slabs.
    """
    ONE_WAY = "One Way"
    TWO_WAY = "Two Way"
    UNKNOWN = "Unknown"
