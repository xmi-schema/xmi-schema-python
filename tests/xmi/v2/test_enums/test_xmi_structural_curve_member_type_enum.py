from xmi.v2.models.enums.xmi_structural_curve_member_type_enum import XmiStructuralCurveMemberTypeEnum

def test_enum_values():
    assert XmiStructuralCurveMemberTypeEnum.BEAM.value == "Beam"
    assert XmiStructuralCurveMemberTypeEnum.COLUMN.value == "Column"
    assert XmiStructuralCurveMemberTypeEnum.BRACING.value == "Bracing"
    assert XmiStructuralCurveMemberTypeEnum.OTHER.value == "Other"


# .venv/bin/python -m pytest tests/xmi/v2/test_enums/test_xmi_structural_curve_member_type_enum.py