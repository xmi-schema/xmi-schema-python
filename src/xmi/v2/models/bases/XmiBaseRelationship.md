# XmiBaseRelationship

## Overview

`XmiBaseRelationship` is the base class for all relationships in the XMI schema v2 implementation. Relationships connect entities together to form a graph structure, representing connections like materials assigned to cross-sections, members linked to nodes, and geometric associations. This base class ensures all relationships have consistent identification, naming, and references to source and target entities.

## Class Hierarchy

- **Parent**: `BaseModel` (Pydantic)
- **Version**: v2 (Pydantic-based implementation)
- **Module**: `src/xmi/v2/models/bases/xmi_base_relationship.py`
- **Children**: All XMI relationship classes (HasStructuralMaterial, HasCrossSection, HasStructuralNode, etc.)

## Properties

### Core Properties

| Property | Type | Description | Default | Alias | Required |
|----------|------|-------------|---------|-------|----------|
| `id` | `str` | Unique identifier (GUID) | Auto-generated UUID | "ID" | No |
| `source` | `XmiBaseEntity` | Source entity of the relationship | - | "Source" | Yes |
| `target` | `XmiBaseEntity` | Target entity of the relationship | - | "Target" | Yes |
| `name` | `str` | Relationship name/type | - | "Name" | Yes |
| `description` | `str` | Optional description or notes | "" (empty string) | "Description" | No |
| `entity_type` | `str` | Type name of the relationship | "XmiRelBaseRelationship" | "EntityType" | No |
| `uml_type` | `str` | UML relationship type | "" (empty string) | "UmlType" | No |

### Field Aliases

All properties support both PascalCase (JSON/XMI format) and snake_case (Python):
- `id` ↔ `ID`
- `source` ↔ `Source`
- `target` ↔ `Target`
- `name` ↔ `Name`
- `description` ↔ `Description`
- `entity_type` ↔ `EntityType`
- `uml_type` ↔ `UmlType`

## Purpose and Functionality

### Relationship Structure

`XmiBaseRelationship` provides the foundation for the entity-relationship graph:

1. **Directed Connections**: Each relationship has a source and target entity
2. **Named Relationships**: The `name` field identifies the relationship type
3. **Unique Identity**: Each relationship has a unique `id` for traceability
4. **Type Classification**: `entity_type` identifies the specific relationship class

### Key Concepts

**Source and Target:**
- **Source**: The entity that "owns" or initiates the relationship
- **Target**: The entity being referenced or connected to
- Example: Cross-section (source) → Material (target) via `XmiHasStructuralMaterial`

**Relationship Directionality:**
- All relationships are directed (source → target)
- Direction indicates semantic meaning
- Reverse lookups must scan all relationships

### Validation

The `validate_fields` validator ensures:
- `name` must be provided (cannot be empty or None)
- Raises `ValueError` if name is missing

## Usage Examples

### Direct Instantiation (Subclasses)

```python
from xmi.v2.models.relationships.xmi_has_structural_material import XmiHasStructuralMaterial
from xmi.v2.models.entities.xmi_structural_cross_section import XmiCrossSection
from xmi.v2.models.entities.xmi_structural_material import XmiStructuralMaterial

# Create entities
material = XmiStructuralMaterial(
    id="mat-001",
    name="Concrete C30",
    material_type="Concrete",
    grade="C30"
)

cross_section = XmiCrossSection(
    id="cs-001",
    name="RECT_300x500",
    shape="Rectangle"
)

# Create relationship linking cross-section to material
relationship = XmiHasStructuralMaterial(
    source=cross_section,
    target=material,
    name="HasStructuralMaterial"
)

print(f"Relationship: {relationship.name}")
print(f"Source: {relationship.source.name}")
print(f"Target: {relationship.target.name}")
print(f"ID: {relationship.id}")  # Auto-generated UUID
```

### Loading from Dictionary

```python
# Note: Typically relationships are created programmatically, not from dictionaries
# But the base class supports it via Pydantic

relationship_dict = {
    "ID": "rel-001",
    "Source": source_entity,
    "Target": target_entity,
    "Name": "HasStructuralMaterial",
    "Description": "Links cross-section to material",
    "EntityType": "XmiHasStructuralMaterial"
}

relationship = XmiHasStructuralMaterial(**relationship_dict)
```

### Common Patterns

#### Finding Relationships by Source

```python
def find_relationships_by_source(xmi_model, source_entity):
    """Find all relationships originating from a source entity."""
    return [
        rel for rel in xmi_model.relationships
        if rel.source.id == source_entity.id
    ]

# Usage
cross_section = xmi_model.get_entity_by_id("cs-001")
relationships = find_relationships_by_source(xmi_model, cross_section)

for rel in relationships:
    print(f"{rel.name}: {rel.source.name} → {rel.target.name}")
```

#### Finding Relationships by Target

```python
def find_relationships_by_target(xmi_model, target_entity):
    """Find all relationships pointing to a target entity."""
    return [
        rel for rel in xmi_model.relationships
        if rel.target.id == target_entity.id
    ]

# Usage
material = xmi_model.get_entity_by_id("mat-001")
relationships = find_relationships_by_target(xmi_model, material)

print(f"Material '{material.name}' is used by:")
for rel in relationships:
    print(f"  - {rel.source.name} ({rel.source.entity_type})")
```

#### Finding Relationships by Type

```python
def find_relationships_by_type(xmi_model, relationship_type: str):
    """Find all relationships of a specific type."""
    return [
        rel for rel in xmi_model.relationships
        if rel.entity_type == relationship_type
    ]

# Usage
material_rels = find_relationships_by_type(xmi_model, "XmiHasStructuralMaterial")
print(f"Found {len(material_rels)} material relationships")
```

#### Finding Target Entities

```python
def get_targets_from_source(xmi_model, source_entity, relationship_name: str = None):
    """Get all target entities connected to a source entity."""
    relationships = find_relationships_by_source(xmi_model, source_entity)

    if relationship_name:
        relationships = [r for r in relationships if r.name == relationship_name]

    return [rel.target for rel in relationships]

# Usage
cross_section = xmi_model.get_entity_by_id("cs-001")
materials = get_targets_from_source(cross_section, "HasStructuralMaterial")

for material in materials:
    print(f"Material: {material.name}")
```

#### Creating Relationship Network

```python
class RelationshipGraph:
    """Build a graph structure from relationships."""

    def __init__(self, xmi_model):
        self.model = xmi_model
        self.graph = self._build_graph()

    def _build_graph(self):
        """Build adjacency list from relationships."""
        from collections import defaultdict
        graph = defaultdict(list)

        for rel in self.model.relationships:
            graph[rel.source.id].append({
                "target": rel.target,
                "relationship": rel.name,
                "relationship_id": rel.id
            })

        return dict(graph)

    def get_neighbors(self, entity_id: str):
        """Get all entities connected to this entity."""
        return self.graph.get(entity_id, [])

    def get_path(self, start_id: str, end_id: str):
        """Find path between two entities (BFS)."""
        from collections import deque

        queue = deque([(start_id, [start_id])])
        visited = {start_id}

        while queue:
            current_id, path = queue.popleft()

            if current_id == end_id:
                return path

            for neighbor in self.get_neighbors(current_id):
                target_id = neighbor["target"].id
                if target_id not in visited:
                    visited.add(target_id)
                    queue.append((target_id, path + [target_id]))

        return None  # No path found

# Usage
graph = RelationshipGraph(xmi_model)
neighbors = graph.get_neighbors("cs-001")
print(f"Cross-section cs-001 is connected to {len(neighbors)} entities")
```

#### Grouping Relationships

```python
def group_relationships_by_name(xmi_model):
    """Group relationships by their name/type."""
    from collections import defaultdict
    grouped = defaultdict(list)

    for rel in xmi_model.relationships:
        grouped[rel.name].append(rel)

    return dict(grouped)

# Usage
grouped = group_relationships_by_name(xmi_model)
for rel_name, rels in grouped.items():
    print(f"{rel_name}: {len(rels)} relationships")
```

#### Validating Relationships

```python
def validate_relationships(xmi_model):
    """Validate all relationships in the model."""
    errors = []
    entity_ids = {entity.id for entity in xmi_model.entities}

    for rel in xmi_model.relationships:
        # Check source exists
        if rel.source.id not in entity_ids:
            errors.append(f"Relationship {rel.id}: source {rel.source.id} not found")

        # Check target exists
        if rel.target.id not in entity_ids:
            errors.append(f"Relationship {rel.id}: target {rel.target.id} not found")

        # Check name is provided
        if not rel.name:
            errors.append(f"Relationship {rel.id}: name is empty")

    return errors

# Usage
errors = validate_relationships(xmi_model)
if errors:
    print("Relationship validation errors:")
    for error in errors:
        print(f"  - {error}")
else:
    print("All relationships are valid")
```

## Validation Rules

### Required Fields

- **name**: Must be provided and non-empty
  - Raises `ValueError` if missing
  - Cannot be None or empty string

### Optional Fields

- **id**: Auto-generated UUID if not provided
- **description**: Defaults to empty string
- **entity_type**: Defaults to "XmiRelBaseRelationship"
- **uml_type**: Defaults to empty string

### Entity References

- **source** and **target** must be `XmiBaseEntity` instances
- Pydantic validates type compatibility
- Both are required fields

## Integration with XMI Schema

### Relationship Creation

In the v2 implementation, relationships are typically created programmatically during parsing:

```python
# In XmiManager.read_xmi_dict():
for cross_section_dict in xmi_dict.get("CrossSection", []):
    cross_section, errors = XmiCrossSection.from_dict(cross_section_dict)

    # Find material by ID
    material_id = cross_section_dict.get("MaterialID")
    material = find_entity_by_id(entities, material_id)

    # Create relationship
    if material:
        relationship = XmiHasStructuralMaterial(
            source=cross_section,
            target=material,
            name="HasStructuralMaterial"
        )
        relationships.append(relationship)
```

### Common Relationship Types

1. **XmiHasStructuralMaterial**: Links cross-sections/surfaces to materials
2. **XmiHasCrossSection**: Links curve members to cross-sections
3. **XmiHasStructuralNode**: Links members/segments to point connections
4. **XmiHasSegment**: Links members to their geometric segments
5. **XmiHasGeometry**: Links entities to geometric primitives

### Relationship Storage

Relationships are stored in `XmiModel.relationships`:
```python
xmi_model = XmiModel(
    entities=[...],
    relationships=[...],
    errors=[]
)
```

## Notes

### Version Differences (v1 vs v2)

**v2 Characteristics (XmiBaseRelationship):**
- Pydantic `BaseModel` with validation
- Direct entity references (not string IDs)
- Automatic UUID generation
- Field aliases for PascalCase/snake_case
- Type validation via Pydantic

**v1 Characteristics:**
- Uses `__slots__` for memory efficiency
- May use string IDs for references
- Manual validation logic
- Explicit property setters/getters

### Entity References vs IDs

Unlike some graph databases, v2 relationships store direct entity references:
- **Advantage**: Direct access to related entities without lookups
- **Disadvantage**: Circular reference considerations for serialization
- **Note**: Serialization may need special handling (store IDs, not objects)

### Pydantic Configuration

```python
model_config = ConfigDict(populate_by_name=True)
```

This allows both field names and aliases:
```python
# Both work:
rel1 = XmiHasStructuralMaterial(source=cs, target=mat, name="HasStructuralMaterial")
rel2 = XmiHasStructuralMaterial(Source=cs, Target=mat, Name="HasStructuralMaterial")
```

### Arbitrary Types

The configuration includes `arbitrary_types_allowed=True` (implicitly) to allow non-Pydantic types like `XmiBaseEntity` references.

### Performance Considerations

- Relationship lookup is O(n) where n = number of relationships
- For large models, consider building indices/dictionaries
- Direct entity references eliminate double lookups
- UUID generation is fast (~1 microsecond)

### Common Pitfalls

1. **Missing Name**: Forgetting to provide `name` raises validation error
2. **Circular References**: Serializing relationships with direct entity refs can cause issues
3. **Orphaned Relationships**: Deleting entities without removing their relationships
4. **Reverse Lookup**: No automatic reverse index; must scan all relationships

### Best Practices

1. **Use XmiModel Methods**: Use `find_relationships_by_source()` and similar helpers
2. **Validate References**: Ensure source and target entities exist in the model
3. **Consistent Naming**: Use standard relationship names (e.g., "HasStructuralMaterial")
4. **Build Indices**: For large models, build lookup dictionaries for performance

## Related Classes

### Direct Subclasses (Relationships)
- `XmiHasStructuralMaterial` - Links entities to materials
- `XmiHasCrossSection` - Links members to cross-sections
- `XmiHasStructuralNode` - Links entities to point connections
- `XmiHasSegment` - Links members to segments
- `XmiHasGeometry` - Links entities to geometric primitives

### Entity Classes
- [`XmiBaseEntity`](./XmiBaseEntity.md) - Base class for all entities (source/target)
- [`XmiStructuralMaterial`](../entities/XmiStructuralMaterial.md) - Common target for material relationships
- [`XmiCrossSection`](../entities/XmiCrossSection.md) - Common source/target
- [`XmiStructuralCurveMember`](../entities/XmiStructuralCurveMember.md) - Common source

### Model Classes
- [`XmiModel`](../xmi_model/XmiModel.md) - Stores relationships collection
- [`XmiManager`](../xmi_model/XmiManager.md) - Creates relationships during parsing

### Pydantic Classes
- `BaseModel` - Pydantic base providing validation
- `Field` - Pydantic field definition with aliases
- `ConfigDict` - Pydantic configuration settings
