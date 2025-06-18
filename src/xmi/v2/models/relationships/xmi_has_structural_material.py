from pydantic import Field, field_validator, model_validator
from ..bases.xmi_base_relationship import XmiBaseRelationship
from ..bases.xmi_base_entity import XmiBaseEntity
from ..entities.xmi_structural_material import XmiStructuralMaterial

class XmiHasStructuralMaterial(XmiBaseRelationship):
    @field_validator("source")
    @classmethod
    def validate_source(cls, v):
        if not isinstance(v, XmiBaseEntity):
            raise TypeError("Source must be of type XmiBaseEntity")
        return v

    @field_validator("target")
    @classmethod
    def validate_target(cls, v):
        if not isinstance(v, XmiStructuralMaterial):
            raise TypeError("Target must be of type XmiStructuralMaterial")
        return v

    @model_validator(mode="before")
    @classmethod
    def set_defaults(cls, values):
        values.setdefault("name", "hasStructuralMaterial")
        values.setdefault("entity_type", "XmiRelHasStructuralMaterial")
        return values


# Testing run python -m src.xmi.v2.models.relationships.xmi_has_structural_material
if __name__ == "__main__":
    from ..entities.xmi_structural_cross_section import XmiStructuralCrossSection
    from ..enums.xmi_structural_material_type_enum import XmiStructuralMaterialTypeEnum
    from ..enums.xmi_shape_enum import XmiShapeEnum

    material = XmiStructuralMaterial(
        id="mat001",
        name="Steel S355",
        description="High-strength steel",
        material_type=XmiStructuralMaterialTypeEnum.STEEL,
        grade=355.0,
        unit_weight=7850.0,
        e_modulus=200000.0,
        g_modulus=80000.0,
        poisson_ratio=0.3,
        thermal_coefficient=1.2e-5
    )

    cross_section = XmiStructuralCrossSection(
        id="cs001",
        name="I-Beam 300x150",
        shape=XmiShapeEnum.I_SHAPE,
        parameters=(300.0, 150.0, 10.0, 6.0, 8.0),
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
        description="Test I-beam section"
    )

    rel = XmiHasStructuralMaterial(
        source=cross_section,
        target=material,
        name="hasStructuralMaterial"
    )

    print("Created XmiHasStructuralMaterial relationship:")
    print(rel.model_dump(by_alias=True))