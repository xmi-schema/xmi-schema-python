from pydantic import Field, field_validator, model_validator, ConfigDict
from typing import Optional, Tuple, Union, List, Dict, Any
from ..bases.xmi_base_entity import XmiBaseEntity
from ..enums.xmi_shape_enum import XmiShapeEnum
from ..shape_parameters import BaseShapeParameters, create_shape_parameters
from ...utils.xmi_utilities import is_empty_or_whitespace
from ...utils.xmi_errors import XmiInconsistentDataTypeError, XmiMissingRequiredAttributeError

class XmiCrossSection(XmiBaseEntity):
    """
    XMI cross-section entity with strongly-typed shape parameters.

    This class represents a structural cross-section with its geometric properties.
    Parameters are stored as strongly-typed classes (RectangularShapeParameters,
    IShapeParameters, etc.) that serialize to dictionaries with symbolic keys.

    Attributes:
        shape: Cross-section shape type (enum)
        parameters: Shape-specific parameters (strongly-typed or dict/tuple for compatibility)
        area: Cross-sectional area
        second_moment_of_area_x_axis: Moment of inertia about X axis (Ix)
        second_moment_of_area_y_axis: Moment of inertia about Y axis (Iy)
        radius_of_gyration_x_axis: Radius of gyration about X axis (rx)
        radius_of_gyration_y_axis: Radius of gyration about Y axis (ry)
        elastic_modulus_x_axis: Elastic section modulus about X axis (Ex)
        elastic_modulus_y_axis: Elastic section modulus about Y axis (Ey)
        plastic_modulus_x_axis: Plastic section modulus about X axis (Zx)
        plastic_modulus_y_axis: Plastic section modulus about Y axis (Zy)
        torsional_constant: Torsional constant (J)

    Examples:
        >>> from xmi.v2.models.enums.xmi_shape_enum import XmiShapeEnum
        >>> from xmi.v2.models.shape_parameters import RectangularShapeParameters
        >>> # Using strongly-typed parameters
        >>> params = RectangularShapeParameters(H=0.5, B=0.3)
        >>> section = XmiCrossSection(
        ...     name="RECT_500x300",
        ...     shape=XmiShapeEnum.RECTANGULAR,
        ...     parameters=params
        ... )
        >>> # Using dictionary (will be converted to typed parameters)
        >>> section = XmiCrossSection(
        ...     name="RECT_500x300",
        ...     shape=XmiShapeEnum.RECTANGULAR,
        ...     parameters={"H": 0.5, "B": 0.3}
        ... )
    """
    shape: XmiShapeEnum = Field(..., alias="Shape")
    parameters: Union[BaseShapeParameters, Dict[str, float], Tuple[Union[float, int], ...]] = Field(..., alias="Parameters")
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
        # Accept BaseShapeParameters instances directly
        if isinstance(v, BaseShapeParameters):
            return v

        # Accept dictionaries (convert to tuple for backward compatibility or keep as dict)
        if isinstance(v, dict):
            # Keep as dictionary for now - will be converted to typed params in model_validator
            for key, value in v.items():
                if not isinstance(value, (int, float)):
                    raise TypeError(f"Parameter value for '{key}' must be numeric, got {type(value)}")
                if value < 0:
                    raise ValueError(f"Parameter value for '{key}' cannot be negative")
            return v

        # Accept tuples/lists (backward compatibility - old string format)
        if isinstance(v, (list, tuple)):
            for item in v:
                if not isinstance(item, (int, float)):
                    raise TypeError("Each parameter must be an int or float")
                if item < 0:
                    raise ValueError("Value cannot be smaller than 0")
            return tuple(v)

        raise TypeError(f"parameters must be BaseShapeParameters, dict, list, or tuple, got {type(v)}")

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
        values.setdefault("entity_type", "XmiCrossSection")
        return values

    @model_validator(mode="after")
    def convert_dict_to_typed_parameters(self):
        """
        Convert dictionary parameters to strongly-typed shape parameter instances.

        If parameters is a dict and not already a BaseShapeParameters instance,
        this will convert it to the appropriate typed parameter class based on
        the shape.
        """
        if isinstance(self.parameters, dict) and not isinstance(self.parameters, BaseShapeParameters):
            try:
                typed_params = create_shape_parameters(self.shape, self.parameters)
                # Use object.__setattr__ to bypass Pydantic's frozen model check
                object.__setattr__(self, 'parameters', typed_params)
            except Exception:
                # If conversion fails, keep as dictionary (backward compatibility)
                pass
        return self

    def get_parameters_dict(self) -> Dict[str, float]:
        """
        Get parameters as a dictionary.

        Returns:
            Dict[str, float]: Parameter dictionary with symbolic keys

        Examples:
            >>> section = XmiCrossSection(
            ...     name="RECT",
            ...     shape=XmiShapeEnum.RECTANGULAR,
            ...     parameters={"H": 0.5, "B": 0.3}
            ... )
            >>> section.get_parameters_dict()
            {"H": 0.5, "B": 0.3}
        """
        if isinstance(self.parameters, BaseShapeParameters):
            return self.parameters.to_dict()
        elif isinstance(self.parameters, dict):
            return self.parameters.copy()
        else:
            # Tuple format - return empty dict (legacy format not supported)
            return {}

    def get_parameter(self, key: str) -> Optional[float]:
        """
        Get a specific parameter value by key.

        Args:
            key: Parameter symbol (e.g., "H", "B", "T")

        Returns:
            Optional[float]: Parameter value or None if not found

        Examples:
            >>> section.get_parameter("H")
            0.5
            >>> section.get_parameter("B")
            0.3
        """
        params_dict = self.get_parameters_dict()
        return params_dict.get(key)
    
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
                    f"The parameter [{param}] within the XmiCrossSection 'parameters' attribute should be convertible to float")
        return tuple(float(param) for param in parameter_list)

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> Tuple[Optional["XmiCrossSection"], List[Exception]]:
        """
        Create XmiCrossSection from dictionary.

        Supports multiple parameter formats:
        1. Dictionary with symbolic keys: {"H": 0.5, "B": 0.3}
        2. String with semicolon-separated values: "0.5;0.3" (legacy)
        3. Typed parameter instance: RectangularShapeParameters(H=0.5, B=0.3)

        Args:
            obj: Dictionary containing cross-section data

        Returns:
            Tuple of (XmiCrossSection instance or None, list of errors)

        Examples:
            >>> # New format with dictionary parameters
            >>> data = {
            ...     "Shape": "Rectangular",
            ...     "Parameters": {"H": 0.5, "B": 0.3}
            ... }
            >>> section, errors = XmiCrossSection.from_dict(data)

            >>> # Legacy format with string parameters
            >>> data = {
            ...     "Shape": "Rectangular",
            ...     "Parameters": "0.5;0.3"
            ... }
            >>> section, errors = XmiCrossSection.from_dict(data)
        """
        errors = []
        processed = obj.copy()

        if "Shape" in processed:
            processed["shape"] = processed.pop("Shape")
        elif "shape" not in processed:
            errors.append(XmiMissingRequiredAttributeError("Missing 'shape'"))
            return None, errors

        if "Parameters" in processed:
            param_value = processed.pop("Parameters")

            # Check if parameters is already a dictionary (new format)
            if isinstance(param_value, dict):
                processed["parameters"] = param_value
            # Check if it's a string (legacy format with semicolon-separated values)
            elif isinstance(param_value, str):
                try:
                    processed["parameters"] = cls.convert_parameter_string_to_tuple(param_value)
                except Exception as e:
                    errors.append(e)
                    return None, errors
            # Check if it's already a BaseShapeParameters instance
            elif isinstance(param_value, BaseShapeParameters):
                processed["parameters"] = param_value
            else:
                # Try to use as-is (could be list/tuple)
                processed["parameters"] = param_value

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
    ) -> Tuple[Optional["XmiCrossSection"], List[Exception]]:
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

        instance: XmiCrossSection | None = None
        error_logs: list[Exception] = []
        processed = {key_map.get(k, k): v for k, v in xmi_dict_obj.items()}

        if material is not None:
            processed["material"] = material

        instance, error_logs_found = cls.from_dict(processed)
        error_logs.extend(error_logs_found)

        return instance, error_logs'''
    