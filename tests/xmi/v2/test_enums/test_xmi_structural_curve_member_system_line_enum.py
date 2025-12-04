from xmi.v2.models.enums.xmi_structural_curve_member_system_line_enum import XmiStructuralCurveMemberSystemLineEnum

def test_xmi_structural_curve_member_system_line_enum_values():
    assert XmiStructuralCurveMemberSystemLineEnum.TOP_LEFT.value == "TopLeft"
    assert XmiStructuralCurveMemberSystemLineEnum.TOP_MIDDLE.value == "TopMiddle"
    assert XmiStructuralCurveMemberSystemLineEnum.TOP_RIGHT.value == "TopRight"
    assert XmiStructuralCurveMemberSystemLineEnum.MIDDLE_LEFT.value == "MiddleLeft"
    assert XmiStructuralCurveMemberSystemLineEnum.MIDDLE_MIDDLE.value == "MiddleMiddle"
    assert XmiStructuralCurveMemberSystemLineEnum.MIDDLE_RIGHT.value == "MiddleRight"
    assert XmiStructuralCurveMemberSystemLineEnum.BOTTOM_LEFT.value == "BottomLeft"
    assert XmiStructuralCurveMemberSystemLineEnum.BOTTOM_MIDDLE.value == "BottomMiddle"
    assert XmiStructuralCurveMemberSystemLineEnum.BOTTOM_RIGHT.value == "BottomRight"
    assert XmiStructuralCurveMemberSystemLineEnum.UNKNOWN.value == "Unknown"


# .venv/bin/python -m pytest tests/xmi/v2/test_enums/test_xmi_structural_curve_member_system_line_enum.py