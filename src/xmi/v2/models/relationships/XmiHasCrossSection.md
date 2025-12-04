# XmiHasCrossSection

## Overview

`XmiHasCrossSection` is a relationship class that links structural curve members to their cross-section definitions. It establishes which cross-sectional properties (area, inertia, shape) apply to beams, columns, braces, and other linear structural elements. This relationship is essential for structural analysis, as cross-sectional properties directly affect element stiffness, strength, and capacity.

## Class Hierarchy

- **Parent**: `XmiBaseRelationship`
- **Version**: v2 (Pydantic-based implementation)
- **Module**: `src/xmi/v2/models/relationships/xmi_has_structural_cross_section.py`

## Properties

### Relationship-Specific Properties

| Property | Type | Description | Validation |
|----------|------|-------------|------------|
| `source` | `XmiBaseEntity` | Curve member that uses the cross-section | Must be XmiBaseEntity (typically XmiStructuralCurveMember) |
| `target` | `XmiCrossSection` | The cross-section definition | Must be XmiCrossSection |

### Inherited Properties

Inherits from `XmiBaseRelationship`:
- `id`: Unique identifier (auto-generated UUID)
- `name`: Relationship name (default: "hasCrossSection")
- `description`: Optional description
- `entity_type`: Type identifier (set to "XmiRelHasCrossSection")
- `uml_type`: UML relationship type (optional)

## Purpose and Usage

### Cross-Section Assignment

This relationship serves to:

1. **Define Member Properties**: Link curve members to their geometric and material properties
2. **Enable Analysis**: Provide cross-sectional properties for stiffness calculations
3. **Track Section Usage**: Identify which members use which cross-sections
4. **Support Design**: Enable section optimization and design checks

### Common Source Entities

Typical source entities:
- **`XmiStructuralCurveMember`**: Beams, columns, braces, and other linear elements

### Target Entity

The target is always:
- **`XmiCrossSection`**: Cross-section definition with geometric properties

## Relationship Direction

```
[XmiStructuralCurveMember] --hasCrossSection--> [XmiCrossSection]

Example:
[Beam B01] --hasCrossSection--> [Cross-Section CS_300x600]
```

## Usage Examples

### Creating Relationships Directly

```python
from xmi.v2.models.entities.xmi_structural_curve_member import XmiStructuralCurveMember
from xmi.v2.models.entities.xmi_structural_cross_section import XmiCrossSection
from xmi.v2.models.relationships.xmi_has_structural_cross_section import XmiHasCrossSection

# Create cross-section
cross_section = XmiCrossSection(
    name="CS_300x600",
    cross_section_type="Rectangular"
)

# Create curve member (beam)
beam = XmiStructuralCurveMember(
    name="B01",
    curve_member_type="Beam",
    nodes="N1;N2",
    segments="Line"
)

# Create relationship linking beam to cross-section
cs_rel = XmiHasCrossSection(
    source=beam,
    target=cross_section
)

print(f"Relationship: {cs_rel.source.name} uses cross-section {cs_rel.target.name}")
# Output: Relationship: B01 uses cross-section CS_300x600
```

### Typical Creation Pattern (during parsing)

```python
# This is typically done by XmiManager during parsing
def create_curve_member_with_cross_section(member_dict, cross_section):
    """Create curve member and link to cross-section."""
    # Create curve member
    curve_member = XmiStructuralCurveMember.from_dict(member_dict)

    # Create relationship
    cs_rel = XmiHasCrossSection(
        source=curve_member,
        target=cross_section,
        name="hasCrossSection"
    )

    return curve_member, cs_rel
```

### Common Patterns

#### Finding Cross-Section for a Member

```python
from xmi.v2.models.relationships.xmi_has_structural_cross_section import XmiHasCrossSection

def find_cross_section_for_member(xmi_model, member):
    """Find the cross-section referenced by a curve member."""
    # Find cross-section relationships where member is the source
    relationships = xmi_model.find_relationships_by_source(
        member,
        relationship_type=XmiHasCrossSection
    )

    if relationships:
        # Return the target cross-section from the first relationship
        return relationships[0].target

    return None

# Usage
beam = find_entity_by_name(xmi_model, "B01")
cross_section = find_cross_section_for_member(xmi_model, beam)

if cross_section:
    print(f"Beam {beam.name} uses cross-section {cross_section.name}")
    print(f"Section type: {cross_section.cross_section_type}")
```

#### Finding All Members Using a Cross-Section

```python
def find_members_using_cross_section(xmi_model, cross_section):
    """Find all curve members that reference a specific cross-section."""
    # Find cross-section relationships where cross-section is the target
    relationships = xmi_model.find_relationships_by_target(
        cross_section,
        relationship_type=XmiHasCrossSection
    )

    # Extract source curve members
    members = [rel.source for rel in relationships]

    return members

# Usage
cs_300x600 = find_entity_by_name(xmi_model, "CS_300x600")
members = find_members_using_cross_section(xmi_model, cs_300x600)

print(f"Cross-section {cs_300x600.name} is used by {len(members)} members:")
for member in members:
    print(f"  - {member.curve_member_type}: {member.name}")
```

#### Grouping Members by Cross-Section

```python
from collections import defaultdict

def group_members_by_cross_section(xmi_model):
    """Group all curve members by their cross-section."""
    grouped = defaultdict(list)

    # Find all cross-section relationships
    cs_rels = [
        rel for rel in xmi_model.relationships
        if isinstance(rel, XmiHasCrossSection)
    ]

    for rel in cs_rels:
        cs_name = rel.target.name
        grouped[cs_name].append(rel.source)

    return dict(grouped)

# Usage
by_cross_section = group_members_by_cross_section(xmi_model)

for cs_name, members in by_cross_section.items():
    print(f"\nCross-section: {cs_name}")
    print(f"Used by {len(members)} members:")

    # Group by member type
    from collections import Counter
    type_counts = Counter(m.curve_member_type for m in members)
    for member_type, count in type_counts.items():
        print(f"  - {member_type}: {count}")
```

#### Calculate Total Member Lengths per Cross-Section

```python
def calculate_lengths_by_cross_section(xmi_model):
    """Calculate total member length for each cross-section."""
    by_cs = group_members_by_cross_section(xmi_model)
    lengths = {}

    for cs_name, members in by_cs.items():
        total_length = 0.0
        for member in members:
            if hasattr(member, 'length') and member.length:
                total_length += member.length

        lengths[cs_name] = total_length

    return lengths

# Usage
lengths = calculate_lengths_by_cross_section(xmi_model)

print("Total member lengths by cross-section:")
for cs_name, length in sorted(lengths.items(), key=lambda x: -x[1]):
    print(f"  {cs_name}: {length / 1000:.2f} m")
```

#### Validate Cross-Section Assignments

```python
def validate_cross_section_assignments(xmi_model):
    """Check that all curve members have cross-sections assigned."""
    from xmi.v2.models.entities.xmi_structural_curve_member import XmiStructuralCurveMember

    issues = []

    # Get all curve members
    curve_members = [
        e for e in xmi_model.entities
        if isinstance(e, XmiStructuralCurveMember)
    ]

    for member in curve_members:
        cs = find_cross_section_for_member(xmi_model, member)
        if not cs:
            issues.append(f"Curve member {member.name} has no cross-section assigned")

    return issues

# Usage
issues = validate_cross_section_assignments(xmi_model)
if issues:
    print("Cross-section assignment issues:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("All curve members have cross-sections assigned ✓")
```

#### Replace Cross-Section for Members

```python
def replace_cross_section(xmi_model, old_cross_section, new_cross_section):
    """Replace all references to old cross-section with new cross-section."""
    # Find all relationships using old cross-section
    relationships = xmi_model.find_relationships_by_target(
        old_cross_section,
        relationship_type=XmiHasCrossSection
    )

    count = 0
    for rel in relationships:
        # Update the target to new cross-section
        rel.target = new_cross_section
        count += 1

    return count

# Usage
old_cs = find_entity_by_name(xmi_model, "CS_200x400")
new_cs = find_entity_by_name(xmi_model, "CS_300x600")

replaced = replace_cross_section(xmi_model, old_cs, new_cs)
print(f"Replaced {replaced} cross-section references from {old_cs.name} to {new_cs.name}")
```

#### Find Members by Cross-Section Type

```python
def find_members_by_section_type(xmi_model, section_type: str):
    """Find all members with a specific cross-section type."""
    from xmi.v2.models.entities.xmi_structural_curve_member import XmiStructuralCurveMember

    matching_members = []

    curve_members = [
        e for e in xmi_model.entities
        if isinstance(e, XmiStructuralCurveMember)
    ]

    for member in curve_members:
        cs = find_cross_section_for_member(xmi_model, member)
        if cs and cs.cross_section_type == section_type:
            matching_members.append(member)

    return matching_members

# Usage
i_section_members = find_members_by_section_type(xmi_model, "I-Section")
print(f"Found {len(i_section_members)} members with I-Section:")
for member in i_section_members[:10]:  # Show first 10
    cs = find_cross_section_for_member(xmi_model, member)
    print(f"  - {member.name}: {cs.name}")
```

#### Get Cross-Section Properties for Member

```python
def get_member_properties(xmi_model, member):
    """Get cross-sectional properties for a member."""
    cs = find_cross_section_for_member(xmi_model, member)

    if not cs:
        return None

    # Get material from cross-section
    from xmi.v2.models.relationships.xmi_has_structural_material import XmiHasStructuralMaterial
    material_rels = xmi_model.find_relationships_by_source(
        cs,
        relationship_type=XmiHasStructuralMaterial
    )

    material = material_rels[0].target if material_rels else None

    return {
        "cross_section": cs.name,
        "type": cs.cross_section_type,
        "material": material.name if material else None,
        "area": cs.section_area if hasattr(cs, 'section_area') else None,
        "inertia_x": cs.moment_of_inertia_y if hasattr(cs, 'moment_of_inertia_y') else None,
        "inertia_y": cs.moment_of_inertia_z if hasattr(cs, 'moment_of_inertia_z') else None
    }

# Usage
beam = find_entity_by_name(xmi_model, "B01")
props = get_member_properties(xmi_model, beam)

if props:
    print(f"Member {beam.name} properties:")
    for key, value in props.items():
        print(f"  {key}: {value}")
```

## Validation Rules

### Type Validation

- **Source**: Must be any `XmiBaseEntity` subclass (typically `XmiStructuralCurveMember`)
- **Target**: Must be `XmiCrossSection`
- Attempting to create a relationship with wrong types raises `TypeError`

### Required Fields

Both source and target are required:
```python
# Valid
rel = XmiHasCrossSection(
    source=curve_member,
    target=cross_section
)

# Invalid - will raise validation error
# rel = XmiHasCrossSection(source=curve_member)  # Missing target
```

### Automatic Defaults

- `name` defaults to "hasCrossSection"
- `entity_type` automatically set to "XmiRelHasCrossSection"

## Integration with XMI Schema

### Relationship Creation

Relationships are created during XMI parsing when curve members define their cross-section:

```json
{
  "StructuralCurveMember": [
    {
      "Name": "B01",
      "CrossSection": "CS_300x600",
      "CurveMemberType": "Beam",
      "Nodes": "N1;N2",
      "Segments": "Line",
      ...
    }
  ]
}
```

The `XmiManager`:
1. Parses curve member dictionary
2. Resolves `"CrossSection": "CS_300x600"` to actual `XmiCrossSection` object
3. Creates `XmiHasCrossSection` relationship linking member to cross-section

### Dependency Order

Cross-sections must be parsed before members that reference them:
1. Parse `StructuralMaterial` entities
2. Parse `CrossSection` entities (which reference materials)
3. Parse `StructuralCurveMember` entities
4. Create `XmiHasCrossSection` relationships

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

### One-to-Many Relationship

- One cross-section can be used by many members (common)
- One member typically has one cross-section (standard)
- Multiple cross-sections per member is unusual but technically possible

### Cross-Section Optimization

Common workflow:
1. Identify members using each cross-section
2. Group by loading conditions
3. Optimize cross-section sizes
4. Update relationships to new optimized cross-sections

### Performance Considerations

- Relationship queries are O(n) where n = number of relationships
- For large models (10,000+ members), consider caching cross-section lookups
- Indexing relationships by source/target can improve performance

## Related Classes

### Source Entity Class
- [`XmiStructuralCurveMember`](../entities/XmiStructuralCurveMember.md) - Curve member (beam, column, brace)

### Target Entity Class
- [`XmiCrossSection`](../entities/XmiCrossSection.md) - Cross-section definition

### Related Relationship Classes
- [`XmiHasStructuralMaterial`](./XmiHasStructuralMaterial.md) - Links cross-sections to materials
- `XmiHasStructuralNode` - Links members to nodes
- `XmiHasSegment` - Links members to segments
- `XmiHasGeometry` - Links segments to geometric definitions

### Base Classes
- `XmiBaseRelationship` - Base class for all relationships
- [`XmiBaseEntity`](../bases/XmiBaseEntity.md) - Base class for entities

### Manager Classes
- [`XmiManager`](../xmi_model/XmiManager.md) - Creates relationships during parsing
- [`XmiModel`](../xmi_model/XmiModel.md) - Stores and queries relationships
