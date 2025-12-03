from pydantic import Field, model_validator, ConfigDict
from typing import Optional
from .xmi_base_entity import XmiBaseEntity

class XmiBaseGeometry(XmiBaseEntity):
    """
    Abstract base class for all geometric primitives in the XMI schema.

    This class inherits from XmiBaseEntity and serves as the parent for all geometric
    objects such as points, lines, and arcs. It ensures that all geometric objects have
    consistent identification and metadata while providing specialized validation for
    geometric types.

    Inherits all properties from XmiBaseEntity:
    - id: Unique identifier (auto-generated UUID)
    - name: Human-readable name/identifier
    - ifcguid: IFC Global Unique Identifier
    - native_id: Original identifier from source application
    - description: Optional description or notes
    - entity_type: Type name of the geometry (auto-set to class name)

    The class provides automatic entity_type setting to ensure each geometry instance
    knows its specific type (Point3D, Line3D, Arc3D, etc.).

    Examples:
        >>> from xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D
        >>> from xmi.v2.models.geometries.xmi_line_3d import XmiLine3D
        >>> # Create point - entity_type automatically set to "XmiPoint3D"
        >>> point = XmiPoint3D(x=1000.0, y=2000.0, z=3000.0, name="P1")
        >>> print(point.entity_type)  # "XmiPoint3D"

        >>> # Create line - entity_type automatically set to "XmiLine3D"
        >>> line = XmiLine3D(
        ...     start_point=XmiPoint3D(x=0, y=0, z=0),
        ...     end_point=XmiPoint3D(x=1000, y=0, z=0),
        ...     name="LINE-001"
        ... )
        >>> print(line.entity_type)  # "XmiLine3D"

    Note:
        This is an abstract base class and cannot be instantiated directly.
        Use concrete subclasses: XmiPoint3D, XmiLine3D, XmiArc3D.
    """
    entity_type: Optional[str] = Field(None, alias="EntityType")

    @model_validator(mode="before")
    @classmethod
    def set_entity_type(cls, values):
        """
        Pre-validation model validator that sets the entity_type field.

        This validator ensures that the entity_type field is always set to the specific
        geometry class name (e.g., "XmiPoint3D", "XmiLine3D", "XmiArc3D"). This allows
        runtime type identification and proper serialization.

        Args:
            values: Dictionary of field values (both PascalCase and snake_case keys)

        Returns:
            dict: Updated values dictionary with entity_type set

        Examples:
            >>> # Input without EntityType
            >>> values = {"x": 100.0, "y": 200.0, "z": 300.0}
            >>> # After set_entity_type for XmiPoint3D:
            >>> # values["EntityType"] = "XmiPoint3D"
        """
        values["EntityType"] = values.get("EntityType") or values.get("entity_type") or cls.__name__

        return values

    model_config = ConfigDict(populate_by_name=True)
