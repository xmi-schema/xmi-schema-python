from pydantic import Field, field_validator, model_validator
from typing import List, Optional, Tuple, Union
from ..bases.xmi_base_entity import XmiBaseEntity
from ..entities.xmi_structural_material import XmiStructuralMaterial
from ..entities.xmi_structural_point_connection import XmiStructuralPointConnection
from ..entities.xmi_segment import XmiSegment
from ..entities.xmi_structural_storey import XmiStructuralStorey
from ..enums.xmi_structural_surface_member_type_enum import XmiStructuralSurfaceMemberTypeEnum
from ..enums.xmi_structural_surface_member_system_plane_enum import XmiStructuralSurfaceMemberSystemPlaneEnum
from ...utils.xmi_errors import *

class XmiStructuralSurfaceMember(XmiBaseEntity):
    material: XmiStructuralMaterial = Field(..., alias="Material")
    surface_member_type: XmiStructuralSurfaceMemberTypeEnum = Field(..., alias="Type")
    thickness: Union[float, int] = Field(..., alias="Thickness")
    system_plane: XmiStructuralSurfaceMemberSystemPlaneEnum = Field(..., alias="SystemPlane")
    segments: List[XmiSegment] = Field(..., alias="Segments")
    nodes: List[XmiStructuralPointConnection] = Field(..., alias="Nodes")
    area: Optional[Union[float, int]] = Field(None, alias="Area")
    z_offset: Union[float, int] = Field(0.0, alias="ZOffset")
    local_axis_x: Tuple[float, float, float] = Field((1.0, 0.0, 0.0), alias="LocalAxisX")
    local_axis_y: Tuple[float, float, float] = Field((0.0, 1.0, 0.0), alias="LocalAxisY")
    local_axis_z: Tuple[float, float, float] = Field((0.0, 0.0, 1.0), alias="LocalAxisZ")
    storey: Optional[XmiStructuralStorey] = Field(None, alias="Storey")
    height: Optional[Union[float, int]] = Field(None, alias="Height")

    class Config:
        populate_by_name = True

    @field_validator("segments")
    @classmethod
    def validate_segments(cls, v):
        if not isinstance(v, list) or len(v) < 3:
            raise ValueError("segments list should have at least 3 items of type XmiSegment")
        for item in v:
            if not isinstance(item, XmiSegment):
                raise TypeError(f"All items must be instances of type XmiSegment, got {type(item)} instead")
        return v

    @field_validator("nodes")
    @classmethod
    def validate_nodes(cls, v):
        if not isinstance(v, list):
            raise TypeError("nodes should be a list")
        for item in v:
            if not isinstance(item, XmiStructuralPointConnection):
                raise TypeError(f"All items must be instances of XmiStructuralPointConnection, got {type(item)} insteads")
        return v

    @field_validator("local_axis_x", "local_axis_y", "local_axis_z")
    @classmethod
    def validate_local_axes(cls, v, info):
        if isinstance(v, str):
            parts = v.split(',')
            if len(parts) != 3:
                raise XmiMissingRequiredAttributeError(
                    f"{info.field_name} must have exactly 3 components")
            try:
                v = tuple(float(p.strip()) for p in parts)
            except ValueError:
                raise XmiInconsistentDataTypeError(
                    f"All parts of {info.field_name} must be convertible to float")
        elif isinstance(v, (list, tuple)):
            if len(v) != 3:
                raise ValueError(f"{info.field_name} must have 3 elements")
            if not all(isinstance(val, (float, int)) for val in v):
                raise TypeError(f"Each value in {info.field_name} must be float or int")
            v = tuple(v)
        else:
            raise TypeError(f"{info.field_name} must be a tuple, list, or comma-separated string")
        return v

    @model_validator(mode="before")
    @classmethod
    def set_entity_type(cls, values):
        values.setdefault("EntityType", cls.__name__)
        return values
    

# Testing run python -m src.xmi.v2.models.entities.xmi_structural_surface_member
if __name__ == "__main__":
    material = XmiStructuralMaterial(
        ID="mat001",
        Name="Steel S355",
        Description="Standard steel",
        material_type="Steel",
        grade=355,
        unit_weight=7850,
        e_modulus=200000,
        g_modulus=80000,
        poisson_ratio=0.3,
        thermal_coefficient=1.2e-5
    )

    node = XmiStructuralPointConnection(
        ID="n001",
        Name="Point A",
        Description="Test node",
        Point={"X": 1.0, "Y": 0.5, "Z": 0.0} 
)

    segment = XmiSegment(
        ID="s001",
        Name="Segment 1",
        Geometry={"type": "Line"},  
        Position=1,
        BeginNode=node,
        EndNode=node,
        SegmentType="LINE"
    )

    surface_member = XmiStructuralSurfaceMember(
        ID="sf001",
        Name="Surface Slab",
        Material=material,
        Type="SLAB",
        Thickness=250,
        SystemPlane="TOP", 
        Segments=[segment, segment, segment],
        Nodes=[node, node],
        Area=12000.0,
        ZOffset=0.0,
        LocalAxisX=[1.0, 0.0, 0.0],
        LocalAxisY=(0.0, 1.0, 0.0),
        LocalAxisZ=[0.0, 0.0, 1.0],
        Height=500.0
    )

    print("Created XmiStructuralSurfaceMember:")
    print(surface_member.model_dump(by_alias=True, exclude_unset=True))