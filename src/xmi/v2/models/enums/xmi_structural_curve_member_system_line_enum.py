from enum import unique
from ..bases.xmi_base_enum import XmiBaseEnum

@unique
class XmiStructuralCurveMemberSystemLineEnum(XmiBaseEnum):
    """
    Enumeration of reference lines (system lines) for curve members.

    This enum defines which point within a cross-section is used as the reference
    for the member's axis. The system line determines eccentricity and how members
    connect to each other.

    Attributes:
        TOP_LEFT: Top-left corner of cross-section
        TOP_MIDDLE: Top center of cross-section
        TOP_RIGHT: Top-right corner of cross-section
        MIDDLE_LEFT: Middle-left edge of cross-section
        MIDDLE_MIDDLE: Centroid/center of cross-section
        MIDDLE_RIGHT: Middle-right edge of cross-section
        BOTTOM_LEFT: Bottom-left corner of cross-section
        BOTTOM_MIDDLE: Bottom center of cross-section
        BOTTOM_RIGHT: Bottom-right corner of cross-section
        UNKNOWN: System line not specified

    Examples:
        >>> from xmi.v2.models.enums.xmi_structural_curve_member_system_line_enum import XmiStructuralCurveMemberSystemLineEnum
        >>> # Direct access
        >>> line = XmiStructuralCurveMemberSystemLineEnum.MIDDLE_MIDDLE
        >>> print(line.value)  # "MiddleMiddle"
        >>>
        >>> # Case-insensitive lookup
        >>> line = XmiStructuralCurveMemberSystemLineEnum("topmiddle")  # Returns TOP_MIDDLE
        >>>
        >>> # Use in curve member
        >>> from xmi.v2.models.entities.structural_analytical.xmi_structural_curve_member import XmiStructuralCurveMember
        >>> beam = XmiStructuralCurveMember(
        ...     name="B1",
        ...     system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_MIDDLE
        ... )

    Note:
        Beams often use TOP_MIDDLE (top of beam at slab level), while columns
        typically use MIDDLE_MIDDLE (centroid) for analytical models.
    """
    TOP_LEFT = "TopLeft"
    TOP_MIDDLE = "TopMiddle"
    TOP_RIGHT = "TopRight"
    MIDDLE_LEFT = "MiddleLeft"
    MIDDLE_MIDDLE = "MiddleMiddle"
    MIDDLE_RIGHT = "MiddleRight"
    BOTTOM_LEFT = "BottomLeft"
    BOTTOM_MIDDLE = "BottomMiddle"
    BOTTOM_RIGHT = "BottomRight"
    UNKNOWN = "Unknown"
