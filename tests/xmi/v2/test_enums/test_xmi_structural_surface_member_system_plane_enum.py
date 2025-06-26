from src.xmi.v2.models.enums.xmi_structural_surface_member_system_plane_enum import XmiStructuralSurfaceMemberSystemPlaneEnum

def test_enum_values():
    assert XmiStructuralSurfaceMemberSystemPlaneEnum.BOTTOM.value == "Bottom"
    assert XmiStructuralSurfaceMemberSystemPlaneEnum.TOP.value == "Top"
    assert XmiStructuralSurfaceMemberSystemPlaneEnum.MIDDLE.value == "Middle"
    assert XmiStructuralSurfaceMemberSystemPlaneEnum.LEFT.value == "Left"
    assert XmiStructuralSurfaceMemberSystemPlaneEnum.RIGHT.value == "Right"


# .venv/bin/python -m pytest tests/xmi/v2/test_enums/test_xmi_structural_surface_member_system_plane_enum.py