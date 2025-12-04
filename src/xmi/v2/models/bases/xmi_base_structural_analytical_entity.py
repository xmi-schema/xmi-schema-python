from pydantic import model_validator
from xmi.v2.models.bases.xmi_base_entity import XmiBaseEntity
from xmi.v2.models.enums.xmi_base_entity_domain_enum import XmiBaseEntityDomainEnum


class XmiBaseStructuralAnalyticalEntity(XmiBaseEntity):
    """
    Abstract base class for all structural analytical entities in the XMI schema.

    Structural analytical entities represent idealized mathematical models used for
    structural analysis and calculations. These entities simplify the physical geometry
    into analytically tractable forms such as line elements (curve members) or
    surface elements (surface members).

    This class automatically assigns type (domain) = "StructuralAnalytical" to all subclasses,
    enabling domain classification and filtering of analytical elements. The entity_type
    field still contains the specific class name (e.g., "XmiStructuralCurveMember").

    Inherits all properties from XmiBaseEntity:
    - id: Unique identifier (auto-generated UUID if not provided)
    - name: Human-readable name/identifier (defaults to id if not provided)
    - ifcguid: IFC Global Unique Identifier for BIM interoperability
    - native_id: Original identifier from source application
    - description: Optional description or notes
    - entity_type: Class name (e.g., "XmiStructuralCurveMember")
    - type: Domain classification set to "StructuralAnalytical"

    Structural analytical entities typically:
    - Represent simplified geometry for analysis (lines, surfaces, nodes)
    - Have structural properties (cross-sections, materials, boundary conditions)
    - May be referenced by physical entities through relationships
    - Are used for structural calculations and simulations

    Examples:
        >>> from xmi.v2.models.entities.xmi_structural_curve_member import XmiStructuralCurveMember
        >>> # Create an analytical curve member
        >>> member = XmiStructuralCurveMember(
        ...     id="member-001",
        ...     name="M1",
        ...     description="Analytical beam element",
        ...     curve_member_type="Beam",
        ...     system_line="Top Middle"
        ... )
        >>> print(member.entity_type)  # "XmiStructuralCurveMember"
        >>> print(member.type)  # XmiBaseEntityDomainEnum.STRUCTURAL_ANALYTICAL

    Note:
        This is an abstract base class and should not be instantiated directly.
        Use concrete subclasses like XmiStructuralCurveMember, XmiStructuralSurfaceMember,
        XmiStructuralPointConnection, or XmiStorey.

    See Also:
        - XmiBasePhysicalEntity: Base class for physical entities
        - XmiBaseEntity: Root base class for all entities
        - XmiBaseEntityDomainEnum: Enum defining domain classifications
    """

    @model_validator(mode="before")
    @classmethod
    def set_structural_analytical_domain_type(cls, values: dict):
        """
        Pre-validation model validator that sets domain type to "StructuralAnalytical".

        This validator ensures all structural analytical entities are properly classified
        with type (domain) = "StructuralAnalytical" while maintaining entity_type as the
        class name.

        Args:
            values: Dictionary of field values (both PascalCase and snake_case keys)

        Returns:
            dict: Updated values dictionary with Type set to "StructuralAnalytical"

        Examples:
            >>> # Input without Type
            >>> values = {"ID": "member-1", "Name": "M1", "CurveMemberType": "Beam"}
            >>> # After set_structural_analytical_domain_type:
            >>> # values["Type"] = "StructuralAnalytical"
        """
        if "Type" not in values and "type" not in values:
            values["Type"] = XmiBaseEntityDomainEnum.STRUCTURAL_ANALYTICAL.value

        return values
