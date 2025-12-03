# XmiCrossSection

## Overview

`XmiCrossSection` represents a structural cross-section profile in the XMI schema. Cross-sections define the geometric shape and sectional properties of structural members like beams, columns, and braces. This class stores both the basic shape definition (shape type and parameters) and calculated sectional properties (area, moments of inertia, moduli, etc.).

Cross-sections are fundamental to structural analysis as they:
- **Define member geometry**: Shape and dimensions of structural elements
- **Provide sectional properties**: Area, moments of inertia, moduli for structural calculations
- **Link to materials**: Via `XmiHasStructuralMaterial` relationships
- **Support multiple shape types**: Rectangular, circular, I-shape, hollow sections, etc.

## Class Hierarchy

- **Parent**: `XmiBaseEntity`
- **Module**: `xmi.v2.models.entities.xmi_structural_cross_section`
- **Implementation**: Pydantic model with validation

## Properties

### Required Properties

| Property | Type | Description | Validation |
|----------|------|-------------|------------|
| `shape` | `XmiShapeEnum` | Cross-section shape type (Rectangular, I-Shape, etc.) | Must be valid enum value |
| `parameters` | `Tuple[Union[float, int], ...]` | Shape-specific dimensional parameters | All values must be non-negative numbers |

### Optional Sectional Properties

| Property | Type | Default | Description | Units (typical) |
|----------|------|---------|-------------|-----------------|
| `area` | `float` | `None` | Cross-sectional area | mm² or m² |
| `second_moment_of_area_x_axis` | `float` | `None` | Moment of inertia about X-axis (Ix) | mm⁴ or m⁴ |
| `second_moment_of_area_y_axis` | `float` | `None` | Moment of inertia about Y-axis (Iy) | mm⁴ or m⁴ |
| `radius_of_gyration_x_axis` | `float` | `None` | Radius of gyration about X-axis (rx) | mm or m |
| `radius_of_gyration_y_axis` | `float` | `None` | Radius of gyration about Y-axis (ry) | mm or m |
| `elastic_modulus_x_axis` | `float` | `None` | Elastic section modulus about X-axis (Sx) | mm³ or m³ |
| `elastic_modulus_y_axis` | `float` | `None` | Elastic section modulus about Y-axis (Sy) | mm³ or m³ |
| `plastic_modulus_x_axis` | `float` | `None` | Plastic section modulus about X-axis (Zx) | mm³ or m³ |
| `plastic_modulus_y_axis` | `float` | `None` | Plastic section modulus about Y-axis (Zy) | mm³ or m³ |
| `torsional_constant` | `float` | `None` | Torsional constant (J) | mm⁴ or m⁴ |

### Inherited Properties (from XmiBaseEntity)

| Property | Type | Default | Description | Required |
|----------|------|---------|-------------|----------|
| `id` | `str` | Auto-generated | Unique identifier | Yes (via from_dict) |
| `name` | `str` | `None` | Human-readable name | Yes (via from_dict) |
| `description` | `str` | `None` | Detailed description | No |
| `ifcguid` | `str` | `None` | IFC GUID for interoperability | No |
| `native_id` | `str` | `None` | Native ID from source application | No |
| `entity_type` | `str` | `"XmiCrossSection"` | Entity type identifier | No |

## Relationships

`XmiCrossSection` participates in the following relationships:

- **XmiHasStructuralMaterial**: Links cross-sections to materials (source: cross-section, target: material)
- **XmiHasCrossSection**: Referenced by `XmiStructuralCurveMember` to define member cross-section (source: member, target: cross-section)

## Shape Types and Parameters

### Available Shape Types (XmiShapeEnum)

| Shape Type | Enum Value | Parameter Count | Parameter Meaning |
|------------|------------|-----------------|-------------------|
| `RECTANGULAR` | "Rectangular" | 2 | [width, height] |
| `CIRCULAR` | "Circular" | 1 | [diameter] |
| `I_SHAPE` | "I Shape" | 6+ | [width, height, web_thickness, flange_thickness, ...] |
| `SQUARE_HOLLOW` | "Square Hollow" | 2 | [outer_size, thickness] |
| `RECTANGULAR_HOLLOW` | "Rectangular Hollow" | 3 | [width, height, thickness] |
| `C_SHAPE` | "C Shape" | 5+ | [width, height, web_thickness, flange_thickness, ...] |
| `T_SHAPE` | "T Shape" | 4+ | [flange_width, total_height, web_thickness, flange_thickness] |
| `L_SHAPE` | "L Shape" | 3+ | [width, height, thickness] |
| `OTHERS` | "Others" | Variable | Application-specific |
| `UNKNOWN` | "Unknown" | Variable | Unknown or unspecified shape |

### Parameter Format

Parameters are stored as a tuple of numbers separated by semicolons in XMI format:
- **XMI format**: `"300;600;10;15"` (string with semicolons)
- **Python format**: `(300.0, 600.0, 10.0, 15.0)` (tuple of floats)

The `from_dict()` method automatically converts from string format to tuple format.

## Usage Examples

### Creating a Rectangular Cross-Section

```python
from xmi.v2.models.entities.xmi_structural_cross_section import XmiCrossSection
from xmi.v2.models.enums.xmi_shape_enum import XmiShapeEnum

# Create rectangular section: 300mm x 600mm
rect_section = XmiCrossSection(
    id="cs_rect_001",
    name="300x600 Beam",
    shape=XmiShapeEnum.RECTANGULAR,
    parameters=(300.0, 600.0),
    area=180000.0,  # mm²
    second_moment_of_area_x_axis=5400000000.0,  # mm⁴
    second_moment_of_area_y_axis=675000000.0,   # mm⁴
    description="Rectangular concrete beam section"
)

print(f"Section: {rect_section.name}")
print(f"Shape: {rect_section.shape.value}")
print(f"Dimensions: {rect_section.parameters[0]} x {rect_section.parameters[1]} mm")
print(f"Area: {rect_section.area} mm²")
```

### Loading from Dictionary (XMI Format)

```python
from xmi.v2.models.entities.xmi_structural_cross_section import XmiCrossSection

# Dictionary from XMI file
section_dict = {
    "ID": "b22bd84c-91fd-445b-a61a-54268be48999",
    "Name": "300 x 300mm Column",
    "Shape": "Rectangular",
    "Parameters": "300;300",  # String format with semicolons
    "Area": 90000.0,
    "SecondMomentOfAreaXAxis": 675000000.0,
    "SecondMomentOfAreaYAxis": 675000000.0,
    "RadiusOfGyrationXAxis": 86.6,
    "RadiusOfGyrationYAxis": 86.6
}

# Load and validate
section, errors = XmiCrossSection.from_dict(section_dict)

if section:
    print(f"Loaded: {section.name}")
    print(f"Parameters: {section.parameters}")  # Converted to tuple: (300.0, 300.0)
    print(f"Area: {section.area} mm²")
else:
    print(f"Errors: {errors}")
```

### Creating a Circular Section

```python
from xmi.v2.models.entities.xmi_structural_cross_section import XmiCrossSection
from xmi.v2.models.enums.xmi_shape_enum import XmiShapeEnum

# Create circular section: 500mm diameter
circular_section = XmiCrossSection(
    id="cs_circ_001",
    name="500mm Circular Column",
    shape=XmiShapeEnum.CIRCULAR,
    parameters=(500.0,),  # Single parameter: diameter
    area=196350.0,  # π * (250)²
    second_moment_of_area_x_axis=3068000000.0,  # π * (250)⁴ / 4
    second_moment_of_area_y_axis=3068000000.0,
    radius_of_gyration_x_axis=125.0,
    radius_of_gyration_y_axis=125.0
)

print(f"Section: {circular_section.name}")
print(f"Diameter: {circular_section.parameters[0]} mm")
```

### Creating an I-Shape (Steel Beam)

```python
from xmi.v2.models.entities.xmi_structural_cross_section import XmiCrossSection
from xmi.v2.models.enums.xmi_shape_enum import XmiShapeEnum

# Create I-beam: W-shape profile
# Parameters: [overall_width, overall_height, web_thickness, flange_thickness, fillet_radius, flange_width]
i_section = XmiCrossSection(
    id="cs_i_001",
    name="W24x76",
    shape=XmiShapeEnum.I_SHAPE,
    parameters=(228.6, 609.6, 11.2, 17.3, 12.7, 228.6),
    area=14500.0,  # mm²
    second_moment_of_area_x_axis=457000000.0,  # mm⁴
    second_moment_of_area_y_axis=22400000.0,
    elastic_modulus_x_axis=1500000.0,  # mm³
    elastic_modulus_y_axis=196000.0,
    plastic_modulus_x_axis=1690000.0,
    plastic_modulus_y_axis=301000.0,
    torsional_constant=372000.0
)

print(f"Section: {i_section.name}")
print(f"Depth: {i_section.parameters[1]} mm")
print(f"Plastic modulus Zx: {i_section.plastic_modulus_x_axis} mm³")
```

### Creating a Rectangular Hollow Section

```python
from xmi.v2.models.entities.xmi_structural_cross_section import XmiCrossSection
from xmi.v2.models.enums.xmi_shape_enum import XmiShapeEnum

# RHS: 200x100x8mm
rhs_section = XmiCrossSection(
    id="cs_rhs_001",
    name="RHS 200x100x8",
    shape=XmiShapeEnum.RECTANGULAR_HOLLOW,
    parameters=(200.0, 100.0, 8.0),  # width, height, thickness
    area=4352.0,  # mm²
    second_moment_of_area_x_axis=8500000.0,
    second_moment_of_area_y_axis=3200000.0,
    radius_of_gyration_x_axis=44.2,
    radius_of_gyration_y_axis=27.1
)

print(f"Section: {rhs_section.name}")
print(f"Dimensions: {rhs_section.parameters[0]}x{rhs_section.parameters[1]}x{rhs_section.parameters[2]} mm")
```

### Minimal Cross-Section (Required Fields Only)

```python
from xmi.v2.models.entities.xmi_structural_cross_section import XmiCrossSection
from xmi.v2.models.enums.xmi_shape_enum import XmiShapeEnum

# Minimum viable cross-section
minimal_section = XmiCrossSection(
    id="cs_min_001",
    name="Simple Section",
    shape=XmiShapeEnum.UNKNOWN,
    parameters=(300.0, 300.0)  # Just shape and parameters required
)

print(f"Section: {minimal_section.name}")
print(f"Has area defined? {minimal_section.area is not None}")  # False
```

### Handling Validation Errors

```python
from xmi.v2.models.entities.xmi_structural_cross_section import XmiCrossSection

# Missing required fields
invalid_dict = {
    "ID": "cs_invalid",
    "Name": "Invalid Section",
    "Area": 10000.0
    # Missing: Shape and Parameters
}

section, errors = XmiCrossSection.from_dict(invalid_dict)

if not section:
    print("Validation failed:")
    for error in errors:
        print(f"  - {error}")
    # Output:
    # - Missing 'shape'
```

### Negative Parameter Validation

```python
from xmi.v2.models.entities.xmi_structural_cross_section import XmiCrossSection
from xmi.v2.models.enums.xmi_shape_enum import XmiShapeEnum

try:
    # Negative parameters are not allowed
    invalid_section = XmiCrossSection(
        id="cs_neg",
        name="Invalid",
        shape=XmiShapeEnum.RECTANGULAR,
        parameters=(300.0, -600.0)  # Negative height!
    )
except ValueError as e:
    print(f"Validation error: {e}")
    # Output: Value cannot be smaller than 0
```

### Accessing Sectional Properties

```python
from xmi.v2.models.entities.xmi_structural_cross_section import XmiCrossSection
from xmi.v2.models.enums.xmi_shape_enum import XmiShapeEnum

section = XmiCrossSection(
    id="cs_props",
    name="Test Section",
    shape=XmiShapeEnum.RECTANGULAR,
    parameters=(300.0, 600.0),
    area=180000.0,
    second_moment_of_area_x_axis=5400000000.0,
    elastic_modulus_x_axis=18000000.0
)

# Access properties safely
print(f"Area: {section.area if section.area else 'Not defined'}")
print(f"Ix: {section.second_moment_of_area_x_axis if section.second_moment_of_area_x_axis else 'Not defined'}")

# Check if property is defined
has_plastic_modulus = section.plastic_modulus_x_axis is not None
print(f"Plastic modulus defined? {has_plastic_modulus}")  # False
```

### Using with XmiHasCrossSection Relationship

```python
from xmi.v2.models.entities.xmi_structural_cross_section import XmiCrossSection
from xmi.v2.models.entities.xmi_structural_curve_member import XmiStructuralCurveMember
from xmi.v2.models.relationships.xmi_has_structural_cross_section import XmiHasCrossSection
from xmi.v2.models.enums.xmi_shape_enum import XmiShapeEnum

# Create cross-section
section = XmiCrossSection(
    id="cs_001",
    name="300x600 Beam Section",
    shape=XmiShapeEnum.RECTANGULAR,
    parameters=(300.0, 600.0)
)

# Create structural member
beam = XmiStructuralCurveMember(
    id="beam_001",
    name="Main Beam",
    # ... other properties
)

# Create relationship linking beam to cross-section
relationship = XmiHasCrossSection(
    source=beam,
    target=section
)

print(f"Beam '{relationship.source.name}' uses section '{relationship.target.name}'")
print(f"Section shape: {relationship.target.shape.value}")
```

### Converting Parameters String to Tuple

```python
from xmi.v2.models.entities.xmi_structural_cross_section import XmiCrossSection

# Use the utility method for manual conversion
parameter_string = "400;800;12;20"
parameter_tuple = XmiCrossSection.convert_parameter_string_to_tuple(parameter_string)

print(f"String: '{parameter_string}'")
print(f"Tuple: {parameter_tuple}")
# Output: Tuple: (400.0, 800.0, 12.0, 20.0)

# This happens automatically in from_dict()
section_dict = {
    "ID": "cs_auto",
    "Name": "Auto Convert",
    "Shape": "I Shape",
    "Parameters": "400;800;12;20"  # String format
}

section, _ = XmiCrossSection.from_dict(section_dict)
print(f"Converted parameters: {section.parameters}")
# Output: (400.0, 800.0, 12.0, 20.0)
```

### Creating Multiple Standard Sections

```python
from xmi.v2.models.entities.xmi_structural_cross_section import XmiCrossSection
from xmi.v2.models.enums.xmi_shape_enum import XmiShapeEnum

# Build a library of standard sections
standard_sections = {
    "300x300_COL": XmiCrossSection(
        id="cs_std_col_300",
        name="300x300 Column",
        shape=XmiShapeEnum.RECTANGULAR,
        parameters=(300.0, 300.0),
        area=90000.0
    ),
    "300x600_BEAM": XmiCrossSection(
        id="cs_std_beam_300x600",
        name="300x600 Beam",
        shape=XmiShapeEnum.RECTANGULAR,
        parameters=(300.0, 600.0),
        area=180000.0
    ),
    "500_CIRC": XmiCrossSection(
        id="cs_std_circ_500",
        name="500mm Circular",
        shape=XmiShapeEnum.CIRCULAR,
        parameters=(500.0,),
        area=196350.0
    )
}

for key, section in standard_sections.items():
    print(f"{key}: {section.name} ({section.shape.value})")
```

## Validation Rules

### Type Validation

- `shape`: Must be a valid `XmiShapeEnum` instance
- `parameters`: Must be a list or tuple of numbers (int or float)
- All sectional properties: Must be float, int, or None

### Value Validation

- **Parameters**: All values must be non-negative (≥ 0)
- **Sectional properties**: All values must be non-negative if provided
- **Parameters count**: Must have at least 1 parameter

### Required Fields (via from_dict)

The `from_dict()` method enforces these requirements:
- `shape`: Must be provided (either "Shape" or "shape" key)
- `parameters`: Must be provided (either "Parameters" or "parameters" key)

Note: When creating instances directly via `__init__()`, both `shape` and `parameters` are required by Pydantic.

### Field Aliases

The class supports both PascalCase (external/XMI format) and snake_case (internal Python) naming:
- `Shape` ↔ `shape`
- `Parameters` ↔ `parameters`
- `Area` ↔ `area`
- `SecondMomentOfAreaXAxis` ↔ `second_moment_of_area_x_axis`
- `SecondMomentOfAreaYAxis` ↔ `second_moment_of_area_y_axis`
- `RadiusOfGyrationXAxis` ↔ `radius_of_gyration_x_axis`
- `RadiusOfGyrationYAxis` ↔ `radius_of_gyration_y_axis`
- `ElasticModulusXAxis` ↔ `elastic_modulus_x_axis`
- `ElasticModulusYAxis` ↔ `elastic_modulus_y_axis`
- `PlasticModulusXAxis` ↔ `plastic_modulus_x_axis`
- `PlasticModulusYAxis` ↔ `plastic_modulus_y_axis`
- `TorsionalConstant` ↔ `torsional_constant`

## Coordinate System and Axis Convention

### Local Axes

Cross-section properties are defined relative to the **local coordinate system** of the cross-section:
- **X-axis**: Typically the major axis (strong axis) - perpendicular to web for I-sections
- **Y-axis**: Typically the minor axis (weak axis) - parallel to web for I-sections
- **Origin**: Usually at the centroid of the cross-section

### Property Naming

| Property | Common Symbol | Axis | Description |
|----------|---------------|------|-------------|
| `second_moment_of_area_x_axis` | Ix | Major | Resistance to bending about X-axis |
| `second_moment_of_area_y_axis` | Iy | Minor | Resistance to bending about Y-axis |
| `radius_of_gyration_x_axis` | rx | Major | √(Ix/A) |
| `radius_of_gyration_y_axis` | ry | Minor | √(Iy/A) |
| `elastic_modulus_x_axis` | Sx or Wx | Major | Ix / y_max (elastic bending) |
| `elastic_modulus_y_axis` | Sy or Wy | Minor | Iy / x_max (elastic bending) |
| `plastic_modulus_x_axis` | Zx | Major | Plastic section modulus (plastic bending) |
| `plastic_modulus_y_axis` | Zy | Minor | Plastic section modulus (plastic bending) |
| `torsional_constant` | J | - | Resistance to torsion |

### Units

The class does not enforce specific units, but typical conventions are:
- **Parameters**: mm (millimeters)
- **Area**: mm²
- **Moments of inertia**: mm⁴
- **Radii of gyration**: mm
- **Elastic/Plastic moduli**: mm³
- **Torsional constant**: mm⁴

**Important**: Ensure unit consistency across your entire model.

## Common Use Cases

### 1. Loading Cross-Sections from XMI File

```python
import json
from xmi.v2.models.entities.xmi_structural_cross_section import XmiCrossSection

# Load from XMI JSON file
with open("cross_sections.json") as f:
    xmi_data = json.load(f)

sections = []
errors_log = []

for section_dict in xmi_data.get("StructuralCrossSection", []):
    section, errors = XmiCrossSection.from_dict(section_dict)
    if section:
        sections.append(section)
    else:
        errors_log.extend(errors)

print(f"Loaded {len(sections)} cross-sections")
if errors_log:
    print(f"Encountered {len(errors_log)} errors")
    for error in errors_log:
        print(f"  - {error}")
```

### 2. Creating a Cross-Section Library

```python
from xmi.v2.models.entities.xmi_structural_cross_section import XmiCrossSection
from xmi.v2.models.enums.xmi_shape_enum import XmiShapeEnum
from typing import Dict

class CrossSectionLibrary:
    def __init__(self):
        self.sections: Dict[str, XmiCrossSection] = {}

    def add_rectangular(self, name: str, width: float, height: float) -> XmiCrossSection:
        section = XmiCrossSection(
            id=f"cs_{name}",
            name=name,
            shape=XmiShapeEnum.RECTANGULAR,
            parameters=(width, height),
            area=width * height,
            second_moment_of_area_x_axis=(width * height**3) / 12,
            second_moment_of_area_y_axis=(height * width**3) / 12
        )
        self.sections[name] = section
        return section

    def add_circular(self, name: str, diameter: float) -> XmiCrossSection:
        import math
        radius = diameter / 2
        section = XmiCrossSection(
            id=f"cs_{name}",
            name=name,
            shape=XmiShapeEnum.CIRCULAR,
            parameters=(diameter,),
            area=math.pi * radius**2,
            second_moment_of_area_x_axis=(math.pi * radius**4) / 4,
            second_moment_of_area_y_axis=(math.pi * radius**4) / 4
        )
        self.sections[name] = section
        return section

    def get_section(self, name: str) -> XmiCrossSection:
        return self.sections.get(name)

# Usage
library = CrossSectionLibrary()
library.add_rectangular("300x600", 300.0, 600.0)
library.add_rectangular("400x800", 400.0, 800.0)
library.add_circular("500_CIRC", 500.0)

beam_section = library.get_section("300x600")
print(f"Beam section area: {beam_section.area} mm²")
```

### 3. Finding Sections by Shape Type

```python
from xmi.v2.models.entities.xmi_structural_cross_section import XmiCrossSection
from xmi.v2.models.enums.xmi_shape_enum import XmiShapeEnum
from typing import List

def filter_sections_by_shape(
    sections: List[XmiCrossSection],
    shape_type: XmiShapeEnum
) -> List[XmiCrossSection]:
    """Filter cross-sections by shape type"""
    return [s for s in sections if s.shape == shape_type]

# Usage
all_sections = [...]  # List of all cross-sections

rectangular_sections = filter_sections_by_shape(all_sections, XmiShapeEnum.RECTANGULAR)
i_sections = filter_sections_by_shape(all_sections, XmiShapeEnum.I_SHAPE)
circular_sections = filter_sections_by_shape(all_sections, XmiShapeEnum.CIRCULAR)

print(f"Rectangular: {len(rectangular_sections)}")
print(f"I-Shape: {len(i_sections)}")
print(f"Circular: {len(circular_sections)}")
```

## Notes

### Parameter Interpretation

The meaning of parameters varies by shape type and is **application-specific**. There is no universal standard for parameter ordering. Common conventions include:

- **Rectangular**: `[width, height]`
- **Circular**: `[diameter]`
- **I-Shape**: `[width, height, web_thickness, flange_thickness, ...]`
- **Hollow sections**: `[outer_dim1, outer_dim2, thickness]`

Always document or communicate parameter conventions when exchanging XMI data between applications.

### Calculated vs Provided Properties

This class **stores** sectional properties but does **not calculate** them. Properties like area and moments of inertia should be:
- Pre-calculated by the source application
- Provided in the XMI data
- Or calculated separately before creating the instance

The class performs validation but not geometric calculation.

### Relationship to Materials

Cross-sections are typically linked to materials via `XmiHasStructuralMaterial` relationships:
```
XmiCrossSection --[XmiHasStructuralMaterial]--> XmiStructuralMaterial
```

This allows the same cross-section geometry to be used with different materials, or the same material to be shared across multiple cross-sections.

### Optional Properties

All sectional properties beyond `shape` and `parameters` are optional. This allows for:
- **Minimal cross-sections**: Just shape and dimensions
- **Partial properties**: Only the properties needed for specific analyses
- **Full specification**: Complete sectional property set

### String to Tuple Conversion

The `from_dict()` method uses `convert_parameter_string_to_tuple()` to handle the XMI format:
- Input: `"300;600;10;15"` (semicolon-separated string)
- Output: `(300.0, 600.0, 10.0, 15.0)` (tuple of floats)
- Validation: Checks for empty/whitespace values and non-numeric values

### Performance Considerations

For large models with thousands of cross-sections:
- Consider caching frequently used sections
- Use dictionaries for O(1) lookup by ID or name
- Avoid redundant calculations of derived properties
- Consider creating a section library/catalog for reuse

### Version Differences (v1 vs v2)

- **v2** (this version): Uses Pydantic with automatic validation
- **v1**: Uses `__slots__` with manual validation
- v2 provides better type checking and more Pythonic API
- Field aliases in v2 enable seamless XMI file compatibility

## Related Classes

- **`XmiBaseEntity`**: Parent class providing common entity properties
- **`XmiShapeEnum`**: Enum defining valid cross-section shapes
- **`XmiStructuralMaterial`**: Materials linked to cross-sections via relationships
- **`XmiStructuralCurveMember`**: Structural members that reference cross-sections
- **`XmiHasCrossSection`**: Relationship linking members to cross-sections
- **`XmiHasStructuralMaterial`**: Relationship linking cross-sections to materials

## See Also

- [XmiStructuralMaterial.md](XmiStructuralMaterial.md) - Materials used with cross-sections
- [XmiStructuralCurveMember.md](XmiStructuralCurveMember.md) - Members using cross-sections
- [XmiBaseEntity.md](../bases/XmiBaseEntity.md) - Base entity documentation
- [XmiShapeEnum.md](../enums/XmiShapeEnum.md) - Shape type enumeration
