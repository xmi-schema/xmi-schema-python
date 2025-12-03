import json
import pytest
from tests.xmi.v2.test_inputs.xmi_manager_input import json_xmi_data
from xmi.v2.models.xmi_model.xmi_manager import XmiManager
from xmi.v2.models.entities.xmi_structural_material import XmiStructuralMaterial
from xmi.v2.models.entities.xmi_structural_cross_section import XmiCrossSection
from xmi.v2.models.entities.xmi_structural_curve_member import XmiStructuralCurveMember
from xmi.v2.models.entities.xmi_structural_surface_member import XmiStructuralSurfaceMember
from xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D
from xmi.v2.models.relationships.xmi_has_structural_material import XmiHasStructuralMaterial
from xmi.v2.models.relationships.xmi_has_structural_cross_section import XmiHasCrossSection
from xmi.v2.models.relationships.xmi_has_structural_storey import XmiHasStructuralStorey


def test_xmi_manager_parsing():
    manager = XmiManager()
    model = manager.read_xmi_dict(json_xmi_data)

    model_dict = model.model_dump(by_alias=True, exclude_none=True)
    print(json.dumps(model_dict, indent=4))

    assert model is not None
    assert len(model.entities) == 7

    assert any(isinstance(e, XmiStructuralMaterial) for e in model.entities)
    assert any(isinstance(e, XmiCrossSection) for e in model.entities)
    assert any(isinstance(e, XmiStructuralCurveMember) for e in model.entities)
    assert any(isinstance(e, XmiStructuralSurfaceMember) for e in model.entities)
    assert any(isinstance(e, XmiPoint3D) for e in model.entities)

    assert len(model.relationships) > 0
    assert any(isinstance(r, XmiHasStructuralMaterial) for r in model.relationships)
    assert any(isinstance(r, XmiHasCrossSection) for r in model.relationships)
    assert any(isinstance(r, XmiHasStructuralStorey) for r in model.relationships)


if __name__ == "__main__":
    pytest.main([__file__])


# .venv/bin/python -m pytest -s tests/xmi/v2/test_models/test_xmi_manager.py