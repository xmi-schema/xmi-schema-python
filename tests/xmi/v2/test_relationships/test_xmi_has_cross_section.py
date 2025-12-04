import pytest
from xmi.v2.models.relationships.xmi_has_cross_section import XmiHasCrossSection
from xmi.v2.models.bases.xmi_base_entity import XmiBaseEntity
from xmi.v2.models.entities.xmi_cross_section import XmiCrossSection
from xmi.v2.models.enums.xmi_material_type_enum import XmiMaterialTypeEnum

def test_has_structural_cross_section_valid_instantiation():
    source = XmiBaseEntity(id="E1", name="Beam")

    target = XmiCrossSection(
        id="CS1",
        description="Rectangular section",
        shape="rectangular",
        material_type=XmiMaterialTypeEnum.CONCRETE,
        width=0.3,
        height=0.5,
        parameters=(300, 300)
    )

    rel = XmiHasCrossSection(source=source, target=target)

    assert rel.source == source
    assert rel.target == target
    assert rel.name == "hasCrossSection"
    assert rel.entity_type == "XmiRelHasCrossSection"


def test_invalid_source_type():
    target = XmiCrossSection(
        id="CS1",
        shape="rectangular",
        material_type=XmiMaterialTypeEnum.CONCRETE,
        width=0.3,
        height=0.5,
        parameters=(300, 300)
    )

    with pytest.raises(TypeError, match="Source must be of type XmiBaseEntity"):
        XmiHasCrossSection(source="not a base entity", target=target)


def test_invalid_target_type():
    source = XmiBaseEntity(id="E1", name="Beam")

    with pytest.raises(TypeError, match="Target must be of type XmiCrossSection"):
        XmiHasCrossSection(source=source, target="not a cross section")


# .venv/bin/python -m pytest tests/xmi/v2/test_relationships/test_xmi_has_structural_cross_section.py