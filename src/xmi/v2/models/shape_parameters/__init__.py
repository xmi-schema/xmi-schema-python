"""
Shape parameter classes for XMI cross-sections.

This package provides strongly-typed parameter classes for each cross-section
shape in the XMI schema, following the specification from:
https://github.com/xmi-schema/xmi-schema-csharp/blob/main/XmiShapeEnumParameters.md

Each shape parameter class serializes into a dictionary pairing symbols
(H, B, T, etc.) with numeric values for use in XmiCrossSection.
"""

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
from .shape_parameter_factory import (
    create_shape_parameters,
    get_parameter_class,
    get_required_parameters,
    SHAPE_PARAMETER_CLASS_MAP,
)

__all__ = [
    # Base class
    "BaseShapeParameters",
    # Parameter classes
    "CircularShapeParameters",
    "RectangularShapeParameters",
    "LShapeParameters",
    "TShapeParameters",
    "CShapeParameters",
    "IShapeParameters",
    "CircularHollowShapeParameters",
    "SquareHollowShapeParameters",
    "RectangularHollowShapeParameters",
    "TrapeziumShapeParameters",
    "PolygonShapeParameters",
    "EqualAngleShapeParameters",
    "UnequalAngleShapeParameters",
    "FlatBarShapeParameters",
    "SquareBarShapeParameters",
    "RoundBarShapeParameters",
    "DeformedBarShapeParameters",
    "CustomShapeParameters",
    # Factory functions
    "create_shape_parameters",
    "get_parameter_class",
    "get_required_parameters",
    "SHAPE_PARAMETER_CLASS_MAP",
]

# Rebuild models now that XmiUnitEnum is fully defined
from ..enums.xmi_unit_enum import XmiUnitEnum
BaseShapeParameters.model_rebuild()
CircularShapeParameters.model_rebuild()
RectangularShapeParameters.model_rebuild()
LShapeParameters.model_rebuild()
TShapeParameters.model_rebuild()
CShapeParameters.model_rebuild()
IShapeParameters.model_rebuild()
CircularHollowShapeParameters.model_rebuild()
SquareHollowShapeParameters.model_rebuild()
RectangularHollowShapeParameters.model_rebuild()
TrapeziumShapeParameters.model_rebuild()
PolygonShapeParameters.model_rebuild()
EqualAngleShapeParameters.model_rebuild()
UnequalAngleShapeParameters.model_rebuild()
FlatBarShapeParameters.model_rebuild()
SquareBarShapeParameters.model_rebuild()
RoundBarShapeParameters.model_rebuild()
DeformedBarShapeParameters.model_rebuild()
CustomShapeParameters.model_rebuild()
