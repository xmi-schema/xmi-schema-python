from enum import unique
from ..bases.xmi_base_enum import XmiBaseEnum

@unique
class XmiStructuralMaterialTypeEnum(XmiBaseEnum):
    CONCRETE = "Concrete"
    STEEL = "Steel"
    TIMBER = "Timber"
    ALUMINIUM = "Aluminium"
    COMPOSITE = "Composite"
    MASONRY = "Masonry"
    OTHERS = "Others"
    REBAR = "Rebar"  # to be removed
    TENDON = "Tendon"  # to be removed
