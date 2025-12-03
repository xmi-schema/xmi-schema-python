from enum import unique
from ..bases.xmi_base_enum import XmiBaseEnum

@unique
class XmiStructuralMaterialTypeEnum(XmiBaseEnum):
    """
    Enumeration of structural material types.

    This enum defines the types of structural materials used in building
    construction. Material type affects properties, behavior, and applicable
    design standards.

    Attributes:
        CONCRETE: Concrete material (most common for buildings)
        STEEL: Structural steel (frames, connections, bracing)
        TIMBER: Wood/timber material
        ALUMINIUM: Aluminum/aluminium (lightweight structures)
        COMPOSITE: Composite materials (steel-concrete, FRP)
        MASONRY: Brick, block, stone masonry
        OTHERS: Other material types
        REBAR: Reinforcing bar (DEPRECATED - to be removed)
        TENDON: Post-tensioning tendon (DEPRECATED - to be removed)

    Examples:
        >>> from xmi.v2.models.enums.xmi_structural_material_type_enum import XmiStructuralMaterialTypeEnum
        >>> # Direct access
        >>> material_type = XmiStructuralMaterialTypeEnum.CONCRETE
        >>> print(material_type.value)  # "Concrete"
        >>>
        >>> # Case-insensitive lookup
        >>> material_type = XmiStructuralMaterialTypeEnum("steel")  # Returns STEEL
        >>>
        >>> # Use in structural material
        >>> from xmi.v2.models.entities.xmi_structural_material import XmiStructuralMaterial
        >>> concrete = XmiStructuralMaterial(
        ...     name="C30",
        ...     material_type=XmiStructuralMaterialTypeEnum.CONCRETE,
        ...     grade="C30/37"
        ... )

    Note:
        REBAR and TENDON values are marked for removal in future versions.
        They should not be used for new models. Reinforcement should be
        modeled differently.
    """
    CONCRETE = "Concrete"
    STEEL = "Steel"
    TIMBER = "Timber"
    ALUMINIUM = "Aluminium"
    COMPOSITE = "Composite"
    MASONRY = "Masonry"
    OTHERS = "Others"
    REBAR = "Rebar"  # to be removed
    TENDON = "Tendon"  # to be removed
