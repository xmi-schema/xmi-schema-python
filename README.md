# XMI Schema Python Library

[![PyPI version](https://img.shields.io/pypi/v/xmi.svg)](https://pypi.org/project/xmi/)
[![Python Version](https://img.shields.io/pypi/pyversions/xmi.svg)](https://pypi.org/project/xmi/)
[![License](https://img.shields.io/github/license/xmi-schema/xmi-schema-python)](https://github.com/xmi-schema/xmi-schema-python/blob/main/LICENSE)
[![Tests](https://github.com/xmi-schema/xmi-schema-python/workflows/Pull%20Request%20Validation/badge.svg)](https://github.com/xmi-schema/xmi-schema-python/actions)

A Python library for interpreting and managing XMI (Cross Model Information) schema data. XMI is an open-source schema for representing built environment information using graph methodology.

## Overview

The `xmi-schema-python` library provides a robust framework for reading, parsing, and managing structural data from JSON dictionaries, converting them into structured Python objects that represent materials, cross-sections, members, connections, and geometric elements.

## Feature Parity Status

As of **v0.4.0**, Phase 5 of the feature-parity plan is complete: base physical entities, their analytical bridge (`XmiHasStructuralCurveMember`), and the coordinate deduplication point factory are all implemented and fully tested. Phase 6 adds end-to-end integration coverage plus documentation for the new graph patterns so downstream applications can rely on physical ↔ analytical mappings out of the box. This keeps the Python implementation aligned with the C# 0.8.0 reference and ready for the final parity push.

## Features

- **Two parallel implementations** (v1 and v2) with different architectural approaches
- **Comprehensive entity support** for structural engineering elements
- **Pydantic-based validation** (v2) for type safety and data integrity
- **Shape parameter system** supporting 18+ cross-section types
- **Relationship tracking** between entities
- **Error handling** with detailed logging
- **Well-tested** with 138 unit tests and 72% code coverage

## Installation

```bash
pip install xmi
```

### Development Installation

```bash
git clone https://github.com/xmi-schema/xmi-schema-python.git
cd xmi-schema-python
poetry install
```

## Quick Start

### Using v2 (Recommended - Pydantic-based)

```python
from xmi.v2.models.xmi_model.xmi_manager import XmiManager
import json

# Load XMI data from JSON file
with open('your_xmi_data.json', 'r') as f:
    xmi_dict = json.load(f)

# Parse the XMI data
manager = XmiManager()
xmi_model = manager.read_xmi_dict(xmi_dict)

# Access entities
materials = [e for e in xmi_model.entities
             if e.__class__.__name__ == 'XmiStructuralMaterial']
members = [e for e in xmi_model.entities
           if e.__class__.__name__ == 'XmiStructuralCurveMember']

# Check for errors
if xmi_model.errors:
    for error in xmi_model.errors:
        print(f"Error: {error.message}")
```

### Physical Entities & Analytical Bridges

```python
from xmi.v2.models.xmi_model.xmi_manager import XmiManager

manager = XmiManager()
xmi_model = manager.read_xmi_dict(physical_model_dict)  # contains XmiBeam/XmiColumn + curves

beams = [e for e in xmi_model.entities if e.entity_type == "XmiBeam"]
bridges = [
    rel for rel in xmi_model.relationships
    if rel.entity_type == "XmiHasStructuralCurveMember"
]

for bridge in bridges:
    print(f"Physical {bridge.source.name} → Analytical {bridge.target.name}")
```

Each bridge guarantees that the physical entity shares a deduplicated coordinate graph with its analytical counterpart, so graph queries can follow identity relationships rather than re-computing geometry.

### Using v1 (Legacy - Slots-based)

```python
from xmi.v1.xmi_manager import XmiManager
import json

# Load and parse XMI data
with open('your_xmi_data.json', 'r') as f:
    xmi_dict = json.load(f)

manager = XmiManager()
xmi_model = manager.read_xmi_dict(xmi_dict)

# Access entities
materials = [e for e in xmi_model.entities
             if isinstance(e, XmiStructuralMaterial)]
```

## Implemented Entities

### Core Structural Entities

| Entity Name | v1 Status | v2 Status | Description |
|-------------|-----------|-----------|-------------|
| **StructuralMaterial** | ![DONE](https://img.shields.io/badge/Status-DONE-green) | ![DONE](https://img.shields.io/badge/Status-DONE-green) | Material definitions (concrete, steel, timber, etc.) |
| **StructuralPointConnection** | ![DONE](https://img.shields.io/badge/Status-DONE-green) | ![DONE](https://img.shields.io/badge/Status-DONE-green) | Nodal points in 3D space with coordinates |
| **CrossSection** | ![DONE](https://img.shields.io/badge/Status-DONE-green) | ![DONE](https://img.shields.io/badge/Status-DONE-green) | Cross-section definitions with shape parameters |
| **StructuralCurveMember** | ![DONE](https://img.shields.io/badge/Status-DONE-green) | ![DONE](https://img.shields.io/badge/Status-DONE-green) | Linear structural members (beams, columns, braces) |
| **StructuralSurfaceMember** | ![DONE](https://img.shields.io/badge/Status-DONE-green) | ![DONE](https://img.shields.io/badge/Status-DONE-green) | Surface elements (slabs, walls, plates) |
| **StructuralStorey** | ![TODO](https://img.shields.io/badge/Status-TODO-red) | ![DONE](https://img.shields.io/badge/Status-DONE-green) | Building level/storey definitions |
| **StructuralUnit** | ![PARTIAL](https://img.shields.io/badge/Status-PARTIAL-yellow) | ![DONE](https://img.shields.io/badge/Status-DONE-green) | Unit system definitions (SI, Imperial) |
| **StructuralModel** | ![TODO](https://img.shields.io/badge/Status-TODO-red) | ![TODO](https://img.shields.io/badge/Status-TODO-red) | Top-level model container |

### Geometry Classes

| Geometry Type | v1 Status | v2 Status | Description |
|---------------|-----------|-----------|-------------|
| **Point3D** | ![DONE](https://img.shields.io/badge/Status-DONE-green) | ![DONE](https://img.shields.io/badge/Status-DONE-green) | 3D point coordinates (X, Y, Z) |
| **Line3D** | ![DONE](https://img.shields.io/badge/Status-DONE-green) | ![DONE](https://img.shields.io/badge/Status-DONE-green) | Linear segments between two points |
| **Arc3D** | ![DONE](https://img.shields.io/badge/Status-DONE-green) | ![DONE](https://img.shields.io/badge/Status-DONE-green) | Circular arc segments with center point |
| **Segment** | ![DONE](https://img.shields.io/badge/Status-DONE-green) | ![DONE](https://img.shields.io/badge/Status-DONE-green) | Generic segment wrapper for geometry |

### Relationship Types

| Relationship | v1 Status | v2 Status | Purpose |
|--------------|-----------|-----------|---------|
| **HasStructuralMaterial** | ![DONE](https://img.shields.io/badge/Status-DONE-green) | ![DONE](https://img.shields.io/badge/Status-DONE-green) | Links entities to material definitions |
| **HasCrossSection** | ![DONE](https://img.shields.io/badge/Status-DONE-green) | ![DONE](https://img.shields.io/badge/Status-DONE-green) | Links members to cross-section definitions |
| **HasStructuralNode** | ![DONE](https://img.shields.io/badge/Status-DONE-green) | ![DONE](https://img.shields.io/badge/Status-DONE-green) | Links members to point connections |
| **HasSegment** | ![DONE](https://img.shields.io/badge/Status-DONE-green) | ![DONE](https://img.shields.io/badge/Status-DONE-green) | Links members to geometric segments |
| **HasGeometry** | ![DONE](https://img.shields.io/badge/Status-DONE-green) | ![DONE](https://img.shields.io/badge/Status-DONE-green) | Links entities to geometric elements |
| **HasLine3D** | ![DONE](https://img.shields.io/badge/Status-DONE-green) | ![DONE](https://img.shields.io/badge/Status-DONE-green) | Links segments to line geometry |
| **HasPoint3D** | ![DONE](https://img.shields.io/badge/Status-DONE-green) | ![DONE](https://img.shields.io/badge/Status-DONE-green) | Links entities to point geometry |
| **HasStructuralStorey** | ![TODO](https://img.shields.io/badge/Status-TODO-red) | ![DONE](https://img.shields.io/badge/Status-DONE-green) | Links entities to storey definitions |

## Supported Cross-Section Shapes

The library supports 18 different cross-section shape types with strongly-typed parameters:

### Solid Sections
- **Circular** - Parameters: `D` (diameter)
- **Rectangular** - Parameters: `H` (height), `B` (width)

### Structural Steel Shapes
- **I-Shape** - Parameters: `D`, `B`, `T` (flange thickness), `t` (web thickness), `r` (radius)
- **C-Shape** - Parameters: `D`, `B`, `T`, `t`, `r`
- **T-Shape** - Parameters: `D`, `B`, `T`, `t`, `r`
- **L-Shape** - Parameters: `D`, `B`, `T`, `t`

### Hollow Sections
- **Circular Hollow** - Parameters: `D` (outer diameter), `T` (wall thickness)
- **Square Hollow** - Parameters: `D` (outer dimension), `T` (wall thickness)
- **Rectangular Hollow** - Parameters: `H` (height), `B` (width), `T` (wall thickness)

### Specialty Shapes
- **Trapezium** - Parameters: `H`, `B1` (top width), `B2` (bottom width)
- **Polygon** - Parameters: `N` (number of sides), `R` (circumradius)

### Angle Sections
- **Equal Angle** - Parameters: `D`, `B`, `T`, `t`
- **Unequal Angle** - Parameters: `D`, `B`, `T1`, `T2`, `t`

### Bar Sections
- **Flat Bar** - Parameters: `H`, `B`
- **Square Bar** - Parameters: `D`
- **Round Bar** - Parameters: `D`
- **Deformed Bar** - Parameters: `D`

### Custom
- **Custom** - Flexible parameters for non-standard shapes
- **Unknown** - Fallback for unrecognized shapes

## Architecture

### v1 Implementation (`src/xmi/v1/`)
- Memory-efficient using `__slots__`
- Manual property setters/getters
- Procedural entity creation in `XmiManager.read_xmi_dict()`
- Direct dictionary parsing

### v2 Implementation (`src/xmi/v2/`)
- **Pydantic models** for validation and type safety
- Modular architecture with entity type mappings
- Mapping-based entity resolution via `ENTITY_CLASS_MAPPING`
- `XmiModel.load_from_dict()` handles instantiation
- Located in `src/xmi/v2/utils/xmi_entity_type_mapping.py`

### Key Differences
- **v1**: Procedural parsing with explicit entity creation logic
- **v2**: Declarative mapping approach with automatic type resolution

### Point Factory & Coordinate Deduplication

The v2 model keeps a single source of truth for `Point3D` data by routing all coordinate creation through `XmiModel.create_point_3d()`. When `XmiModel.load_from_dict()` instantiates geometry-heavy entities (such as `XmiStructuralPointConnection`, `XmiLine3D`, and `XmiArc3D`), it injects this point factory into their `from_dict` loaders. The factory quantizes coordinates using a tight tolerance (default `1e-10`) and reuses an existing `XmiPoint3D` instance whenever the incoming coordinates match within that tolerance. This lightweight cache means:

- Members, segments, and relationships that reference the same coordinates automatically share the same `XmiPoint3D` object, producing a graph-friendly topology.
- Structural relationships like `XmiHasStructuralCurveMember` can rely on identity equality instead of manual coordinate comparisons when traversing the graph.
- Geometry parsing remains deterministic even if the input JSON contains duplicate nodes, since the first occurrence becomes canonical.

You can opt into the same behavior for custom loaders by exposing a `point_factory` parameter on your entity’s `from_dict()` function and calling it instead of instantiating `XmiPoint3D` directly:

```python
@classmethod
def from_dict(cls, data: dict, point_factory: Callable[[float, float, float], XmiPoint3D]):
    x, y, z = data["Point"]["X"], data["Point"]["Y"], data["Point"]["Z"]
    point = point_factory(x, y, z)
    return cls(point=point), []
```

This pattern keeps the object graph compact while still letting you model additional tolerances or caching strategies by swapping in a different factory.

## Development

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=src/xmi --cov-report=html --cov-report=term

# Run specific test suite
poetry run pytest tests/xmi/v2/

# Run specific test file
poetry run pytest tests/xmi/v2/test_entities/test_xmi_material.py
```

### Test Coverage

Current test coverage: **~72%** (188 tests passing)

- **v1 Coverage**: ~75% average
- **v2 Coverage**: ~85% average
- **Total Tests**: 188 passing
- **Coverage Report**: Generated in `htmlcov/index.html`

#### Generating Coverage Reports Locally

```bash
# Generate coverage report with HTML output
poetry run pytest --cov=src/xmi --cov-report=html --cov-report=term

# Open the HTML report in your browser
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

#### Coverage in CI/CD

Coverage is automatically calculated on every PR:
- **PR Validation**: Runs tests with coverage on Python 3.12
- **Coverage Comment**: Bot comments coverage metrics on PRs
- **Artifacts**: HTML coverage reports are uploaded as workflow artifacts
- **No Cloud Service**: All coverage processing happens locally in GitHub Actions

The PR validation workflow will:
1. Run all tests with coverage tracking
2. Generate XML and HTML coverage reports
3. Calculate coverage percentage
4. Post a comment on the PR with coverage metrics
5. Upload the full HTML report as an artifact (downloadable for 30 days)

### Building the Package

```bash
# Build distribution
poetry build

# Install locally (Linux/Mac)
bash install_package.sh

# Install locally (Windows)
setup_and_install.bat
```

## Project Structure

```
xmi-schema-python/
├── src/xmi/
│   ├── v1/                      # Legacy implementation
│   │   ├── entities/            # Entity classes with __slots__
│   │   ├── enums/               # Enumeration types
│   │   ├── geometries/          # 3D geometry classes
│   │   ├── relationships/       # Entity relationships
│   │   ├── shapes/              # Shape definitions
│   │   ├── xmi_manager.py       # Entry point for v1
│   │   └── xmi_model.py         # Model container
│   │
│   └── v2/                      # Modern Pydantic implementation
│       ├── models/
│       │   ├── bases/           # Base classes for entities/relationships
│       │   ├── entities/        # Pydantic entity models
│       │   ├── enums/           # Typed enumerations
│       │   ├── geometries/      # Pydantic geometry models
│       │   ├── relationships/   # Pydantic relationship models
│       │   ├── shape_parameters/# Strongly-typed shape parameters
│       │   └── xmi_model/       # Model and manager
│       └── utils/
│           ├── xmi_entity_type_mapping.py  # Entity type mappings
│           └── xmi_errors.py    # Error definitions
│
├── tests/                       # Comprehensive test suite
│   ├── xmi/v1/                 # v1 tests
│   └── xmi/v2/                 # v2 tests
│
├── .github/workflows/           # CI/CD workflows
│   ├── pr-validation.yml       # PR test validation
│   └── python-publish.yml      # PyPI publishing
│
├── pyproject.toml              # Poetry configuration
├── pytest.ini                  # Pytest configuration
└── README.md                   # This file
```

## Error Handling

Both versions include comprehensive error handling:

```python
# Errors are accumulated without stopping execution
xmi_model = manager.read_xmi_dict(xmi_dict)

# Check for parsing errors
if xmi_model.errors:
    for error in xmi_model.errors:
        print(f"Entity: {error.entity_type}")
        print(f"Index: {error.entity_index}")
        print(f"Message: {error.message}")
        if error.raw_object:
            print(f"Raw data: {error.raw_object}")
```

### Error Types (v2)
- `XmiError` - Base error class
- `XmiInconsistentDatatypeError` - Type mismatch errors
- `XmiMissingReferenceInstanceError` - Missing entity references
- `XmiMissingRequiredAttributeError` - Required field missing

## CI/CD

The project uses GitHub Actions for continuous integration:

### Pull Request Validation
- Runs on all PRs to `main` branch
- Tests against Python 3.9, 3.10, 3.11, 3.12
- All tests must pass before merging
- Uses Poetry for dependency management
- Cached dependencies for faster builds

### Publishing Workflow
- Automatic semantic versioning
- Publishes to PyPI on merge to `main`
- Creates GitHub releases with artifacts
- Updates version in `pyproject.toml`

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Ensure all tests pass: `poetry run pytest`
5. Submit a pull request

### Adding New Entities (v2)

1. Create entity class in `src/xmi/v2/models/entities/`
2. Add tests in `tests/xmi/v2/test_entities/`
3. Add to `ENTITY_CLASS_MAPPING` in `xmi_entity_type_mapping.py`
4. If relationships exist, add to `RELATIONSHIP_CLASS_MAPPING`
5. Update dependency order in `_rearrange_xmi_dict()` if needed

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links

- **PyPI**: https://pypi.org/project/xmi/
- **GitHub**: https://github.com/xmi-schema/xmi-schema-python
- **XMI Schema**: https://xmi-schema.org
- **Documentation**: [Coming soon]

## Acknowledgments

Based on the XMI Schema specification and inspired by the C# implementation:
- [XMI Schema C#](https://github.com/xmi-schema/xmi-schema-csharp)
- [Shape Parameters Reference](https://github.com/xmi-schema/xmi-schema-csharp/blob/main/XmiShapeEnumParameters.md)

## Version History

- **v0.4.0** - Physical entities + bridges, coordinate deduplication, Phase 6 docs/tests
- **v0.3.0** - Added shape parameters, improved v2 implementation
- **v0.2.x** - Enhanced entity support, improved testing
- **v0.1.x** - Initial release with v1 implementation

---

**Status Legend:**
- ![DONE](https://img.shields.io/badge/Status-DONE-green) - Fully implemented and tested
- ![PARTIAL](https://img.shields.io/badge/Status-PARTIAL-yellow) - Partially implemented
- ![TODO](https://img.shields.io/badge/Status-TODO-red) - Not yet implemented
