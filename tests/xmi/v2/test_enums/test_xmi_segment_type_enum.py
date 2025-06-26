import pytest
from src.xmi.v2.models.enums.xmi_segment_type_enum import XmiSegmentTypeEnum
from src.xmi.v2.models.geometries.xmi_line_3d import XmiLine3D
from src.xmi.v2.models.geometries.xmi_arc_3d import XmiArc3D

def test_xmi_segment_type_enum_values():
    assert XmiSegmentTypeEnum.LINE.value == "Line"
    assert XmiSegmentTypeEnum.CIRCULAR_ARC.value == "Circular Arc"
    assert XmiSegmentTypeEnum.PARABOLIC_ARC.value == "Parabolic Arc"
    assert XmiSegmentTypeEnum.BEZIER.value == "Bezier"
    assert XmiSegmentTypeEnum.SPLINE.value == "Spline"
    assert XmiSegmentTypeEnum.OTHERS.value == "Others"


def test_get_geometry_class_for_mapped_types():
    assert XmiSegmentTypeEnum.LINE.get_geometry_class() is XmiLine3D
    assert XmiSegmentTypeEnum.CIRCULAR_ARC.get_geometry_class() is XmiArc3D


@pytest.mark.parametrize("enum_value", [
    XmiSegmentTypeEnum.PARABOLIC_ARC,
    XmiSegmentTypeEnum.BEZIER,
    XmiSegmentTypeEnum.SPLINE,
    XmiSegmentTypeEnum.OTHERS,
])
def test_get_geometry_class_for_unmapped_types(enum_value):
    assert enum_value.get_geometry_class() is None


# .venv/bin/python -m pytest tests/xmi/v2/test_enums/test_xmi_segment_type_enum.py
