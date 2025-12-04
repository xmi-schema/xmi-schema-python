from pydantic import model_validator, ConfigDict
from typing import Dict, Any, List, Optional, Tuple
from ...bases.xmi_base_physical_entity import XmiBasePhysicalEntity


class XmiWall(XmiBasePhysicalEntity):
    """
    Represents a physical wall element in the XMI schema.

    A wall is a vertical structural or non-structural element designed to enclose
    spaces or resist lateral loads. This class inherits from XmiBasePhysicalEntity
    and is automatically classified with type (domain) = "Physical".

    The XmiWall class currently inherits all properties from XmiBasePhysicalEntity:
    - id: Unique identifier (auto-generated UUID if not provided)
    - name: Human-readable name/identifier (defaults to id if not provided)
    - ifcguid: IFC Global Unique Identifier for BIM interoperability
    - native_id: Original identifier from source application
    - description: Optional description or notes
    - entity_type: Class name ("XmiWall")
    - type: Domain classification (XmiBaseEntityDomainEnum.PHYSICAL)

    Examples:
        >>> wall = XmiWall(
        ...     id="wall-001",
        ...     name="Exterior Wall A",
        ...     native_id="67890",
        ...     description="Load-bearing concrete wall"
        ... )
        >>> print(wall.entity_type)  # "XmiWall"
        >>> print(wall.type)  # XmiBaseEntityDomainEnum.PHYSICAL
    """

    model_config = ConfigDict(populate_by_name=True)

    @model_validator(mode="before")
    @classmethod
    def set_entity_type(cls, values):
        """Set entity_type to class name if not already set."""
        values.setdefault("EntityType", cls.__name__)
        return values

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> Tuple[Optional["XmiWall"], List[Exception]]:
        """
        Create an XmiWall instance from a dictionary, collecting any errors.

        Args:
            obj: Dictionary containing wall data with PascalCase keys

        Returns:
            Tuple of (XmiWall instance or None, list of exceptions)
        """
        try:
            instance = cls(**obj)
            return instance, []
        except Exception as e:
            return None, [e]
