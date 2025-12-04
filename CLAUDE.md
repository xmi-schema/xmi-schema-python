# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is the `xmi-schema-python` library - a Python package for interpreting and managing XMI (Cross Model Information) schema data. XMI is an open source schema for representing built environment information using graph methodology. The library reads structural data from JSON dictionaries and converts them into structured Python objects representing materials, cross-sections, members, connections, and geometric elements.

## Project Structure

The codebase has **two parallel implementations** (v1 and v2) with different architectural approaches:

### v1 Implementation (`src/xmi/v1/`)
- Uses `__slots__` for memory efficiency and manual property setters/getters
- Manual relationship and entity management in `XmiManager.read_xmi_dict()`
- Legacy implementation with direct dictionary parsing

### v2 Implementation (`src/xmi/v2/`)
- Uses Pydantic models for validation and data handling
- More modular architecture with entity type mappings
- `XmiModel.load_from_dict()` handles entity/relationship instantiation via mapping dictionaries
- Entity and relationship classes are mapped in `src/xmi/v2/utils/xmi_entity_type_mapping.py`

**Key architectural difference**: v1 uses procedural parsing with explicit entity creation logic, while v2 uses a mapping-based approach where entity types are resolved through `ENTITY_CLASS_MAPPING` and `RELATIONSHIP_CLASS_MAPPING` dictionaries.

## Core Architecture

### Base Class Hierarchy

```
XmiBaseEntity
├─ XmiBasePhysicalEntity (type = Physical)
│  ├─ XmiBeam / XmiColumn
│  └─ XmiSlab / XmiWall
└─ XmiBaseStructuralAnalyticalEntity (type = StructuralAnalytical)
   ├─ XmiStructuralPointConnection
   ├─ XmiStructuralCurveMember
   └─ XmiStructuralSurfaceMember
```

All concrete entities inherit from the appropriate branch so `entity_type`/`type` are auto-filled before validation.

### Entity-Relationship Model
Both versions follow an entity-relationship architecture:
- **Entities**: Base classes (`XmiBaseEntity` in v1, Pydantic models in v2) represent structural elements (materials, connections, members, geometries)
- **Relationships**: Connect entities together (e.g., `XmiHasStructuralMaterial`, `XmiHasGeometry`, `XmiHasSegment`)
- **XmiModel**: Container for entities and relationships with error logging via `ErrorLog` class
- **XmiManager**: Entry point that reads XMI dictionaries and creates XmiModel instances

### Key Entity Types
- `XmiStructuralMaterial`: Material definitions (concrete, steel, etc.)
- `XmiStructuralPointConnection`: Nodal points in 3D space
- `XmiCrossSection`: Cross-section definitions with material references
- `XmiStructuralCurveMember`: Linear structural members (beams, columns) with segments
- `XmiStructuralSurfaceMember`: Surface elements (slabs, walls) with edge definitions
- `XmiSegment`: Individual geometric segments (lines, arcs) connecting nodes
- Geometry classes: `XmiPoint3D`, `XmiLine3D`, `XmiArc3D`

### Physical Entity Layer
- `XmiBeam`, `XmiColumn`: Physical members that mirror analytical curve members
- `XmiSlab`, `XmiWall`: Plate elements represented as physical metadata containers
- `XmiBasePhysicalEntity`: Shared parent that auto-sets the `type`/domain to `Physical`
- `XmiHasStructuralCurveMember`: Relationship linking a physical element to its analytical `XmiStructuralCurveMember`

These entities are fully implemented in v2 and mapped through `ENTITY_CLASS_MAPPING`, enabling one-to-one parity with the C# 0.8.0 reference.

### Dependency Order
When parsing XMI dictionaries, entities must be created in dependency order:
1. `StructuralMaterial` (no dependencies)
2. `StructuralPointConnection` (creates `XmiPoint3D` geometry)
3. `CrossSection` (references materials)
4. `StructuralCurveMember` (references cross-sections and point connections)
5. `StructuralSurfaceMember` (references materials and point connections)

The `_rearrange_xmi_dict()` method enforces this order.

## Development Commands

### Testing
```bash
# Run all tests
pytest

# Run tests for specific version
pytest tests/xmi/v1/
pytest tests/xmi/v2/

# Run specific test file
pytest tests/xmi/v1/test_scripts/test_xmi_manager_v1.py

# Run specific test function
pytest tests/xmi/v1/test_scripts/test_xmi_manager_v1.py::test_xmi_manager_1
```

### Building the Package
```bash
# Build the package
python -m build

# Build and install locally (Linux/Mac)
bash install_package.sh

# Build and install locally (Windows)
setup_and_install.bat
```

### Running After Installation
```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Run post-install tests
pytest after_install_tests/
```

## Important Implementation Details

### Error Handling
Both versions use `ErrorLog` objects to track parsing errors without stopping execution:
- Errors are accumulated in `xmi_model.errors` list
- Allows partial model loading even when some entities fail to parse
- Each error includes: entity type, index, message, and optional raw object data

### Segment Creation
`XmiSegment` objects are created during member parsing (not from input data directly):
- Segments represent geometry between consecutive nodes
- Segment type is parsed from string attribute (e.g., "Line", "CircularArc")
- v1 uses `SEGMENT_TYPE_MAPPING` dictionary to map segment types to geometry classes
- Each segment links to begin/end nodes and contains a geometry object

### Relationship Creation
Relationships are explicitly created to track connections between entities:
- `XmiHasStructuralMaterial`: Links cross-sections/surfaces to materials
- `XmiHasCrossSection`: Links curve members to cross-sections
- `XmiHasStructuralNode`: Links members/segments to point connections
- `XmiHasSegment`: Links members to their segments
- `XmiHasGeometry`: Links entities to geometric elements
- `XmiHasStructuralCurveMember`: Bridges `XmiBeam`/`XmiColumn` instances to analytical curve members, ensuring graph traversal from physical to analytical layers is a single hop

### Physical-to-Analytical Mapping Pattern
1. Parse physical entities (beam/column) via `XmiModel.load_from_dict()`—`entity_type` auto-assigns.
2. Parse their analytical `XmiStructuralCurveMember` counterparts.
3. During relationship parsing, `XmiHasStructuralCurveMember` validates the pairing (physical source, analytical target).
4. Downstream queries grab the relationship edge to pivot between representations, allowing graph algorithms (e.g., QuikGraph / NetworkX) to reason across layers.

### v2 Pydantic Models
When working with v2 models:
- Use `model_validate()` for validation from dictionaries
- Custom `from_dict()` methods exist on some entities for complex parsing
- Field aliases support both PascalCase (external) and snake_case (internal) naming
- Set `arbitrary_types_allowed=True` in model config when using non-Pydantic types

## Testing Patterns

Tests use JSON input files located in:
- `tests/xmi/v1/test_inputs/` (v1 tests)
- `tests/xmi/v2/test_inputs/` (v2 tests)

Typical test pattern:
```python
xmi_manager = XmiManager()
xmi_model = xmi_manager.read_xmi_dict(json_dict)

# Query entities by type
materials = [obj for obj in xmi_model.entities if isinstance(obj, XmiStructuralMaterial)]

# Check relationships
relationships = xmi_model.find_relationships_by_source(source_entity)
```

## Package Information

- **Package Name**: `xmi`
- **Current Version**: 0.4.0
- **Build System**: poetry-core
- **Python Requirement**: >=3.9
- **Testing Framework**: pytest ^8.3.5
- **Repository**: https://github.com/darellchua2/xmi-schema

## Version Comparison

| Version | Highlights | Feature Parity |
|---------|------------|----------------|
| v0.4.0 | Physical entities + bridges, coordinate deduplication, integration docs/tests | Phase 5 complete, Phase 6 docs/testing complete |
| v0.3.x | Expanded shape parameters, improved v2 coverage | ~60% parity |
| v0.2.x | Added materials + curve member refactors | ~45% parity |
| v0.1.x | Initial v1 release | Baseline |

## When Adding New Entity Types

1. Create entity class in appropriate `entities/` directory
2. Add corresponding tests in `tests/xmi/v{1,2}/test_entities/`
3. For v2: Add entity to `ENTITY_CLASS_MAPPING` in `xmi_entity_type_mapping.py`
4. If entity has relationships, create relationship class in `relationships/`
5. For v2: Add relationship to `RELATIONSHIP_CLASS_MAPPING`
6. Update `_rearrange_xmi_dict()` if entity has dependencies
7. Add parsing logic to `XmiManager.read_xmi_dict()` (v1) or ensure proper `from_dict()` method (v2)
