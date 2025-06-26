from src.xmi.v2.models.enums.xmi_structural_surface_member_type_enum import XmiStructuralSurfaceMemberTypeEnum

def test_enum_values():
    assert XmiStructuralSurfaceMemberTypeEnum.SLAB.value == "Slab"
    assert XmiStructuralSurfaceMemberTypeEnum.WALL.value == "Wall"
    assert XmiStructuralSurfaceMemberTypeEnum.PAD_FOOTING.value == "Pad Footing"
    assert XmiStructuralSurfaceMemberTypeEnum.STRIP_FOOTING.value == "Strip Footing"
    assert XmiStructuralSurfaceMemberTypeEnum.PILECAP.value == "Pilecap"
    assert XmiStructuralSurfaceMemberTypeEnum.ROOF_PANEL.value == "Roof Panel"
    assert XmiStructuralSurfaceMemberTypeEnum.WALL_PANEL.value == "Wall Panel"
    assert XmiStructuralSurfaceMemberTypeEnum.RAFT.value == "Raft"


# .venv/bin/python -m pytest tests/xmi/v2/test_enums/test_xmi_structural_surface_member_type_enum.py