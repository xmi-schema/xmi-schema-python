from pydantic import BaseModel, Field, model_validator, ConfigDict
from typing import Optional
from .xmi_base_entity import XmiBaseEntity
import uuid


class XmiBaseRelationship(BaseModel):
    """
    Base class for all relationships in the XMI schema v2 implementation.

    Relationships connect entities together to form a graph structure, representing
    connections like materials assigned to cross-sections, members linked to nodes,
    and geometric associations. This base class ensures all relationships have
    consistent identification, naming, and references to source and target entities.

    Properties:
        id: Unique identifier (auto-generated UUID if not provided)
        source: Source entity of the relationship (the entity that "owns" the relationship)
        target: Target entity of the relationship (the entity being referenced)
        name: Relationship name/type (required, e.g., "HasStructuralMaterial")
        description: Optional description or notes
        entity_type: Type name of the relationship (defaults to "XmiRelBaseRelationship")
        uml_type: UML relationship type (optional)

    All relationships are directed (source → target), where the direction indicates
    the semantic meaning of the connection.

    Examples:
        >>> from xmi.v2.models.relationships.xmi_has_structural_material import XmiHasStructuralMaterial
        >>> from xmi.v2.models.entities.xmi_structural_material import XmiStructuralMaterial
        >>> from xmi.v2.models.entities.xmi_structural_cross_section import XmiStructuralCrossSection
        >>>
        >>> # Create entities
        >>> material = XmiStructuralMaterial(
        ...     id="mat-001",
        ...     name="Concrete C30",
        ...     material_type="Concrete",
        ...     grade="C30"
        ... )
        >>> cross_section = XmiStructuralCrossSection(
        ...     id="cs-001",
        ...     name="RECT_300x500",
        ...     shape="Rectangle"
        ... )
        >>>
        >>> # Create relationship linking cross-section to material
        >>> relationship = XmiHasStructuralMaterial(
        ...     source=cross_section,
        ...     target=material,
        ...     name="HasStructuralMaterial"
        ... )
        >>> print(f"{relationship.source.name} → {relationship.target.name}")
        RECT_300x500 → Concrete C30

    Note:
        The 'name' field is required and must be provided during instantiation.
        If missing, a ValueError will be raised during validation.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="ID")
    source: XmiBaseEntity = Field(..., alias="Source", description="Source entity")
    target: XmiBaseEntity = Field(..., alias="Target", description="Target entity")
    name: str = Field(..., alias="Name", description="Relationship name")
    description: Optional[str] = Field("", alias="Description")
    entity_type: str = Field(default="XmiRelBaseRelationship", alias="EntityType")
    uml_type: Optional[str] = Field("", alias="UmlType")

    @model_validator(mode="before")
    @classmethod
    def validate_fields(cls, values):
        """
        Pre-validation model validator that ensures required fields are provided.

        This validator checks that the 'name' field is provided and not empty.
        The name field is critical as it identifies the type of relationship
        (e.g., "HasStructuralMaterial", "HasStructuralNode").

        Args:
            values: Dictionary of field values

        Returns:
            dict: The values dictionary unchanged if validation passes

        Raises:
            ValueError: If the 'name' field is missing or empty

        Examples:
            >>> # Valid relationship values
            >>> values = {
            ...     "source": source_entity,
            ...     "target": target_entity,
            ...     "name": "HasStructuralMaterial"
            ... }
            >>> # Passes validation

            >>> # Invalid relationship values (missing name)
            >>> values = {
            ...     "source": source_entity,
            ...     "target": target_entity
            ... }
            >>> # Raises ValueError: "Name must be provided"
        """
        if not values.get("name"):
            raise ValueError("Name must be provided")
        return values

    model_config = ConfigDict(populate_by_name=True)