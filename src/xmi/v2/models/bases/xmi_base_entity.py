from abc import ABC
from pydantic import BaseModel, Field, model_validator, ConfigDict
from typing import Optional
import uuid

class XmiBaseEntity(BaseModel, ABC):
    """
    Abstract base class for all XMI entities in the v2 implementation.

    This class provides common identification, naming, and metadata properties that every
    entity in the XMI schema inherits. It ensures consistency across all entity types and
    provides standard fields for uniqueness, interoperability, and description.

    All entities inherit the following core properties:
    - id: Unique identifier (auto-generated UUID if not provided)
    - name: Human-readable name/identifier (defaults to id if not provided)
    - ifcguid: IFC Global Unique Identifier for BIM interoperability
    - native_id: Original identifier from source application
    - description: Optional description or notes
    - entity_type: Type name of the entity (auto-set to class name)

    The class uses Pydantic for validation and supports both PascalCase (JSON/XMI format)
    and snake_case (Python) field names through aliases.

    Examples:
        >>> from xmi.v2.models.entities.xmi_structural_material import XmiStructuralMaterial
        >>> # Minimal creation - all fields auto-generated
        >>> material = XmiStructuralMaterial(material_type="Concrete", grade="C30")
        >>> print(material.id)  # Auto-generated UUID
        >>> print(material.name)  # Same as ID by default
        >>> print(material.entity_type)  # "XmiStructuralMaterial"

        >>> # Full creation with all base fields
        >>> material = XmiStructuralMaterial(
        ...     id="mat-001",
        ...     name="MAT_C30",
        ...     ifcguid="3cJh8fHxj3FwU$9vPQK1PN",
        ...     native_id="1",
        ...     description="Concrete C30/37",
        ...     material_type="Concrete",
        ...     grade="C30"
        ... )

    Note:
        This is an abstract base class and cannot be instantiated directly.
        Use concrete subclasses like XmiStructuralMaterial, XmiStructuralCrossSection, etc.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="ID")
    name: Optional[str] = Field(None, alias="Name")
    ifcguid: Optional[str] = Field(None, alias="IFCGUID")
    native_id: Optional[str] = Field(None, alias="NativeId")
    description: Optional[str] = Field(None, alias="Description")
    entity_type: Optional[str] = Field(None, alias="EntityType")

    @model_validator(mode="before")
    @classmethod
    def fill_defaults(cls, values: dict):
        """
        Pre-validation model validator that fills in default values for key fields.

        This validator runs before Pydantic's standard validation and ensures that:
        - If no ID is provided, a UUID is auto-generated
        - If no Name is provided, it defaults to the ID value
        - If no EntityType is provided, it defaults to the class name

        Args:
            values: Dictionary of field values (both PascalCase and snake_case keys)

        Returns:
            dict: Updated values dictionary with defaults filled in

        Examples:
            >>> # Input with no ID or Name
            >>> values = {"MaterialType": "Concrete"}
            >>> # After fill_defaults:
            >>> # values["ID"] = "some-uuid"
            >>> # values["Name"] = "some-uuid"
            >>> # values["EntityType"] = "XmiStructuralMaterial"
        """
        id_ = values.get("ID") or values.get("id") or str(uuid.uuid4())

        if "ID" not in values and "id" not in values:
            values["ID"] = id_

        if "Name" not in values and "name" not in values:
            values["Name"] = id_

        if "EntityType" not in values and "entity_type" not in values:
            values["EntityType"] = cls.__name__

        return values

    model_config = ConfigDict(populate_by_name=True)
