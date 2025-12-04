"""
XmiHasStructuralCurveMember relationship class.

This module defines the XmiHasStructuralCurveMember relationship, which links
physical structural elements (beams, columns) to their analytical curve member
representations. This relationship is the bridge between the physical design model
and the structural analytical model.

The relationship ensures that:
- Source is a physical entity (XmiBasePhysicalEntity)
- Target is a structural analytical curve member (XmiStructuralCurveMember)
- Default relationship name and entity_type are set
"""

from pydantic import field_validator, model_validator
from ..bases.xmi_base_relationship import XmiBaseRelationship
from ..bases.xmi_base_physical_entity import XmiBasePhysicalEntity
from ..entities.xmi_structural_curve_member import XmiStructuralCurveMember


class XmiHasStructuralCurveMember(XmiBaseRelationship):
    """
    Links physical elements to their structural curve member analytical representation.

    This relationship connects physical entities (like XmiBeam or XmiColumn) to their
    corresponding analytical representations (XmiStructuralCurveMember). This enables
    the library to maintain both the physical design model and the structural analytical
    model while keeping them connected through explicit relationships.

    The relationship follows the pattern:
        Physical Entity (XmiBeam, XmiColumn) → Analytical Entity (XmiStructuralCurveMember)

    Attributes:
        source: Physical entity (must be XmiBasePhysicalEntity subclass)
        target: Analytical curve member entity (must be XmiStructuralCurveMember)
        name: Relationship name (defaults to "hasStructuralCurveMember")
        entity_type: Relationship type identifier (defaults to "XmiRelHasStructuralCurveMember")

    Examples:
        >>> from xmi.v2.models.entities.xmi_beam import XmiBeam
        >>> from xmi.v2.models.entities.xmi_structural_curve_member import XmiStructuralCurveMember
        >>> from xmi.v2.models.enums.xmi_structural_curve_member_system_line_enum import XmiStructuralCurveMemberSystemLineEnum
        >>> from xmi.v2.models.enums.xmi_structural_curve_member_type_enum import XmiStructuralCurveMemberTypeEnum
        >>>
        >>> # Create physical beam
        >>> beam = XmiBeam(
        ...     id="beam-001",
        ...     name="B1",
        ...     system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_MIDDLE,
        ...     length=5000.0
        ... )
        >>>
        >>> # Create analytical curve member
        >>> curve_member = XmiStructuralCurveMember(
        ...     id="cm-001",
        ...     name="CM1",
        ...     curve_member_type=XmiStructuralCurveMemberTypeEnum.BEAM,
        ...     system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_MIDDLE
        ... )
        >>>
        >>> # Link physical to analytical
        >>> relationship = XmiHasStructuralCurveMember(
        ...     source=beam,
        ...     target=curve_member
        ... )
        >>>
        >>> print(f"{relationship.source.name} → {relationship.target.name}")
        B1 → CM1
        >>> print(relationship.name)
        hasStructuralCurveMember

    Note:
        This relationship is essential for maintaining feature parity with the C# v0.8.0
        implementation, which uses this same pattern to bridge physical and analytical models.
    """

    @field_validator("source", mode="before")
    @classmethod
    def validate_source(cls, v):
        """
        Validate that source is a physical entity.

        Args:
            v: The source entity to validate

        Returns:
            The validated source entity

        Raises:
            TypeError: If source is not an instance of XmiBasePhysicalEntity
        """
        if not isinstance(v, XmiBasePhysicalEntity):
            raise TypeError("Source must be of type XmiBasePhysicalEntity")
        return v

    @field_validator("target", mode="before")
    @classmethod
    def validate_target(cls, v):
        """
        Validate that target is a structural curve member.

        Args:
            v: The target entity to validate

        Returns:
            The validated target entity

        Raises:
            TypeError: If target is not an instance of XmiStructuralCurveMember
        """
        if not isinstance(v, XmiStructuralCurveMember):
            raise TypeError("Target must be of type XmiStructuralCurveMember")
        return v

    @model_validator(mode="before")
    @classmethod
    def set_defaults(cls, values):
        """
        Set default values for name and entity_type.

        Args:
            values: Dictionary of field values

        Returns:
            dict: Updated values with defaults applied
        """
        values.setdefault("name", "hasStructuralCurveMember")
        values.setdefault("entity_type", "XmiRelHasStructuralCurveMember")
        values.setdefault("uml_type", "Association")
        return values
