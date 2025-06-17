from pydantic import Field, field_validator, model_validator
from typing import List, Optional, Tuple, Union
from ..bases.xmi_base_entity import XmiBaseEntity
from ..entities.xmi_structural_cross_section import XmiStructuralCrossSection
from ..entities.xmi_structural_point_connection import XmiStructuralPointConnection
from ..entities.xmi_segment import XmiSegment
from ..entities.xmi_structural_storey import XmiStructuralStorey
from ..enums.xmi_structural_curve_member_type_enum import XmiStructuralCurveMemberTypeEnum
from ..enums.xmi_structural_curve_member_system_line_enum import XmiStructuralCurveMemberSystemLineEnum
from ...utils.xmi_errors import *

class XmiStructuralCurveMember(XmiBaseEntity):
    cross_section: XmiStructuralCrossSection = Field(..., alias="CrossSection")
    curve_member_type: XmiStructuralCurveMemberTypeEnum = Field(..., alias="CurveMemberType")
    system_line: XmiStructuralCurveMemberSystemLineEnum = Field(..., alias="SystemLine")
    nodes: List[XmiStructuralPointConnection] = Field(..., alias="Nodes")
    segments: List[XmiSegment] = Field(..., alias="Segments")
    begin_node: XmiStructuralPointConnection = Field(..., alias="BeginNode")
    end_node: XmiStructuralPointConnection = Field(..., alias="EndNode")

    local_axis_x: Tuple[float, float, float] = Field((1.0, 0.0, 0.0), alias="LocalAxisX")
    local_axis_y: Tuple[float, float, float] = Field((0.0, 1.0, 0.0), alias="LocalAxisY")
    local_axis_z: Tuple[float, float, float] = Field((0.0, 0.0, 1.0), alias="LocalAxisZ")

    begin_node_x_offset: float = Field(0.0, alias="BeginNodeXOffset")
    end_node_x_offset: float = Field(0.0, alias="EndNodeXOffset")
    begin_node_y_offset: float = Field(0.0, alias="BeginNodeYOffset")
    end_node_y_offset: float = Field(0.0, alias="EndNodeYOffset")
    begin_node_z_offset: float = Field(0.0, alias="BeginNodeZOffset")
    end_node_z_offset: float = Field(0.0, alias="EndNodeZOffset")

    length: Optional[Union[int, float]] = Field(None, alias="Length")
    storey: Optional[XmiStructuralStorey] = Field(None, alias="Storey")

    end_fixity_start: Optional[float]  = Field(None, alias="EndFixityStart")
    end_fixity_end: Optional[float] = Field(None, alias="EndFixityEnd")

    class Config:
        populate_by_name = True

    @field_validator("nodes")
    @classmethod
    def validate_nodes(cls, v):
        if not isinstance(v, list) or not all(isinstance(n, XmiStructuralPointConnection) for n in v):
            raise ValueError("All nodes must be of type XmiStructuralPointConnection")
        return v

    @field_validator("segments")
    @classmethod
    def validate_segments(cls, v):
        if not isinstance(v, list) or not all(isinstance(s, XmiSegment) for s in v):
            raise ValueError("All segments must be of type XmiSegment")
        if len(v) == 0:
            raise ValueError("segments list must have at least 1 item")
        return v

    @field_validator("local_axis_x", "local_axis_y", "local_axis_z")
    @classmethod
    def validate_axis(cls, v, info):
        if not isinstance(v, tuple) or len(v) != 3 or not all(isinstance(i, (int, float)) for i in v):
            raise ValueError(f"{info.field_name} must be a tuple of 3 numbers")
        return v

    @field_validator("begin_node", "end_node")
    @classmethod
    def validate_nodes_ref(cls, v, info):
        if not isinstance(v, XmiStructuralPointConnection):
            raise TypeError(f"{info.field_name} must be of type XmiStructuralPointConnection")
        return v

    @field_validator("cross_section")
    @classmethod
    def validate_cross_section(cls, v):
        if not isinstance(v, XmiStructuralCrossSection):
            raise TypeError("cross_section must be a XmiStructuralCrossSection")
        return v

    @model_validator(mode="before")
    @classmethod
    def fill_entity_type(cls, values):
        values.setdefault("EntityType", "XmiStructuralCurveMember")
        return values
    

# Testing run python -m src.xmi.v2.models.entities.xmi_structural_curve_member
if __name__ == "__main__":
    from ..enums.xmi_structural_material_type_enum import XmiStructuralMaterialTypeEnum
    from ..enums.xmi_segment_type_enum import XmiSegmentTypeEnum
    from ..geometries.xmi_point_3d import XmiPoint3D
    from ..bases.xmi_base_geometry import XmiBaseGeometry
    from .xmi_structural_material import XmiStructuralMaterial

    storey = XmiStructuralStorey(
        id="storey1",
        name="Level 1",
        storey_elevation=0
    )

    material = XmiStructuralMaterial(
        id="mat1",
        name="Steel",
        material_type=XmiStructuralMaterialTypeEnum.STEEL,
        grade=355,
        unit_weight=7850,
        e_modulus=200000,
        g_modulus=80000,
        poisson_ratio=0.3,
        thermal_coefficient=1.2e-5
    )

    cross_section = XmiStructuralCrossSection(
        id="cs1",
        name="Rect I",
        material=material,
        shape="I Shape",
        parameters=(300.0, 150.0, 10.0, 6.0, 8.0),
        ix=1200,
        iy=500,
        rx=3.5,
        ry=1.2,
        ex=200000,
        ey=200000,
        zx=300,
        zy=150,
        j=80,
        area=4500
    )

    node1 = XmiStructuralPointConnection(
        id="node1",
        name="Start Node",
        point=XmiPoint3D(x=0.0, y=0.0, z=0.0),
        storey=storey
    )

    node2 = XmiStructuralPointConnection(
        id="node2",
        name="End Node",
        point=XmiPoint3D(x=5.0, y=0.0, z=0.0),
        storey=storey
    )

    geometry = XmiBaseGeometry(
        id="g1",
        name="Line Geometry"
    )

    segment = XmiSegment(
        id="seg1",
        name="Beam Segment",
        geometry=geometry,
        position=1,
        begin_node=node1,
        end_node=node2,
        segment_type=XmiSegmentTypeEnum.LINE
    )

    curve_member = XmiStructuralCurveMember(
        id="curve1",
        name="Main Beam",
        cross_section=cross_section,
        curve_member_type=XmiStructuralCurveMemberTypeEnum.BEAM,
        system_line=XmiStructuralCurveMemberSystemLineEnum.MIDDLE_LEFT,
        nodes=[node1, node2],
        segments=[segment],
        begin_node=node1,
        end_node=node2,
        local_axis_x=(1.0, 0.0, 0.0),
        local_axis_y=(0.0, 1.0, 0.0),
        local_axis_z=(0.0, 0.0, 1.0),
        begin_node_x_offset=0.0,
        end_node_x_offset=0.0,
        begin_node_y_offset=0.0,
        end_node_y_offset=0.0,
        begin_node_z_offset=0.0,
        end_node_z_offset=0.0,
        length=5.0,
        storey=storey,
        end_fixity_start=0.0,
        end_fixity_end=0.0
    )

    print("Created XmiStructuralCurveMember:")
    print(curve_member.model_dump(by_alias=True, exclude_unset=True))