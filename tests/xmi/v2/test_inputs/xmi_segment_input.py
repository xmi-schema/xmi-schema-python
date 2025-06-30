from src.xmi.v2.models.enums.xmi_segment_type_enum import XmiSegmentTypeEnum
from src.xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D
from src.xmi.v2.models.geometries.xmi_line_3d import XmiLine3D
from src.xmi.v2.models.entities.xmi_structural_point_connection import XmiStructuralPointConnection

valid_segment_input = {
    "id": "seg-001",
    "name": "Segment 1",
    "geometry": XmiLine3D(
        start_point=XmiPoint3D(x=0.0, y=0.0, z=0.0),
        end_point=XmiPoint3D(x=10.0, y=0.0, z=0.0),
    ),
    "position": 1,
    "begin_node": XmiStructuralPointConnection(
        id="node-001",
        name="Begin Node",
        point=XmiPoint3D(x=0.0, y=0.0, z=0.0),
    ),
    "end_node": XmiStructuralPointConnection(
        id="node-002",
        name="End Node",
        point=XmiPoint3D(x=10.0, y=0.0, z=0.0),
    ),
    "segment_type": XmiSegmentTypeEnum.LINE,
}

missing_geometry_input = {
    **valid_segment_input,
}
missing_geometry_input.pop("geometry")

invalid_segment_type_input = {
    **valid_segment_input,
    "segment_type": "INVALID_TYPE"
}