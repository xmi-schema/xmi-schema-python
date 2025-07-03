import json
from xmi.v2.models.xmi_model.xmi_model import XmiModel
from tests.xmi.v2.test_inputs.xmi_model_input import json_data
from xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D
from xmi.v2.models.entities.xmi_structural_material import XmiStructuralMaterial
from xmi.v2.models.entities.xmi_structural_cross_section import XmiStructuralCrossSection
from xmi.v2.models.entities.xmi_structural_curve_member import XmiStructuralCurveMember
from xmi.v2.models.entities.xmi_structural_surface_member import XmiStructuralSurfaceMember

def test_xmi_model_from_json():
    xmi_model = XmiModel.model_validate(json_data)

    model_dict = xmi_model.model_dump(by_alias=True, exclude_none=True)
    print(json.dumps(model_dict, indent=5))

    assert xmi_model.name == "TestModel"
    assert xmi_model.xmi_version == "1.0"
    assert len(xmi_model.entities) == 6

    point_3d = [e for e in xmi_model.entities if isinstance(e, XmiPoint3D)]
    material = [e for e in xmi_model.entities if isinstance(e, XmiStructuralMaterial)]
    cross_sections = [e for e in xmi_model.entities if isinstance(e, XmiStructuralCrossSection)]
    curve_members = [e for e in xmi_model.entities if isinstance(e, XmiStructuralCurveMember)]
    surface_members = [e for e in xmi_model.entities if isinstance(e, XmiStructuralSurfaceMember)]

    assert len(point_3d) == 2
    assert len(material) == 1
    assert len(cross_sections) == 1
    assert len(curve_members) == 1
    assert len(surface_members) == 1


# .venv/bin/python -m pytest -s tests/xmi/v2/test_models/test_xmi_model.py