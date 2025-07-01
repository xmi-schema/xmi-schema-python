import pytest
from src.xmi.v2.models.entities.xmi_structural_curve_member import XmiStructuralCurveMember
from src.xmi.v2.models.enums.xmi_structural_curve_member_type_enum import XmiStructuralCurveMemberTypeEnum
from src.xmi.v2.models.enums.xmi_structural_curve_member_system_line_enum import XmiStructuralCurveMemberSystemLineEnum
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


# .venv/bin/python -m pytest tests/xmi/v2/test_entities/test_xmi_structural_curve_member.py