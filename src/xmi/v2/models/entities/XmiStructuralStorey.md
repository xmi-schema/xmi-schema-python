# XmiStructuralStorey

## Overview

`XmiStructuralStorey` represents a building level or floor in a multi-storey structural model. It defines the vertical organization of the structure by specifying elevation, mass, and optional reaction forces at each level. Storeys are fundamental for organizing structural elements by level, calculating mass distribution, and analyzing inter-storey drift in seismic or wind analysis.

## Class Hierarchy

- **Parent**: `XmiBaseEntity`
- **Version**: v2 (Pydantic-based implementation)
- **Module**: `src/xmi/v2/models/entities/xmi_structural_storey.py`

## Properties

### Required Properties

| Property | Type | Description | Validation |
|----------|------|-------------|------------|
| `storey_elevation` | `float` | Elevation of the storey level (typically from project datum) | Must be numeric |
| `storey_mass` | `float` | Total mass at this storey level (for seismic/dynamic analysis) | Must be numeric |

### Optional Properties

| Property | Type | Description | Default |
|----------|------|-------------|---------|
| `storey_horizontal_reaction_x` | `str` | Horizontal reaction force in X direction | None |
| `storey_horizontal_reaction_y` | `str` | Horizontal reaction force in Y direction | None |
| `storey_vertical_reaction` | `str` | Vertical reaction force (gravity loads) | None |

### Inherited Properties

Inherits from `XmiBaseEntity`:
- `name`: Name/identifier of the storey (e.g., "Level 1", "Floor 2")
- `id`: Unique identifier (GUID)
- `ifcguid`: IFC GUID for interoperability
- `entity_type`: Set to "XmiStructuralStorey"
- `description`: Optional description (e.g., "Ground Floor", "Typical Floor")

## Relationships

`XmiStructuralStorey` typically participates in:

### Implicit Relationships
- **Storey Membership**: Structural elements (nodes, members) reference storey names to indicate which level they belong to
- **Model Hierarchy**: Storeys organize the vertical structure of the building

## Purpose and Use Cases

### Vertical Organization

Storeys provide:
1. **Level Definition**: Define vertical organization of the building
2. **Mass Distribution**: Specify seismic mass at each level for dynamic analysis
3. **Reaction Tracking**: Record reaction forces from analysis results
4. **Element Grouping**: Group structural elements by level for queries and visualization

### Analysis Applications

- **Seismic Analysis**: Storey mass used for equivalent lateral force calculations
- **Drift Calculation**: Inter-storey drift computed between consecutive storeys
- **Gravity Analysis**: Track vertical reactions at each level
- **Dynamic Analysis**: Mass distribution affects modal analysis results

## Usage Examples

### Creating Storeys Directly

```python
from xmi.v2.models.entities.xmi_structural_storey import XmiStructuralStorey

# Ground floor at elevation 0
ground_floor = XmiStructuralStorey(
    name="339",
    storey_elevation=0.0,
    storey_mass=0.0,  # Mass TBD or calculated
    description="Level 1",
    id="storey-ground"
)

# First floor at 3000mm (3m)
first_floor = XmiStructuralStorey(
    name="2787",
    storey_elevation=3000.0,
    storey_mass=0.0,
    description="Level 2",
    id="storey-first"
)

# Second floor at 6000mm (6m)
second_floor = XmiStructuralStorey(
    name="351314",
    storey_elevation=6000.0,
    storey_mass=0.0,
    description="Level 3",
    id="storey-second"
)

print(f"{ground_floor.description} elevation: {ground_floor.storey_elevation} mm")
# Output: Level 1 elevation: 0.0 mm
```

### Loading from Dictionary (XMI Format)

```python
from xmi.v2.models.entities.xmi_structural_storey import XmiStructuralStorey

# Dictionary format from XMI JSON
storey_dict = {
    "Name": "2787",
    "StoreyElevation": 3000.0,
    "StoreyMass": 45000.0,  # kg
    "ID": "74e46f31-7d48-47ee-9207-931708e57a52-00000ae3",
    "Description": "Level 2",
    "IFCGUID": "1qv6ynVKX7xf87anS8vN2n"
}

# Parse using from_dict
storey, errors = XmiStructuralStorey.from_dict(storey_dict)

if storey and not errors:
    print(f"Storey: {storey.description}")
    print(f"Elevation: {storey.storey_elevation} mm")
    print(f"Mass: {storey.storey_mass} kg")
    # Output:
    # Storey: Level 2
    # Elevation: 3000.0 mm
    # Mass: 45000.0 kg
else:
    print(f"Errors: {errors}")
```

### Creating Building with Multiple Storeys

```python
# Define a complete multi-storey building
building_storeys = [
    # Basement
    XmiStructuralStorey(
        name="BASEMENT",
        storey_elevation=-3000.0,
        storey_mass=50000.0,
        description="Basement"
    ),

    # Ground floor
    XmiStructuralStorey(
        name="GROUND",
        storey_elevation=0.0,
        storey_mass=48000.0,
        description="Ground Floor"
    ),

    # Typical floors (3m height each)
    *[
        XmiStructuralStorey(
            name=f"FLOOR_{i}",
            storey_elevation=3000.0 * i,
            storey_mass=45000.0,
            description=f"Floor {i}"
        )
        for i in range(1, 11)  # 10 typical floors
    ],

    # Roof
    XmiStructuralStorey(
        name="ROOF",
        storey_elevation=33000.0,
        storey_mass=30000.0,
        description="Roof Level"
    )
]

for storey in building_storeys:
    print(f"{storey.description}: {storey.storey_elevation / 1000:.1f}m")
```

### Common Patterns

#### Querying Storeys in XmiModel

```python
from xmi.v2.models.xmi_model.xmi_manager import XmiManager
from xmi.v2.models.entities.xmi_structural_storey import XmiStructuralStorey

# Load XMI data
xmi_manager = XmiManager()
xmi_model = xmi_manager.read_xmi_dict(xmi_dict)

# Find all storeys
storeys = [
    entity for entity in xmi_model.entities
    if isinstance(entity, XmiStructuralStorey)
]

print(f"Total storeys: {len(storeys)}")

# Sort storeys by elevation
storeys.sort(key=lambda s: s.storey_elevation)

print("\nBuilding levels:")
for storey in storeys:
    print(f"  {storey.description}: {storey.storey_elevation / 1000:.2f}m")
```

#### Finding Storey by Name

```python
def find_storey_by_name(xmi_model, storey_name: str):
    """Find a storey by its name."""
    storeys = [
        entity for entity in xmi_model.entities
        if isinstance(entity, XmiStructuralStorey)
    ]

    for storey in storeys:
        if storey.name == storey_name:
            return storey

    return None

# Example usage
level_2 = find_storey_by_name(xmi_model, "2787")
if level_2:
    print(f"Found storey: {level_2.description} at {level_2.storey_elevation}mm")
```

#### Calculate Inter-Storey Heights

```python
def calculate_storey_heights(storeys: list) -> dict:
    """Calculate height of each storey from floor to floor."""
    # Sort by elevation
    sorted_storeys = sorted(storeys, key=lambda s: s.storey_elevation)

    heights = {}
    for i in range(len(sorted_storeys) - 1):
        current = sorted_storeys[i]
        next_storey = sorted_storeys[i + 1]
        height = next_storey.storey_elevation - current.storey_elevation
        heights[current.name] = height

    return heights

# Example usage
storey_heights = calculate_storey_heights(storeys)
for storey_name, height in storey_heights.items():
    storey = find_storey_by_name(xmi_model, storey_name)
    print(f"{storey.description}: {height / 1000:.2f}m high")
```

#### Calculate Total Building Height

```python
def calculate_building_height(storeys: list) -> float:
    """Calculate total building height from lowest to highest storey."""
    if not storeys:
        return 0.0

    elevations = [s.storey_elevation for s in storeys]
    return max(elevations) - min(elevations)

# Example usage
total_height = calculate_building_height(storeys)
print(f"Total building height: {total_height / 1000:.2f}m")
```

#### Calculate Total Seismic Mass

```python
def calculate_total_mass(storeys: list) -> float:
    """Calculate total seismic mass of the building."""
    return sum(s.storey_mass for s in storeys)

# Example usage
total_mass = calculate_total_mass(storeys)
print(f"Total seismic mass: {total_mass:.0f} kg ({total_mass / 1000:.2f} tonnes)")
```

#### Find Elements at Storey Level

```python
from xmi.v2.models.entities.xmi_structural_point_connection import XmiStructuralPointConnection

def find_nodes_at_storey(xmi_model, storey: XmiStructuralStorey, tolerance: float = 10.0):
    """
    Find all nodes at a given storey elevation (within tolerance).

    Args:
        xmi_model: The XMI model
        storey: The storey to search for
        tolerance: Elevation tolerance in mm (default 10mm)

    Returns:
        List of XmiStructuralPointConnection at this storey
    """
    nodes = [
        entity for entity in xmi_model.entities
        if isinstance(entity, XmiStructuralPointConnection)
    ]

    nodes_at_storey = []
    for node in nodes:
        # Parse coordinate to get Z elevation
        coords = node.coordinate.split(',')
        if len(coords) >= 3:
            z_elevation = float(coords[2])
            if abs(z_elevation - storey.storey_elevation) <= tolerance:
                nodes_at_storey.append(node)

    return nodes_at_storey

# Example usage
ground_floor = find_storey_by_name(xmi_model, "339")
if ground_floor:
    nodes = find_nodes_at_storey(xmi_model, ground_floor)
    print(f"Nodes at {ground_floor.description}: {len(nodes)}")
```

#### Storey Mass from Tributary Area

```python
def calculate_storey_mass(storey_area: float, dead_load: float, live_load_factor: float = 0.25) -> float:
    """
    Calculate storey mass from tributary area and loads.

    Args:
        storey_area: Floor area in m²
        dead_load: Dead load in kPa (kN/m²)
        live_load_factor: Fraction of live load to include (typically 0.25)

    Returns:
        Seismic mass in kg
    """
    # Typical live load (can be parameter)
    live_load = 2.0  # kPa

    # Total load
    total_load = dead_load + (live_load * live_load_factor)  # kPa

    # Convert to mass (load in kN/m², g = 9.81 m/s²)
    mass = (total_load * storey_area * 1000) / 9.81  # kg

    return mass

# Example: 500m² floor with 5 kPa dead load
area = 500.0  # m²
dead_load = 5.0  # kPa
mass = calculate_storey_mass(area, dead_load)

storey = XmiStructuralStorey(
    name="TYPICAL",
    storey_elevation=3000.0,
    storey_mass=mass,
    description="Typical Floor"
)

print(f"Calculated mass: {storey.storey_mass:.0f} kg")
```

#### Storey Comparison (Equality)

```python
# Storeys are compared by native_id (case-insensitive)
storey1 = XmiStructuralStorey(
    name="Level1",
    storey_elevation=0.0,
    storey_mass=45000.0
)

storey2 = XmiStructuralStorey(
    name="LEVEL1",  # Different case
    storey_elevation=0.0,
    storey_mass=45000.0
)

# Equality based on name (case-insensitive)
print(storey1 == storey2)  # True if native_id matches
```

## Validation Rules

### Type Validation

- `storey_elevation` must be numeric (float)
- `storey_mass` must be numeric (float)
- Optional reaction fields are strings (may contain formulas or references)

### Required Fields

Both elevation and mass are required:
```python
# Valid
storey = XmiStructuralStorey(
    storey_elevation=3000.0,
    storey_mass=45000.0
)

# Invalid - will raise validation error
# storey = XmiStructuralStorey(storey_elevation=3000.0)  # Missing storey_mass
```

### Logical Validation

While not enforced, best practices include:
- Elevations should be monotonically increasing from bottom to top
- Storey mass should be positive (or zero if not calculated)
- Storey heights (differences between elevations) should be reasonable (typically 2.5-5m)

## Integration with XMI Schema

### XMI Input Format

`StructuralStorey` entries are typically found at the top level of XMI JSON:

```json
{
  "StructuralStorey": [
    {
      "Name": "339",
      "StoreyElevation": 0.0,
      "StoreyMass": 48000.0,
      "ID": "74e46f31-7d48-47ee-9207-931708e57a52-00000153",
      "Description": "Level 1",
      "IFCGUID": "1qv6ynVKX7xf87anS8vNi1"
    },
    {
      "Name": "2787",
      "StoreyElevation": 3000.0,
      "StoreyMass": 45000.0,
      "ID": "74e46f31-7d48-47ee-9207-931708e57a52-00000ae3",
      "Description": "Level 2",
      "IFCGUID": "1qv6ynVKX7xf87anS8vN2n"
    },
    {
      "Name": "351314",
      "StoreyElevation": 6000.0,
      "StoreyMass": 45000.0,
      "ID": "ac57991d-73eb-402c-abe6-9e3d3ff9c128-00055c52",
      "Description": "Level 3",
      "IFCGUID": "1qv6ynVKX7xf87anS8vN3q"
    }
  ],
  "StructuralPointConnection": [...],
  "StructuralCurveMember": [...]
}
```

### Parsing Order

`StructuralStorey` entries are typically parsed early, as they provide organizational structure for other elements.

### Units

Elevation is typically in millimeters (mm), matching coordinate units. A corresponding `StructuralUnit` entry should specify:
```json
{
  "Entity": "StructuralStorey",
  "Attribute": "StoreyElevation",
  "Unit": "mm"
}
```

## Notes

### Version Differences (v1 vs v2)

**v2 Characteristics:**
- Uses Pydantic for automatic validation
- Field aliases support both PascalCase and snake_case
- Custom `__eq__` and `__hash__` for comparison by native_id
- Type hints improve IDE support

**v1 Characteristics:**
- Uses `__slots__` for memory efficiency
- Manual property validation
- Explicit parsing logic

### Elevation Reference

- Elevations are typically relative to a project datum (e.g., ground level = 0)
- Negative elevations indicate below-grade levels (basements)
- Elevations should match Z-coordinates of nodes at that level

### Mass Calculation

Seismic mass typically includes:
- **Dead Load**: Self-weight of structure and permanent loads
- **Live Load**: Portion of live load (often 25% for office buildings)
- **Superimposed Dead Load**: Finishes, MEP systems, partitions

Mass excludes:
- Foundation and below-grade portions (usually)
- Transient loads

### Reaction Forces

Reaction force fields are optional strings that may contain:
- Numerical values with units
- References to load combinations
- Formulas or expressions

These are typically populated from analysis results rather than input.

### Storey vs Level

"Storey" and "Level" are often used interchangeably:
- **Storey**: British/IFC terminology (IfcBuildingStorey)
- **Level**: American terminology (common in software like Revit)

### Performance Considerations

- Storeys are lightweight objects with minimal data
- Typical buildings have 1-100 storeys
- Sorting by elevation is fast and commonly needed

### Common Pitfalls

1. **Unit Confusion**: Ensure elevations match coordinate system units (typically mm)
2. **Missing Mass**: Zero mass storeys may cause issues in seismic analysis
3. **Elevation Mismatch**: Storey elevations should match actual node Z-coordinates
4. **Duplicate Names**: Ensure unique storey names for reliable lookups

## Related Classes

### Entity Classes
- [`XmiStructuralPointConnection`](./XmiStructuralPointConnection.md) - Nodes located at storey elevations
- [`XmiStructuralCurveMember`](./XmiStructuralCurveMember.md) - Members spanning between storeys
- [`XmiStructuralSurfaceMember`](./XmiStructuralSurfaceMember.md) - Slabs at storey levels
- [`XmiStructuralUnit`](./XmiStructuralUnit.md) - Unit definitions for storey attributes

### Base Classes
- `XmiBaseEntity` - Base entity class

### Manager Classes
- [`XmiManager`](../xmi_model/XmiManager.md) - Handles storey parsing from XMI dictionaries
- [`XmiModel`](../xmi_model/XmiModel.md) - Container for storey entities and other elements
