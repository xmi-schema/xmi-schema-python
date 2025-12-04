# XmiHasStructuralMaterial

## Overview

`XmiHasStructuralMaterial` is a relationship class that links structural entities to their material definitions. It connects entities like cross-sections and surface members to `XmiStructuralMaterial` objects, establishing what material properties apply to each structural element. This relationship is fundamental for structural analysis, as material properties (elasticity, strength, density) govern structural behavior.

## Class Hierarchy

- **Parent**: `XmiBaseRelationship`
- **Version**: v2 (Pydantic-based implementation)
- **Module**: `src/xmi/v2/models/relationships/xmi_has_structural_material.py`

## Properties

### Relationship-Specific Properties

| Property | Type | Description | Validation |
|----------|------|-------------|------------|
| `source` | `XmiBaseEntity` | Entity that uses the material (cross-section, surface member, etc.) | Must be XmiBaseEntity |
| `target` | `XmiStructuralMaterial` | The material definition | Must be XmiStructuralMaterial |

### Inherited Properties

Inherits from `XmiBaseRelationship`:
- `id`: Unique identifier (auto-generated UUID)
- `name`: Relationship name (default: "hasStructuralMaterial")
- `description`: Optional description
- `entity_type`: Type identifier (set to "XmiRelHasStructuralMaterial")
- `uml_type`: UML relationship type (optional)

## Purpose and Usage

### Material Assignment

This relationship serves to:

1. **Link Elements to Materials**: Connect structural elements to their material definitions
2. **Enable Analysis**: Provide material properties (E, G, density) for structural calculations
3. **Track Material Usage**: Identify which elements use which materials
4. **Support Quantities**: Calculate material quantities by element type

### Common Source Entities

Typical source entities include:
- **`XmiCrossSection`**: Cross-sections reference materials
- **`XmiStructuralSurfaceMember`**: Surface members (slabs, walls) reference materials

### Target Entity

The target is always:
- **`XmiStructuralMaterial`**: Material definition with properties

## Relationship Direction

```
[Source Entity] --hasStructuralMaterial--> [XmiStructuralMaterial]

Examples:
[XmiCrossSection] --hasStructuralMaterial--> [XmiStructuralMaterial]
[XmiStructuralSurfaceMember] --hasStructuralMaterial--> [XmiStructuralMaterial]
```

## Usage Examples

### Creating Relationships Directly

```python
from xmi.v2.models.entities.xmi_structural_cross_section import XmiCrossSection
from xmi.v2.models.entities.xmi_material import XmiStructuralMaterial
from xmi.v2.models.relationships.xmi_has_structural_material import XmiHasStructuralMaterial

# Create material
concrete = XmiStructuralMaterial(
    name="MAT_C30",
    material_type="Concrete",
    grade="C30"
)

# Create cross-section
cross_section = XmiCrossSection(
    name="CS_300x600",
    cross_section_type="Rectangular"
)

# Create relationship linking cross-section to material
material_rel = XmiHasStructuralMaterial(
    source=cross_section,
    target=concrete
)

print(f"Relationship: {material_rel.source.name} uses {material_rel.target.name}")
# Output: Relationship: CS_300x600 uses MAT_C30
```

### Typical Creation Pattern (during parsing)

```python
# This is typically done by XmiManager during parsing
def create_cross_section_with_material(cs_dict, material):
    """Create cross-section and link to material."""
    # Create cross-section
    cross_section = XmiCrossSection.from_dict(cs_dict)

    # Create relationship
    material_rel = XmiHasStructuralMaterial(
        source=cross_section,
        target=material,
        name="hasStructuralMaterial"
    )

    return cross_section, material_rel
```

### Common Patterns

#### Finding Material for an Entity

```python
from xmi.v2.models.relationships.xmi_has_structural_material import XmiHasStructuralMaterial

def find_material_for_entity(xmi_model, entity):
    """Find the material referenced by an entity."""
    # Find all material relationships where entity is the source
    relationships = xmi_model.find_relationships_by_source(
        entity,
        relationship_type=XmiHasStructuralMaterial
    )

    if relationships:
        # Return the target material from the first relationship
        return relationships[0].target

    return None

# Usage
cross_section = find_entity_by_name(xmi_model, "CS_300x600")
material = find_material_for_entity(xmi_model, cross_section)

if material:
    print(f"Cross-section {cross_section.name} uses material {material.name}")
    print(f"Material type: {material.material_type}")
    print(f"Grade: {material.grade}")
```

#### Finding All Elements Using a Material

```python
def find_elements_using_material(xmi_model, material):
    """Find all elements that reference a specific material."""
    # Find all material relationships where material is the target
    relationships = xmi_model.find_relationships_by_target(
        material,
        relationship_type=XmiHasStructuralMaterial
    )

    # Extract source entities
    elements = [rel.source for rel in relationships]

    return elements

# Usage
concrete_c30 = find_entity_by_name(xmi_model, "MAT_C30")
elements = find_elements_using_material(xmi_model, concrete_c30)

print(f"Material {concrete_c30.name} is used by {len(elements)} elements:")
for element in elements:
    print(f"  - {element.entity_type}: {element.name}")
```

#### Grouping Elements by Material

```python
from collections import defaultdict

def group_elements_by_material(xmi_model):
    """Group all elements by their material."""
    grouped = defaultdict(list)

    # Find all material relationships
    material_rels = [
        rel for rel in xmi_model.relationships
        if isinstance(rel, XmiHasStructuralMaterial)
    ]

    for rel in material_rels:
        material_name = rel.target.name
        grouped[material_name].append(rel.source)

    return dict(grouped)

# Usage
by_material = group_elements_by_material(xmi_model)

for material_name, elements in by_material.items():
    print(f"\nMaterial: {material_name}")
    print(f"Used by {len(elements)} elements:")
    for elem in elements[:5]:  # Show first 5
        print(f"  - {elem.entity_type}: {elem.name}")
```

#### Calculate Material Quantities

```python
def calculate_material_usage(xmi_model, material):
    """Calculate total usage of a material."""
    from xmi.v2.models.entities.xmi_structural_cross_section import XmiCrossSection
    from xmi.v2.models.entities.structural_analytical.xmi_structural_surface_member import XmiStructuralSurfaceMember
    from xmi.v2.models.entities.structural_analytical.xmi_structural_curve_member import XmiStructuralCurveMember

    # Find all elements using this material
    elements = find_elements_using_material(xmi_model, material)

    stats = {
        "cross_sections": 0,
        "curve_members": 0,
        "surface_members": 0,
        "total_volume": 0.0,  # Would require additional calculations
        "total_mass": 0.0
    }

    for elem in elements:
        if isinstance(elem, XmiCrossSection):
            stats["cross_sections"] += 1

            # Find curve members using this cross-section
            cs_rels = xmi_model.find_relationships_by_target(elem)
            for cs_rel in cs_rels:
                if isinstance(cs_rel.source, XmiStructuralCurveMember):
                    stats["curve_members"] += 1

        elif isinstance(elem, XmiStructuralSurfaceMember):
            stats["surface_members"] += 1

    return stats

# Usage
concrete = find_entity_by_name(xmi_model, "MAT_C30")
usage = calculate_material_usage(xmi_model, concrete)

print(f"Material {concrete.name} usage:")
print(f"  Cross-sections: {usage['cross_sections']}")
print(f"  Curve members: {usage['curve_members']}")
print(f"  Surface members: {usage['surface_members']}")
```

#### Validate Material Assignments

```python
def validate_material_assignments(xmi_model):
    """Check that all elements requiring materials have them assigned."""
    from xmi.v2.models.entities.xmi_structural_cross_section import XmiCrossSection
    from xmi.v2.models.entities.structural_analytical.xmi_structural_surface_member import XmiStructuralSurfaceMember

    issues = []

    # Get all entities that should have materials
    cross_sections = [e for e in xmi_model.entities if isinstance(e, XmiCrossSection)]
    surface_members = [e for e in xmi_model.entities if isinstance(e, XmiStructuralSurfaceMember)]

    for cs in cross_sections:
        material = find_material_for_entity(xmi_model, cs)
        if not material:
            issues.append(f"Cross-section {cs.name} has no material assigned")

    for sm in surface_members:
        material = find_material_for_entity(xmi_model, sm)
        if not material:
            issues.append(f"Surface member {sm.name} has no material assigned")

    return issues

# Usage
issues = validate_material_assignments(xmi_model)
if issues:
    print("Material assignment issues:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("All elements have materials assigned ✓")
```

#### Replace Material Reference

```python
def replace_material(xmi_model, old_material, new_material):
    """Replace all references to old material with new material."""
    # Find all relationships using old material
    relationships = xmi_model.find_relationships_by_target(
        old_material,
        relationship_type=XmiHasStructuralMaterial
    )

    count = 0
    for rel in relationships:
        # Update the target to new material
        rel.target = new_material
        count += 1

    return count

# Usage
old_concrete = find_entity_by_name(xmi_model, "MAT_C25")
new_concrete = find_entity_by_name(xmi_model, "MAT_C30")

replaced = replace_material(xmi_model, old_concrete, new_concrete)
print(f"Replaced {replaced} material references from {old_concrete.name} to {new_concrete.name}")
```

## Validation Rules

### Type Validation

- **Source**: Must be any `XmiBaseEntity` subclass (typically cross-section or surface member)
- **Target**: Must be `XmiStructuralMaterial`
- Attempting to create a relationship with wrong types raises `TypeError`

### Required Fields

Both source and target are required:
```python
# Valid
rel = XmiHasStructuralMaterial(
    source=cross_section,
    target=material
)

# Invalid - will raise validation error
# rel = XmiHasStructuralMaterial(source=cross_section)  # Missing target
```

### Automatic Defaults

- `name` defaults to "hasStructuralMaterial"
- `entity_type` automatically set to "XmiRelHasStructuralMaterial"

## Integration with XMI Schema

### Relationship Creation

Relationships are created during XMI parsing when:

1. **Cross-section defines material**:
   ```json
   {
     "CrossSection": [
       {
         "Name": "CS_300x600",
         "StructuralMaterial": "MAT_C30",
         ...
       }
     ]
   }
   ```

2. **Surface member defines material**:
   ```json
   {
     "StructuralSurfaceMember": [
       {
         "Name": "SLAB_01",
         "StructuralMaterial": "MAT_C30",
         ...
       }
     ]
   }
   ```

The `XmiManager` resolves material names to `XmiStructuralMaterial` objects and creates `XmiHasStructuralMaterial` relationships.

### Dependency Order

Materials must be parsed before elements that reference them:
1. Parse `StructuralMaterial` entities
2. Parse `CrossSection` and `StructuralSurfaceMember`
3. Create `XmiHasStructuralMaterial` relationships

## Notes

### Version Differences (v1 vs v2)

**v2 Characteristics:**
- Pydantic-based with automatic validation
- Type validation via `field_validator`
- Cleaner syntax and better error messages

**v1 Characteristics:**
- Manual validation in constructors
- Explicit type checking
- `__slots__` for memory efficiency

### Relationship Storage

Relationships are stored separately from entities in `XmiModel`:
```python
xmi_model.entities         # List of all entities
xmi_model.relationships    # List of all relationships
```

Query methods:
- `find_relationships_by_source(entity)` - Find relationships from an entity
- `find_relationships_by_target(entity)` - Find relationships to an entity

### Multiple Materials

Typically, each element has one material. However, the model allows:
- One element referencing multiple materials (unusual)
- Multiple elements referencing the same material (common)

### Material Inheritance

In some cases, material assignment is implicit:
- Curve members inherit material from their cross-section
- Cross-section defines material, not the individual member

### Performance Considerations

- Relationship queries are O(n) where n = number of relationships
- For large models, consider caching material lookups
- Indexing relationships by source/target can improve performance

## Related Classes

### Source Entity Classes
- [`XmiCrossSection`](../entities/XmiCrossSection.md) - Primary source entity
- [`XmiStructuralSurfaceMember`](../entities/XmiStructuralSurfaceMember.md) - Surface element source

### Target Entity Class
- [`XmiStructuralMaterial`](../entities/XmiStructuralMaterial.md) - Material definition

### Related Relationship Classes
- `XmiHasCrossSection` - Links curve members to cross-sections
- `XmiHasGeometry` - Links elements to geometric definitions
- `XmiHasStructuralNode` - Links members to nodes

### Base Classes
- `XmiBaseRelationship` - Base class for all relationships
- [`XmiBaseEntity`](../bases/XmiBaseEntity.md) - Base class for entities

### Manager Classes
- [`XmiManager`](../xmi_model/XmiManager.md) - Creates relationships during parsing
- [`XmiModel`](../xmi_model/XmiModel.md) - Stores and queries relationships
