from xmi.v2.models.entities.xmi_structural_curve_member import XmiStructuralCurveMember
from xmi.v2.models.enums.xmi_structural_curve_member_type_enum import XmiStructuralCurveMemberTypeEnum
from xmi.v2.models.enums.xmi_structural_curve_member_system_line_enum import XmiStructuralCurveMemberSystemLineEnum
from tests.xmi.v2.test_inputs.xmi_structural_curve_member_input import valid_curve_member_input

def test_curve_member_instantiation():
    instance, errors = XmiStructuralCurveMember.from_dict(valid_curve_member_input)

    assert errors == [], f"Unexpected errors during parsing: {errors}"
    assert instance is not None

    assert instance.name == "eebf4b4f-14b0-4be1-8a6d-94b9858cff4a"
    assert instance.curve_member_type == XmiStructuralCurveMemberTypeEnum.UNKNOWN
    assert instance.system_line == XmiStructuralCurveMemberSystemLineEnum.UNKNOWN
    assert instance.local_axis_x == (0.0, 0.0, 1.0)
    assert instance.local_axis_y == (1.0, 0.0, 0.0)
    assert instance.local_axis_z == (0.0, 1.0, 0.0)
    assert instance.length == 0.0


def test_invalid_local_axis_format():
    bad_input = valid_curve_member_input.copy()
    bad_input["LocalAxisX"] = "0,0"

    instance, errors = XmiStructuralCurveMember.from_dict(bad_input)
    print(errors)
    
    assert instance is None
    assert any("must contain exactly 3 comma-separated values" in str(e) for e in errors)


def test_non_float_axis_component():
    bad_input = valid_curve_member_input.copy()
    bad_input["LocalAxisX"] = "a,b,c"

    instance, errors = XmiStructuralCurveMember.from_dict(bad_input)

    assert instance is None
    assert any("must be valid numbers" in str(e) for e in errors)


def test_invalid_enum_values():
    bad_input = valid_curve_member_input.copy()
    bad_input["CurveMemberType"] = "NotAValidEnum"

    instance, errors = XmiStructuralCurveMember.from_dict(bad_input)

    assert instance is None
    assert any("Invalid XmiStructuralCurveMemberTypeEnum value" in str(e) for e in errors)


# .venv/bin/python -m pytest tests/xmi/v2/test_entities/test_xmi_structural_curve_member.py