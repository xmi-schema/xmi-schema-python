# XmiStructuralMaterialTypeEnum

## Overview

`XmiStructuralMaterialTypeEnum` is an enumeration that defines the types of structural materials available in the XMI schema. This classification helps identify material properties, behavior, and appropriate design standards.

## Class Hierarchy

- **Parent**: [`XmiBaseEnum`](../bases/XmiBaseEnum.md)
- **Grandparent**: `str`, `Enum`
- **Version**: v2 (Pydantic-based implementation)
- **Module**: `src/xmi/v2/models/enums/xmi_structural_material_type_enum.py`

## Enum Values

| Member Name | Value | Description | Typical Use |
|-------------|-------|-------------|-------------|
| `CONCRETE` | "Concrete" | Concrete material | Structural members, foundations |
| `STEEL` | "Steel" | Structural steel | Beams, columns, connections |
| `TIMBER` | "Timber" | Wood/timber | Timber structures |
| `ALUMINIUM` | "Aluminium" | Aluminum/aluminium | Lightweight structures |
| `COMPOSITE` | "Composite" | Composite materials | Steel-concrete composite, FRP |
| `MASONRY` | "Masonry" | Brick, block, stone masonry | Walls, bearing walls |
| `OTHERS` | "Others" | Other material types | Custom or specialty materials |
| `REBAR` | "Rebar" | Reinforcing bar (reinforcement) | **To be removed** (deprecated) |
| `TENDON` | "Tendon" | Post-tensioning tendon | **To be removed** (deprecated) |

## Purpose and Functionality

### Material Type Classification

Material types determine:
- **Material Properties**: Elastic modulus, strength, density
- **Design Standards**: Code-specific design requirements
- **Structural Behavior**: Elastic, plastic, brittle, ductile
- **Construction Methods**: Fabrication, installation, detailing

### Material Categories

1. **Primary Structural Materials**: CONCRETE, STEEL, TIMBER
2. **Specialty Materials**: ALUMINIUM, COMPOSITE
3. **Masonry**: MASONRY
4. **Other/Custom**: OTHERS
5. **Deprecated**: REBAR, TENDON (will be removed in future versions)

## Usage Examples

### Basic Usage

```python
from xmi.v2.models.enums.xmi_structural_material_type_enum import XmiStructuralMaterialTypeEnum

# Direct access
material_type = XmiStructuralMaterialTypeEnum.CONCRETE
print(material_type.value)  # "Concrete"

# Case-insensitive lookup
material_type = XmiStructuralMaterialTypeEnum("steel")  # Returns STEEL
material_type = XmiStructuralMaterialTypeEnum("CONCRETE")  # Returns CONCRETE
```

### Creating Materials

```python
from xmi.v2.models.entities.xmi_structural_material import XmiStructuralMaterial

# Concrete material
concrete = XmiStructuralMaterial(
    name="C30",
    material_type=XmiStructuralMaterialTypeEnum.CONCRETE,
    grade="C30/37",
    elastic_modulus=31000,  # MPa
    density=2400  # kg/m³
)

# Steel material
steel = XmiStructuralMaterial(
    name="S355",
    material_type=XmiStructuralMaterialTypeEnum.STEEL,
    grade="S355",
    elastic_modulus=210000,  # MPa
    density=7850  # kg/m³
)

# Timber material
timber = XmiStructuralMaterial(
    name="GL24h",
    material_type=XmiStructuralMaterialTypeEnum.TIMBER,
    grade="GL24h",
    elastic_modulus=11500,  # MPa
    density=420  # kg/m³
)
```

### Filtering Materials by Type

```python
def get_materials_by_type(xmi_model, material_type):
    """Get all materials of a specific type."""
    from xmi.v2.models.entities.xmi_structural_material import XmiStructuralMaterial

    return [
        entity for entity in xmi_model.entities
        if isinstance(entity, XmiStructuralMaterial)
        and entity.material_type == material_type
    ]

# Usage
concrete_materials = get_materials_by_type(xmi_model, XmiStructuralMaterialTypeEnum.CONCRETE)
steel_materials = get_materials_by_type(xmi_model, XmiStructuralMaterialTypeEnum.STEEL)

print(f"Found {len(concrete_materials)} concrete materials")
print(f"Found {len(steel_materials)} steel materials")
```

### Material Type Statistics

```python
def analyze_material_types(xmi_model):
    """Analyze distribution of material types in model."""
    from collections import Counter
    from xmi.v2.models.entities.xmi_structural_material import XmiStructuralMaterial

    materials = [
        entity for entity in xmi_model.entities
        if isinstance(entity, XmiStructuralMaterial)
    ]

    type_counts = Counter(m.material_type for m in materials if m.material_type)

    print(f"Total materials: {len(materials)}")
    for mat_type, count in type_counts.most_common():
        percentage = (count / len(materials)) * 100
        print(f"{mat_type.value}: {count} ({percentage:.1f}%)")

# Usage
analyze_material_types(xmi_model)
# Output:
# Total materials: 10
# Concrete: 5 (50.0%)
# Steel: 4 (40.0%)
# Timber: 1 (10.0%)
```

### Getting Typical Material Properties

```python
def get_typical_density(material_type):
    """Get typical density for a material type (kg/m³)."""
    densities = {
        XmiStructuralMaterialTypeEnum.CONCRETE: 2400,
        XmiStructuralMaterialTypeEnum.STEEL: 7850,
        XmiStructuralMaterialTypeEnum.TIMBER: 500,
        XmiStructuralMaterialTypeEnum.ALUMINIUM: 2700,
        XmiStructuralMaterialTypeEnum.MASONRY: 1800,
    }
    return densities.get(material_type, 2400)  # Default to concrete

def get_typical_elastic_modulus(material_type):
    """Get typical elastic modulus for a material type (MPa)."""
    moduli = {
        XmiStructuralMaterialTypeEnum.CONCRETE: 30000,
        XmiStructuralMaterialTypeEnum.STEEL: 210000,
        XmiStructuralMaterialTypeEnum.TIMBER: 10000,
        XmiStructuralMaterialTypeEnum.ALUMINIUM: 70000,
        XmiStructuralMaterialTypeEnum.MASONRY: 15000,
    }
    return moduli.get(material_type, 30000)  # Default to concrete

# Usage
for mat_type in [XmiStructuralMaterialTypeEnum.CONCRETE,
                  XmiStructuralMaterialTypeEnum.STEEL,
                  XmiStructuralMaterialTypeEnum.TIMBER]:
    density = get_typical_density(mat_type)
    modulus = get_typical_elastic_modulus(mat_type)
    print(f"{mat_type.value}: ρ={density} kg/m³, E={modulus} MPa")
```

### Design Code Selection

```python
def get_design_codes(material_type):
    """Get applicable design codes for a material type."""
    codes = {
        XmiStructuralMaterialTypeEnum.CONCRETE: ["Eurocode 2", "ACI 318", "BS 8110"],
        XmiStructuralMaterialTypeEnum.STEEL: ["Eurocode 3", "AISC 360", "BS 5950"],
        XmiStructuralMaterialTypeEnum.TIMBER: ["Eurocode 5", "NDS", "BS 5268"],
        XmiStructuralMaterialTypeEnum.MASONRY: ["Eurocode 6", "TMS 402"],
        XmiStructuralMaterialTypeEnum.ALUMINIUM: ["Eurocode 9", "ADM"],
        XmiStructuralMaterialTypeEnum.COMPOSITE: ["Eurocode 4", "AISC 360"],
    }
    return codes.get(material_type, [])

# Usage
for mat_type in XmiStructuralMaterialTypeEnum:
    if mat_type not in [XmiStructuralMaterialTypeEnum.REBAR,
                        XmiStructuralMaterialTypeEnum.TENDON,
                        XmiStructuralMaterialTypeEnum.OTHERS]:
        codes = get_design_codes(mat_type)
        if codes:
            print(f"{mat_type.value}: {', '.join(codes)}")
```

### Material-Member Compatibility

```python
def validate_material_member_compatibility(member, material):
    """Check if material type is suitable for member type."""
    from xmi.v2.models.enums.xmi_structural_curve_member_type_enum import XmiStructuralCurveMemberTypeEnum

    # Typical combinations
    warnings = []

    # Steel is suitable for all member types
    if material.material_type == XmiStructuralMaterialTypeEnum.STEEL:
        return warnings

    # Timber rarely used for bracing in modern construction
    if (material.material_type == XmiStructuralMaterialTypeEnum.TIMBER
        and hasattr(member, 'member_type')
        and member.member_type == XmiStructuralCurveMemberTypeEnum.BRACING):
        warnings.append("Timber bracing is uncommon in modern structures")

    # Aluminium less common for primary structural members
    if material.material_type == XmiStructuralMaterialTypeEnum.ALUMINIUM:
        warnings.append("Aluminium structures require specialized design")

    return warnings
```

## Integration with XMI Schema

### XMI JSON Format

```json
{
  "StructuralMaterial": [
    {
      "Name": "C30",
      "MaterialType": "Concrete",
      "Grade": "C30/37",
      "ElasticModulus": 31000,
      "Density": 2400
    },
    {
      "Name": "S355",
      "MaterialType": "Steel",
      "Grade": "S355",
      "ElasticModulus": 210000,
      "Density": 7850
    }
  ]
}
```

### Usage in XmiStructuralMaterial

```python
class XmiStructuralMaterial(XmiBaseEntity):
    material_type: XmiStructuralMaterialTypeEnum = Field(..., alias="MaterialType")
```

## Notes

### Deprecated Values

The code contains comments indicating future changes:
- `REBAR`: "to be removed" - Reinforcement should be modeled differently
- `TENDON`: "to be removed" - Post-tensioning should be modeled differently

These values may be removed in future versions of the schema. They should not be used for new models.

### Common Material Types

- **CONCRETE**: Most common for buildings (columns, slabs, walls)
- **STEEL**: Common for frames, connections, bracing
- **TIMBER**: Growing usage in sustainable construction
- **COMPOSITE**: Increasingly used in modern design

### Material vs Grade

- **MaterialType** (this enum): Broad classification (Concrete, Steel, etc.)
- **Grade**: Specific material grade (C30/37, S355, GL24h, etc.)

Both are needed for complete material definition.

### ALUMINIUM Spelling

Note the British spelling "Aluminium" in the enum value. This should be considered when parsing international data.

## Related Classes

### Entity Classes
- [`XmiStructuralMaterial`](../entities/XmiStructuralMaterial.md) - Uses this enum

### Other Enums
- [`XmiShapeEnum`](./XmiShapeEnum.md) - Cross-section shapes often paired with materials

### Base Classes
- [`XmiBaseEnum`](../bases/XmiBaseEnum.md)

## See Also

- [Material Documentation](../entities/XmiStructuralMaterial.md)
- [XMI Schema Specification](https://github.com/IfcOpenShell/xmi-schema)
