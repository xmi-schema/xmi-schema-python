from src.xmi.v2.models.enums.xmi_structural_curve_member_system_line_enum import XmiStructuralCurveMemberSystemLineEnum

def test_xmi_structural_curve_member_system_line_enum_values():
    assert XmiStructuralCurveMemberSystemLineEnum.TOP_LEFT.value == "Top Left"
    assert XmiStructuralCurveMemberSystemLineEnum.TOP_MIDDLE.value == "Top Middle"
    assert XmiStructuralCurveMemberSystemLineEnum.TOP_RIGHT.value == "Top Right"
    assert XmiStructuralCurveMemberSystemLineEnum.MIDDLE_LEFT.value == "Middle Left"
    assert XmiStructuralCurveMemberSystemLineEnum.MIDDLE_MIDDLE.value == "Middle Middle"
    assert XmiStructuralCurveMemberSystemLineEnum.MIDDLE_RIGHT.value == "Middle Right"
    assert XmiStructuralCurveMemberSystemLineEnum.BOTTOM_LEFT.value == "Bottom Left"
    assert XmiStructuralCurveMemberSystemLineEnum.BOTTOM_MIDDLE.value == "Bottom Middle"
    assert XmiStructuralCurveMemberSystemLineEnum.BOTTOM_RIGHT.value == "Bottom Right"
    assert XmiStructuralCurveMemberSystemLineEnum.UNKNOWN.value == "Unknown"


# .venv/bin/python -m pytest tests/xmi/v2/test_enums/test_xmi_structural_curve_member_system_line_enum.py