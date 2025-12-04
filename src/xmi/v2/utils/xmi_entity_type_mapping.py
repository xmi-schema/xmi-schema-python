from xmi.v2.models.entities.xmi_segment import XmiSegment
from xmi.v2.models.entities.xmi_cross_section import XmiCrossSection
from xmi.v2.models.entities.xmi_structural_curve_member import XmiStructuralCurveMember
from xmi.v2.models.entities.xmi_material import XmiMaterial
from xmi.v2.models.entities.xmi_structural_point_connection import XmiStructuralPointConnection
from xmi.v2.models.entities.xmi_storey import XmiStorey
from xmi.v2.models.entities.xmi_structural_surface_member import XmiStructuralSurfaceMember
from xmi.v2.models.entities.xmi_unit import XmiUnit
from xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D
from xmi.v2.models.geometries.xmi_line_3d import XmiLine3D
from xmi.v2.models.geometries.xmi_arc_3d import XmiArc3D
from xmi.v2.models.relationships.xmi_has_geometry import XmiHasGeometry
from xmi.v2.models.relationships.xmi_has_line_3d import XmiHasLine3D
from xmi.v2.models.relationships.xmi_has_point_3d import XmiHasPoint3D
from xmi.v2.models.relationships.xmi_has_segment import XmiHasSegment
from xmi.v2.models.relationships.xmi_has_cross_section import XmiHasCrossSection
from xmi.v2.models.relationships.xmi_has_material import XmiHasMaterial
from xmi.v2.models.relationships.xmi_has_structural_point_connection import XmiHasStructuralPointConnection
from xmi.v2.models.relationships.xmi_has_storey import XmiHasStorey

ENTITY_CLASS_MAPPING = {
    "XmiCrossSection": XmiCrossSection,
    "XmiStructuralCurveMember": XmiStructuralCurveMember,
    "XmiSegment": XmiSegment,
    "XmiStructuralMaterial": XmiMaterial,
    "XmiStructuralPointConnection": XmiStructuralPointConnection,
    "XmiStorey": XmiStorey,
    "XmiStructuralSurfaceMember": XmiStructuralSurfaceMember,
    "XmiUnit": XmiUnit,
    "XmiPoint3D": XmiPoint3D,
    "XmiLine3D": XmiLine3D,
    "XmiArc3D": XmiArc3D,
}

RELATIONSHIP_CLASS_MAPPING = {
    "XmiHasGeometry": XmiHasGeometry,
    "XmiHasLine3D": XmiHasLine3D,
    "XmiHasPoint3D": XmiHasPoint3D,
    "XmiHasSegment": XmiHasSegment,
    "XmiHasCrossSection": XmiHasCrossSection,
    "XmiHasStructuralMaterial": XmiHasMaterial,
    "XmiHasStructuralPointConnection": XmiHasStructuralPointConnection,
    "XmiHasStructuralStorey": XmiHasStorey,
}