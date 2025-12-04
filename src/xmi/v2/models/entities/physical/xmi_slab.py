from pydantic import model_validator, ConfigDict
from typing import Dict, Any, List, Optional, Tuple
from ...bases.xmi_base_physical_entity import XmiBasePhysicalEntity


class XmiSlab(XmiBasePhysicalEntity):
    """
    Represents a physical slab element in the XMI schema.

    A slab is a horizontal structural element (such as a floor or roof) designed to
    resist loads primarily through bending. This class inherits from XmiBasePhysicalEntity
    and is automatically classified with type (domain) = "Physical".

    The XmiSlab class currently inherits all properties from XmiBasePhysicalEntity:
    - id: Unique identifier (auto-generated UUID if not provided)
    - name: Human-readable name/identifier (defaults to id if not provided)
    - ifcguid: IFC Global Unique Identifier for BIM interoperability
    - native_id: Original identifier from source application
    - description: Optional description or notes
    - entity_type: Class name ("XmiSlab")
    - type: Domain classification (XmiBaseEntityDomainEnum.PHYSICAL)

    Examples:
        >>> slab = XmiSlab(
        ...     id="slab-001",
        ...     name="Floor Slab Level 1",
        ...     native_id="12345",
        ...     description="Concrete floor slab"
        ... )
        >>> print(slab.entity_type)  # "XmiSlab"
        >>> print(slab.type)  # XmiBaseEntityDomainEnum.PHYSICAL
    """

    model_config = ConfigDict(populate_by_name=True)

    @model_validator(mode="before")
    @classmethod
    def set_entity_type(cls, values):
        """Set entity_type to class name if not already set."""
        values.setdefault("EntityType", cls.__name__)
        return values

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> Tuple[Optional["XmiSlab"], List[Exception]]:
        """
        Create an XmiSlab instance from a dictionary, collecting any errors.

        Args:
            obj: Dictionary containing slab data with PascalCase keys

        Returns:
            Tuple of (XmiSlab instance or None, list of exceptions)
        """
        try:
            instance = cls(**obj)
            return instance, []
        except Exception as e:
            return None, [e]
