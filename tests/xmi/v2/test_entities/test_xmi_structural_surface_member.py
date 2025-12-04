from xmi.v2.models.entities.structural_analytical.xmi_structural_surface_member import XmiStructuralSurfaceMember
from xmi.v2.models.enums.xmi_structural_surface_member_type_enum import XmiStructuralSurfaceMemberTypeEnum
from xmi.v2.models.enums.xmi_structural_surface_member_system_plane_enum import XmiStructuralSurfaceMemberSystemPlaneEnum
from tests.xmi.v2.test_inputs.xmi_structural_surface_member_input import valid_surface_member_input

def test_surface_member_instantiation():
    instance, errors = XmiStructuralSurfaceMember.from_dict(valid_surface_member_input)

    assert errors == [], f"Unexpected errors during parsing: {errors}"
    assert instance is not None

    assert instance.id == "defc7646-29f3-4f12-93b9-b85142ec1cdf"
    assert instance.name == "defc7646-29f3-4f12-93b9-b85142ec1cdf"
    assert instance.surface_member_type == XmiStructuralSurfaceMemberTypeEnum.UNKNOWN
    assert instance.system_plane == XmiStructuralSurfaceMemberSystemPlaneEnum.UNKNOWN
    assert instance.thickness == 300.0
    assert instance.area == 0.0
    assert instance.z_offset == 0.0
    assert instance.local_axis_x == (1.0, 0.0, 0.0)
    assert instance.local_axis_y == (0.0, 1.0, 0.0)
    assert instance.local_axis_z == (0.0, 0.0, 1.0)
    assert instance.height == 0.0

def test_invalid_surface_member_type():
    bad_input = valid_surface_member_input.copy()
    bad_input["SurfaceMemberType"] = "INVALID_ENUM"
    instance, errors = XmiStructuralSurfaceMember.from_dict(bad_input)
    assert instance is None
    assert any("INVALID_ENUM" in str(e) for e in errors)

def test_malformed_axis_string():
    bad_input = valid_surface_member_input.copy()
    bad_input["LocalAxisX"] = "1,0"
    instance, errors = XmiStructuralSurfaceMember.from_dict(bad_input)
    assert instance is None
    assert any("comma-separated values" in str(e) for e in errors)

def test_missing_required_field():
    bad_input = valid_surface_member_input.copy()
    del bad_input["Thickness"]
    instance, errors = XmiStructuralSurfaceMember.from_dict(bad_input)
    assert instance is None
    assert any("field required" in str(e).lower() for e in errors)


# .venv/bin/python -m pytest tests/xmi/v2/test_entities/test_xmi_structural_surface_member.py