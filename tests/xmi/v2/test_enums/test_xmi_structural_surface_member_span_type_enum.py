from src.xmi.v2.models.enums.xmi_structural_surface_member_span_type_enum import XmiStructuralSurfaceMemberSpanTypeEnum

def test_xmi_shape_enum_values():
    assert XmiStructuralSurfaceMemberSpanTypeEnum.ONE_WAY.value == "One Way"
    assert XmiStructuralSurfaceMemberSpanTypeEnum.TWO_WAY.value == "Two Way"


# .venv/bin/python -m pytest tests/xmi/v2/test_enums/test_xmi_structural_surface_member_span_type_enum.py