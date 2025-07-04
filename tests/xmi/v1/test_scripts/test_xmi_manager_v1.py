import json

from xmi.v1.xmi_manager import XmiManager
from xmi.v1.entities.xmi_structural_material import XmiStructuralMaterial
from xmi.v1.entities.xmi_structural_cross_section import XmiStructuralCrossSection
from xmi.v1.entities.xmi_structural_point_connection import XmiStructuralPointConnection
from xmi.v1.entities.xmi_structural_curve_member import XmiStructuralCurveMember
from xmi.v1.entities.xmi_structural_surface_member import XmiStructuralSurfaceMember

from xmi.v1.entities.xmi_segment import XmiSegment

from xmi.v1.geometries.xmi_point_3d import XmiPoint3D
from xmi.v1.geometries.xmi_line_3d import XmiLine3D

from xmi.v1.relationships.xmi_has_structural_material import XmiHasStructuralMaterial
from xmi.v1.relationships.xmi_has_structural_node import XmiHasStructuralNode
from xmi.v1.relationships.xmi_has_structural_cross_section import XmiHasStructuralCrossSection
from xmi.v1.relationships.xmi_has_segment import XmiHasSegment
from xmi.v1.relationships.xmi_has_geometry import XmiHasGeometry

TEST_INPUTS_DIRECTORY = "tests/xmi/v1/test_inputs/xmi_manager"


# @pytest.mark.skip()
def test_xmi_manager_1():
    # ERROR FOUND IN DATA as material values should not be 0.0
    FILENAME = "xmi_structural_manager_test_1.json"
    json_path = "{test_inputs_directory}/{filename}".format(
        test_inputs_directory=TEST_INPUTS_DIRECTORY, filename=FILENAME)
    with open(json_path, 'r') as f:
        xmi_file_dict = json.load(f)

    xmi_manager = XmiManager()
    xmi_model = xmi_manager.read_xmi_dict(xmi_file_dict)

    print(xmi_model)

    # StructuralMaterial = 1
    # StructuralPointConnection = 562
    # StructuralCurveMember = 555
    # Line3D = 555
    # Point3D = 562
    # StructuralCrossSection = 8

    xmi_structural_materials_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiStructuralMaterial)]
    # cannot find because cross sections has errors
    xmi_structural_cross_sections_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiStructuralCrossSection)]
    xmi_structural_point_connections_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiStructuralPointConnection)]
    xmi_point_3d_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiPoint3D)]
    xmi_line_3d_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiLine3D)]
    xmi_segments_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiSegment)]
    xmi_structural_curve_members_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiStructuralCurveMember)]
    xmi_structural_surface_members_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiStructuralSurfaceMember)]

    assert len(xmi_structural_materials_found) == 1
    assert len(xmi_structural_cross_sections_found) == 8
    assert len(xmi_structural_point_connections_found) == 562
    assert len(xmi_structural_curve_members_found) == 555
    assert len(xmi_structural_surface_members_found) == 334

    assert len(xmi_point_3d_found) == 562


# @pytest.mark.skip()
def test_xmi_manager_test0_bim1():
    # error found in ZOffet not in StructuralSurfaceMember
    FILENAME = "test0-bim1.json"
    json_path = "{test_inputs_directory}/{filename}".format(
        test_inputs_directory=TEST_INPUTS_DIRECTORY, filename=FILENAME)
    # json_path = "after_install_tests/xmi/v1/test_inputs/xmi_manager/test0-bim1.json"
    with open(json_path, 'r') as f:
        xmi_file_dict = json.load(f)

    xmi_manager = XmiManager()
    xmi_model = xmi_manager.read_xmi_dict(xmi_file_dict)

    xmi_structural_materials_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiStructuralMaterial)]
    xmi_structural_cross_sections_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiStructuralCrossSection)]
    xmi_structural_surface_members_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiStructuralSurfaceMember)]

    assert len(xmi_structural_materials_found) == 4
    assert len(xmi_structural_cross_sections_found) == 7
    assert len(xmi_structural_surface_members_found) == 0


# @pytest.mark.skip()
def test_xmi_manager_test0_analysis1():
    # bug found inside test0-analysis1.json
    # StructuralCrossSection's material should refer to 'Name' of the StructuralMaterial instance and not the 'Type' of the StructuralMaterial instance.
    FILENAME = "test0-analysis1_mod.json"
    json_path = "{test_inputs_directory}/{filename}".format(
        test_inputs_directory=TEST_INPUTS_DIRECTORY, filename=FILENAME)
    with open(json_path, 'r') as f:
        xmi_file_dict = json.load(f)

    xmi_manager = XmiManager()
    xmi_model = xmi_manager.read_xmi_dict(xmi_file_dict)

    xmi_structural_materials_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiStructuralMaterial)]
    xmi_structural_cross_sections_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiStructuralCrossSection)]

    assert len(xmi_structural_materials_found) == 3
    # ERROR FOUND IN STRUCTURAL_CROSS_SECTIONS
    assert len(xmi_structural_cross_sections_found) == 7


# @pytest.mark.skip()
def test_xmi_manager_test0_bim1_mod():
    # bug found inside test0-analysis1.json
    # StructuralCrossSection's material should refer to 'Name' of the StructuralMaterial instance and not the 'Type' of the StructuralMaterial instance.
    FILENAME = "test0-bim1_mod.json"
    json_path = "{test_inputs_directory}/{filename}".format(
        test_inputs_directory=TEST_INPUTS_DIRECTORY, filename=FILENAME)
    with open(json_path, 'r') as f:
        xmi_file_dict = json.load(f)

    xmi_manager = XmiManager()
    xmi_model = xmi_manager.read_xmi_dict(xmi_file_dict)

    xmi_structural_materials_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiStructuralMaterial)]
    xmi_structural_cross_sections_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiStructuralCrossSection)]
    xmi_structural_surface_members_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiStructuralSurfaceMember)]
    xmi_structural_curve_members_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiStructuralCurveMember)]

    assert len(xmi_structural_materials_found) == 4
    assert len(xmi_structural_cross_sections_found) == 7
    assert len(xmi_structural_surface_members_found) == 8


# @pytest.mark.skip()
def test_xmi_manager_test0_analysis1_mod():
    # bug found inside test0-analysis1.json
    # StructuralCrossSection's material should refer to 'Name' of the StructuralMaterial instance and not the 'Type' of the StructuralMaterial instance.
    FILENAME = "test0-analysis1_mod.json"
    json_path = "{test_inputs_directory}/{filename}".format(
        test_inputs_directory=TEST_INPUTS_DIRECTORY, filename=FILENAME)
    with open(json_path, 'r') as f:
        xmi_file_dict = json.load(f)

    xmi_manager = XmiManager()
    xmi_model = xmi_manager.read_xmi_dict(xmi_file_dict)

    xmi_structural_materials_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiStructuralMaterial)]
    xmi_structural_cross_sections_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiStructuralCrossSection)]

    assert len(xmi_structural_materials_found) == 3
    # ERROR FOUND IN STRUCTURAL_CROSS_SECTIONS
    assert len(xmi_structural_cross_sections_found) == 7


# @pytest.mark.skip()
def test_xmi_manager_2():
    # error found in ZOffet not in StructuralSurfaceMember
    FILENAME = "xmi_structural_manager_test_2.json"
    json_path = "{test_inputs_directory}/{filename}".format(
        test_inputs_directory=TEST_INPUTS_DIRECTORY, filename=FILENAME)
    # json_path = "after_install_tests/xmi/v1/test_inputs/xmi_manager/test0-bim1.json"
    with open(json_path, 'r') as f:
        xmi_file_dict = json.load(f)

    xmi_manager = XmiManager()
    xmi_model = xmi_manager.read_xmi_dict(xmi_file_dict)

    print(xmi_model)

    # StructuralMaterial = 1
    # StructuralCrossSection = 1
    # HasStructuralMaterialRelationship = 1

    # assert len(xmi_model.entities) == 3
    # assert len(xmi_model.relationships) == 2

    xmi_structural_materials_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiStructuralMaterial)]
    xmi_structural_cross_sections_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiStructuralCrossSection)]
    xmi_structural_point_connections_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiStructuralPointConnection)]
    xmi_point_3d_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiPoint3D)]
    xmi_line_3d_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiLine3D)]

    xmi_has_structural_material_relationships_found = [
        obj for obj in xmi_model.relationships if isinstance(obj, XmiHasStructuralMaterial)]
    xmi_has_geometry_relationships_found = [
        obj for obj in xmi_model.relationships if isinstance(obj, XmiHasGeometry)]

    assert len(xmi_structural_materials_found) == 1
    assert len(xmi_structural_cross_sections_found) == 1
    assert len(xmi_structural_point_connections_found) == 1

    assert len(xmi_point_3d_found) == 1
    assert len(xmi_line_3d_found) == 0

    assert len(xmi_has_structural_material_relationships_found) == 1
    assert len(xmi_has_geometry_relationships_found) == 1

    xmi_has_structural_material = xmi_has_structural_material_relationships_found[0]
    assert xmi_has_structural_material.source == xmi_structural_cross_sections_found[0]
    assert xmi_has_structural_material.target == xmi_structural_materials_found[0]


# @pytest.mark.skip()
def test_xmi_manager_3():
    FILENAME = "xmi_structural_manager_test_3.json"
    json_path = "{test_inputs_directory}/{filename}".format(
        test_inputs_directory=TEST_INPUTS_DIRECTORY, filename=FILENAME)
    # json_path = "tests/xmi/v1/test_inputs/xmi_manager/xmi_structural_manager_test_3.json"
    with open(json_path, 'r') as f:
        xmi_file_dict = json.load(f)

    xmi_manager = XmiManager()
    xmi_model = xmi_manager.read_xmi_dict(xmi_file_dict)

    print(xmi_model)

    # StructuralMaterial = 1
    # StructuralCrossSection = 1
    # HasStructuralMaterialRelationship = 1

    xmi_structural_materials_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiStructuralMaterial)]
    xmi_structural_cross_sections_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiStructuralCrossSection)]
    xmi_structural_point_connections_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiStructuralPointConnection)]
    xmi_structural_curve_members_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiStructuralCurveMember)]
    xmi_point_3d_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiPoint3D)]
    xmi_line_3d_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiLine3D)]
    xmi_segments_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiSegment)]

    xmi_has_structural_material_relationships_found = [
        obj for obj in xmi_model.relationships if isinstance(obj, XmiHasStructuralMaterial)]
    xmi_has_segment_relationships_found = [
        obj for obj in xmi_model.relationships if isinstance(obj, XmiHasSegment)]
    xmi_has_structural_cross_sections_relationships_found = [
        obj for obj in xmi_model.relationships if isinstance(obj, XmiHasStructuralCrossSection)]
    xmi_has_structural_nodes_relationships_found = [
        obj for obj in xmi_model.relationships if isinstance(obj, XmiHasStructuralNode)]
    xmi_has_geometry_relationships_found = [
        obj for obj in xmi_model.relationships if isinstance(obj, XmiHasGeometry)]

    assert len(xmi_model.entities) == 9
    assert len(xmi_model.relationships) == 12

    assert len(xmi_structural_materials_found) == 1
    assert len(xmi_structural_cross_sections_found) == 1
    assert len(xmi_structural_point_connections_found) == 2
    assert len(xmi_structural_curve_members_found) == 1
    assert len(xmi_segments_found) == 1
    assert len(xmi_point_3d_found) == 2
    assert len(xmi_line_3d_found) == 1

    assert len(xmi_has_structural_material_relationships_found) == 1
    assert len(xmi_has_structural_cross_sections_relationships_found) == 1
    assert len(xmi_has_geometry_relationships_found) == 5
    assert len(xmi_has_segment_relationships_found) == 1
    assert len(xmi_has_structural_nodes_relationships_found) == 4

    xmi_has_structural_material = xmi_has_structural_material_relationships_found[0]
    assert xmi_has_structural_material.source == xmi_structural_cross_sections_found[0]
    assert xmi_has_structural_material.target == xmi_structural_materials_found[0]


# @pytest.mark.skip()
def test_xmi_manager_4():
    FILENAME = "xmi_structural_manager_test_4.json"
    json_path = "{test_inputs_directory}/{filename}".format(
        test_inputs_directory=TEST_INPUTS_DIRECTORY, filename=FILENAME)
    # json_path = "tests/xmi/v1/test_inputs/xmi_manager/xmi_structural_manager_test_4.json"
    with open(json_path, 'r') as f:
        xmi_file_dict = json.load(f)

    xmi_manager = XmiManager()
    xmi_model = xmi_manager.read_xmi_dict(xmi_file_dict)

    print(xmi_model)

    # StructuralMaterial = 1
    # StructuralSurfaceMember = 1
    # HasStructuralMaterialRelationship = 1
    # Segment = 4
    # Line3D = 4
    # Point3D = 4
    # StructuralPointConnection = 4

    xmi_structural_materials_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiStructuralMaterial)]
    xmi_structural_point_connections_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiStructuralPointConnection)]
    xmi_structural_surface_members_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiStructuralSurfaceMember)]
    xmi_point_3d_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiPoint3D)]
    xmi_line_3d_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiLine3D)]
    xmi_segments_found = [
        obj for obj in xmi_model.entities if isinstance(obj, XmiSegment)]

    xmi_has_structural_material_relationships_found = [
        obj for obj in xmi_model.relationships if isinstance(obj, XmiHasStructuralMaterial)]
    xmi_has_segment_relationships_found = [
        obj for obj in xmi_model.relationships if isinstance(obj, XmiHasSegment)]
    xmi_has_structural_structural_nodes_relationships_found = [
        obj for obj in xmi_model.relationships if isinstance(obj, XmiHasStructuralNode)]
    xmi_has_geometry_relationships_found = [
        obj for obj in xmi_model.relationships if isinstance(obj, XmiHasGeometry)]

    assert len(xmi_model.entities) == 18
    assert len(xmi_model.relationships) == 29

    assert len(xmi_structural_materials_found) == 1
    assert len(xmi_structural_point_connections_found) == 4
    assert len(xmi_segments_found) == 4
    assert len(xmi_point_3d_found) == 4
    assert len(xmi_line_3d_found) == 4
    assert len(xmi_structural_surface_members_found) == 1

    assert len(xmi_has_structural_material_relationships_found) == 1
    assert len(xmi_has_geometry_relationships_found) == 12
    assert len(xmi_has_segment_relationships_found) == 4
    assert len(xmi_has_structural_structural_nodes_relationships_found) == 12
