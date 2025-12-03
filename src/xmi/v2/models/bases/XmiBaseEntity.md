# XmiBaseEntity

## Overview

`XmiBaseEntity` is the abstract base class for all XMI entities in the v2 implementation. It provides common identification, naming, and metadata properties that every entity in the XMI schema inherits. This base class ensures consistency across all entity types and provides standard fields for uniqueness, interoperability, and description.

## Class Hierarchy

- **Parent**: `BaseModel` (Pydantic), `ABC` (Abstract Base Class)
- **Version**: v2 (Pydantic-based implementation)
- **Module**: `src/xmi/v2/models/bases/xmi_base_entity.py`
- **Children**: All XMI entity classes (materials, cross-sections, members, connections, etc.)

## Properties

### Common Properties

All properties are optional with automatic defaults:

| Property | Type | Description | Default | Alias |
|----------|------|-------------|---------|-------|
| `id` | `str` | Unique identifier (GUID) | Auto-generated UUID | "ID" |
| `name` | `str` | Human-readable name/identifier | Same as `id` if not provided | "Name" |
| `ifcguid` | `str` | IFC Global Unique Identifier for BIM interoperability | None | "IFCGUID" |
| `native_id` | `str` | Original identifier from source application | None | "NativeId" |
| `description` | `str` | Optional description or notes | None | "Description" |
| `entity_type` | `str` | Type name of the entity | Class name (auto-set) | "EntityType" |

### Field Aliases

All properties support both PascalCase (JSON/XMI format) and snake_case (Python):
- `id` ↔ `ID`
- `name` ↔ `Name`
- `ifcguid` ↔ `IFCGUID`
- `native_id` ↔ `NativeId`
- `description` ↔ `Description`
- `entity_type` ↔ `EntityType`

## Purpose and Functionality

### Identification

`XmiBaseEntity` provides multiple identification mechanisms:

1. **id**: Primary unique identifier used internally
   - Auto-generated as UUID if not provided
   - Guaranteed to be unique across all entities

2. **name**: Human-readable identifier
   - Defaults to `id` if not provided
   - Can be non-unique (e.g., multiple beams named "B01")
   - Useful for display and reporting

3. **ifcguid**: IFC GUID for BIM interoperability
   - 22-character encoded GUID from IFC standard
   - Enables linking XMI entities with IFC models
   - Optional but recommended for BIM workflows

4. **native_id**: Original source application ID
   - Preserves identifier from analysis software (SAP2000, ETABS, etc.)
   - Useful for traceability and roundtrip workflows

### Automatic Defaults

The `fill_defaults` validator ensures:
- If no `id` provided → auto-generate UUID
- If no `name` provided → use `id` as name
- If no `entity_type` provided → use class name (e.g., "XmiStructuralMaterial")

This guarantees that every entity has valid identification even with minimal input.

## Usage Examples

### Direct Instantiation (Subclass)

```python
from xmi.v2.models.entities.xmi_structural_material import XmiStructuralMaterial

# Minimal creation - all fields auto-generated
material1 = XmiStructuralMaterial(
    material_type="Concrete",
    grade="C30"
)
print(f"ID: {material1.id}")  # Auto-generated UUID
print(f"Name: {material1.name}")  # Same as ID
print(f"Entity type: {material1.entity_type}")  # "XmiStructuralMaterial"

# Full creation with all base fields
material2 = XmiStructuralMaterial(
    id="mat-001",
    name="MAT_CONCRETE_C30",
    ifcguid="3cJh8fHxj3FwU$9vPQK1PN",
    native_id="1",
    description="Normal weight concrete C30/37",
    material_type="Concrete",
    grade="C30"
)
```

### Loading from Dictionary

```python
# PascalCase (XMI JSON format)
material_dict = {
    "ID": "mat-001",
    "Name": "MAT_C30",
    "IFCGUID": "3cJh8fHxj3FwU$9vPQK1PN",
    "NativeId": "1",
    "Description": "Concrete C30",
    "MaterialType": "Concrete",
    "Grade": "C30"
}

material, errors = XmiStructuralMaterial.from_dict(material_dict)

# snake_case (Python format)
material_dict_python = {
    "id": "mat-001",
    "name": "MAT_C30",
    "ifcguid": "3cJh8fHxj3FwU$9vPQK1PN",
    "native_id": "1",
    "description": "Concrete C30",
    "material_type": "Concrete",
    "grade": "C30"
}

material2 = XmiStructuralMaterial(**material_dict_python)
```

### Common Patterns

#### Finding Entity by ID

```python
def find_entity_by_id(xmi_model, entity_id: str):
    """Find any entity by its ID."""
    for entity in xmi_model.entities:
        if entity.id == entity_id:
            return entity
    return None

# Usage
entity = find_entity_by_id(xmi_model, "mat-001")
if entity:
    print(f"Found {entity.entity_type}: {entity.name}")
```

#### Finding Entities by Name

```python
def find_entities_by_name(xmi_model, name: str):
    """Find all entities with a given name (may be multiple)."""
    return [entity for entity in xmi_model.entities if entity.name == name]

# Usage
materials = find_entities_by_name(xmi_model, "MAT_C30")
print(f"Found {len(materials)} entities named MAT_C30")
```

#### Finding Entity by IFC GUID

```python
def find_entity_by_ifcguid(xmi_model, ifcguid: str):
    """Find entity by IFC GUID (useful for BIM interoperability)."""
    for entity in xmi_model.entities:
        if entity.ifcguid == ifcguid:
            return entity
    return None

# Usage
entity = find_entity_by_ifcguid(xmi_model, "3cJh8fHxj3FwU$9vPQK1PN")
```

#### Grouping Entities by Type

```python
from collections import defaultdict

def group_entities_by_type(xmi_model):
    """Group all entities by their entity_type."""
    grouped = defaultdict(list)
    for entity in xmi_model.entities:
        grouped[entity.entity_type].append(entity)
    return dict(grouped)

# Usage
groups = group_entities_by_type(xmi_model)
for entity_type, entities in groups.items():
    print(f"{entity_type}: {len(entities)} entities")
```

#### Creating Entity with Custom ID Strategy

```python
class EntityFactory:
    """Factory for creating entities with custom ID generation."""

    def __init__(self, prefix: str):
        self.prefix = prefix
        self.counter = 0

    def next_id(self) -> str:
        """Generate sequential ID with prefix."""
        self.counter += 1
        return f"{self.prefix}-{self.counter:04d}"

    def create_material(self, material_type: str, grade: str):
        """Create material with auto-generated ID."""
        return XmiStructuralMaterial(
            id=self.next_id(),
            name=f"MAT_{material_type}_{grade}",
            material_type=material_type,
            grade=grade
        )

# Usage
factory = EntityFactory("MAT")
concrete = factory.create_material("Concrete", "C30")
steel = factory.create_material("Steel", "S355")

print(concrete.id)  # MAT-0001
print(steel.id)     # MAT-0002
```

#### Exporting Entity Metadata

```python
def export_entity_metadata(entity) -> dict:
    """Export common entity metadata."""
    return {
        "id": entity.id,
        "name": entity.name,
        "type": entity.entity_type,
        "ifcguid": entity.ifcguid,
        "native_id": entity.native_id,
        "description": entity.description
    }

# Usage
metadata = export_entity_metadata(material)
print(metadata)
```

#### Comparing Entities

```python
def entities_match(entity1, entity2) -> bool:
    """Check if two entities represent the same object."""
    # Compare by ID (primary identifier)
    if entity1.id == entity2.id:
        return True

    # Compare by IFC GUID if both have it
    if entity1.ifcguid and entity2.ifcguid:
        return entity1.ifcguid == entity2.ifcguid

    # Compare by native_id if both have it
    if entity1.native_id and entity2.native_id:
        return entity1.native_id == entity2.native_id

    return False
```

## Validation Rules

### Automatic Field Generation

The `fill_defaults` validator runs before validation and ensures:

```python
# If ID not provided, generate UUID
if "ID" not in values and "id" not in values:
    values["ID"] = str(uuid.uuid4())

# If Name not provided, use ID
if "Name" not in values and "name" not in values:
    values["Name"] = values.get("ID") or values.get("id")

# If EntityType not provided, use class name
if "EntityType" not in values and "entity_type" not in values:
    values["EntityType"] = cls.__name__
```

### Type Validation

All fields are strings:
- `id` must be string (or auto-generated)
- `name` must be string (or auto-set from id)
- All optional fields must be strings if provided

### Optional vs Required

All base entity fields are optional:
- Subclasses may override to make fields required
- Defaults ensure valid entities even with no input

## Integration with XMI Schema

### XMI JSON Format

Base entity fields appear in all XMI entity dictionaries:

```json
{
  "StructuralMaterial": [
    {
      "ID": "4eddb960-5e2a-44a7-b3f5-03ab96796a68-00056c7b",
      "Name": "1",
      "IFCGUID": "1EtRbWNYf4fxFr0wkMV0KH",
      "NativeId": "1",
      "Description": "Concrete C30/37",
      "MaterialType": "Concrete",
      "Grade": "C30"
    }
  ]
}
```

### Parsing from XMI

`XmiManager` uses `from_dict()` methods that leverage base entity field aliases:

```python
# XmiManager internally does:
entity_dict = {
    "ID": "mat-001",
    "Name": "MAT_C30",
    "MaterialType": "Concrete",
    "Grade": "C30"
}

# Pydantic handles alias mapping automatically
material = XmiStructuralMaterial.model_validate(entity_dict)
# Accesses via: material.id, material.name (snake_case in Python)
```

## Notes

### Version Differences (v1 vs v2)

**v2 Characteristics (XmiBaseEntity):**
- Pydantic `BaseModel` with field validation
- Automatic UUID generation
- Field aliases for PascalCase/snake_case mapping
- Model validators for default value injection
- Clean, declarative syntax

**v1 Characteristics:**
- Uses `__slots__` for memory efficiency
- Manual property setters/getters
- Explicit validation in each property
- Tuple-based storage for some fields

### Abstract Base Class

`XmiBaseEntity` is abstract (`ABC`) and cannot be instantiated directly:
```python
# This will fail - XmiBaseEntity is abstract
# entity = XmiBaseEntity()  # Error!

# Must use concrete subclasses
material = XmiStructuralMaterial(material_type="Concrete", grade="C30")
```

### Pydantic Configuration

```python
model_config = ConfigDict(populate_by_name=True)
```

This allows both field names and aliases to be used:
```python
# Both work:
material1 = XmiStructuralMaterial(id="mat-001", name="MAT_C30", ...)
material2 = XmiStructuralMaterial(ID="mat-001", Name="MAT_C30", ...)
```

### UUID Generation

Uses Python's `uuid.uuid4()` for globally unique identifiers:
- Version 4 UUID (random)
- 36 characters with hyphens: `4eddb960-5e2a-44a7-b3f5-03ab96796a68`
- Collision probability is negligible

### IFC GUID Format

IFC GUIDs are 22-character Base64-encoded GUIDs:
- Example: `3cJh8fHxj3FwU$9vPQK1PN`
- Derived from 128-bit UUID
- Standard defined by IFC specification
- Used for interoperability with IFC models

### Native ID Preservation

`native_id` preserves original application identifiers:
- SAP2000, ETABS, Robot, etc. often use simple numeric IDs (1, 2, 3...)
- Preserving these IDs helps with:
  - Traceability to source models
  - Roundtrip workflows (XMI → Edit → Back to source)
  - User recognition (engineers know "Column 23" not UUID)

### Performance Considerations

- UUID generation is fast (~1 microsecond per UUID)
- String fields are lightweight
- Pydantic validation adds minimal overhead
- For large models (10,000+ entities), UUID generation is negligible

### Common Pitfalls

1. **Assuming Unique Names**: Names are not guaranteed unique, use `id` for uniqueness
2. **Forgetting Aliases**: When parsing JSON, remember PascalCase aliases
3. **Modifying entity_type**: The `entity_type` field is auto-set from class name and should not be modified
4. **Comparing by Name**: Use `id` or `ifcguid` for identity comparison, not `name`

## Related Classes

### Direct Subclasses (Entities)
- [`XmiStructuralMaterial`](../entities/XmiStructuralMaterial.md)
- [`XmiStructuralPointConnection`](../entities/XmiStructuralPointConnection.md)
- [`XmiCrossSection`](../entities/XmiCrossSection.md)
- [`XmiStructuralCurveMember`](../entities/XmiStructuralCurveMember.md)
- [`XmiStructuralSurfaceMember`](../entities/XmiStructuralSurfaceMember.md)
- [`XmiSegment`](../entities/XmiSegment.md)
- [`XmiStructuralUnit`](../entities/XmiStructuralUnit.md)
- [`XmiStructuralStorey`](../entities/XmiStructuralStorey.md)

### Sibling Base Classes
- [`XmiBaseGeometry`](./XmiBaseGeometry.md) - Base class for geometric primitives
- `XmiBaseRelationship` - Base class for relationships (not covered here)

### Manager Classes
- [`XmiManager`](../xmi_model/XmiManager.md) - Uses base entity fields during parsing
- [`XmiModel`](../xmi_model/XmiModel.md) - Stores collections of entities with base fields

### Pydantic Classes
- `BaseModel` - Pydantic base model providing validation
- `Field` - Pydantic field definition with aliases and defaults
