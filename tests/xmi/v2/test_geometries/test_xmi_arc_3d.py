from xmi.v2.models.geometries.xmi_arc_3d import XmiArc3D
from xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D
from tests.xmi.v2.test_inputs import xmi_arc_3d_input as input_data

def test_valid_arc():
    instance, errors = XmiArc3D.from_dict(input_data.valid_arc_input)
    assert instance is not None
    assert isinstance(instance.start_point, XmiPoint3D)
    assert isinstance(instance.end_point, XmiPoint3D)
    assert isinstance(instance.center_point, XmiPoint3D)
    assert instance.radius == 0.5
    assert instance.name == "Arc between P1 and P2"
    assert len(errors) == 0

def test_missing_center_point():
    instance, errors = XmiArc3D.from_dict(input_data.missing_center_input)
    assert instance is None
    assert any("Missing attribute: center_point" in str(e) for e in errors)


# .venv/bin/python -m pytest tests/xmi/v2/test_geometries/test_xmi_arc_3d.py