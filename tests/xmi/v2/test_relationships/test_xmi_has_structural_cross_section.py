import pytest
from xmi.v2.models.relationships.xmi_has_structural_cross_section import XmiHasStructuralCrossSection
from xmi.v2.models.bases.xmi_base_entity import XmiBaseEntity
from xmi.v2.models.entities.xmi_structural_cross_section import XmiStructuralCrossSection
from xmi.v2.models.enums.xmi_structural_material_type_enum import XmiStructuralMaterialTypeEnum

def test_has_structural_cross_section_valid_instantiation():
    source = XmiBaseEntity(id="E1", name="Beam")

    target = XmiStructuralCrossSection(
        id="CS1",
        description="Rectangular section",
        shape="rectangular",
        material_type=XmiStructuralMaterialTypeEnum.CONCRETE,
        width=0.3,
        height=0.5,
        parameters=(300, 300)
    )

    rel = XmiHasStructuralCrossSection(source=source, target=target)

    assert rel.source == source
    assert rel.target == target
    assert rel.name == "hasStructuralCrossSection"
    assert rel.entity_type == "XmiRelHasStructuralCrossSection"


def test_invalid_source_type():
    target = XmiStructuralCrossSection(
        id="CS1",
        shape="rectangular",
        material_type=XmiStructuralMaterialTypeEnum.CONCRETE,
        width=0.3,
        height=0.5,
        parameters=(300, 300)
    )

    with pytest.raises(TypeError, match="Source must be of type XmiBaseEntity"):
        XmiHasStructuralCrossSection(source="not a base entity", target=target)


def test_invalid_target_type():
    source = XmiBaseEntity(id="E1", name="Beam")

    with pytest.raises(TypeError, match="Target must be of type XmiStructuralCrossSection"):
        XmiHasStructuralCrossSection(source=source, target="not a cross section")


# .venv/bin/python -m pytest tests/xmi/v2/test_relationships/test_xmi_has_structural_cross_section.py