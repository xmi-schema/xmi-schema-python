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
    