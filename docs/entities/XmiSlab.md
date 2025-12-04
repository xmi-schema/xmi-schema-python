# XmiSlab

## Overview
`XmiSlab` models horizontal plate-like physical elements (floors, roofs, mats). It inherits everything from `XmiBasePhysicalEntity`, so only metadata is required—geometry and analysis are tracked via relationships (e.g., `XmiHasGeometry`, `XmiHasStructuralSurfaceMember`).

## Properties
Slabs currently expose the base properties: `id`, `name`, `description`, `entity_type`, `ifcguid`, `native_id`, and `type`. Additional geometric/detail data is provided through relationships or higher-level analytical entities.

## Usage
```python
from xmi.v2.models.entities.xmi_slab import XmiSlab

slab, errors = XmiSlab.from_dict({
    "ID": "slab-001",
    "Name": "Level 2 Slab",
    "Description": "Post-tensioned floor"
})
```

Slabs typically participate in:
- `XmiHasStructuralCurveMember` (when bridged via analytical members such as shells)
- `XmiHasGeometry` (linking to polygon or surface geometry)
- `XmiHasStructuralStorey` (elevation grouping)

Because `XmiSlab` adds no additional validation beyond the base class, it is lightweight and ideal for graph traversals centered on metadata (story assignment, materials, etc.).
