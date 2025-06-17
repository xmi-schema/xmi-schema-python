from enum import unique
from ..bases.xmi_base_enum import XmiBaseEnum

@unique
class XmiSegmentTypeEnum(XmiBaseEnum):
    LINE = "Line"
    CIRCULAR_ARC = "Circular Arc"
    PARABOLIC_ARC = "Parabolic Arc"
    BEZIER = "Bezier"
    SPLINE = "Spline"
    OTHERS = "Others"

    def get_geometry_class(self):
        from ..geometries.xmi_line_3d import XmiLine3D
        from ..geometries.xmi_arc_3d import XmiArc3D

        mapping = {
            XmiSegmentTypeEnum.LINE: XmiLine3D,
            XmiSegmentTypeEnum.CIRCULAR_ARC: XmiArc3D,
        }
        return mapping.get(self)
    

# Testing run python -m src.xmi.v2.models.enums.xmi_segment_type_enum

if __name__ == "__main__":
    from ..geometries.xmi_point_3d import XmiPoint3D
    from .xmi_segment_type_enum import XmiSegmentTypeEnum

    start = XmiPoint3D(x=0, y=0, z=0, id="start", name="Start")
    end = XmiPoint3D(x=1, y=1, z=1, id="end", name="End")
    center = XmiPoint3D(x=0.5, y=0.5, z=0, id="center", name="Center")

    print("\nTesting LINE segment:")
    segment_type = XmiSegmentTypeEnum.LINE
    LineClass = segment_type.get_geometry_class()
    line = LineClass(start_point=start, end_point=end, id="line1", name="Line 1")
    print(line.model_dump(by_alias=True))

    print("\nTesting CIRCULAR_ARC segment:")
    segment_type = XmiSegmentTypeEnum.CIRCULAR_ARC
    ArcClass = segment_type.get_geometry_class()
    arc = ArcClass(start_point=start, end_point=end, center_point=center, id="arc1", name="Arc 1")
    print(arc.model_dump(by_alias=True))