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