from pydantic import model_validator
from xmi.v2.models.bases.xmi_base_entity import XmiBaseEntity
from xmi.v2.models.enums.xmi_base_entity_domain_enum import XmiBaseEntityDomainEnum


class XmiBasePhysicalEntity(XmiBaseEntity):
    """
    Abstract base class for all physical entities in the XMI schema.

    Physical entities represent actual built environment elements as designed
    or constructed, such as beams, columns, slabs, and walls. They are distinct
    from analytical entities which represent idealized models for structural analysis.

    This class automatically assigns type (domain) = "Physical" to all subclasses,
    enabling domain classification and filtering of physical elements. The entity_type
    field still contains the specific class name (e.g., "XmiBeam").

    Inherits all properties from XmiBaseEntity:
    - id: Unique identifier (auto-generated UUID if not provided)
    - name: Human-readable name/identifier (defaults to id if not provided)
    - ifcguid: IFC Global Unique Identifier for BIM interoperability
    - native_id: Original identifier from source application
    - description: Optional description or notes
    - entity_type: Class name (e.g., "XmiBeam", "XmiColumn")
    - type: Domain classification set to "Physical"

    Physical entities typically:
    - Represent as-designed or as-built geometry
    - Have physical dimensions and material properties
    - May reference analytical models through relationships
    - Correspond to actual construction elements

    Examples:
        >>> from xmi.v2.models.entities.physical.xmi_beam import XmiBeam
        >>> # Create a physical beam
        >>> beam = XmiBeam(
        ...     id="beam-001",
        ...     name="B1",
        ...     description="Main floor beam"
        ... )
        >>> print(beam.entity_type)  # "XmiBeam"
        >>> print(beam.type)  # XmiBaseEntityDomainEnum.PHYSICAL

    Note:
        This is an abstract base class and should not be instantiated directly.
        Use concrete subclasses like XmiBeam, XmiColumn, XmiSlab, or XmiWall.

    See Also:
        - XmiBaseStructuralAnalyticalEntity: Base class for analytical entities
        - XmiBaseEntity: Root base class for all entities
        - XmiBaseEntityDomainEnum: Enum defining domain classifications
    """

    @model_validator(mode="before")
    @classmethod
    def set_physical_domain_type(cls, values: dict):
        """
        Pre-validation model validator that sets domain type to "Physical".

        This validator ensures all physical entities are properly classified
        with type (domain) = "Physical" while maintaining entity_type as the
        class name.

        Args:
            values: Dictionary of field values (both PascalCase and snake_case keys)

        Returns:
            dict: Updated values dictionary with Type set to "Physical"

        Examples:
            >>> # Input without Type
            >>> values = {"ID": "beam-1", "Name": "B1"}
            >>> # After set_physical_domain_type:
            >>> # values["Type"] = "Physical"
        """
        if "Type" not in values and "type" not in values:
            values["Type"] = XmiBaseEntityDomainEnum.PHYSICAL.value

        return values
