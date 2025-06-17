from pydantic import Field, field_validator, model_validator
from typing import Optional, Tuple, Union, List, Dict, Any
from ..bases.xmi_base_entity import XmiBaseEntity
from ..entities.xmi_structural_material import XmiStructuralMaterial
from ..enums.xmi_shape_enum import XmiShapeEnum
from ...utils.xmi_utilities import is_empty_or_whitespace
from ...utils.xmi_errors import XmiInconsistentDataTypeError, XmiMissingRequiredAttributeError

class XmiStructuralCrossSection(XmiBaseEntity):
    material: XmiStructuralMaterial = Field(..., alias="Material")
    shape: XmiShapeEnum = Field(..., alias="Shape")
    parameters: Tuple[Union[float, int], ...] = Field(..., alias="Parameters")
    area: Optional[float] = Field(None, alias="Area")
    second_moment_of_area_x_axis: Optional[float] = Field(None, alias="SecondMomentOfAreaXAxis")
    second_moment_of_area_y_axis: Optional[float] = Field(None, alias="SecondMomentOfAreaYAxis")
    radius_of_gyration_x_axis: Optional[float] = Field(None, alias="RadiusOfGyrationXAxis")
    radius_of_gyration_y_axis: Optional[float] = Field(None, alias="RadiusOfGyrationYAxis")
    elastic_modulus_x_axis: Optional[float] = Field(None, alias="ElasticModulusXAxis")
    elastic_modulus_y_axis: Optional[float] = Field(None, alias="ElasticModulusYAxis")
    plastic_modulus_x_axis: Optional[float] = Field(None, alias="PlasticModulusXAxis")
    plastic_modulus_y_axis: Optional[float] = Field(None, alias="PlasticModulusYAxis")
    torsional_constant: Optional[float] = Field(None, alias="TorsionalConstant")
    
    class Config:
        populate_by_name = True

    @field_validator("parameters")
    @classmethod
    def validate_parameters(cls, v):
        if not isinstance(v, (list, tuple)):
            raise TypeError("parameters must be a list or tuple")
        for item in v:
            if not isinstance(item, (int, float)):
                raise TypeError("Each parameter must be an int or float")
            if item < 0:
                raise ValueError("Value cannot be smaller than 0")
        return tuple(v)

    @field_validator("material")
    @classmethod
    def validate_material(cls, v):
        if not isinstance(v, XmiStructuralMaterial):
            raise TypeError("material must be of type XmiStructuralMaterial")
        return v

    @field_validator("shape")
    @classmethod
    def validate_shape(cls, v):
        if not isinstance(v, XmiShapeEnum):
            raise TypeError("shape must be of type XmiShapeEnum")
        return v
    
    @field_validator(
            "area", "torsional_constant", "second_moment_of_area_x_axis", "second_moment_of_area_y_axis", 
            "radius_of_gyration_x_axis", "radius_of_gyration_y_axis", "elastic_modulus_x_axis",
            "elastic_modulus_y_axis", "plastic_modulus_x_axis", "plastic_modulus_y_axis"
        )
    @classmethod
    def validate_positive_or_none(cls, v, info):
        if v is not None and v < 0:
            raise ValueError(f"{info.field_name} must be non-negative")
        return v

    @model_validator(mode="before")
    @classmethod
    def set_entity_type(cls, values):
        values.setdefault("entity_type", "XmiStructuralCrossSection")
        return values
    
    '''@classmethod
    def convert_parameter_string_to_tuple(cls, parameter_str: str) -> Tuple[float, ...]:
        parameter_list: List[str] = parameter_str.split(';')
        for param in parameter_list:
            if is_empty_or_whitespace(param):
                raise XmiInconsistentDataTypeError(
                    f"The parameter [{param}] should not be empty or whitespace")
            try:
                float(param)
            except ValueError:
                raise XmiInconsistentDataTypeError(
                    f"The parameter [{param}] within the XmiStructuralCrossSection 'parameters' attribute should be convertible to float")
        return tuple(float(param) for param in parameter_list)

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> Tuple[Optional["XmiStructuralCrossSection"], List[Exception]]:
        errors = []
        processed = obj.copy()

        if "shape" in processed:
            shape = XmiShapeEnum.from_attribute_get_enum(processed["shape"])
            if shape is None:
                errors.append(Exception(f"Invalid shape enum value: {processed['shape']}"))
                return None, errors
            processed["shape"] = shape
        else:
            errors.append(XmiMissingRequiredAttributeError("Missing 'shape'"))
            return None, errors

        if "parameters" in processed:
            try:
                processed["parameters"] = cls.convert_parameter_string_to_tuple(processed["parameters"])
            except Exception as e:
                errors.append(e)
                return None, errors
        else:
            errors.append(XmiMissingRequiredAttributeError("Missing 'parameters'"))
            return None, errors

        try:
            instance = cls(**processed)
        except Exception as e:
            errors.append(e)
            instance = None

        return instance, errors

    
    @classmethod
    def from_xmi_dict_obj(
        cls,
        xmi_dict_obj: Dict[str, Any],
        material: Optional[XmiStructuralMaterial] = None
    ) -> Tuple[Optional["XmiStructuralCrossSection"], List[Exception]]:
        key_map = {
            "Name": "name",
            "Material": "material",
            "Parameters": "parameters",
            "Shape": "shape",
            "Ix": "second_moment_of_area_x_axis",
            "Iy": "second_moment_of_area_y_axis",
            "rx": "radius_of_gyration_x_axis",
            "ry": "radius_of_gyration_y_axis",
            "Ex": "elastic_modulus_x_axis",
            "Ey": "elastic_modulus_y_axis",
            "Zx": "plastic_modulus_x_axis",
            "Zy": "plastic_modulus_y_axis",
            "J": "torsional_constant",
            "Area": "area",
            "Description": "description",
            "ID": "id",
            "IFCGUID": "ifcguid",
        }

        instance: XmiStructuralCrossSection | None = None
        error_logs: list[Exception] = []
        processed = {key_map.get(k, k): v for k, v in xmi_dict_obj.items()}

        if material is not None:
            processed["material"] = material

        instance, error_logs_found = cls.from_dict(processed)
        error_logs.extend(error_logs_found)

        return instance, error_logs'''
    

# Testing run python -m src.xmi.v2.models.entities.xmi_structural_cross_section
if __name__ == "__main__":
    from ..enums.xmi_structural_material_type_enum import XmiStructuralMaterialTypeEnum

    material = XmiStructuralMaterial(
        id="mat001",
        name="S450",
        material_type=XmiStructuralMaterialTypeEnum.STEEL,
        grade=450.0,
        unit_weight=7850.0,
        e_modulus=200000.0,
        g_modulus=80000.0,
        poisson_ratio=0.3,
        thermal_coefficient=1.2e-5,
        description="High-strength steel"
    )

    cross_section = XmiStructuralCrossSection(
        id="xs001",
        name="I-Beam 300x150",
        description="Test I-beam section",
        ifcguid="a-b-c-d",
        shape="I Shape",
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
        area=4500
    )

    print("Created XmiStructuralCrossSection:")
    print(cross_section.model_dump(by_alias=True))