from enum import unique
from ..bases.xmi_base_enum import XmiBaseEnum

@unique
class XmiStructuralCurveMemberTypeEnum(XmiBaseEnum):
    """
    Enumeration of structural curve member types (linear elements).

    This enum defines the structural function/role of linear structural members
    in the building system, which affects design requirements and structural behavior.

    Attributes:
        BEAM: Horizontal load-bearing member (carries floor/roof loads)
        COLUMN: Vertical load-bearing member (carries gravity loads to foundation)
        BRACING: Lateral stability member (diagonal members for wind/seismic)
        OTHER: Other member types (struts, ties, specialty members)
        UNKNOWN: Member type not specified

    Examples:
        >>> from xmi.v2.models.enums.xmi_structural_curve_member_type_enum import XmiStructuralCurveMemberTypeEnum
        >>> # Direct access
        >>> member_type = XmiStructuralCurveMemberTypeEnum.BEAM
        >>> print(member_type.value)  # "Beam"
        >>>
        >>> # Case-insensitive lookup
        >>> member_type = XmiStructuralCurveMemberTypeEnum("column")  # Returns COLUMN
        >>>
        >>> # Use in curve member
        >>> from xmi.v2.models.entities.structural_analytical.xmi_structural_curve_member import XmiStructuralCurveMember
        >>> beam = XmiStructuralCurveMember(
        ...     name="B1",
        ...     member_type=XmiStructuralCurveMemberTypeEnum.BEAM
        ... )

    Note:
        Member type affects design checks, load combinations, and code requirements.
    """
    BEAM = "Beam"
    COLUMN = "Column"
    BRACING = "Bracing"
    OTHER = "Other"
    UNKNOWN = "Unknown"
