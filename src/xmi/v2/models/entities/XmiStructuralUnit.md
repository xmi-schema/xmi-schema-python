# XmiStructuralUnit

## Overview

`XmiStructuralUnit` defines the physical units of measurement for specific attributes of XMI entities. It acts as metadata that specifies what unit system is being used for various properties throughout the model, such as lengths in millimeters, forces in kN, or periods in seconds. This allows different software tools to correctly interpret numerical values when exchanging structural data.

## Class Hierarchy

- **Parent**: `XmiBaseEntity`
- **Version**: v2 (Pydantic-based implementation)
- **Module**: `src/xmi/v2/models/entities/xmi_structural_unit.py`

## Properties

### Required Properties

| Property | Type | Description | Validation |
|----------|------|-------------|------------|
| `entity` | `str` | The entity type whose attribute unit is being specified | Must be string |
| `attribute` | `str` | The specific attribute name within the entity | Must be string |
| `unit` | `XmiUnitEnum` | The unit of measurement for this attribute | Must be valid enum value |

### Inherited Properties

Inherits from `XmiBaseEntity`:
- `name`: Name/identifier of the unit definition
- `id`: Unique identifier (GUID)
- `ifcguid`: IFC GUID for interoperability
- `entity_type`: Set to "XmiStructuralUnit"
- `description`: Optional description

## Enums

### XmiUnitEnum

Defines supported units of measurement:

#### Length Units
- `METER` = "m" - Meters
- `CENTIMETER` = "cm" - Centimeters
- `MILLIMETER` = "mm" - Millimeters (common for structural models)

#### Area Units
- `METER2` = "m^2" - Square meters
- `MILLIMETER2` = "mm^2" - Square millimeters

#### Volume Units
- `METER3` = "m^3" - Cubic meters
- `MILLIMETER3` = "mm^3" - Cubic millimeters

#### Second Moment of Area (Inertia) Units
- `METER4` = "m^4" - Meters to the fourth power
- `MILLIMETER4` = "mm^4" - Millimeters to the fourth power (common for cross-section properties)

#### Time Units
- `SECOND` = "sec" - Seconds (for modal periods, time history analysis)

## Relationships

`XmiStructuralUnit` typically does not have explicit relationships to other entities. It serves as standalone metadata that describes the unit system used throughout the model.

## Purpose and Use Cases

### Unit System Documentation

`XmiStructuralUnit` entries document the units used for specific attributes, enabling:

1. **Interoperability**: Different software can correctly interpret values
2. **Validation**: Verify that expected units match actual units
3. **Conversion**: Facilitate unit conversion when needed
4. **Clarity**: Remove ambiguity about measurement units

### Common Entity-Attribute Pairs

Typical unit specifications include:

- **StructuralMaterial attributes**:
  - `ThermalCoefficient` → "1/C"
  - `Density` → "kg/m^3"
  - `ElasticModulus` → "MPa" or "GPa"

- **StructuralCrossSection attributes**:
  - `SectionArea` → "mm^2"
  - `MomentOfInertia` → "mm^4"
  - `TorsionalConstant` → "mm^4"

- **StructuralModel attributes**:
  - `GlobalCoordinateSystem` → "" (no unit)

- **StructuralModelAnalysis attributes**:
  - `ModalPeriod` → "sec"
  - `Displacement` → "mm"
  - `Drift` → "%" or ratio

- **StructuralPointConnection attributes**:
  - `Coordinate` → "mm" (X, Y, Z coordinates)

- **StructuralCurveMember attributes**:
  - `Length` → "mm"
  - `NodeOffsetBegin` / `NodeOffsetEnd` → "mm"

## Usage Examples

### Creating Unit Definitions Directly

```python
from xmi.v2.models.entities.xmi_structural_unit import XmiStructuralUnit
from xmi.v2.models.enums.xmi_unit_enum import XmiUnitEnum

# Define unit for material thermal coefficient
thermal_unit = XmiStructuralUnit(
    entity="StructuralMaterial",
    attribute="ThermalCoefficient",
    unit=XmiUnitEnum.from_attribute_get_enum("1/C"),
    name="UNIT_THERMAL"
)

# Define unit for cross-section area
area_unit = XmiStructuralUnit(
    entity="StructuralCrossSection",
    attribute="SectionArea",
    unit=XmiUnitEnum.MILLIMETER2,
    name="UNIT_AREA"
)

# Define unit for modal period
period_unit = XmiStructuralUnit(
    entity="StructuralModelAnalysis",
    attribute="ModalPeriod",
    unit=XmiUnitEnum.SECOND,
    name="UNIT_PERIOD"
)

print(f"Thermal coefficient unit: {thermal_unit.unit.value}")
# Output: Thermal coefficient unit: 1/C

print(f"Section area unit: {area_unit.unit.value}")
# Output: Section area unit: mm^2
```

### Loading from Dictionary (XMI Format)

```python
from xmi.v2.models.entities.xmi_structural_unit import XmiStructuralUnit

# Dictionary format from XMI JSON
unit_dict = {
    "Entity": "StructuralModelAnalysis",
    "Attribute": "ModalPeriod",
    "Unit": "sec"
}

# Parse using from_dict
unit, errors = XmiStructuralUnit.from_dict(unit_dict)

if unit and not errors:
    print(f"Entity: {unit.entity}")
    print(f"Attribute: {unit.attribute}")
    print(f"Unit: {unit.unit.value}")
    # Output:
    # Entity: StructuralModelAnalysis
    # Attribute: ModalPeriod
    # Unit: sec
else:
    print(f"Errors: {errors}")
```

### Common Patterns

#### Building Complete Unit Specification

```python
# Create comprehensive unit definitions for a structural model
unit_definitions = [
    # Coordinate units
    XmiStructuralUnit(
        entity="StructuralPointConnection",
        attribute="Coordinate",
        unit=XmiUnitEnum.MILLIMETER
    ),

    # Material property units
    XmiStructuralUnit(
        entity="StructuralMaterial",
        attribute="Density",
        unit=XmiUnitEnum.from_attribute_get_enum("kg/m^3")
    ),

    # Cross-section property units
    XmiStructuralUnit(
        entity="StructuralCrossSection",
        attribute="MomentOfInertia",
        unit=XmiUnitEnum.MILLIMETER4
    ),

    # Analysis result units
    XmiStructuralUnit(
        entity="StructuralModelAnalysis",
        attribute="Displacement",
        unit=XmiUnitEnum.MILLIMETER
    )
]

for unit_def in unit_definitions:
    print(f"{unit_def.entity}.{unit_def.attribute}: {unit_def.unit.value}")
```

#### Querying Units in XmiModel

```python
from xmi.v2.models.xmi_model.xmi_manager import XmiManager
from xmi.v2.models.entities.xmi_structural_unit import XmiStructuralUnit

# Load XMI data
xmi_manager = XmiManager()
xmi_model = xmi_manager.read_xmi_dict(xmi_dict)

# Find all unit definitions
units = [
    entity for entity in xmi_model.entities
    if isinstance(entity, XmiStructuralUnit)
]

print(f"Total unit definitions: {len(units)}")

# Group units by entity
from collections import defaultdict
units_by_entity = defaultdict(list)

for unit in units:
    units_by_entity[unit.entity].append(unit)

for entity_name, entity_units in units_by_entity.items():
    print(f"\n{entity_name}:")
    for unit in entity_units:
        print(f"  {unit.attribute}: {unit.unit.value}")
```

#### Finding Unit for Specific Attribute

```python
def find_unit_for_attribute(xmi_model, entity_name: str, attribute_name: str):
    """Find the unit specification for a given entity and attribute."""
    units = [
        entity for entity in xmi_model.entities
        if isinstance(entity, XmiStructuralUnit)
    ]

    for unit in units:
        if unit.entity == entity_name and unit.attribute == attribute_name:
            return unit.unit

    return None

# Example usage
modal_period_unit = find_unit_for_attribute(
    xmi_model,
    "StructuralModelAnalysis",
    "ModalPeriod"
)

if modal_period_unit:
    print(f"Modal period is measured in: {modal_period_unit.value}")
    # Output: Modal period is measured in: sec
else:
    print("No unit definition found for modal period")
```

#### Validating Expected Units

```python
def validate_unit(xmi_model, entity: str, attribute: str, expected_unit: XmiUnitEnum) -> bool:
    """Validate that an attribute has the expected unit."""
    actual_unit = find_unit_for_attribute(xmi_model, entity, attribute)

    if actual_unit is None:
        print(f"Warning: No unit defined for {entity}.{attribute}")
        return False

    if actual_unit != expected_unit:
        print(f"Error: {entity}.{attribute} has unit {actual_unit.value}, "
              f"expected {expected_unit.value}")
        return False

    return True

# Validate coordinate units are in millimeters
is_valid = validate_unit(
    xmi_model,
    "StructuralPointConnection",
    "Coordinate",
    XmiUnitEnum.MILLIMETER
)
```

#### Unit Conversion Helper

```python
class UnitConverter:
    """Helper class for converting between different unit systems."""

    # Conversion factors to meters
    LENGTH_TO_METERS = {
        XmiUnitEnum.METER: 1.0,
        XmiUnitEnum.CENTIMETER: 0.01,
        XmiUnitEnum.MILLIMETER: 0.001
    }

    @classmethod
    def convert_length(cls, value: float, from_unit: XmiUnitEnum, to_unit: XmiUnitEnum) -> float:
        """Convert length between different units."""
        if from_unit not in cls.LENGTH_TO_METERS or to_unit not in cls.LENGTH_TO_METERS:
            raise ValueError("Unsupported length unit")

        # Convert to meters, then to target unit
        meters = value * cls.LENGTH_TO_METERS[from_unit]
        return meters / cls.LENGTH_TO_METERS[to_unit]

# Example: Convert 1000mm to meters
result = UnitConverter.convert_length(
    1000.0,
    XmiUnitEnum.MILLIMETER,
    XmiUnitEnum.METER
)
print(f"1000mm = {result}m")
# Output: 1000mm = 1.0m
```

## Validation Rules

### Type Validation

- `entity` must be a string (entity type name)
- `attribute` must be a string (attribute name)
- `unit` must be a valid `XmiUnitEnum` value

### Required Fields

All three fields are required:
```python
# Valid
unit = XmiStructuralUnit(
    entity="StructuralMaterial",
    attribute="Density",
    unit=XmiUnitEnum.from_attribute_get_enum("kg/m^3")
)

# Invalid - will raise validation error
# unit = XmiStructuralUnit(entity="StructuralMaterial")  # Missing attribute and unit
```

### Unit Consistency

While not enforced by validation, ensure consistency:
- Use the same unit system throughout a model (typically all SI or all imperial)
- Match units to attribute types (e.g., don't use time units for length attributes)

## Integration with XMI Schema

### XMI Input Format

`StructuralUnit` entries are typically found in the top-level XMI JSON:

```json
{
  "StructuralUnit": [
    {
      "Entity": "StructuralModel",
      "Attribute": "GlobalCoordinateSystem",
      "Unit": ""
    },
    {
      "Entity": "StructuralModelAnalysis",
      "Attribute": "ModalPeriod",
      "Unit": "sec"
    },
    {
      "Entity": "StructuralMaterial",
      "Attribute": "ThermalCoefficient",
      "Unit": "1/C"
    },
    {
      "Entity": "StructuralCrossSection",
      "Attribute": "MomentOfInertia",
      "Unit": "mm^4"
    }
  ],
  "StructuralMaterial": [...],
  "StructuralCrossSection": [...]
}
```

### Parsing Order

`StructuralUnit` entries are typically parsed early in the process, as they provide metadata needed to interpret other entities' attribute values.

### Empty Units

Some attributes may have empty units ("") when:
- The attribute is dimensionless
- The attribute is a name or identifier rather than a measurement
- The attribute uses a compound unit not in the enum

## Notes

### Version Differences (v1 vs v2)

**v2 Characteristics:**
- Uses Pydantic for automatic validation
- Field aliases support both PascalCase and snake_case
- Type hints improve IDE support
- Cleaner validation with decorators

**v1 Characteristics:**
- Uses `__slots__` for memory efficiency
- Manual property validation
- Explicit parsing logic

### Unit System Recommendations

For structural engineering models, commonly use:
- **Lengths**: millimeters (mm) for coordinates and dimensions
- **Areas**: mm² for cross-section areas
- **Inertias**: mm⁴ for section properties
- **Forces**: kN (kilonewtons)
- **Stresses**: MPa (megapascals)
- **Time**: seconds for dynamic analysis

### Extending Unit Enum

If your application requires units not in `XmiUnitEnum`, you can:
1. Add new values to the enum definition
2. Use the `from_attribute_get_enum()` method for string-based unit values
3. Store custom units as strings if enum extension is not possible

### Performance Considerations

- Unit definitions are lightweight metadata objects
- Typically a model has 5-20 unit definitions
- Units can be cached in a dictionary for fast lookup by entity/attribute pair

### Common Pitfalls

1. **Unit Mismatch**: Ensure values and units match (e.g., if coordinates are in mm, specify MILLIMETER)
2. **Missing Units**: Always define units for measurable attributes
3. **Inconsistent Systems**: Mixing SI and imperial units can cause confusion
4. **Custom Units**: Units not in the enum (like "kN", "MPa") may need special handling

## Related Classes

### Entity Classes
- [`XmiStructuralMaterial`](./XmiStructuralMaterial.md) - Material definitions with measurable properties
- [`XmiCrossSection`](./XmiCrossSection.md) - Cross-sections with area and inertia properties
- [`XmiStructuralPointConnection`](./XmiStructuralPointConnection.md) - Nodes with coordinates
- [`XmiStructuralStorey`](./XmiStructuralStorey.md) - Storeys with elevation values

### Enum Classes
- `XmiUnitEnum` - Enumeration of supported unit types

### Base Classes
- `XmiBaseEntity` - Base entity class
- `XmiBaseEnum` - Base enum class

### Manager Classes
- [`XmiManager`](../xmi_model/XmiManager.md) - Handles unit parsing from XMI dictionaries
- [`XmiModel`](../xmi_model/XmiModel.md) - Container for unit definitions and other entities
