# XmiStructuralMaterial

## Overview

`XmiStructuralMaterial` represents a structural material in the XMI schema. This class defines the physical and mechanical properties of materials used in structural engineering, such as concrete, steel, timber, and other construction materials. It is a fundamental entity that gets referenced by other structural components like cross-sections, beams, columns, and slabs.

## Class Hierarchy

- **Parent**: `XmiBaseEntity`
- **Module**: `xmi.v2.models.entities.xmi_structural_material`
- **Implementation**: Pydantic model with validation

## Properties

### Required Properties

| Property | Type | Description | Validation |
|----------|------|-------------|------------|
| `material_type` | `XmiStructuralMaterialTypeEnum` | Type of material (Concrete, Steel, Timber, etc.) | Must be a valid enum value |

### Optional Properties

| Property | Type | Default | Description | Validation |
|----------|------|---------|-------------|------------|
| `grade` | `float` | `None` | Material grade or strength class (e.g., C35 for concrete, S355 for steel) | Must be numeric or None |
| `unit_weight` | `float` | `None` | Unit weight/density of the material (kg/m³ or similar) | Must be numeric or None |
| `e_modulus` | `Tuple[float, float, float]` | `None` | Young's modulus (elastic modulus) in three directions (Ex, Ey, Ez) | Must be tuple of 3 numbers or None |
| `g_modulus` | `Tuple[float, float, float]` | `None` | Shear modulus in three directions (Gxy, Gyz, Gzx) | Must be tuple of 3 numbers or None |
| `poisson_ratio` | `Tuple[float, float, float]` | `None` | Poisson's ratio in three directions (νxy, νyz, νzx) | Must be tuple of 3 numbers or None |
| `thermal_coefficient` | `float` | `None` | Coefficient of thermal expansion | Must be numeric or None |

### Inherited Properties (from XmiBaseEntity)

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `id` | `str` | Auto-generated | Unique identifier |
| `name` | `str` | `None` | Human-readable name |
| `description` | `str` | `None` | Detailed description |
| `ifcguid` | `str` | `None` | IFC GUID for interoperability |
| `entity_type` | `str` | `"XmiStructuralMaterial"` | Entity type identifier |

## Relationships

`XmiStructuralMaterial` participates in the following relationships:

- **XmiHasStructuralMaterial**: Referenced by `XmiCrossSection` and `XmiStructuralSurfaceMember` to define material properties
- Materials are source entities that get linked to cross-sections and surface members

## Usage Examples

### Creating an Instance Directly

```python
from xmi.v2.models.entities.xmi_structural_material import XmiStructuralMaterial
from xmi.v2.models.enums.xmi_structural_material_type_enum import XmiStructuralMaterialTypeEnum

# Create a concrete material
material = XmiStructuralMaterial(
    id="mat_001",
    name="Concrete C35/45",
    material_type=XmiStructuralMaterialTypeEnum.CONCRETE,
    grade=35.0,
    unit_weight=2400.0,
    e_modulus=(30000000000.0, 30000000000.0, 30000000000.0),
    g_modulus=(12500000000.0, 12500000000.0, 12500000000.0),
    poisson_ratio=(0.2, 0.2, 0.2),
    thermal_coefficient=0.00001
)

print(f"Material: {material.name}")
print(f"Type: {material.material_type.value}")
print(f"Grade: {material.grade}")
```

### Loading from Dictionary

```python
from xmi.v2.models.entities.xmi_structural_material import XmiStructuralMaterial

# Dictionary from XMI file or database
material_dict = {
    "ID": "7cadcb92-45b2-4ae1-a774-56857a75d7d2",
    "Name": "Concrete - Cast-in-Place",
    "MaterialType": "Concrete",
    "Grade": 35.0,
    "UnitWeight": 2406.5,
    "EModulus": "(9116568000, 9116568000, 9116568000)",
    "GModulus": "(3798722400, 3798722400, 3798722400)",
    "PoissonRatio": "(0.2, 0.2, 0.2)",
    "ThermalCoefficient": 9.9E-06
}

# Load and validate
material, errors = XmiStructuralMaterial.from_dict(material_dict)

if material:
    print(f"Successfully loaded: {material.name}")
    print(f"E-modulus: {material.e_modulus}")
else:
    print(f"Errors: {errors}")
```

### Creating Different Material Types

```python
from xmi.v2.models.entities.xmi_structural_material import XmiStructuralMaterial
from xmi.v2.models.enums.xmi_structural_material_type_enum import XmiStructuralMaterialTypeEnum

# Steel material
steel = XmiStructuralMaterial(
    name="Steel S355",
    material_type=XmiStructuralMaterialTypeEnum.STEEL,
    grade=355.0,
    unit_weight=7850.0,
    e_modulus=(210000000000.0, 210000000000.0, 210000000000.0),
    g_modulus=(81000000000.0, 81000000000.0, 81000000000.0),
    poisson_ratio=(0.3, 0.3, 0.3)
)

# Timber material
timber = XmiStructuralMaterial(
    name="Timber GL24h",
    material_type=XmiStructuralMaterialTypeEnum.TIMBER,
    grade=24.0,
    unit_weight=420.0,
    e_modulus=(11500000000.0, 9600000000.0, 300000000.0),
    g_modulus=(720000000.0, 720000000.0, 650000000.0),
    poisson_ratio=(0.0, 0.0, 0.0)
)

# Aluminium material
aluminium = XmiStructuralMaterial(
    name="Aluminium 6061-T6",
    material_type=XmiStructuralMaterialTypeEnum.ALUMINIUM,
    grade=6061.0,
    unit_weight=2700.0,
    e_modulus=(69000000000.0, 69000000000.0, 69000000000.0)
)
```

### Handling Validation Errors

```python
from xmi.v2.models.entities.xmi_structural_material import XmiStructuralMaterial

# Missing required material_type
invalid_dict = {
    "Name": "Unknown Material",
    "Grade": 35.0
}

material, errors = XmiStructuralMaterial.from_dict(invalid_dict)

if not material:
    print("Validation failed:")
    for error in errors:
        print(f"  - {error}")
    # Output: Missing attribute: material_type
```

### Accessing Properties

```python
material = XmiStructuralMaterial(
    name="Concrete C30",
    material_type=XmiStructuralMaterialTypeEnum.CONCRETE,
    grade=30.0,
    e_modulus=(32000000000.0, 32000000000.0, 32000000000.0)
)

# Access properties
print(f"Material name: {material.name}")
print(f"Material type: {material.material_type.value}")
print(f"Is concrete? {material.material_type == XmiStructuralMaterialTypeEnum.CONCRETE}")

# Access modulus values
if material.e_modulus:
    ex, ey, ez = material.e_modulus
    print(f"E-modulus X: {ex}, Y: {ey}, Z: {ez}")
```

## Validation Rules

### Type Validation
- `material_type`: Must be a valid `XmiStructuralMaterialTypeEnum` value
- `grade`, `unit_weight`, `thermal_coefficient`: Must be float, int, or None
- `e_modulus`, `g_modulus`, `poisson_ratio`: Must be tuple of 3 numeric values or None

### Required Fields
- `material_type`: Always required, cannot be None

### Field Aliases
The class supports both PascalCase (external/XMI format) and snake_case (internal Python) naming:
- `MaterialType` ↔ `material_type`
- `Grade` ↔ `grade`
- `EModulus` ↔ `e_modulus`
- `GModulus` ↔ `g_modulus`
- `PoissonRatio` ↔ `poisson_ratio`
- `ThermalCoefficient` ↔ `thermal_coefficient`

### Tuple String Parsing
When loading from dictionaries, tuple fields accept both:
- Tuple objects: `(30000.0, 30000.0, 30000.0)`
- String representations: `"(30000.0, 30000.0, 30000.0)"`

The `from_dict()` method automatically converts string tuples to proper tuple objects.

## Material Type Enum Values

Available material types (via `XmiStructuralMaterialTypeEnum`):
- `CONCRETE`: "Concrete"
- `STEEL`: "Steel"
- `TIMBER`: "Timber"
- `ALUMINIUM`: "Aluminium"
- `COMPOSITE`: "Composite"
- `MASONRY`: "Masonry"
- `REBAR`: "Rebar"
- `TENDON`: "Tendon"
- `OTHERS`: "Others"

## Notes

### Directional Properties
The tuple properties (`e_modulus`, `g_modulus`, `poisson_ratio`) represent material properties in three orthogonal directions:
- For **isotropic materials** (concrete, steel): All three values are typically the same
- For **orthotropic materials** (timber, composites): Values differ by direction
- Format: `(X-direction, Y-direction, Z-direction)`

### Unit Systems
The class does not enforce specific units, but typical conventions are:
- `grade`: MPa (megapascals) for strength
- `unit_weight`: kg/m³ (kilograms per cubic meter)
- `e_modulus`, `g_modulus`: Pa (pascals), typically in billions (GPa)
- `thermal_coefficient`: per degree Celsius (1/°C)

Ensure consistency across your entire model when using this class.

### Version Differences (v1 vs v2)
- **v2** (this version): Uses Pydantic for automatic validation and serialization
- **v1**: Uses `__slots__` with manual property setters and validation
- v2 provides better error messages and more Pythonic API
- Field aliases enable compatibility with XMI file format (PascalCase keys)

### Error Handling
The `from_dict()` method returns a tuple: `(instance, error_logs)`
- If successful: `instance` is populated, `error_logs` is empty
- If failed: `instance` is `None`, `error_logs` contains Exception objects
- This allows partial validation: continue processing even if some materials fail

## Related Classes

- **`XmiBaseEntity`**: Parent class providing common entity properties
- **`XmiStructuralMaterialTypeEnum`**: Enum defining valid material types
- **`XmiCrossSection`**: References materials via `XmiHasStructuralMaterial` relationship
- **`XmiStructuralSurfaceMember`**: Can reference materials directly
- **`XmiHasStructuralMaterial`**: Relationship class linking materials to other entities

## Common Use Cases

### 1. Building Material Library
```python
materials = {
    "C30": XmiStructuralMaterial(
        name="Concrete C30/37",
        material_type=XmiStructuralMaterialTypeEnum.CONCRETE,
        grade=30.0,
        unit_weight=2400.0
    ),
    "S355": XmiStructuralMaterial(
        name="Steel S355",
        material_type=XmiStructuralMaterialTypeEnum.STEEL,
        grade=355.0,
        unit_weight=7850.0
    )
}
```

### 2. Loading from XMI File
```python
import json

with open("materials.json") as f:
    xmi_data = json.load(f)

materials = []
for mat_dict in xmi_data.get("StructuralMaterial", []):
    material, errors = XmiStructuralMaterial.from_dict(mat_dict)
    if material:
        materials.append(material)
    else:
        print(f"Failed to load material: {errors}")
```

### 3. Material Comparison
```python
def is_high_strength_concrete(material: XmiStructuralMaterial) -> bool:
    """Check if material is high-strength concrete (grade > 50 MPa)"""
    return (
        material.material_type == XmiStructuralMaterialTypeEnum.CONCRETE
        and material.grade is not None
        and material.grade > 50.0
    )
```

## See Also

- [XmiCrossSection.md](XmiCrossSection.md) - Cross-sections that use materials
- [XmiBaseEntity.md](../bases/XmiBaseEntity.md) - Base entity documentation
- [XmiStructuralMaterialTypeEnum.md](../enums/XmiStructuralMaterialTypeEnum.md) - Material type enumeration
