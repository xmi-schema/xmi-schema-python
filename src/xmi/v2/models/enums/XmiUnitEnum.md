# XmiUnitEnum

## Overview

`XmiUnitEnum` is an enumeration that defines the units of measurement used in the XMI schema for geometric and physical quantities. This enum ensures consistent unit handling across the model.

## Class Hierarchy

- **Parent**: [`XmiBaseEnum`](../bases/XmiBaseEnum.md)
- **Grandparent**: `str`, `Enum`
- **Version**: v2 (Pydantic-based implementation)
- **Module**: `src/xmi/v2/models/enums/xmi_unit_enum.py`

## Enum Values

| Member Name | Value | Dimension | Typical Use |
|-------------|-------|-----------|-------------|
| `METER` | "m" | Length | Large dimensions, spans |
| `CENTIMETER` | "cm" | Length | Medium dimensions |
| `MILLIMETER` | "mm" | Length | Cross-section dimensions |
| `METER2` | "m^2" | Area | Floor areas, surface areas |
| `MILLIMETER2` | "mm^2" | Area | Cross-section areas |
| `METER3` | "m^3" | Volume | Concrete volumes |
| `MILLIMETER3` | "mm^3" | Volume | Small volumes |
| `METER4` | "m^4" | Second moment of area | Large-scale inertia |
| `MILLIMETER4` | "mm^4" | Second moment of area | Cross-section inertia |
| `SECOND` | "sec" | Time | Dynamic analysis, durations |

## Purpose and Functionality

### Unit System

The XMI schema supports SI (metric) units with the following dimensional groups:

**Length Units:**
- `METER` (m): Primary length unit for coordinates and spans
- `CENTIMETER` (cm): Intermediate length unit
- `MILLIMETER` (mm): Common for cross-section dimensions

**Area Units:**
- `METER2` (m²): Large areas (floor plans, site areas)
- `MILLIMETER2` (mm²): Cross-section properties

**Volume Units:**
- `METER3` (m³): Material quantities
- `MILLIMETER3` (mm³): Small volumes

**Inertia Units:**
- `METER4` (m⁴): Moment of inertia for large members
- `MILLIMETER4` (mm⁴): Section properties (I, J)

**Time Units:**
- `SECOND` (sec): Time-dependent analysis

## Usage Examples

### Basic Usage

```python
from xmi.v2.models.enums.xmi_unit_enum import XmiUnitEnum

# Direct access
unit = XmiUnitEnum.MILLIMETER
print(unit.value)  # "mm"

# Case-insensitive lookup
unit = XmiUnitEnum("m")      # Returns METER
unit = XmiUnitEnum("mm^2")   # Returns MILLIMETER2
```

### Specifying Units in Entities

```python
from xmi.v2.models.entities.xmi_structural_unit import XmiStructuralUnit

# Define length unit
length_unit = XmiStructuralUnit(
    name="LengthUnit",
    unit=XmiUnitEnum.MILLIMETER
)

# Define area unit
area_unit = XmiStructuralUnit(
    name="AreaUnit",
    unit=XmiUnitEnum.MILLIMETER2
)

# Define moment of inertia unit
inertia_unit = XmiStructuralUnit(
    name="InertiaUnit",
    unit=XmiUnitEnum.MILLIMETER4
)
```

### Unit Conversion

```python
def convert_length(value, from_unit, to_unit):
    """Convert length values between units."""
    # Conversion factors to meters
    to_meters = {
        XmiUnitEnum.METER: 1.0,
        XmiUnitEnum.CENTIMETER: 0.01,
        XmiUnitEnum.MILLIMETER: 0.001,
    }

    # Convert to meters first, then to target unit
    value_in_meters = value * to_meters[from_unit]
    converted_value = value_in_meters / to_meters[to_unit]

    return converted_value

# Usage
length_mm = 1000  # mm
length_m = convert_length(length_mm, XmiUnitEnum.MILLIMETER, XmiUnitEnum.METER)
print(f"{length_mm} mm = {length_m} m")  # 1000 mm = 1.0 m
```

### Getting Unit Dimension

```python
def get_unit_dimension(unit):
    """Get the physical dimension of a unit."""
    length_units = {XmiUnitEnum.METER, XmiUnitEnum.CENTIMETER, XmiUnitEnum.MILLIMETER}
    area_units = {XmiUnitEnum.METER2, XmiUnitEnum.MILLIMETER2}
    volume_units = {XmiUnitEnum.METER3, XmiUnitEnum.MILLIMETER3}
    inertia_units = {XmiUnitEnum.METER4, XmiUnitEnum.MILLIMETER4}
    time_units = {XmiUnitEnum.SECOND}

    if unit in length_units:
        return "Length"
    elif unit in area_units:
        return "Area"
    elif unit in volume_units:
        return "Volume"
    elif unit in inertia_units:
        return "Second Moment of Area"
    elif unit in time_units:
        return "Time"
    else:
        return "Unknown"

# Usage
for unit in XmiUnitEnum:
    dimension = get_unit_dimension(unit)
    print(f"{unit.value}: {dimension}")
```

### Unit Validation

```python
def validate_unit_for_property(value, unit, property_type):
    """Validate that unit is appropriate for a property type."""
    valid_units = {
        "coordinate": {XmiUnitEnum.METER, XmiUnitEnum.CENTIMETER, XmiUnitEnum.MILLIMETER},
        "area": {XmiUnitEnum.METER2, XmiUnitEnum.MILLIMETER2},
        "volume": {XmiUnitEnum.METER3, XmiUnitEnum.MILLIMETER3},
        "inertia": {XmiUnitEnum.METER4, XmiUnitEnum.MILLIMETER4},
        "time": {XmiUnitEnum.SECOND},
    }

    if property_type not in valid_units:
        return False, f"Unknown property type: {property_type}"

    if unit not in valid_units[property_type]:
        return False, f"Invalid unit {unit.value} for {property_type}"

    return True, None

# Usage
is_valid, error = validate_unit_for_property(1000, XmiUnitEnum.MILLIMETER, "coordinate")
print(f"Valid: {is_valid}")  # True

is_valid, error = validate_unit_for_property(100, XmiUnitEnum.METER3, "coordinate")
print(f"Valid: {is_valid}, Error: {error}")  # False, Invalid unit m^3 for coordinate
```

### Model Unit System

```python
def get_model_units(xmi_model):
    """Extract the unit system used in the model."""
    from xmi.v2.models.entities.xmi_structural_unit import XmiStructuralUnit

    units = [
        entity for entity in xmi_model.entities
        if isinstance(entity, XmiStructuralUnit)
    ]

    unit_system = {}
    for unit_entity in units:
        unit_system[unit_entity.name] = unit_entity.unit

    return unit_system

# Usage
units = get_model_units(xmi_model)
for name, unit in units.items():
    print(f"{name}: {unit.value}")
# Output:
# LengthUnit: mm
# AreaUnit: mm^2
# InertiaUnit: mm^4
```

## Integration with XMI Schema

### XMI JSON Format

```json
{
  "StructuralUnit": [
    {
      "Name": "LengthUnit",
      "Unit": "mm"
    },
    {
      "Name": "AreaUnit",
      "Unit": "mm^2"
    },
    {
      "Name": "InertiaUnit",
      "Unit": "mm^4"
    }
  ]
}
```

### Usage in XmiStructuralUnit

```python
class XmiStructuralUnit(XmiBaseEntity):
    unit: XmiUnitEnum = Field(..., alias="Unit")
```

## Notes

### Common Unit Combinations

Most structural models use one of these combinations:
- **mm system**: mm, mm², mm³, mm⁴ (most common for building structures)
- **m system**: m, m², m³, m⁴ (common for large-scale structures)
- **Mixed**: m for coordinates, mm for sections (less common, requires care)

### Unit Consistency

For accurate calculations, maintain consistency:
- Use the same length unit system throughout (all mm or all m)
- Ensure force units match length units (kN with mm, or N with m)
- Be careful with density units (kg/m³ or t/mm³)

### Superscript in String Values

The enum values use `^` for exponents (e.g., "mm^2") rather than superscript characters for compatibility.

## Related Classes

### Entity Classes
- [`XmiStructuralUnit`](../entities/XmiStructuralUnit.md) - Uses this enum
- [`XmiCrossSection`](../entities/XmiCrossSection.md) - Section properties have units

### Base Classes
- [`XmiBaseEnum`](../bases/XmiBaseEnum.md)

## See Also

- [XMI Schema Specification](https://github.com/IfcOpenShell/xmi-schema)
