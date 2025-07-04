from xmi.v2.models.entities.xmi_segment import XmiSegment
from xmi.v2.models.entities.xmi_structural_cross_section import XmiStructuralCrossSection
from xmi.v2.models.entities.xmi_structural_curve_member import XmiStructuralCurveMember
from xmi.v2.models.entities.xmi_structural_material import XmiStructuralMaterial
from xmi.v2.models.entities.xmi_structural_point_connection import XmiStructuralPointConnection
from xmi.v2.models.entities.xmi_structural_storey import XmiStructuralStorey
from xmi.v2.models.entities.xmi_structural_surface_member import XmiStructuralSurfaceMember
from xmi.v2.models.entities.xmi_structural_unit import XmiStructuralUnit
from xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D
from xmi.v2.models.geometries.xmi_line_3d import XmiLine3D
from xmi.v2.models.geometries.xmi_arc_3d import XmiArc3D
from xmi.v2.models.relationships.xmi_has_geometry import XmiHasGeometry
from xmi.v2.models.relationships.xmi_has_line_3d import XmiHasLine3D
from xmi.v2.models.relationships.xmi_has_point_3d import XmiHasPoint3D
from xmi.v2.models.relationships.xmi_has_segment import XmiHasSegment
from xmi.v2.models.relationships.xmi_has_structural_cross_section import XmiHasStructuralCrossSection
from xmi.v2.models.relationships.xmi_has_structural_material import XmiHasStructuralMaterial
from xmi.v2.models.relationships.xmi_has_structural_point_connection import XmiHasStructuralPointConnection
from xmi.v2.models.relationships.xmi_has_structural_storey import XmiHasStructuralStorey

ENTITY_CLASS_MAPPING = {
    "XmiStructuralCrossSection": XmiStructuralCrossSection,
    "XmiStructuralCurveMember": XmiStructuralCurveMember,
    "XmiSegment": XmiSegment,
    "XmiStructuralMaterial": XmiStructuralMaterial,
    "XmiStructuralPointConnection": XmiStructuralPointConnection,
    "XmiStructuralStorey": XmiStructuralStorey,
    "XmiStructuralSurfaceMember": XmiStructuralSurfaceMember,
    "XmiStructuralUnit": XmiStructuralUnit,
    "XmiPoint3D": XmiPoint3D,
    "XmiLine3D": XmiLine3D,
    "XmiArc3D": XmiArc3D,
}

RELATIONSHIP_CLASS_MAPPING = {
    "XmiHasGeometry": XmiHasGeometry,
    "XmiHasLine3D": XmiHasLine3D,
    "XmiHasPoint3D": XmiHasPoint3D,
    "XmiHasSegment": XmiHasSegment,
    "XmiHasStructuralCrossSection": XmiHasStructuralCrossSection,
    "XmiHasStructuralMaterial": XmiHasStructuralMaterial,
    "XmiHasStructuralPointConnection": XmiHasStructuralPointConnection,
    "XmiHasStructuralStorey": XmiHasStructuralStorey,
}