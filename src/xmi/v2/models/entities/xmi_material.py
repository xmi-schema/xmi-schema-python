from pydantic import Field, field_validator, model_validator, ConfigDict
from typing import Optional, Tuple, List
from ast import literal_eval
from ..bases.xmi_base_entity import XmiBaseEntity
from ..enums.xmi_structural_material_type_enum import XmiStructuralMaterialTypeEnum


class XmiMaterial(XmiBaseEntity):
    material_type: XmiStructuralMaterialTypeEnum = Field(..., alias="MaterialType")
    grade: Optional[float] = Field(None, alias="Grade")
    unit_weight: Optional[float] = Field(None, alias="UnitWeight")
    e_modulus: Optional[Tuple[float, float, float]] = Field(None, alias="EModulus")
    g_modulus: Optional[Tuple[float, float, float]] = Field(None, alias="GModulus")
    poisson_ratio: Optional[Tuple[float, float, float]] = Field(None, alias="PoissonRatio")
    thermal_coefficient: Optional[float] = Field(None, alias="ThermalCoefficient")

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("material_type")
    @classmethod
    def validate_material_type(cls, v):
        if not isinstance(v, XmiStructuralMaterialTypeEnum):
            raise TypeError("material_type must be a valid XmiStructuralMaterialTypeEnum")
        return v

    @field_validator("grade", "unit_weight", "thermal_coefficient")
    @classmethod
    def validate_floats(cls, v):
        if v is not None and not isinstance(v, (float, int)):
            raise TypeError("Value must be float, int, or None")
        return v

    @field_validator("e_modulus", "g_modulus", "poisson_ratio")
    @classmethod
    def validate_float_tuples(cls, v):
        if v is not None:
            if not isinstance(v, tuple) or not all(isinstance(i, (float, int)) for i in v):
                raise TypeError("Value must be a tuple of floats or None")
        return v

    @model_validator(mode="before")
    @classmethod
    def set_entity_type(cls, values):
        values.setdefault("entity_type", "XmiStructuralMaterial")
        return values

    @classmethod
    def from_dict(cls, obj: dict) -> Tuple[Optional["XmiMaterial"], List[Exception]]:
        error_logs: List[Exception] = []
        processed = {}

        for name, field in cls.model_fields.items():
            alias = field.alias or name
            if alias in obj:
                processed[name] = obj[alias]

        required_attrs = ("material_type",)
        missing = [attr for attr in required_attrs if attr not in processed]
        if missing:
            for attr in missing:
                error_logs.append(Exception(f"Missing attribute: {attr}"))
            return None, error_logs

        try:
            processed["material_type"] = XmiStructuralMaterialTypeEnum.from_attribute_get_enum(
                processed.get("material_type")
            )
        except ValueError as e:
            error_logs.append(Exception(f"Invalid material_type: {e}"))
            processed["material_type"] = None

        tuple_fields = ("e_modulus", "g_modulus", "poisson_ratio")
        for key in tuple_fields:
            val = processed.get(key)
            if isinstance(val, str) and val.startswith("(") and val.endswith(")"):
                try:
                    processed[key] = tuple(float(x.strip()) for x in val[1:-1].split(","))
                except Exception as e:
                    error_logs.append(Exception(f"Invalid tuple format in {key}: {e}"))
                    processed[key] = None

        try:
            instance = cls.model_validate(processed)
        except Exception as e:
            error_logs.append(Exception(f"Error instantiating XmiStructuralMaterial: {e}"))
            instance = None

        return instance, error_logs

    '''@classmethod
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
