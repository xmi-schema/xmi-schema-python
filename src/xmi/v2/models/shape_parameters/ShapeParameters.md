# XMI Shape Parameters

## Overview

The XMI Shape Parameters system provides strongly-typed parameter classes for cross-section shapes. Each shape (Rectangular, I-Shape, Circular, etc.) has a dedicated parameter class that serializes into a dictionary pairing symbolic keys (H, B, T, etc.) with numeric values.

This implementation follows the C# reference specification:
https://github.com/xmi-schema/xmi-schema-csharp/blob/main/XmiShapeEnumParameters.md

## Architecture

### Base Class

All shape parameter classes inherit from `BaseShapeParameters`, which provides:
- Abstract interface (`to_dict()` and `from_dict()`)
- Common validation helpers
- Pydantic integration for type safety

### Parameter Classes

Each cross-section shape has a corresponding parameter class:
- `CircularShapeParameters`
- `RectangularShapeParameters`
- `IShapeParameters`
- `CircularHollowShapeParameters`
- And many more...

### Factory Pattern

The `create_shape_parameters()` factory function creates the appropriate parameter instance based on `XmiShapeEnum` value.

## Shape Parameter Reference

| Shape | Parameter Class | Required Keys | Notes |
|-------|-----------------|---------------|-------|
| Circular | `CircularShapeParameters` | D | D = Diameter |
| Rectangular | `RectangularShapeParameters` | H, B | H = Height, B = Width |
| L Shape | `LShapeParameters` | H, B, T, t | Angle section |
| T Shape | `TShapeParameters` | H, B, T, t | Alt: d, B, T, t, r |
| C Shape | `CShapeParameters` | H, B, T1, T2, t | Channel section |
| I Shape | `IShapeParameters` | D, B, T, t, r | Wide flange |
| Circular Hollow | `CircularHollowShapeParameters` | D, t | CHS/Pipe |
| Square Hollow | `SquareHollowShapeParameters` | D, t | SHS |
| Rectangular Hollow | `RectangularHollowShapeParameters` | D, B, t | RHS |
| Trapezium | `TrapeziumShapeParameters` | H, BTop, BBot | |
| Polygon | `PolygonShapeParameters` | N, R | N = sides, R = radius |
| Equal Angle | `EqualAngleShapeParameters` | A, t, r1, r2 | Constraint: r1 > r2 |
| Unequal Angle | `UnequalAngleShapeParameters` | A, B, t, r1, r2 | |
| Flat Bar | `FlatBarShapeParameters` | B, t | |
| Square Bar | `SquareBarShapeParameters` | a | |
| Round Bar | `RoundBarShapeParameters` | D | |
| Deformed Bar | `DeformedBarShapeParameters` | D | Rebar |
| Others/Unknown | `CustomShapeParameters` | (any) | Custom key-value pairs |

## Usage Examples

### Creating Typed Parameters

```python
from xmi.v2.models.shape_parameters import RectangularShapeParameters, IShapeParameters

# Rectangular section
rect_params = RectangularShapeParameters(H=0.5, B=0.3)
print(rect_params.to_dict())  # {"H": 0.5, "B": 0.3}

# I-section
i_params = IShapeParameters(D=0.3, B=0.15, T=0.015, t=0.01, r=0.012)
print(i_params.to_dict())  # {"D": 0.3, "B": 0.15, "T": 0.015, "t": 0.01, "r": 0.012}
```

### Using with XmiCrossSection

```python
from xmi.v2.models.entities.xmi_structural_cross_section import XmiCrossSection
from xmi.v2.models.enums.xmi_shape_enum import XmiShapeEnum
from xmi.v2.models.shape_parameters import RectangularShapeParameters

# Method 1: Create with typed parameters
params = RectangularShapeParameters(H=0.5, B=0.3)
section = XmiCrossSection(
    name="RECT_500x300",
    shape=XmiShapeEnum.RECTANGULAR,
    parameters=params
)

# Method 2: Create with dictionary (automatically converted to typed parameters)
section = XmiCrossSection(
    name="RECT_500x300",
    shape=XmiShapeEnum.RECTANGULAR,
    parameters={"H": 0.5, "B": 0.3}
)

# Access parameters
params_dict = section.get_parameters_dict()
height = section.get_parameter("H")
width = section.get_parameter("B")
```

### Using the Factory

```python
from xmi.v2.models.shape_parameters import create_shape_parameters
from xmi.v2.models.enums.xmi_shape_enum import XmiShapeEnum

# Create parameters for any shape using factory
params_dict = {"H": 0.5, "B": 0.3}
params = create_shape_parameters(XmiShapeEnum.RECTANGULAR, params_dict)

# Factory automatically selects the correct class
params_dict = {"D": 0.4}
params = create_shape_parameters(XmiShapeEnum.CIRCULAR, params_dict)
```

### Loading from JSON

```python
import json

# JSON format (XMI standard)
json_data = {
    "Name": "RECT_500x300",
    "Shape": "Rectangular",
    "Parameters": {
        "H": 0.5,
        "B": 0.3
    }
}

# Create cross-section from dict
section, errors = XmiCrossSection.from_dict(json_data)

# Parameters are automatically converted to RectangularShapeParameters
assert isinstance(section.parameters, RectangularShapeParameters)
```

### Accessing Parameter Values

```python
# Get all parameters as dictionary
params_dict = section.get_parameters_dict()
# {"H": 0.5, "B": 0.3}

# Get specific parameter
height = section.get_parameter("H")  # 0.5
width = section.get_parameter("B")   # 0.3

# Direct access if you have typed parameters
if isinstance(section.parameters, RectangularShapeParameters):
    height = section.parameters.H
    width = section.parameters.B
```

### Complex Shapes

```python
from xmi.v2.models.shape_parameters import IShapeParameters, CircularHollowShapeParameters

# I-Shape (wide flange beam)
i_params = IShapeParameters(
    D=0.406,      # Depth
    B=0.178,      # Flange width
    T=0.016,      # Flange thickness
    t=0.01,       # Web thickness
    r=0.014       # Root radius
)

section = XmiCrossSection(
    name="W16x26",
    shape=XmiShapeEnum.I_SHAPE,
    parameters=i_params,
    area=4.954e-3,    # m^2
    second_moment_of_area_x_axis=1.19e-4,  # m^4
    second_moment_of_area_y_axis=1.03e-5   # m^4
)

# Circular Hollow Section (pipe)
chs_params = CircularHollowShapeParameters(
    D=0.273,      # Outside diameter
    t=0.008       # Wall thickness
)

section = XmiCrossSection(
    name="CHS273x8",
    shape=XmiShapeEnum.CIRCULAR_HOLLOW,
    parameters=chs_params
)
```

### Custom/Unknown Shapes

```python
from xmi.v2.models.shape_parameters import CustomShapeParameters

# For custom shapes not in the standard set
custom_params = CustomShapeParameters(
    parameters={
        "CustomDim1": 0.5,
        "CustomDim2": 0.3,
        "CustomAngle": 45.0
    }
)

section = XmiCrossSection(
    name="CUSTOM_01",
    shape=XmiShapeEnum.OTHERS,
    parameters=custom_params
)
```

## Validation

### Automatic Validation

All parameter classes include automatic validation:

```python
from xmi.v2.models.shape_parameters import RectangularShapeParameters

# Valid parameters
params = RectangularShapeParameters(H=0.5, B=0.3)  # OK

# Invalid parameters (will raise ValueError)
try:
    params = RectangularShapeParameters(H=-0.5, B=0.3)  # Negative value!
except ValueError as e:
    print(f"Validation error: {e}")

try:
    params = RectangularShapeParameters(H=0.5, B=0)  # Zero value!
except ValueError as e:
    print(f"Validation error: {e}")
```

### Constraint Validation

Some shapes have special constraints:

```python
from xmi.v2.models.shape_parameters import EqualAngleShapeParameters

# Equal angle requires r1 > r2
params = EqualAngleShapeParameters(
    A=0.1,
    t=0.01,
    r1=0.012,  # External radius
    r2=0.006   # Internal radius (must be less than r1)
)

# This will raise ValueError when calling to_dict()
try:
    bad_params = EqualAngleShapeParameters(A=0.1, t=0.01, r1=0.006, r2=0.012)
    bad_params.to_dict()  # Validation happens here
except ValueError as e:
    print(f"Constraint violation: {e}")
```

## Backward Compatibility

The implementation supports multiple parameter formats for backward compatibility:

### 1. New Format (Dictionary with Symbols)
```python
# Recommended: Dictionary with symbolic keys
section = XmiCrossSection(
    name="RECT",
    shape=XmiShapeEnum.RECTANGULAR,
    parameters={"H": 0.5, "B": 0.3}
)
```

### 2. Legacy Format (Semicolon-Separated String)
```python
# Legacy: String with semicolon-separated values
data = {
    "Name": "RECT",
    "Shape": "Rectangular",
    "Parameters": "0.5;0.3"  # H=0.5, B=0.3
}
section, errors = XmiCrossSection.from_dict(data)
# Still works, converted to tuple internally
```

### 3. Typed Parameters (New Feature)
```python
# New: Strongly-typed parameter objects
params = RectangularShapeParameters(H=0.5, B=0.3)
section = XmiCrossSection(
    name="RECT",
    shape=XmiShapeEnum.RECTANGULAR,
    parameters=params
)
```

## JSON Serialization

### Export to JSON

```python
# Cross-section with typed parameters
section = XmiCrossSection(
    name="RECT_500x300",
    shape=XmiShapeEnum.RECTANGULAR,
    parameters={"H": 0.5, "B": 0.3}
)

# Export to dict for JSON
section_dict = section.model_dump()
# {
#     "name": "RECT_500x300",
#     "shape": "Rectangular",
#     "parameters": {"H": 0.5, "B": 0.3},  # Automatically serialized
#     ...
# }

# Convert to JSON
import json
json_str = json.dumps(section_dict, indent=2)
```

### Import from JSON

```python
import json

# JSON string
json_str = '''
{
    "Name": "W16x26",
    "Shape": "I Shape",
    "Parameters": {
        "D": 0.406,
        "B": 0.178,
        "T": 0.016,
        "t": 0.01,
        "r": 0.014
    }
}
'''

# Parse and create cross-section
data = json.loads(json_str)
section, errors = XmiCrossSection.from_dict(data)

# Parameters are automatically converted to IShapeParameters
assert isinstance(section.parameters, IShapeParameters)
```

## Best Practices

1. **Use Typed Parameters**: Prefer using typed parameter classes for type safety and IDE support

```python
# Good: Type-safe
params = RectangularShapeParameters(H=0.5, B=0.3)

# Less ideal: Just a dictionary
params = {"H": 0.5, "B": 0.3}
```

2. **Validate Early**: Let Pydantic validate parameters at creation time

```python
try:
    params = RectangularShapeParameters(H=0.5, B=0.3)
    section = XmiCrossSection(name="RECT", shape=XmiShapeEnum.RECTANGULAR, parameters=params)
except ValueError as e:
    print(f"Invalid parameters: {e}")
```

3. **Use Factory for Dynamic Shapes**: When shape is determined at runtime, use the factory

```python
from xmi.v2.models.shape_parameters import create_shape_parameters

shape_enum = get_shape_from_user()  # Dynamic shape selection
params_dict = get_parameters_from_user()  # User-provided values

params = create_shape_parameters(shape_enum, params_dict)
section = XmiCrossSection(name="DYNAMIC", shape=shape_enum, parameters=params)
```

4. **Document Units**: Always document what units your parameters are in

```python
# Good: Clear units in comments/documentation
params = RectangularShapeParameters(
    H=0.5,  # Height in meters
    B=0.3   # Width in meters
)
```

## Related Documentation

- [XmiCrossSection Entity](../entities/XmiCrossSection.md)
- [XmiShapeEnum](../enums/XmiShapeEnum.md)
- [C# Reference Implementation](https://github.com/xmi-schema/xmi-schema-csharp/blob/main/XmiShapeEnumParameters.md)
