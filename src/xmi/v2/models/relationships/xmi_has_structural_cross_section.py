from pydantic import field_validator, model_validator
from ..bases.xmi_base_relationship import XmiBaseRelationship
from ..bases.xmi_base_entity import XmiBaseEntity
from ..entities.xmi_structural_cross_section import XmiStructuralCrossSection

class XmiHasStructuralCrossSection(XmiBaseRelationship):
    @field_validator("source", mode="before")
    @classmethod
    def validate_source(cls, v):
        if not isinstance(v, XmiBaseEntity):
            raise TypeError("Source must be of type XmiBaseEntity")
        return v

    @field_validator("target", mode="before")
    @classmethod
    def validate_target(cls, v):
        if not isinstance(v, XmiStructuralCrossSection):
            raise TypeError("Target must be of type XmiStructuralCrossSection")
        return v

    @model_validator(mode="before")
    @classmethod
    def set_defaults(cls, values):
        values.setdefault("name", "hasStructuralCrossSection")
        values.setdefault("entity_type", "XmiRelHasStructuralCrossSection")
        return values


# Testing run python -m src.xmi.v2.models.relationships.xmi_has_structural_cross_section
if __name__ == "__main__":
    from ..entities.xmi_structural_material import XmiStructuralMaterial
    from ..enums.xmi_structural_material_type_enum import XmiStructuralMaterialTypeEnum

    material = XmiStructuralMaterial(
        id="mat001",
        name="Steel S355",
        material_type=XmiStructuralMaterialTypeEnum.STEEL,
        grade=355.0,
        unit_weight=7850.0,
        e_modulus=200000.0,
        g_modulus=80000.0,
        poisson_ratio=0.3,
        thermal_coefficient=1.2e-5,
        description="High-strength steel"
    )

    cross_section = XmiStructuralCrossSection(
        id="cs001",
        name="I-Beam 300x150",
        shape="I Shape",
        parameters=(300, 150, 10, 6, 8),
        material=material,
        ix=1200,
        iy=500,
        rx=3.5,
        ry=1.2,
        ex=200000,
        ey=200000,
        zx=300,
        zy=150,
        j=80,
        area=4500,
        description="Test I-beam section",
        ifcguid="a-b-c-d"
    )

    source_entity = XmiBaseEntity(id="sm001", name="Member A", entity_type="XmiStructuralCurveMember")

    rel = XmiHasStructuralCrossSection(source=source_entity, target=cross_section)

    print("Created XmiHasStructuralCrossSection relationship:")
    print(rel.model_dump(by_alias=True))