import json
import pytest
from tests.xmi.v2.test_inputs.xmi_model_input import json_data
from xmi.v2.models.xmi_model.xmi_model import XmiModel
from xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D
from xmi.v2.models.entities.xmi_material import XmiMaterial
from xmi.v2.models.entities.xmi_cross_section import XmiCrossSection
from xmi.v2.models.entities.structural_analytical.xmi_structural_curve_member import XmiStructuralCurveMember
from xmi.v2.models.entities.structural_analytical.xmi_structural_surface_member import XmiStructuralSurfaceMember
from xmi.v2.models.entities.xmi_storey import XmiStorey
from xmi.v2.models.relationships.xmi_has_material import XmiHasMaterial
from xmi.v2.models.relationships.xmi_has_cross_section import XmiHasCrossSection
from xmi.v2.models.relationships.xmi_has_storey import XmiHasStorey


def test_xmi_model_from_json():
    xmi_model = XmiModel()
    xmi_model.load_from_dict(json_data)

    model_dict = xmi_model.model_dump(by_alias=True, exclude_none=True)
    print(json.dumps(model_dict, indent=4))

    assert xmi_model.name == "TestModel"
    assert xmi_model.xmi_version == "1.0"
    assert len(xmi_model.entities) == 7

    assert len(xmi_model.errors) >= 0 

    point_3d = [e for e in xmi_model.entities if isinstance(e, XmiPoint3D)]
    material = [e for e in xmi_model.entities if isinstance(e, XmiMaterial)]
    cross_sections = [e for e in xmi_model.entities if isinstance(e, XmiCrossSection)]
    curve_members = [e for e in xmi_model.entities if isinstance(e, XmiStructuralCurveMember)]
    surface_members = [e for e in xmi_model.entities if isinstance(e, XmiStructuralSurfaceMember)]
    storeys = [e for e in xmi_model.entities if isinstance(e, XmiStorey)]

    assert len(point_3d) == 2
    assert len(material) == 1
    assert len(cross_sections) == 1
    assert len(curve_members) == 1
    assert len(surface_members) == 1
    assert len(storeys) == 1

    has_material = [r for r in xmi_model.relationships if isinstance(r, XmiHasMaterial)]
    has_cross_section = [r for r in xmi_model.relationships if isinstance(r, XmiHasCrossSection)]
    has_storey = [r for r in xmi_model.relationships if isinstance(r, XmiHasStorey)]

    assert len(has_material) == 1
    assert len(has_cross_section) == 1
    assert len(has_storey) == 1 


if __name__ == "__main__":
    pytest.main([__file__])


# .venv/bin/python -m pytest -s tests/xmi/v2/test_models/test_xmi_model.py