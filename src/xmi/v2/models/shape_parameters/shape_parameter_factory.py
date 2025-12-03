"""
Factory for creating shape parameter instances based on shape type.

This module provides a factory function to create the appropriate shape parameter
instance based on the XmiShapeEnum value.
"""

from typing import Dict, Optional
from ..enums.xmi_shape_enum import XmiShapeEnum
from .base_shape_parameters import BaseShapeParameters
from .shape_parameters import (
    CircularShapeParameters,
    RectangularShapeParameters,
    LShapeParameters,
    TShapeParameters,
    CShapeParameters,
    IShapeParameters,
    CircularHollowShapeParameters,
    SquareHollowShapeParameters,
    RectangularHollowShapeParameters,
    TrapeziumShapeParameters,
    PolygonShapeParameters,
    EqualAngleShapeParameters,
    UnequalAngleShapeParameters,
    FlatBarShapeParameters,
    SquareBarShapeParameters,
    RoundBarShapeParameters,
    DeformedBarShapeParameters,
    CustomShapeParameters,
)


# Mapping from XmiShapeEnum to parameter class
SHAPE_PARAMETER_CLASS_MAP = {
    XmiShapeEnum.CIRCULAR: CircularShapeParameters,
    XmiShapeEnum.RECTANGULAR: RectangularShapeParameters,
    XmiShapeEnum.L_SHAPE: LShapeParameters,
    XmiShapeEnum.T_SHAPE: TShapeParameters,
    XmiShapeEnum.C_SHAPE: CShapeParameters,
    XmiShapeEnum.I_SHAPE: IShapeParameters,
    XmiShapeEnum.CIRCULAR_HOLLOW: CircularHollowShapeParameters,
    XmiShapeEnum.SQUARE_HOLLOW: SquareHollowShapeParameters,
    XmiShapeEnum.RECTANGULAR_HOLLOW: RectangularHollowShapeParameters,
    XmiShapeEnum.OTHERS: CustomShapeParameters,
    XmiShapeEnum.UNKNOWN: CustomShapeParameters,
}


def create_shape_parameters(
    shape: XmiShapeEnum,
    parameters_dict: Dict[str, float]
) -> Optional[BaseShapeParameters]:
    """
    Create shape parameter instance based on shape type.

    Args:
        shape: The cross-section shape enum value
        parameters_dict: Dictionary of parameter key-value pairs

    Returns:
        BaseShapeParameters: Instance of the appropriate shape parameter class,
                           or None if shape is not mapped

    Raises:
        ValueError: If parameters_dict is invalid for the given shape
        KeyError: If required parameters are missing

    Examples:
        >>> from xmi.v2.models.enums.xmi_shape_enum import XmiShapeEnum
        >>> params_dict = {"H": 0.5, "B": 0.3}
        >>> params = create_shape_parameters(XmiShapeEnum.RECTANGULAR, params_dict)
        >>> print(params.to_dict())
        {"H": 0.5, "B": 0.3}

        >>> params_dict = {"D": 0.4}
        >>> params = create_shape_parameters(XmiShapeEnum.CIRCULAR, params_dict)
        >>> print(params.to_dict())
        {"D": 0.4}
    """
    parameter_class = SHAPE_PARAMETER_CLASS_MAP.get(shape)

    if parameter_class is None:
        # For unknown shapes, use CustomShapeParameters
        return CustomShapeParameters.from_dict(parameters_dict)

    try:
        return parameter_class.from_dict(parameters_dict)
    except Exception as e:
        raise ValueError(
            f"Failed to create {parameter_class.__name__} from {parameters_dict}: {str(e)}"
        ) from e


def get_parameter_class(shape: XmiShapeEnum) -> Optional[type]:
    """
    Get the parameter class for a given shape.

    Args:
        shape: The cross-section shape enum value

    Returns:
        type: The parameter class, or None if not mapped

    Examples:
        >>> from xmi.v2.models.enums.xmi_shape_enum import XmiShapeEnum
        >>> cls = get_parameter_class(XmiShapeEnum.RECTANGULAR)
        >>> print(cls.__name__)
        RectangularShapeParameters
    """
    return SHAPE_PARAMETER_CLASS_MAP.get(shape)


def get_required_parameters(shape: XmiShapeEnum) -> list[str]:
    """
    Get list of required parameter keys for a shape.

    Args:
        shape: The cross-section shape enum value

    Returns:
        list[str]: List of required parameter symbol keys

    Examples:
        >>> from xmi.v2.models.enums.xmi_shape_enum import XmiShapeEnum
        >>> params = get_required_parameters(XmiShapeEnum.RECTANGULAR)
        >>> print(params)
        ['H', 'B']

        >>> params = get_required_parameters(XmiShapeEnum.I_SHAPE)
        >>> print(params)
        ['D', 'B', 'T', 't', 'r']
    """
    parameter_class = SHAPE_PARAMETER_CLASS_MAP.get(shape)

    if parameter_class is None:
        return []

    # Get field names from the class
    if hasattr(parameter_class, 'model_fields'):
        # Pydantic v2 style
        fields = parameter_class.model_fields
        required_fields = [
            field_name for field_name, field_info in fields.items()
            if field_info.is_required()
        ]
        return required_fields
    else:
        # Fallback: return empty list
        return []
