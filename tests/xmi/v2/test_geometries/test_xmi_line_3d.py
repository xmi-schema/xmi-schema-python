from src.xmi.v2.models.geometries.xmi_line_3d import XmiLine3D
from src.xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D
from tests.xmi.v2.test_inputs import xmi_line_3d_input as input_data

def test_valid_line():
    instance, errors = XmiLine3D.from_dict(input_data.valid_line_input)
    assert instance is not None
    assert isinstance(instance.start_point, XmiPoint3D)
    assert isinstance(instance.end_point, XmiPoint3D)
    assert instance.start_point.x == 1932.2
    assert instance.end_point.z == -3667.1
    assert len(errors) == 0

def test_missing_end_point():
    instance, errors = XmiLine3D.from_dict(input_data.missing_end_input)
    assert instance is None
    assert any("Missing attribute: end_point" in str(e) for e in errors)

def test_invalid_start_point_type():
    instance, errors = XmiLine3D.from_dict(input_data.invalid_start_point_input)
    assert instance is None
    assert any("Missing attribute: X" in str(e) or "value is not a valid float" in str(e) for e in errors)


# .venv/bin/python -m pytest tests/xmi/v2/test_geometries/test_xmi_line_3d.py