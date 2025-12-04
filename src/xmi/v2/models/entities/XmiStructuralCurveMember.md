# XmiStructuralCurveMember

## Overview

`XmiStructuralCurveMember` represents linear structural elements in the XMI schema, such as beams, columns, and bracing members. These are one-dimensional elements that connect between point connections and are defined by their cross-section, local coordinate system, and geometric properties. Curve members can consist of multiple segments (lines or arcs) connecting nodes along their length.

## Class Hierarchy

- **Parent**: `XmiBaseEntity`
- **Version**: v2 (Pydantic-based implementation)
- **Module**: `src/xmi/v2/models/entities/xmi_structural_curve_member.py`

## Properties

### Required Properties

| Property | Type | Description | Validation |
|----------|------|-------------|------------|
| `curve_member_type` | `XmiStructuralCurveMemberTypeEnum` | Type of the structural curve member (Beam, Column, Bracing, Other, Unknown) | Must be valid enum value |
| `system_line` | `XmiStructuralCurveMemberSystemLineEnum` | Reference line position on the cross-section (e.g., Top Left, Middle Middle) | Must be valid enum value |

### Optional Properties with Defaults

| Property | Type | Default | Description | Validation |
|----------|------|---------|-------------|------------|
| `local_axis_x` | `Tuple[float, float, float]` | `(1.0, 0.0, 0.0)` | Local X-axis direction vector | Must be 3 floats or comma-separated string |
| `local_axis_y` | `Tuple[float, float, float]` | `(0.0, 1.0, 0.0)` | Local Y-axis direction vector | Must be 3 floats or comma-separated string |
| `local_axis_z` | `Tuple[float, float, float]` | `(0.0, 0.0, 1.0)` | Local Z-axis direction vector | Must be 3 floats or comma-separated string |
| `begin_node_x_offset` | `float` | `0.0` | Offset at begin node in local X direction | Numeric value |
| `end_node_x_offset` | `float` | `0.0` | Offset at end node in local X direction | Numeric value |
| `begin_node_y_offset` | `float` | `0.0` | Offset at begin node in local Y direction | Numeric value |
| `end_node_y_offset` | `float` | `0.0` | Offset at end node in local Y direction | Numeric value |
| `begin_node_z_offset` | `float` | `0.0` | Offset at begin node in local Z direction | Numeric value |
| `end_node_z_offset` | `float` | `0.0` | Offset at end node in local Z direction | Numeric value |
| `length` | `Optional[Union[int, float]]` | `None` | Total length of the curve member | Numeric value or None |
| `end_fixity_start` | `Optional[str]` | `None` | End fixity condition at start node (e.g., "Fixed", "Pinned") | String or None |
| `end_fixity_end` | `Optional[str]` | `None` | End fixity condition at end node (e.g., "Fixed", "Pinned") | String or None |

### Inherited Properties

Inherits from `XmiBaseEntity`:
- `name`: Name/identifier of the curve member
- `id`: Unique identifier (GUID)
- `ifcguid`: IFC GUID for interoperability
- `entity_type`: Set to "XmiStructuralCurveMember"
- `description`: Optional description

## Enums

### XmiStructuralCurveMemberTypeEnum

Defines the structural function of the curve member:

- `BEAM`: Horizontal structural member (primarily flexural)
- `COLUMN`: Vertical structural member (primarily axial)
- `BRACING`: Diagonal bracing member
- `OTHER`: Other type of curve member
- `UNKNOWN`: Type is unknown or not specified

### XmiStructuralCurveMemberSystemLineEnum

Defines the reference line position on the cross-section:

- `TOP_LEFT`: Top left corner of cross-section
- `TOP_MIDDLE`: Top center of cross-section
- `TOP_RIGHT`: Top right corner of cross-section
- `MIDDLE_LEFT`: Middle left edge of cross-section
- `MIDDLE_MIDDLE`: Centroid of cross-section
- `MIDDLE_RIGHT`: Middle right edge of cross-section
- `BOTTOM_LEFT`: Bottom left corner of cross-section
- `BOTTOM_MIDDLE`: Bottom center of cross-section
- `BOTTOM_RIGHT`: Bottom right corner of cross-section
- `UNKNOWN`: Reference line is unknown

## Relationships

`XmiStructuralCurveMember` participates in several relationships:

### Source Relationships (this entity is the source):

- **`XmiHasCrossSection`**: Links the curve member to its `XmiCrossSection`
- **`XmiHasStructuralNode`**: Links to begin and end `XmiStructuralPointConnection` nodes (with `is_begin` and `is_end` attributes)
- **`XmiHasSegment`**: Links to multiple `XmiSegment` objects representing the geometric path between nodes

### Target Relationships (this entity is the target):

- May be referenced by storey or unit relationships for organizational hierarchy

## Local Coordinate System

The local coordinate system defines the orientation of the curve member:

- **Local X-axis**: Typically aligned with the member's longitudinal direction
- **Local Y-axis**: Defines the major axis of the cross-section
- **Local Z-axis**: Defines the minor axis of the cross-section (perpendicular to X and Y)

The axes form a right-handed coordinate system and are essential for:
- Applying loads in local coordinates
- Defining member orientation
- Interpreting cross-section properties (Ix, Iy)

## Node Offsets

Node offsets allow the analytical centerline to differ from geometric connections:

- **Begin Node Offsets**: `begin_node_x_offset`, `begin_node_y_offset`, `begin_node_z_offset`
- **End Node Offsets**: `end_node_x_offset`, `end_node_y_offset`, `end_node_z_offset`

Use cases:
- Rigid end zones in beams
- Column-to-beam eccentricities
- Connection details where analytical and physical centerlines differ

## Usage Examples

### Creating an Instance Directly

```python
from xmi.v2.models.entities.xmi_structural_curve_member import XmiStructuralCurveMember
from xmi.v2.models.enums.xmi_structural_curve_member_type_enum import XmiStructuralCurveMemberTypeEnum
from xmi.v2.models.enums.xmi_structural_curve_member_system_line_enum import XmiStructuralCurveMemberSystemLineEnum

# Create a column member
column = XmiStructuralCurveMember(
    name="C01",
    id="column-001",
    curve_member_type=XmiStructuralCurveMemberTypeEnum.COLUMN,
    system_line=XmiStructuralCurveMemberSystemLineEnum.MIDDLE_MIDDLE,
    local_axis_x=(0.0, 0.0, 1.0),  # Vertical column (Z-up)
    local_axis_y=(1.0, 0.0, 0.0),
    local_axis_z=(0.0, 1.0, 0.0),
    length=3000.0,
    description="Ground floor column"
)

# Create a beam member with offsets
beam = XmiStructuralCurveMember(
    name="B01",
    id="beam-001",
    curve_member_type=XmiStructuralCurveMemberTypeEnum.BEAM,
    system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_MIDDLE,
    local_axis_x=(1.0, 0.0, 0.0),  # Horizontal beam (along X)
    local_axis_y=(0.0, 0.0, 1.0),
    local_axis_z=(0.0, 1.0, 0.0),
    length=6000.0,
    begin_node_y_offset=150.0,  # Rigid end zone
    end_node_y_offset=150.0,
    end_fixity_start="Fixed",
    end_fixity_end="Pinned"
)
```

### Loading from Dictionary

```python
from xmi.v2.models.entities.xmi_structural_curve_member import XmiStructuralCurveMember

# Dictionary from XMI JSON input
curve_member_dict = {
    "Name": "351142",
    "CrossSection": "350998",
    "Storey": "2787",
    "Type": "Column",
    "CurveMemberType": "Column",
    "Nodes": "351149;351151",
    "Segments": "Line",
    "SystemLine": "Middle Middle",
    "BeginNode": "351149",
    "EndNode": "351151",
    "Length": 3000.0,
    "ID": "ac57991d-73eb-402c-abe6-9e3d3ff9c128-00055ba6",
    "Description": "C001",
    "LocalAxisX": "0,0,1",
    "LocalAxisY": "1,0,0",
    "LocalAxisZ": "0,1,0",
    "BeginNodeYOffset": 0.0,
    "EndNodeYOffset": 0.0,
    "BeginNodeZOffset": 0.0,
    "EndNodeZOffset": 0.0
}

# Parse using from_dict (handles enum conversion and axis parsing)
curve_member, errors = XmiStructuralCurveMember.from_dict(curve_member_dict)

if curve_member:
    print(f"Created curve member: {curve_member.name}")
    print(f"Type: {curve_member.curve_member_type}")
    print(f"Length: {curve_member.length}")
    print(f"Local X-axis: {curve_member.local_axis_x}")
else:
    print(f"Errors during parsing: {errors}")
```

### Common Patterns

#### Working with Local Axes

```python
# Axes can be specified as strings or tuples
beam1 = XmiStructuralCurveMember(
    name="B1",
    id="b1",
    curve_member_type=XmiStructuralCurveMemberTypeEnum.BEAM,
    system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_MIDDLE,
    local_axis_x="1.0,0.0,0.0",  # String format
)

beam2 = XmiStructuralCurveMember(
    name="B2",
    id="b2",
    curve_member_type=XmiStructuralCurveMemberTypeEnum.BEAM,
    system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_MIDDLE,
    local_axis_x=(1.0, 0.0, 0.0),  # Tuple format
)

# Both are converted to tuples internally
assert beam1.local_axis_x == beam2.local_axis_x
```

#### Querying Curve Members in XmiModel

```python
from xmi.v2.models.xmi_model.xmi_manager import XmiManager

# Load XMI data
xmi_manager = XmiManager()
xmi_model = xmi_manager.read_xmi_dict(xmi_dict)

# Find all curve members
curve_members = [
    entity for entity in xmi_model.entities
    if isinstance(entity, XmiStructuralCurveMember)
]

# Filter by type
columns = [
    cm for cm in curve_members
    if cm.curve_member_type == XmiStructuralCurveMemberTypeEnum.COLUMN
]

beams = [
    cm for cm in curve_members
    if cm.curve_member_type == XmiStructuralCurveMemberTypeEnum.BEAM
]

print(f"Total curve members: {len(curve_members)}")
print(f"Columns: {len(columns)}")
print(f"Beams: {len(beams)}")
```

#### Finding Cross-Section for a Curve Member

```python
from xmi.v2.models.relationships.xmi_has_structural_cross_section import XmiHasCrossSection

# Find cross-section relationship
cs_relationships = xmi_model.find_relationships_by_source(
    curve_member,
    relationship_type=XmiHasCrossSection
)

if cs_relationships:
    cross_section = cs_relationships[0].target
    print(f"Member {curve_member.name} uses cross-section: {cross_section.name}")
    print(f"Shape: {cross_section.shape}")
```

#### Finding Nodes Connected to Curve Member

```python
from xmi.v2.models.relationships.xmi_has_structural_node import XmiHasStructuralNode

# Find node relationships
node_relationships = xmi_model.find_relationships_by_source(
    curve_member,
    relationship_type=XmiHasStructuralNode
)

# Separate begin and end nodes
begin_node = None
end_node = None

for rel in node_relationships:
    if rel.is_begin:
        begin_node = rel.target
    elif rel.is_end:
        end_node = rel.target

if begin_node and end_node:
    print(f"Begin node: {begin_node.name} at {begin_node.coordinate}")
    print(f"End node: {end_node.name} at {end_node.coordinate}")
```

## Validation Rules

### Type Validation

- `curve_member_type` must be a valid `XmiStructuralCurveMemberTypeEnum` value
- `system_line` must be a valid `XmiStructuralCurveMemberSystemLineEnum` value
- All axis vectors must be tuples of exactly 3 floats
- All offset values must be numeric (int or float)
- `length` must be numeric or None

### Axis String Parsing

When local axes are provided as strings:
- Must contain exactly 3 comma-separated numeric values
- Whitespace around values is trimmed
- Values are converted to floats

Example valid formats:
- `"1,0,0"`
- `"1.0, 0.0, 0.0"`
- `"0.707, 0.707, 0.0"`

### Coordinate System Rules

- Local axes should form a right-handed coordinate system
- Axes should be normalized (unit vectors) for proper interpretation
- The library does not enforce orthogonality, but it's recommended for analysis

## Integration with XMI Schema

### Typical XMI Dictionary Structure

```json
{
  "StructuralCurveMember": [
    {
      "Name": "C01",
      "CrossSection": "CS-600x600",
      "Type": "Column",
      "CurveMemberType": "Column",
      "Nodes": "N1;N2",
      "Segments": "Line",
      "SystemLine": "Middle Middle",
      "BeginNode": "N1",
      "EndNode": "N2",
      "Length": 3000.0,
      "LocalAxisX": "0,0,1",
      "LocalAxisY": "1,0,0",
      "LocalAxisZ": "0,1,0",
      "ID": "unique-guid-here",
      "IFCGUID": "ifc-guid-here",
      "Description": "Ground floor column"
    }
  ]
}
```

### Dependency Order

`XmiStructuralCurveMember` depends on:
1. `XmiStructuralPointConnection` (begin/end nodes must exist)
2. `XmiCrossSection` (cross-section must exist)

These dependencies must be loaded before curve members during parsing.

## Notes

### Version Differences (v1 vs v2)

**v2 Advantages:**
- Uses Pydantic for automatic validation
- Field aliases support both PascalCase (JSON) and snake_case (Python)
- `from_dict()` method handles enum conversion automatically
- Cleaner validation with decorators

**v1 Characteristics:**
- Uses `__slots__` for memory efficiency
- Manual property validation with setters/getters
- Explicit parsing logic in `from_xmi_dict_obj()`

### Segments

Curve members contain segments that define their geometric path:
- Segments are typically created during parsing (not directly from input)
- Each segment connects consecutive nodes
- Segment types: "Line" for straight segments, "CircularArc" for curved segments
- Segments are linked via `XmiHasSegment` relationships

### System Line Impact

The `system_line` property affects how the member is positioned relative to nodes:
- `MIDDLE_MIDDLE`: Centroid of cross-section aligns with nodes
- `TOP_MIDDLE`: Top face of cross-section aligns with nodes
- `BOTTOM_MIDDLE`: Bottom face of cross-section aligns with nodes
- Important for accurate structural analysis and visualization

### Performance Considerations

- Local axis tuples are immutable after validation
- Offset values default to 0.0 (most common case)
- Use `populate_by_name=True` in model config for flexible field access

## Related Classes

### Entity Classes
- [`XmiCrossSection`](./XmiCrossSection.md) - Cross-section definition
- [`XmiStructuralPointConnection`](./XmiStructuralPointConnection.md) - Node connections
- [`XmiSegment`](../segments/XmiSegment.md) - Geometric segments
- [`XmiStorey`](./XmiStorey.md) - Story organization

### Relationship Classes
- `XmiHasCrossSection` - Links to cross-section
- `XmiHasStructuralNode` - Links to nodes
- `XmiHasSegment` - Links to segments

### Enum Classes
- `XmiStructuralCurveMemberTypeEnum` - Member type enumeration
- `XmiStructuralCurveMemberSystemLineEnum` - System line position enumeration

### Geometry Classes
- `XmiLine3D` - Line segment geometry
- `XmiArc3D` - Arc segment geometry

### Base Classes
- [`XmiBaseEntity`](../bases/XmiBaseEntity.md) - Base entity class

### Manager Classes
- [`XmiManager`](../xmi_model/XmiManager.md) - Entry point for parsing XMI data
- [`XmiModel`](../xmi_model/XmiModel.md) - Container for entities and relationships
