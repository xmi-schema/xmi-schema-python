# XmiModel

## Overview

`XmiModel` is the core container class in the xmi-schema-python library that holds all parsed XMI (Cross Model Information) data. It is a Pydantic-based model that stores collections of entities, relationships, error logs, and metadata about the structural model. XmiModel handles the actual parsing logic for converting raw dictionary data into validated, typed Python objects.

XmiModel serves as:
- **Container** for all entities (materials, members, geometries, etc.)
- **Container** for all relationships (material assignments, node connections, etc.)
- **Parser** that converts dictionaries to typed objects using mapping dictionaries
- **Validator** that ensures data integrity using Pydantic validation
- **Error tracker** that logs parsing failures without stopping execution
- **Metadata store** for model information (name, version, source application)

## Class Hierarchy

- **Parent**: `pydantic.BaseModel`
- **Module**: `xmi.v2.models.xmi_model.xmi_model`
- **Implementation**: Pydantic model with custom validation

## Properties

### Collection Properties

| Property | Type | Default | Description | Validation |
|----------|------|---------|-------------|------------|
| `entities` | `List[XmiBaseEntity]` | `[]` | All entity instances in the model | Must be XmiBaseEntity subclasses |
| `relationships` | `List[XmiBaseRelationship]` | `[]` | All relationship instances connecting entities | Must be XmiBaseRelationship subclasses |
| `histories` | `List[dict]` | `[]` | Historical records (reserved for future use) | Any dictionary |
| `errors` | `List[ErrorLog]` | `[]` | Parsing and validation errors encountered | Must be ErrorLog instances |

### Metadata Properties

| Property | Type | Default | Description | Validation |
|----------|------|---------|-------------|------------|
| `name` | `Optional[str]` | `None` | Human-readable model name | Must be string or None |
| `xmi_version` | `Optional[str]` | `None` | XMI schema version | Must be string or None |
| `application_name` | `Optional[str]` | `None` | Source application that created the XMI data | Must be string or None |
| `application_version` | `Optional[str]` | `None` | Version of the source application | Must be string or None |

### Field Aliases

The class supports both PascalCase (external/XMI format) and snake_case (internal Python) naming:
- `Entities` ↔ `entities`
- `Relationships` ↔ `relationships`
- `Histories` ↔ `histories`
- `Errors` ↔ `errors`
- `Name` ↔ `name`
- `XmiVersion` ↔ `xmi_version`
- `ApplicationName` ↔ `application_name`
- `ApplicationVersion` ↔ `application_version`

## Methods

### Public Methods

#### `find_entity(entity_id: str) -> Optional[XmiBaseEntity]`

Finds an entity by its ID in the model's entity collection.

**Parameters**:
- `entity_id`: The unique identifier of the entity to find

**Returns**:
- `XmiBaseEntity`: The entity with matching ID, or `None` if not found

**Example**:
```python
model = xmi_model

# Find entity by ID
material = model.find_entity("71d8b547-ba42-4854-9542-fda1d72da314")
if material:
    print(f"Found: {material.name}")
else:
    print("Entity not found")
```

#### `load_from_dict(data: Dict[str, Any]) -> None`

Primary parsing method that populates the model from a dictionary. This method:
1. Extracts metadata (name, version, application info)
2. Parses entities using `ENTITY_CLASS_MAPPING`
3. Parses relationships using `RELATIONSHIP_CLASS_MAPPING`
4. Validates all data with Pydantic
5. Logs errors without stopping execution

**Parameters**:
- `data`: Dictionary containing XMI data with keys like "Entities", "Relationships", "Name", etc.

**Returns**:
- `None` (modifies the model in place)

**Side Effects**:
- Populates `self.entities` list
- Populates `self.relationships` list
- Populates `self.errors` list with any parsing failures
- Sets metadata properties

**Example**:
```python
from xmi.v2.models.xmi_model.xmi_model import XmiModel

xmi_data = {
    "Name": "Office Building",
    "XmiVersion": "2.0",
    "Entities": [...],
    "Relationships": [...]
}

model = XmiModel()
model.load_from_dict(xmi_data)

print(f"Loaded {len(model.entities)} entities")
print(f"Loaded {len(model.relationships)} relationships")
```

#### `model_dump(by_alias: bool = False, exclude_none: bool = False) -> dict`

Pydantic method to export the model as a dictionary.

**Parameters**:
- `by_alias`: If True, use field aliases (PascalCase); if False, use Python names (snake_case)
- `exclude_none`: If True, omit fields with None values

**Returns**:
- `dict`: Dictionary representation of the model

**Example**:
```python
# Export with PascalCase keys (XMI format)
xmi_dict = model.model_dump(by_alias=True, exclude_none=True)

# Export with snake_case keys (Python format)
python_dict = model.model_dump(by_alias=False, exclude_none=False)
```

## ErrorLog Class

The `ErrorLog` class is defined in the same module and represents a parsing error.

### ErrorLog Properties

| Property | Type | Description |
|----------|------|-------------|
| `entity_type` | `str` | Type of entity or relationship that failed |
| `index` | `int` | Position in the Entities or Relationships list |
| `message` | `str` | Human-readable error description |
| `obj` | `Optional[str]` | String representation of the problematic data |

### ErrorLog Field Aliases

- `EntityType` ↔ `entity_type`
- `Index` ↔ `index`
- `Message` ↔ `message`
- `Obj` ↔ `obj`

## Usage Examples

### Creating an Empty Model

```python
from xmi.v2.models.xmi_model.xmi_model import XmiModel

# Create empty model
model = XmiModel()

print(f"Entities: {len(model.entities)}")  # 0
print(f"Relationships: {len(model.relationships)}")  # 0
print(f"Errors: {len(model.errors)}")  # 0
```

### Loading from Dictionary

```python
from xmi.v2.models.xmi_model.xmi_model import XmiModel
import json

# Load XMI data
with open("structure.json") as f:
    xmi_data = json.load(f)

# Create and populate model
model = XmiModel()
model.load_from_dict(xmi_data)

# Access metadata
print(f"Model: {model.name}")
print(f"XMI Version: {model.xmi_version}")
print(f"Created by: {model.application_name} {model.application_version}")

# Access collections
print(f"Entities: {len(model.entities)}")
print(f"Relationships: {len(model.relationships)}")
print(f"Errors: {len(model.errors)}")
```

### Filtering Entities by Type

```python
from xmi.v2.models.xmi_model.xmi_model import XmiModel
from xmi.v2.models.entities.xmi_structural_material import XmiStructuralMaterial
from xmi.v2.models.entities.xmi_structural_cross_section import XmiCrossSection
from xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D

model = XmiModel()
model.load_from_dict(xmi_data)

# Filter entities
materials = [e for e in model.entities if isinstance(e, XmiStructuralMaterial)]
cross_sections = [e for e in model.entities if isinstance(e, XmiCrossSection)]
points = [e for e in model.entities if isinstance(e, XmiPoint3D)]

print(f"Materials: {len(materials)}")
print(f"Cross-sections: {len(cross_sections)}")
print(f"Points: {len(points)}")

# Access specific material
for material in materials:
    print(f"  {material.name}: {material.material_type.value}")
```

### Finding Entity by ID

```python
from xmi.v2.models.xmi_model.xmi_model import XmiModel

model = XmiModel()
model.load_from_dict(xmi_data)

# Find entity
entity_id = "71d8b547-ba42-4854-9542-fda1d72da314"
entity = model.find_entity(entity_id)

if entity:
    print(f"Found entity: {entity.name}")
    print(f"Type: {entity.entity_type}")
else:
    print(f"Entity {entity_id} not found")
```

### Filtering Relationships by Type

```python
from xmi.v2.models.xmi_model.xmi_model import XmiModel
from xmi.v2.models.relationships.xmi_has_structural_material import XmiHasStructuralMaterial
from xmi.v2.models.relationships.xmi_has_structural_cross_section import XmiHasCrossSection

model = XmiModel()
model.load_from_dict(xmi_data)

# Filter relationships
material_rels = [r for r in model.relationships
                 if isinstance(r, XmiHasStructuralMaterial)]
cross_section_rels = [r for r in model.relationships
                      if isinstance(r, XmiHasCrossSection)]

print(f"Material relationships: {len(material_rels)}")
print(f"Cross-section relationships: {len(cross_section_rels)}")

# Inspect relationship
for rel in material_rels:
    print(f"  {rel.source.name} → {rel.target.name}")
```

### Handling Parsing Errors

```python
from xmi.v2.models.xmi_model.xmi_model import XmiModel

model = XmiModel()
model.load_from_dict(xmi_data)

# Check for errors
if model.errors:
    print(f"⚠ {len(model.errors)} errors occurred during parsing:")

    for error in model.errors:
        print(f"\n[{error.entity_type}] at index {error.index}")
        print(f"  Message: {error.message}")

        if error.obj:
            print(f"  Data: {error.obj[:100]}...")  # First 100 chars
else:
    print("✓ Model loaded successfully with no errors")

# Continue working with successfully loaded entities
print(f"\nSuccessfully loaded: {len(model.entities)} entities")
```

### Exporting Model to Dictionary

```python
from xmi.v2.models.xmi_model.xmi_model import XmiModel
import json

model = XmiModel()
model.load_from_dict(xmi_data)

# Export with XMI format (PascalCase)
xmi_export = model.model_dump(by_alias=True, exclude_none=True)

# Save to file
with open("exported_model.json", "w") as f:
    json.dump(xmi_export, f, indent=2)

print("Model exported to exported_model.json")
```

### Querying Relationships for an Entity

```python
from xmi.v2.models.xmi_model.xmi_model import XmiModel
from xmi.v2.models.entities.xmi_structural_cross_section import XmiCrossSection

model = XmiModel()
model.load_from_dict(xmi_data)

# Find a cross-section
cross_section = next((e for e in model.entities
                      if isinstance(e, XmiCrossSection)), None)

if cross_section:
    # Find relationships where cross-section is the source
    outgoing_rels = [r for r in model.relationships
                     if r.source == cross_section]

    # Find relationships where cross-section is the target
    incoming_rels = [r for r in model.relationships
                     if r.target == cross_section]

    print(f"Cross-section: {cross_section.name}")
    print(f"  Outgoing relationships: {len(outgoing_rels)}")
    print(f"  Incoming relationships: {len(incoming_rels)}")

    for rel in outgoing_rels:
        print(f"    → {rel.entity_type}: {rel.target.name}")
```

### Creating a Model Summary

```python
from xmi.v2.models.xmi_model.xmi_model import XmiModel
from collections import defaultdict

model = XmiModel()
model.load_from_dict(xmi_data)

# Count entities by type
entity_counts = defaultdict(int)
for entity in model.entities:
    entity_counts[entity.entity_type] += 1

# Count relationships by type
rel_counts = defaultdict(int)
for rel in model.relationships:
    rel_counts[rel.entity_type] += 1

# Print summary
print("=" * 50)
print(f"Model: {model.name or 'Unnamed'}")
print(f"XMI Version: {model.xmi_version or 'Unknown'}")
print("=" * 50)

print("\nEntities:")
for entity_type, count in sorted(entity_counts.items()):
    print(f"  {entity_type:30s}: {count:3d}")
print(f"  {'TOTAL':30s}: {len(model.entities):3d}")

print("\nRelationships:")
for rel_type, count in sorted(rel_counts.items()):
    print(f"  {rel_type:30s}: {count:3d}")
print(f"  {'TOTAL':30s}: {len(model.relationships):3d}")

print(f"\nErrors: {len(model.errors)}")
print("=" * 50)
```

### Validating Entity References

```python
from xmi.v2.models.xmi_model.xmi_model import XmiModel

model = XmiModel()
model.load_from_dict(xmi_data)

# Collect all entity IDs
entity_ids = {e.id for e in model.entities}

# Validate relationships
broken_relationships = []

for rel in model.relationships:
    source_id = rel.source.id if hasattr(rel.source, 'id') else None
    target_id = rel.target.id if hasattr(rel.target, 'id') else None

    if source_id not in entity_ids:
        broken_relationships.append((rel, "source"))
    if target_id not in entity_ids:
        broken_relationships.append((rel, "target"))

if broken_relationships:
    print(f"⚠ Found {len(broken_relationships)} broken relationships:")
    for rel, broken_end in broken_relationships:
        print(f"  {rel.entity_type}: broken {broken_end}")
else:
    print("✓ All relationships are valid")
```

### Adding Entities Programmatically

```python
from xmi.v2.models.xmi_model.xmi_model import XmiModel
from xmi.v2.models.entities.xmi_structural_material import XmiStructuralMaterial
from xmi.v2.models.enums.xmi_structural_material_type_enum import XmiStructuralMaterialTypeEnum

# Create model
model = XmiModel(
    name="My Custom Model",
    xmi_version="2.0",
    application_name="Python Script",
    application_version="1.0"
)

# Add entities manually
steel = XmiStructuralMaterial(
    id="mat_001",
    name="Steel S355",
    material_type=XmiStructuralMaterialTypeEnum.STEEL,
    grade=355.0,
    unit_weight=7850.0
)

concrete = XmiStructuralMaterial(
    id="mat_002",
    name="Concrete C30",
    material_type=XmiStructuralMaterialTypeEnum.CONCRETE,
    grade=30.0,
    unit_weight=2400.0
)

model.entities.append(steel)
model.entities.append(concrete)

print(f"Model '{model.name}' has {len(model.entities)} entities")
```

## Parsing Process Details

### Entity Parsing Flow

When `load_from_dict()` processes entities:

1. **Extract entity list**: Gets "Entities" key from input dictionary
2. **For each entity dictionary**:
   - Extract `EntityType` field
   - Look up entity class in `ENTITY_CLASS_MAPPING`
   - If type not recognized: Log error, continue to next
   - Try to instantiate:
     - If class has `from_dict()` method: Call it
     - Otherwise: Use `model_validate()` (Pydantic)
   - If successful: Append to `self.entities`
   - If error occurs: Log error with exception details

### Relationship Parsing Flow

When `load_from_dict()` processes relationships:

1. **Extract relationship list**: Gets "Relationships" key from input dictionary
2. **For each relationship dictionary**:
   - Extract `EntityType` field
   - Look up relationship class in `RELATIONSHIP_CLASS_MAPPING`
   - If type not recognized: Log error, continue to next
   - Extract `Source` and `Target` IDs
   - Find source entity using `find_entity()`
   - Find target entity using `find_entity()`
   - If either entity not found: Log error, continue to next
   - Remove `Source` and `Target` from dict (replaced with entity objects)
   - Try to instantiate relationship with entity objects
   - If successful: Append to `self.relationships`
   - If error occurs: Log error with exception details

### Entity Type Mapping

Entities are resolved using `ENTITY_CLASS_MAPPING` from `xmi.v2.utils.xmi_entity_type_mapping`:

```python
ENTITY_CLASS_MAPPING = {
    "XmiStructuralMaterial": XmiStructuralMaterial,
    "XmiCrossSection": XmiCrossSection,
    "XmiStructuralCurveMember": XmiStructuralCurveMember,
    "XmiStructuralSurfaceMember": XmiStructuralSurfaceMember,
    "XmiStructuralPointConnection": XmiStructuralPointConnection,
    "XmiStorey": XmiStorey,
    "XmiPoint3D": XmiPoint3D,
    "XmiLine3D": XmiLine3D,
    "XmiArc3D": XmiArc3D,
    # ... more types
}
```

### Relationship Type Mapping

Relationships are resolved using `RELATIONSHIP_CLASS_MAPPING`:

```python
RELATIONSHIP_CLASS_MAPPING = {
    "XmiHasStructuralMaterial": XmiHasStructuralMaterial,
    "XmiHasCrossSection": XmiHasCrossSection,
    "XmiHasStructuralPointConnection": XmiHasStructuralPointConnection,
    "XmiHasStructuralStorey": XmiHasStructuralStorey,
    "XmiHasGeometry": XmiHasGeometry,
    # ... more types
}
```

## Validation Rules

### Field Validation

The `validate_strings` validator ensures metadata fields are strings:

```python
@field_validator('name', 'xmi_version', 'application_name', 'application_version', mode="before")
@classmethod
def validate_strings(cls, v):
    if v is not None and not isinstance(v, str):
        raise TypeError("Value must be a string or None")
    return v
```

This prevents non-string values in metadata fields.

### Pydantic Configuration

```python
model_config = ConfigDict(
    populate_by_name=True,      # Allow both alias and field name
    arbitrary_types_allowed=True # Allow non-Pydantic types like XmiBaseEntity
)
```

- `populate_by_name=True`: Accepts both "Name" and "name" in input
- `arbitrary_types_allowed=True`: Allows storing entity objects (which may not be strict Pydantic models)

## Error Handling

### Error Categories

| Error Type | When It Occurs | Example Message |
|------------|----------------|-----------------|
| Unknown entity type | Entity type not in mapping | "Entity type 'XmiUnknownEntity' is not recognized." |
| Entity instantiation failure | Pydantic validation fails | "Failed to instantiate entity: 1 validation error for XmiStructuralMaterial..." |
| Unknown relationship type | Relationship type not in mapping | "Relationship type 'XmiUnknownRelationship' is not recognized." |
| Missing source/target | Referenced entity ID doesn't exist | "Missing source or target entity for relationship." |
| Relationship instantiation failure | Relationship validation fails | "Failed to instantiate relationship: name field required" |

### Error Accumulation

- Errors are **non-fatal**: parsing continues after an error
- Allows **partial model loading**: successfully parsed entities are kept
- Enables **error analysis**: all errors are collected in one list

### Example: Handling Specific Error Types

```python
model = XmiModel()
model.load_from_dict(xmi_data)

# Categorize errors
unknown_types = [e for e in model.errors if "not recognized" in e.message]
validation_errors = [e for e in model.errors if "Failed to instantiate" in e.message]
reference_errors = [e for e in model.errors if "Missing source or target" in e.message]

print(f"Unknown types: {len(unknown_types)}")
print(f"Validation errors: {len(validation_errors)}")
print(f"Reference errors: {len(reference_errors)}")

# Log details for validation errors
for error in validation_errors:
    print(f"\n{error.entity_type} at index {error.index}:")
    print(f"  {error.message}")
```

## Common Use Cases

### 1. Loading and Inspecting Models

```python
import json
from xmi.v2.models.xmi_model.xmi_model import XmiModel

def load_and_inspect(file_path: str):
    """Load XMI file and print summary"""
    with open(file_path) as f:
        xmi_data = json.load(f)

    model = XmiModel()
    model.load_from_dict(xmi_data)

    print(f"Model: {model.name}")
    print(f"Entities: {len(model.entities)}")
    print(f"Relationships: {len(model.relationships)}")
    print(f"Errors: {len(model.errors)}")

    return model
```

### 2. Extracting Specific Entity Types

```python
from xmi.v2.models.xmi_model.xmi_model import XmiModel
from xmi.v2.models.entities.xmi_structural_curve_member import XmiStructuralCurveMember

def extract_beams(model: XmiModel) -> list:
    """Extract all curve members (beams/columns) from model"""
    return [e for e in model.entities if isinstance(e, XmiStructuralCurveMember)]

model = XmiModel()
model.load_from_dict(xmi_data)

beams = extract_beams(model)
print(f"Found {len(beams)} structural members")
```

### 3. Building Relationship Graphs

```python
from xmi.v2.models.xmi_model.xmi_model import XmiModel
from collections import defaultdict

def build_relationship_graph(model: XmiModel) -> dict:
    """Build a graph of entity relationships"""
    graph = defaultdict(list)

    for rel in model.relationships:
        source_id = rel.source.id
        target_id = rel.target.id
        graph[source_id].append((rel.entity_type, target_id))

    return dict(graph)

model = XmiModel()
model.load_from_dict(xmi_data)

graph = build_relationship_graph(model)
for source_id, connections in graph.items():
    print(f"{source_id}:")
    for rel_type, target_id in connections:
        print(f"  → {rel_type} → {target_id}")
```

## Notes

### Thread Safety

- `XmiModel` is **not thread-safe** during `load_from_dict()`
- Do not modify `entities` or `relationships` lists from multiple threads
- For concurrent processing, create separate model instances

### Memory Considerations

- Large models with thousands of entities consume significant memory
- Consider processing in batches for very large XMI files
- Use `del model` or `model = None` to free memory when done

### Performance

- `find_entity()` is O(n) - linear search through entities
- For frequent lookups, create an ID → entity mapping:
  ```python
  entity_map = {e.id: e for e in model.entities}
  entity = entity_map.get(entity_id)
  ```

### Version Differences (v1 vs v2)

**v2 (this version):**
- Pydantic-based with automatic validation
- Uses mapping dictionaries for type resolution
- Better error messages
- Field aliases for format compatibility

**v1:**
- Uses `__slots__` for memory efficiency
- Explicit entity creation in XmiManager
- Manual validation
- More procedural parsing approach

### Best Practices

1. **Always check errors**: After loading, inspect `model.errors`
2. **Use type checking**: Filter entities with `isinstance()`
3. **Cache entity lookups**: Create ID mappings for repeated lookups
4. **Validate relationships**: Check that source/target entities exist
5. **Export for debugging**: Use `model_dump()` to inspect parsed data

## Related Classes

- **`XmiManager`**: Entry point that creates and populates XmiModel instances
- **`XmiBaseEntity`**: Base class for all entity types
- **`XmiBaseRelationship`**: Base class for all relationship types
- **`ErrorLog`**: Pydantic model for tracking parsing errors
- **Entity classes**: XmiStructuralMaterial, XmiCrossSection, XmiStructuralCurveMember, etc.
- **Relationship classes**: XmiHasStructuralMaterial, XmiHasCrossSection, etc.

## See Also

- [XmiManager.md](XmiManager.md) - Manager class that creates XmiModel instances
- [XmiStructuralMaterial.md](../entities/XmiStructuralMaterial.md) - Material entity documentation
- [XmiStructuralPointConnection.md](../entities/XmiStructuralPointConnection.md) - Point connection documentation
- [XmiBaseEntity.md](../bases/XmiBaseEntity.md) - Base entity class documentation (to be created)
- [XmiBaseRelationship.md](../bases/XmiBaseRelationship.md) - Base relationship class documentation (to be created)
