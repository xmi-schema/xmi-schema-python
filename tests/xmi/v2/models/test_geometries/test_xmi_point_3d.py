from src.xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D
from tests.xmi.v2.models.test_inputs import xmi_point_3d_input as input_data

def test_valid_point():
    instance, errors = XmiPoint3D.from_dict(input_data.valid_point_input)
    assert instance is not None
    assert instance.x == 1932.2
    assert instance.y == 187.3
    assert instance.z == -3667.1
    assert len(errors) == 0

def test_missing_z():
    instance, errors = XmiPoint3D.from_dict(input_data.missing_z_input)
    assert instance is None
    assert any("Missing attribute: Z" in str(e) for e in errors)

def test_invalid_x():
    instance, errors = XmiPoint3D.from_dict(input_data.invalid_x_input)
    assert instance is None
    assert any("X must be a number")


# .venv/bin/python -m pytest tests/xmi/v2/models/test_geometries/test_xmi_point_3d.py