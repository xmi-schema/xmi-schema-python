# XmiManager

## Overview

`XmiManager` is the primary entry point for loading and managing XMI (Cross Model Information) data in the xmi-schema-python library. It orchestrates the parsing of XMI dictionaries (typically loaded from JSON files) and converts them into structured `XmiModel` objects containing validated entities and relationships. The manager handles dependency ordering to ensure entities are created in the correct sequence and maintains a collection of all loaded models.

XmiManager serves as:
- **Entry point** for loading XMI data from dictionaries
- **Orchestrator** for entity dependency ordering
- **Collection manager** for multiple XmiModel instances
- **Abstraction layer** between raw XMI data and typed Python objects

## Class Hierarchy

- **Parent**: None (standalone class)
- **Module**: `xmi.v2.models.xmi_model.xmi_manager`
- **Implementation**: Pure Python class (not a Pydantic model)

## Properties

### Instance Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `models` | `List[XmiModel]` | `[]` | Collection of all XmiModel instances created by this manager |

## Methods

### Public Methods

#### `read_xmi_dict(xmi_dict: Dict[str, Any]) -> XmiModel`

Primary method for loading XMI data from a dictionary.

**Parameters**:
- `xmi_dict`: Dictionary containing XMI data with "Entities" and "Relationships" keys

**Returns**:
- `XmiModel`: A fully populated model with entities, relationships, and error logs

**Process**:
1. Rearranges dictionary keys to ensure entities are processed in dependency order
2. Creates a new XmiModel instance
3. Calls `XmiModel.load_from_dict()` to populate entities and relationships
4. Appends the model to the manager's `models` collection
5. Returns the created model

**Example**:
```python
import json
from xmi.v2.models.xmi_model.xmi_manager import XmiManager

# Load XMI data from file
with open("structural_model.json") as f:
    xmi_data = json.load(f)

# Create manager and load model
manager = XmiManager()
model = manager.read_xmi_dict(xmi_data)

# Access loaded entities
print(f"Loaded {len(model.entities)} entities")
print(f"Loaded {len(model.relationships)} relationships")
print(f"Errors encountered: {len(model.errors)}")
```

### Private Methods

#### `_rearrange_xmi_dict(xmi_dict: dict) -> dict`

Internal method that reorders dictionary keys to ensure entities are created in dependency order.

**Parameters**:
- `xmi_dict`: Original XMI dictionary with arbitrary key ordering

**Returns**:
- `dict`: Reordered dictionary with dependency-respecting key sequence

**Dependency Order**:
1. `StructuralMaterial` - No dependencies
2. `StructuralPointConnection` - No entity dependencies (creates own Point3D)
3. `CrossSection` - Depends on StructuralMaterial
4. `StructuralCurveMember` - Depends on CrossSection and StructuralPointConnection
5. `StructuralSurfaceMember` - Depends on StructuralMaterial and StructuralPointConnection
6. All other entity types (if present)

**Why Dependency Order Matters**:
- Materials must exist before cross-sections can reference them
- Point connections must exist before members can reference them as nodes
- Cross-sections must exist before curve members can reference them
- Without correct ordering, relationship validation would fail

## Usage Examples

### Basic Usage - Loading a Model

```python
from xmi.v2.models.xmi_model.xmi_manager import XmiManager
import json

# Load XMI data from JSON file
with open("structure.json") as f:
    xmi_data = json.load(f)

# Create manager and parse
manager = XmiManager()
model = manager.read_xmi_dict(xmi_data)

# Check for errors
if model.errors:
    print(f"Warning: {len(model.errors)} parsing errors occurred")
    for error in model.errors:
        print(f"  - {error.entity_type} at index {error.index}: {error.message}")
else:
    print("Model loaded successfully with no errors")
```

### Querying Loaded Entities

```python
from xmi.v2.models.xmi_model.xmi_manager import XmiManager
from xmi.v2.models.entities.xmi_structural_material import XmiStructuralMaterial
from xmi.v2.models.entities.xmi_structural_cross_section import XmiCrossSection

manager = XmiManager()
model = manager.read_xmi_dict(xmi_data)

# Find all materials
materials = [e for e in model.entities if isinstance(e, XmiStructuralMaterial)]
print(f"Materials: {len(materials)}")
for mat in materials:
    print(f"  - {mat.name}: {mat.material_type.value}")

# Find all cross-sections
cross_sections = [e for e in model.entities if isinstance(e, XmiCrossSection)]
print(f"Cross-sections: {len(cross_sections)}")
```

### Managing Multiple Models

```python
from xmi.v2.models.xmi_model.xmi_manager import XmiManager

manager = XmiManager()

# Load multiple models
model1 = manager.read_xmi_dict(building_a_data)
model2 = manager.read_xmi_dict(building_b_data)
model3 = manager.read_xmi_dict(bridge_data)

# Access all models
print(f"Total models loaded: {len(manager.models)}")
for i, model in enumerate(manager.models):
    print(f"Model {i+1}: {len(model.entities)} entities, {len(model.relationships)} relationships")
```

### Error Handling - Validation Failures

```python
from xmi.v2.models.xmi_model.xmi_manager import XmiManager

# XMI data with invalid material reference
invalid_xmi_data = {
    "Entities": [
        {
            "ID": "cs_001",
            "Name": "300x600mm",
            "EntityType": "XmiCrossSection",
            "Shape": "Rectangular",
            "Area": 0.18
        }
    ],
    "Relationships": [
        {
            "ID": "rel_001",
            "Source": "cs_001",
            "Target": "material_999",  # Material doesn't exist!
            "EntityType": "XmiHasStructuralMaterial"
        }
    ]
}

manager = XmiManager()
model = manager.read_xmi_dict(invalid_xmi_data)

# Check for relationship errors
for error in model.errors:
    if "Missing source or target" in error.message:
        print(f"Broken relationship detected: {error.entity_type}")
        print(f"  Issue: {error.message}")
```

### Accessing Metadata

```python
from xmi.v2.models.xmi_model.xmi_manager import XmiManager

xmi_data_with_metadata = {
    "Name": "Office Building - Main Structure",
    "XmiVersion": "2.0",
    "ApplicationName": "Revit",
    "ApplicationVersion": "2024",
    "Entities": [...],
    "Relationships": [...]
}

manager = XmiManager()
model = manager.read_xmi_dict(xmi_data_with_metadata)

# Access model metadata
print(f"Model Name: {model.name}")
print(f"XMI Version: {model.xmi_version}")
print(f"Created by: {model.application_name} {model.application_version}")
```

### Filtering Entities by Type

```python
from xmi.v2.models.xmi_model.xmi_manager import XmiManager
from xmi.v2.models.entities.xmi_structural_curve_member import XmiStructuralCurveMember
from xmi.v2.models.entities.xmi_structural_surface_member import XmiStructuralSurfaceMember

manager = XmiManager()
model = manager.read_xmi_dict(xmi_data)

# Find all structural members
curve_members = [e for e in model.entities if isinstance(e, XmiStructuralCurveMember)]
surface_members = [e for e in model.entities if isinstance(e, XmiStructuralSurfaceMember)]

print(f"Beams/Columns: {len(curve_members)}")
print(f"Slabs/Walls: {len(surface_members)}")
print(f"Total Members: {len(curve_members) + len(surface_members)}")
```

### Finding Related Entities via Relationships

```python
from xmi.v2.models.xmi_model.xmi_manager import XmiManager
from xmi.v2.models.entities.xmi_structural_cross_section import XmiCrossSection
from xmi.v2.models.relationships.xmi_has_structural_material import XmiHasStructuralMaterial

manager = XmiManager()
model = manager.read_xmi_dict(xmi_data)

# Find a specific cross-section
cross_section = next((e for e in model.entities
                      if isinstance(e, XmiCrossSection)
                      and e.name == "300x600mm"), None)

if cross_section:
    # Find its material relationship
    material_rels = [r for r in model.relationships
                     if isinstance(r, XmiHasStructuralMaterial)
                     and r.source == cross_section]

    if material_rels:
        material = material_rels[0].target
        print(f"Cross-section '{cross_section.name}' uses material '{material.name}'")
```

### Exporting Model Summary

```python
from xmi.v2.models.xmi_model.xmi_manager import XmiManager
from collections import defaultdict

manager = XmiManager()
model = manager.read_xmi_dict(xmi_data)

# Count entities by type
entity_counts = defaultdict(int)
for entity in model.entities:
    entity_counts[entity.entity_type] += 1

# Count relationships by type
rel_counts = defaultdict(int)
for rel in model.relationships:
    rel_counts[rel.entity_type] += 1

# Print summary
print("=== Model Summary ===")
print(f"Model: {model.name or 'Unnamed'}")
print(f"\nEntities:")
for entity_type, count in sorted(entity_counts.items()):
    print(f"  {entity_type}: {count}")
print(f"\nRelationships:")
for rel_type, count in sorted(rel_counts.items()):
    print(f"  {rel_type}: {count}")
print(f"\nErrors: {len(model.errors)}")
```

### Batch Processing Multiple Files

```python
from xmi.v2.models.xmi_model.xmi_manager import XmiManager
import json
from pathlib import Path

def load_xmi_files(directory: str) -> XmiManager:
    """Load all XMI JSON files from a directory"""
    manager = XmiManager()

    for file_path in Path(directory).glob("*.json"):
        try:
            with open(file_path) as f:
                xmi_data = json.load(f)

            model = manager.read_xmi_dict(xmi_data)
            print(f"✓ Loaded {file_path.name}: {len(model.entities)} entities")

            if model.errors:
                print(f"  ⚠ {len(model.errors)} errors in {file_path.name}")

        except Exception as e:
            print(f"✗ Failed to load {file_path.name}: {e}")

    return manager

# Usage
manager = load_xmi_files("./xmi_models/")
print(f"\nTotal models loaded: {len(manager.models)}")
```

## Dependency Order Details

### Why Dependency Order Matters

XMI relationships reference entities by ID. For relationships to be created successfully:
1. **Source entity** must exist before the relationship is processed
2. **Target entity** must exist before the relationship is processed

If entities are processed in the wrong order, relationships will fail to resolve.

### Dependency Chain

```
StructuralMaterial (no dependencies)
    ↓
StructuralPointConnection (no dependencies)
    ↓
CrossSection (references Material via relationship)
    ↓
StructuralCurveMember (references CrossSection and PointConnection via relationships)
    ↓
StructuralSurfaceMember (references Material and PointConnection via relationships)
```

### Example of Incorrect Ordering

**Without `_rearrange_xmi_dict()`:**

```json
{
  "Entities": [
    {"ID": "beam_001", "EntityType": "XmiStructuralCurveMember", ...},
    {"ID": "cs_001", "EntityType": "XmiCrossSection", ...},
    {"ID": "mat_001", "EntityType": "XmiStructuralMaterial", ...}
  ],
  "Relationships": [
    {"Source": "beam_001", "Target": "cs_001", "EntityType": "XmiHasCrossSection"}
  ]
}
```

**Problem**: When parsing `beam_001`, the relationship tries to reference `cs_001` which hasn't been created yet.

**With `_rearrange_xmi_dict()`:**

The method reorders to:
1. Process `mat_001` first
2. Then `cs_001` (can now reference `mat_001`)
3. Finally `beam_001` (can now reference `cs_001`)

Result: All relationships resolve successfully.

## XmiModel Integration

`XmiManager` delegates the actual parsing to `XmiModel.load_from_dict()`. Understanding this delegation is important:

### XmiManager Responsibilities
- Reordering entity keys for dependency resolution
- Managing multiple model instances
- Providing a clean API for users

### XmiModel Responsibilities
- Parsing individual entities using `ENTITY_CLASS_MAPPING`
- Parsing relationships using `RELATIONSHIP_CLASS_MAPPING`
- Validating entity data with Pydantic models
- Tracking errors in `ErrorLog` objects
- Resolving entity references by ID

### Data Flow

```
User Code
    ↓
XmiManager.read_xmi_dict(xmi_dict)
    ↓
XmiManager._rearrange_xmi_dict(xmi_dict)  ← Reorder keys
    ↓
XmiModel() ← Create new model
    ↓
XmiModel.load_from_dict(rearranged_dict)  ← Parse entities & relationships
    ↓
    ├─ Parse Entities (using ENTITY_CLASS_MAPPING)
    ├─ Parse Relationships (using RELATIONSHIP_CLASS_MAPPING)
    ├─ Validate with Pydantic
    └─ Log errors
    ↓
return XmiModel ← Fully populated
```

## Error Handling

### Error Types

XmiManager itself doesn't throw exceptions during parsing. Instead, errors are collected in `model.errors`:

| Error Scenario | Error Message | Cause |
|----------------|---------------|-------|
| Unknown entity type | "Entity type 'XYZ' is not recognized." | Entity type not in `ENTITY_CLASS_MAPPING` |
| Entity validation failure | "Failed to instantiate entity: {exception}" | Pydantic validation failed |
| Unknown relationship type | "Relationship type 'XYZ' is not recognized." | Relationship type not in `RELATIONSHIP_CLASS_MAPPING` |
| Missing source/target | "Missing source or target entity for relationship." | Referenced entity ID doesn't exist |
| Relationship instantiation failure | "Failed to instantiate relationship: {exception}" | Relationship validation failed |

### Error Log Structure

Each error is stored as an `ErrorLog` object with:

```python
class ErrorLog:
    entity_type: str      # Entity or relationship type
    index: int            # Position in the Entities/Relationships list
    message: str          # Human-readable error description
    obj: Optional[str]    # String representation of the problematic data
```

### Handling Errors in Your Code

```python
manager = XmiManager()
model = manager.read_xmi_dict(xmi_data)

# Check if parsing was fully successful
if model.errors:
    print(f"⚠ Parsing completed with {len(model.errors)} errors")

    # Group errors by type
    entity_errors = [e for e in model.errors if "entity" in e.message.lower()]
    relationship_errors = [e for e in model.errors if "relationship" in e.message.lower()]

    print(f"  Entity errors: {len(entity_errors)}")
    print(f"  Relationship errors: {len(relationship_errors)}")

    # Log detailed errors
    for error in model.errors:
        print(f"  [{error.entity_type}] {error.message}")
else:
    print("✓ Model loaded successfully with no errors")

# Continue working with successfully loaded entities
print(f"Successfully loaded: {len(model.entities)} entities")
```

## Common Use Cases

### 1. Loading and Validating XMI Files

```python
import json
from xmi.v2.models.xmi_model.xmi_manager import XmiManager

def validate_xmi_file(file_path: str) -> bool:
    """Validate an XMI file and report any issues"""
    with open(file_path) as f:
        xmi_data = json.load(f)

    manager = XmiManager()
    model = manager.read_xmi_dict(xmi_data)

    if not model.errors:
        print(f"✓ {file_path} is valid")
        return True
    else:
        print(f"✗ {file_path} has {len(model.errors)} errors:")
        for error in model.errors:
            print(f"  - {error.message}")
        return False

# Usage
is_valid = validate_xmi_file("structure.json")
```

### 2. Converting XMI to Custom Format

```python
from xmi.v2.models.xmi_model.xmi_manager import XmiManager
from xmi.v2.models.entities.xmi_structural_material import XmiStructuralMaterial

def extract_material_library(xmi_data: dict) -> dict:
    """Extract materials from XMI and convert to custom format"""
    manager = XmiManager()
    model = manager.read_xmi_dict(xmi_data)

    material_library = {}
    for entity in model.entities:
        if isinstance(entity, XmiStructuralMaterial):
            material_library[entity.id] = {
                "name": entity.name,
                "type": entity.material_type.value,
                "grade": entity.grade,
                "density": entity.unit_weight
            }

    return material_library
```

### 3. Merging Multiple XMI Models

```python
from xmi.v2.models.xmi_model.xmi_manager import XmiManager

def merge_models(xmi_data_list: list) -> dict:
    """Merge multiple XMI models into one manager"""
    manager = XmiManager()

    total_entities = 0
    total_relationships = 0

    for xmi_data in xmi_data_list:
        model = manager.read_xmi_dict(xmi_data)
        total_entities += len(model.entities)
        total_relationships += len(model.relationships)

    return {
        "models": len(manager.models),
        "entities": total_entities,
        "relationships": total_relationships
    }
```

## Notes

### Manager Instance Reuse

- A single `XmiManager` instance can load multiple models
- Each call to `read_xmi_dict()` creates a new `XmiModel` and adds it to `models` list
- Models are independent - no cross-model relationships

### Memory Considerations

- Each `XmiModel` is stored in `manager.models` list
- For large-scale applications, consider clearing old models: `manager.models.clear()`
- Or create a new manager instance when needed

### Thread Safety

- `XmiManager` is **not thread-safe**
- Do not call `read_xmi_dict()` from multiple threads on the same instance
- For concurrent loading, create separate manager instances per thread

### Version Differences (v1 vs v2)

**v2 (this version):**
- Uses Pydantic models for validation
- Entity/relationship types resolved via mapping dictionaries
- `XmiModel.load_from_dict()` handles entity instantiation
- Better error messages and validation

**v1:**
- Uses `__slots__` with manual validation
- Explicit entity creation logic in `XmiManager.read_xmi_dict()`
- `XmiManager` directly creates entity instances
- Manual property setters and getters

### Performance Tips

1. **Pre-validate JSON**: Ensure XMI data is well-formed before passing to manager
2. **Batch loading**: Load multiple files with one manager instance
3. **Error filtering**: If you expect certain errors, filter `model.errors` rather than preventing them
4. **Entity indexing**: For large models, create ID → entity mappings for fast lookup

## Related Classes

- **`XmiModel`**: Container for entities, relationships, and error logs
- **`XmiBaseEntity`**: Base class for all entity types
- **`XmiBaseRelationship`**: Base class for all relationship types
- **`ErrorLog`**: Pydantic model for tracking parsing errors
- **`ENTITY_CLASS_MAPPING`**: Dictionary mapping entity type strings to classes
- **`RELATIONSHIP_CLASS_MAPPING`**: Dictionary mapping relationship type strings to classes

## See Also

- [XmiModel.md](XmiModel.md) - Detailed model documentation (to be created)
- [XmiStructuralMaterial.md](../entities/XmiStructuralMaterial.md) - Material entity documentation
- [XmiStructuralPointConnection.md](../entities/XmiStructuralPointConnection.md) - Point connection documentation
- [XmiCrossSection.md](../entities/XmiCrossSection.md) - Cross-section documentation (to be created)
