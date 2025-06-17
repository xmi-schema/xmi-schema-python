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


# Testing run python -m src.xmi.v2.models.enums.xmi_structural_material_type_enum

print(XmiStructuralMaterialTypeEnum.ALUMINIUM.value)
print(XmiStructuralMaterialTypeEnum.CONCRETE.name)