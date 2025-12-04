from xmi.v2.models.entities.xmi_segment import XmiSegment
from xmi.v2.models.entities.xmi_cross_section import XmiCrossSection
from xmi.v2.models.entities.structural_analytical.xmi_structural_curve_member import XmiStructuralCurveMember
from xmi.v2.models.entities.xmi_material import XmiStructuralMaterial
from xmi.v2.models.entities.structural_analytical.xmi_structural_point_connection import XmiStructuralPointConnection
from xmi.v2.models.entities.xmi_storey import XmiStorey
from xmi.v2.models.entities.structural_analytical.xmi_structural_surface_member import XmiStructuralSurfaceMember
from xmi.v2.models.entities.xmi_unit import XmiUnit
from xmi.v2.models.entities.physical.xmi_beam import XmiBeam
from xmi.v2.models.entities.physical.xmi_column import XmiColumn
from xmi.v2.models.entities.physical.xmi_slab import XmiSlab
from xmi.v2.models.entities.physical.xmi_wall import XmiWall
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
from xmi.v2.models.relationships.xmi_has_structural_curve_member import XmiHasStructuralCurveMember

ENTITY_CLASS_MAPPING = {
    "XmiCrossSection": XmiCrossSection,
    "XmiStructuralCurveMember": XmiStructuralCurveMember,
    "XmiSegment": XmiSegment,
    "XmiStructuralMaterial": XmiStructuralMaterial,
    "XmiStructuralPointConnection": XmiStructuralPointConnection,
    "XmiStorey": XmiStorey,
    "XmiStructuralSurfaceMember": XmiStructuralSurfaceMember,
    "XmiUnit": XmiUnit,
    "XmiBeam": XmiBeam,
    "XmiColumn": XmiColumn,
    "XmiSlab": XmiSlab,
    "XmiWall": XmiWall,
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
    "XmiHasStructuralCurveMember": XmiHasStructuralCurveMember,
}
