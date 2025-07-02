from pydantic import Field, field_validator, model_validator, ConfigDict
from typing import Optional, Tuple, Union, List, Dict, Any
from ..bases.xmi_base_entity import XmiBaseEntity
from ..enums.xmi_shape_enum import XmiShapeEnum
from ...utils.xmi_utilities import is_empty_or_whitespace
from ...utils.xmi_errors import XmiInconsistentDataTypeError, XmiMissingRequiredAttributeError

class XmiStructuralCrossSection(XmiBaseEntity):
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
    
    model_config = ConfigDict(populate_by_name=True)

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
    
    @classmethod
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

        if "Shape" in processed:
            processed["shape"] = processed.pop("Shape")
        elif "shape" not in processed:
            errors.append(XmiMissingRequiredAttributeError("Missing 'shape'"))
            return None, errors

        if "Parameters" in processed:
            try:
                processed["parameters"] = cls.convert_parameter_string_to_tuple(processed.pop("Parameters"))
            except Exception as e:
                errors.append(e)
                return None, errors
        elif "parameters" not in processed:
            errors.append(XmiMissingRequiredAttributeError("Missing 'parameters'"))
            return None, errors

        try:
            instance = cls(**processed)
        except Exception as e:
            errors.append(e)
            instance = None

        return instance, errors

    
    '''@classmethod
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
    