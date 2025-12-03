# XmiShapeEnum

## Overview

`XmiShapeEnum` is an enumeration that defines the cross-sectional shapes available for structural members in the XMI schema. This enum is used to specify the geometric profile of beams, columns, and other structural elements.

## Class Hierarchy

- **Parent**: [`XmiBaseEnum`](../bases/XmiBaseEnum.md)
- **Grandparent**: `str`, `Enum`
- **Version**: v2 (Pydantic-based implementation)
- **Module**: `src/xmi/v2/models/enums/xmi_shape_enum.py`

## Enum Values

| Member Name | Value | Description | Typical Use |
|-------------|-------|-------------|-------------|
| `RECTANGULAR` | "Rectangular" | Solid rectangular cross-section | Concrete beams, columns |
| `CIRCULAR` | "Circular" | Solid circular cross-section | Concrete columns, piles |
| `L_SHAPE` | "L Shape" | L-shaped (angle) cross-section | Steel angles, connections |
| `T_SHAPE` | "T Shape" | T-shaped cross-section | Steel T-sections, beams |
| `C_SHAPE` | "C Shape" | C-shaped (channel) cross-section | Steel channels |
| `I_SHAPE` | "I Shape" | I-shaped (wide flange) cross-section | Steel I-beams, columns |
| `SQUARE_HOLLOW` | "Square Hollow" | Hollow square cross-section | Steel hollow sections |
| `RECTANGULAR_HOLLOW` | "Rectangular Hollow" | Hollow rectangular cross-section | Steel hollow sections |
| `OTHERS` | "Others" | Custom or non-standard shapes | Custom profiles |
| `UNKNOWN` | "Unknown" | Shape not specified or unknown | Default/fallback |

## Purpose and Functionality

### Cross-Section Shape Definition

The shape enum defines the geometric profile of structural cross-sections, which determines:
- The section's geometric properties (area, moment of inertia)
- Material distribution within the cross-section
- Structural behavior and capacity
- Visualization and rendering

### Common Shape Categories

1. **Solid Shapes**: RECTANGULAR, CIRCULAR
   - Typical for concrete members
   - Full cross-section is material

2. **Steel Sections**: I_SHAPE, T_SHAPE, C_SHAPE, L_SHAPE
   - Typical for steel members
   - Optimized for bending resistance

3. **Hollow Sections**: SQUARE_HOLLOW, RECTANGULAR_HOLLOW
   - Efficient use of material
   - Good torsional resistance

4. **Special**: OTHERS, UNKNOWN
   - Custom shapes
   - Fallback values

## Usage Examples

### Basic Usage

```python
from xmi.v2.models.enums.xmi_shape_enum import XmiShapeEnum

# Direct access
shape = XmiShapeEnum.RECTANGULAR
print(shape.value)  # "Rectangular"

# Case-insensitive lookup
shape = XmiShapeEnum("rectangular")  # Returns XmiShapeEnum.RECTANGULAR
shape = XmiShapeEnum("i shape")  # Returns XmiShapeEnum.I_SHAPE

# From name
shape = XmiShapeEnum.from_name_get_enum("rectangular")  # XmiShapeEnum.RECTANGULAR

# From attribute
shape = XmiShapeEnum.from_attribute_get_enum("Rectangular")  # XmiShapeEnum.RECTANGULAR
```

### Creating Cross-Section with Shape

```python
from xmi.v2.models.entities.xmi_structural_cross_section import XmiStructuralCrossSection
from xmi.v2.models.enums.xmi_shape_enum import XmiShapeEnum

# Rectangular concrete beam
rect_section = XmiStructuralCrossSection(
    name="RECT_300x500",
    shape=XmiShapeEnum.RECTANGULAR,
    width=300,  # mm
    height=500  # mm
)

# Circular concrete column
circ_section = XmiStructuralCrossSection(
    name="CIRC_400",
    shape=XmiShapeEnum.CIRCULAR,
    diameter=400  # mm
)

# Steel I-beam
i_section = XmiStructuralCrossSection(
    name="W12x26",
    shape=XmiShapeEnum.I_SHAPE,
    # ... I-section dimensions
)
```

### Parsing Shape from XMI

```python
def parse_cross_section_shape(shape_str: str) -> XmiShapeEnum:
    """Parse cross-section shape from XMI string."""
    try:
        # Try case-insensitive lookup
        return XmiShapeEnum(shape_str.lower())
    except (ValueError, KeyError):
        # Default to UNKNOWN if not recognized
        return XmiShapeEnum.UNKNOWN

# Usage
shape = parse_cross_section_shape("Rectangular")  # XmiShapeEnum.RECTANGULAR
shape = parse_cross_section_shape("I Shape")      # XmiShapeEnum.I_SHAPE
shape = parse_cross_section_shape("invalid")      # XmiShapeEnum.UNKNOWN
```

### Filtering Sections by Shape

```python
def get_sections_by_shape(xmi_model, shape: XmiShapeEnum):
    """Get all cross-sections of a specific shape."""
    from xmi.v2.models.entities.xmi_structural_cross_section import XmiStructuralCrossSection

    sections = [
        entity for entity in xmi_model.entities
        if isinstance(entity, XmiStructuralCrossSection) and entity.shape == shape
    ]
    return sections

# Usage
rect_sections = get_sections_by_shape(xmi_model, XmiShapeEnum.RECTANGULAR)
i_sections = get_sections_by_shape(xmi_model, XmiShapeEnum.I_SHAPE)

print(f"Found {len(rect_sections)} rectangular sections")
print(f"Found {len(i_sections)} I-sections")
```

### Shape Category Classification

```python
def classify_shape(shape: XmiShapeEnum) -> str:
    """Classify shape into broad categories."""
    solid_shapes = {XmiShapeEnum.RECTANGULAR, XmiShapeEnum.CIRCULAR}
    steel_shapes = {XmiShapeEnum.I_SHAPE, XmiShapeEnum.T_SHAPE,
                   XmiShapeEnum.C_SHAPE, XmiShapeEnum.L_SHAPE}
    hollow_shapes = {XmiShapeEnum.SQUARE_HOLLOW, XmiShapeEnum.RECTANGULAR_HOLLOW}

    if shape in solid_shapes:
        return "Solid"
    elif shape in steel_shapes:
        return "Steel Section"
    elif shape in hollow_shapes:
        return "Hollow Section"
    else:
        return "Other"

# Usage
for shape in XmiShapeEnum:
    category = classify_shape(shape)
    print(f"{shape.value}: {category}")
```

### Shape Statistics

```python
def analyze_section_shapes(xmi_model):
    """Analyze distribution of cross-section shapes."""
    from collections import Counter
    from xmi.v2.models.entities.xmi_structural_cross_section import XmiStructuralCrossSection

    sections = [
        entity for entity in xmi_model.entities
        if isinstance(entity, XmiStructuralCrossSection)
    ]

    shape_counts = Counter(sec.shape for sec in sections)

    print(f"Total cross-sections: {len(sections)}")
    for shape, count in shape_counts.most_common():
        percentage = (count / len(sections)) * 100
        print(f"{shape.value}: {count} ({percentage:.1f}%)")

# Usage
analyze_section_shapes(xmi_model)
# Output:
# Total cross-sections: 50
# Rectangular: 25 (50.0%)
# I Shape: 15 (30.0%)
# Circular: 10 (20.0%)
```

### Material-Shape Combinations

```python
def get_common_combinations(xmi_model):
    """Get common material-shape combinations."""
    from collections import Counter
    from xmi.v2.models.entities.xmi_structural_cross_section import XmiStructuralCrossSection

    sections = [
        entity for entity in xmi_model.entities
        if isinstance(entity, XmiStructuralCrossSection)
    ]

    # Get material for each section (via relationship)
    combinations = []
    for section in sections:
        # Find material relationship
        mat_rels = xmi_model.find_relationships_by_source(section)
        for rel in mat_rels:
            if rel.name == "HasStructuralMaterial":
                material = rel.target
                combo = (material.material_type.value, section.shape.value)
                combinations.append(combo)

    combo_counts = Counter(combinations)

    print("Common material-shape combinations:")
    for (material, shape), count in combo_counts.most_common():
        print(f"  {material} + {shape}: {count}")

# Usage
get_common_combinations(xmi_model)
# Output:
# Common material-shape combinations:
#   Concrete + Rectangular: 20
#   Steel + I Shape: 15
#   Concrete + Circular: 10
```

### Validation by Shape

```python
def validate_section_dimensions(section):
    """Validate cross-section dimensions based on shape."""
    errors = []

    if section.shape == XmiShapeEnum.RECTANGULAR:
        if not section.width or not section.height:
            errors.append("Rectangular section requires width and height")

    elif section.shape == XmiShapeEnum.CIRCULAR:
        if not section.diameter:
            errors.append("Circular section requires diameter")

    elif section.shape == XmiShapeEnum.I_SHAPE:
        required = ["flange_width", "flange_thickness", "web_height", "web_thickness"]
        missing = [f for f in required if not getattr(section, f, None)]
        if missing:
            errors.append(f"I-section missing: {', '.join(missing)}")

    elif section.shape in {XmiShapeEnum.SQUARE_HOLLOW, XmiShapeEnum.RECTANGULAR_HOLLOW}:
        if not section.wall_thickness:
            errors.append(f"{section.shape.value} requires wall_thickness")

    return errors

# Usage
section = XmiStructuralCrossSection(
    name="RECT_300x500",
    shape=XmiShapeEnum.RECTANGULAR,
    width=300
    # Missing height!
)

errors = validate_section_dimensions(section)
if errors:
    print("Validation errors:")
    for error in errors:
        print(f"  - {error}")
```

### Shape-Specific Property Calculation

```python
def calculate_area(section):
    """Calculate cross-section area based on shape."""
    import math

    if section.shape == XmiShapeEnum.RECTANGULAR:
        return section.width * section.height

    elif section.shape == XmiShapeEnum.CIRCULAR:
        radius = section.diameter / 2
        return math.pi * radius ** 2

    elif section.shape == XmiShapeEnum.SQUARE_HOLLOW:
        outer_area = section.width ** 2
        inner_width = section.width - 2 * section.wall_thickness
        inner_area = inner_width ** 2
        return outer_area - inner_area

    elif section.shape == XmiShapeEnum.RECTANGULAR_HOLLOW:
        outer_area = section.width * section.height
        inner_width = section.width - 2 * section.wall_thickness
        inner_height = section.height - 2 * section.wall_thickness
        inner_area = inner_width * inner_height
        return outer_area - inner_area

    else:
        # For complex shapes, area might be provided directly
        return section.area if hasattr(section, 'area') else None

# Usage
rect_section = XmiStructuralCrossSection(
    shape=XmiShapeEnum.RECTANGULAR,
    width=300,
    height=500
)
area = calculate_area(rect_section)
print(f"Area: {area} mm²")  # 150000 mm²
```

## Integration with XMI Schema

### XMI JSON Format

Cross-section shapes appear in XMI dictionaries:

```json
{
  "StructuralCrossSection": [
    {
      "Name": "RECT_300x500",
      "Shape": "Rectangular",
      "Width": 300,
      "Height": 500
    },
    {
      "Name": "W12x26",
      "Shape": "I Shape",
      "FlangeWidth": 165,
      "FlangeThickness": 10,
      "WebHeight": 300,
      "WebThickness": 6
    },
    {
      "Name": "CIRC_400",
      "Shape": "Circular",
      "Diameter": 400
    }
  ]
}
```

### Usage in XmiStructuralCrossSection

```python
class XmiStructuralCrossSection(XmiBaseEntity):
    shape: XmiShapeEnum = Field(..., alias="Shape")
    # ... other fields
```

## Notes

### Common Shapes by Material

- **Concrete**: Primarily RECTANGULAR and CIRCULAR
- **Steel**: I_SHAPE, C_SHAPE, T_SHAPE, L_SHAPE, hollow sections
- **Timber**: Primarily RECTANGULAR
- **Composite**: Various shapes depending on design

### Shape Complexity

Shapes range from simple (RECTANGULAR, CIRCULAR) to complex (I_SHAPE with multiple dimensions). More complex shapes require more dimensional parameters.

### Custom Shapes

Use `OTHERS` for:
- Custom fabricated sections
- Proprietary shapes
- Complex composite sections
- Non-standard profiles

### UNKNOWN Usage

Use `UNKNOWN` when:
- Shape information is unavailable
- Parsing from incomplete data
- Placeholder during model development

## Related Classes

### Entity Classes
- [`XmiStructuralCrossSection`](../entities/XmiStructuralCrossSection.md) - Uses this enum for shape field
- [`XmiStructuralCurveMember`](../entities/XmiStructuralCurveMember.md) - References cross-sections with shapes

### Base Classes
- [`XmiBaseEnum`](../bases/XmiBaseEnum.md) - Parent enum class

### Other Enums
- [`XmiStructuralMaterialTypeEnum`](./XmiStructuralMaterialTypeEnum.md) - Material types often paired with shapes

### Manager Classes
- [`XmiManager`](../xmi_model/XmiManager.md) - Parses shape from XMI data

## See Also

- [XMI Cross-Section Documentation](../entities/XmiStructuralCrossSection.md)
- [XMI Schema Specification](https://github.com/IfcOpenShell/xmi-schema)
