from pydantic import Field, field_validator, model_validator
from typing import Optional, Tuple, List
from ..bases.xmi_base_entity import XmiBaseEntity
from ..enums.xmi_structural_material_type_enum import XmiStructuralMaterialTypeEnum


class XmiStructuralMaterial(XmiBaseEntity):
    material_type: XmiStructuralMaterialTypeEnum = Field(..., alias="MaterialType")
    grade: Optional[float] = Field(None, alias="Grade")
    unit_weight: Optional[float] = Field(None, alias="UnitWeight")
    e_modulus: Optional[float] = Field(None, alias="EModulus")
    g_modulus: Optional[float] = Field(None, alias="GModulus")
    poisson_ratio: Optional[float] = Field(None, alias="PoissonRatio")
    thermal_coefficient: Optional[float] = Field(None, alias="ThermalCoefficient")

    class Config:
        populate_by_name = True

    @field_validator("material_type")
    @classmethod
    def validate_material_type(cls, v):
        if not isinstance(v, XmiStructuralMaterialTypeEnum):
            raise TypeError("material_type must be a valid XmiStructuralMaterialTypeEnum")
        return v

    @field_validator("grade", "unit_weight", "e_modulus", "g_modulus", "poisson_ratio", "thermal_coefficient")
    @classmethod
    def validate_floats(cls, v):
        if v is not None and not isinstance(v, (float, int)):
            raise TypeError("Value must be float, int, or None")
        return v

    @model_validator(mode="before")
    @classmethod
    def set_entity_type(cls, values):
        values.setdefault("entity_type", "XmiStructuralMaterial")
        return values

    '''@classmethod
    def from_dict(cls, obj: dict) -> Tuple[Optional["XmiStructuralMaterial"], List[Exception]]:
        error_logs: List[Exception] = []
        required = ["material_type"]
        processed = obj.copy()

        for attr in required:
            if attr not in processed:
                error_logs.append(Exception(f"Missing attribute: {attr}"))
                processed[attr] = None

        try:
            processed["material_type"] = XmiStructuralMaterialTypeEnum.from_attribute_get_enum(
                processed.get("material_type")
            )
        except Exception as e:
            error_logs.append(e)

        try:
            instance = cls.model_validate(processed)
        except Exception as e:
            error_logs.append(Exception(f"Error instantiating XmiStructuralMaterial: {e}"))
            instance = None

        return instance, error_logs

    @classmethod
    def from_xmi_dict_obj(cls, xmi_dict_obj: dict) -> Tuple[Optional["XmiStructuralMaterial"], List[Exception]]:
        key_map = {
            "Name": "name",
            "Type": "material_type",
            "Grade": "grade",
            "UnitWeight": "unit_weight",
            "EModulus": "e_modulus",
            "GModulus": "g_modulus",
            "PoissonRatio": "poisson_ratio",
            "Description": "description",
            "ID": "id",
            "IFCGUID": "ifcguid",
            "ThermalCoefficient": "thermal_coefficient",
        }

        processed = {key_map.get(k, k): v for k, v in xmi_dict_obj.items()}
        return cls.from_dict(processed)'''


# Testing run python -m src.xmi.v2.models.entities.xmi_structural_material
if __name__ == "__main__":
    def test_structural_material():
        test_data = {
            "material_type": "Steel",
            "grade": 450,
            "unit_weight": 7850,
            "e_modulus": 200000,
            "g_modulus": 80000,
            "poisson_ratio": 0.3,
            "thermal_coefficient": 1.2e-5,
            "name": "S450",
            "description": "High-strength steel",
            "id": "mat001"
        }

        instance, errors = XmiStructuralMaterial.from_dict(test_data)

        if errors:
            print("Errors encountered:")
            for e in errors:
                print("-", e)
        else:
            print("Created XmiStructuralMaterial:")
            print(instance.model_dump_json(by_alias=True))

    test_structural_material()