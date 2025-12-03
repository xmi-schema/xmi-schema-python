import pytest
from xmi.v1.geometries.xmi_arc_3d import XmiArc3D
from xmi.v1.geometries.xmi_point_3d import XmiPoint3D


def test_xmi_arc_3d_creation_valid():
    """Test creating a valid XmiArc3D instance"""
    start_point = XmiPoint3D(x=0.0, y=0.0, z=0.0, id="start_1")
    end_point = XmiPoint3D(x=10.0, y=0.0, z=0.0, id="end_1")
    center_point = XmiPoint3D(x=5.0, y=5.0, z=0.0, id="center_1")

    arc = XmiArc3D(
        start_point=start_point,
        end_point=end_point,
        center_point=center_point,
        id="arc_1",
        name="Test Arc",
        description="Test arc description",
        ifcguid="test_guid_123"
    )

    assert arc.start_point == start_point
    assert arc.end_point == end_point
    assert arc.center_point == center_point
    assert arc.id == "arc_1"
    assert arc.name == "Test Arc"
    assert arc.description == "Test arc description"
    assert arc.ifcguid == "test_guid_123"
    assert arc.entity_type == "XmiArc3D"


def test_xmi_arc_3d_creation_minimal():
    """Test creating XmiArc3D with minimal required parameters"""
    start_point = XmiPoint3D(x=0.0, y=0.0, z=0.0)
    end_point = XmiPoint3D(x=10.0, y=0.0, z=0.0)
    center_point = XmiPoint3D(x=5.0, y=5.0, z=0.0)

    arc = XmiArc3D(
        start_point=start_point,
        end_point=end_point,
        center_point=center_point
    )

    assert arc.start_point == start_point
    assert arc.end_point == end_point
    assert arc.center_point == center_point


def test_xmi_arc_3d_missing_start_point():
    """Test that ValueError is raised when start_point is None"""
    end_point = XmiPoint3D(x=10.0, y=0.0, z=0.0)
    center_point = XmiPoint3D(x=5.0, y=5.0, z=0.0)

    with pytest.raises(ValueError, match="'start_point' parameter is compulsory"):
        XmiArc3D(
            start_point=None,
            end_point=end_point,
            center_point=center_point
        )


def test_xmi_arc_3d_missing_end_point():
    """Test that ValueError is raised when end_point is None"""
    start_point = XmiPoint3D(x=0.0, y=0.0, z=0.0)
    center_point = XmiPoint3D(x=5.0, y=5.0, z=0.0)

    with pytest.raises(ValueError, match="'end_point' parameter is compulsory"):
        XmiArc3D(
            start_point=start_point,
            end_point=None,
            center_point=center_point
        )


def test_xmi_arc_3d_missing_center_point():
    """Test that ValueError is raised when center_point is None"""
    start_point = XmiPoint3D(x=0.0, y=0.0, z=0.0)
    end_point = XmiPoint3D(x=10.0, y=0.0, z=0.0)

    with pytest.raises(ValueError, match="'center_point' parameter is compulsory"):
        XmiArc3D(
            start_point=start_point,
            end_point=end_point,
            center_point=None
        )


def test_xmi_arc_3d_invalid_start_point_type():
    """Test that TypeError is raised when start_point is not XmiPoint3D"""
    end_point = XmiPoint3D(x=10.0, y=0.0, z=0.0)
    center_point = XmiPoint3D(x=5.0, y=5.0, z=0.0)

    with pytest.raises(TypeError, match="start_point should be an XmiPoint3D"):
        XmiArc3D(
            start_point="invalid",
            end_point=end_point,
            center_point=center_point
        )


def test_xmi_arc_3d_invalid_end_point_type():
    """Test that TypeError is raised when end_point is not XmiPoint3D"""
    start_point = XmiPoint3D(x=0.0, y=0.0, z=0.0)
    center_point = XmiPoint3D(x=5.0, y=5.0, z=0.0)

    with pytest.raises(TypeError, match="end_point should be an XmiPoint3D"):
        XmiArc3D(
            start_point=start_point,
            end_point=123,
            center_point=center_point
        )


def test_xmi_arc_3d_invalid_center_point_type():
    """Test that TypeError is raised when center_point is not XmiPoint3D"""
    start_point = XmiPoint3D(x=0.0, y=0.0, z=0.0)
    end_point = XmiPoint3D(x=10.0, y=0.0, z=0.0)

    with pytest.raises(TypeError, match="center_point should be an XmiPoint3D"):
        XmiArc3D(
            start_point=start_point,
            end_point=end_point,
            center_point=[5.0, 5.0, 0.0]
        )


def test_xmi_arc_3d_property_setters():
    """Test that property setters work correctly"""
    start_point_1 = XmiPoint3D(x=0.0, y=0.0, z=0.0)
    end_point_1 = XmiPoint3D(x=10.0, y=0.0, z=0.0)
    center_point_1 = XmiPoint3D(x=5.0, y=5.0, z=0.0)

    arc = XmiArc3D(
        start_point=start_point_1,
        end_point=end_point_1,
        center_point=center_point_1
    )

    # Change points
    start_point_2 = XmiPoint3D(x=1.0, y=1.0, z=1.0)
    end_point_2 = XmiPoint3D(x=11.0, y=1.0, z=1.0)
    center_point_2 = XmiPoint3D(x=6.0, y=6.0, z=1.0)

    arc.start_point = start_point_2
    arc.end_point = end_point_2
    arc.center_point = center_point_2

    assert arc.start_point == start_point_2
    assert arc.end_point == end_point_2
    assert arc.center_point == center_point_2


def test_xmi_arc_3d_property_setter_type_validation():
    """Test that property setters validate types"""
    start_point = XmiPoint3D(x=0.0, y=0.0, z=0.0)
    end_point = XmiPoint3D(x=10.0, y=0.0, z=0.0)
    center_point = XmiPoint3D(x=5.0, y=5.0, z=0.0)

    arc = XmiArc3D(
        start_point=start_point,
        end_point=end_point,
        center_point=center_point
    )

    # Try to set invalid types
    with pytest.raises(TypeError, match="start_point should be an XmiPoint3D"):
        arc.start_point = "invalid"

    with pytest.raises(TypeError, match="end_point should be an XmiPoint3D"):
        arc.end_point = 123

    with pytest.raises(TypeError, match="center_point should be an XmiPoint3D"):
        arc.center_point = {"x": 1, "y": 2, "z": 3}


def test_xmi_arc_3d_from_dict_valid():
    """Test creating XmiArc3D from dictionary"""
    start_point = XmiPoint3D(x=0.0, y=0.0, z=0.0, id="start_1")
    end_point = XmiPoint3D(x=10.0, y=0.0, z=0.0, id="end_1")
    center_point = XmiPoint3D(x=5.0, y=5.0, z=0.0, id="center_1")

    data = {
        "start_point": start_point,
        "end_point": end_point,
        "center_point": center_point,
        "id": "arc_from_dict",
        "name": "Arc from dict",
        "description": "Test arc from dictionary",
        "ifcguid": "guid_from_dict"
    }

    arc, error_logs = XmiArc3D.from_dict(data)

    assert arc.start_point == start_point
    assert arc.end_point == end_point
    assert arc.center_point == center_point
    assert arc.id == "arc_from_dict"
    assert arc.name == "Arc from dict"
    assert arc.description == "Test arc from dictionary"
    assert arc.ifcguid == "guid_from_dict"
    assert len(error_logs) == 0


def test_xmi_arc_3d_from_dict_missing_attributes():
    """Test from_dict with missing optional attributes"""
    start_point = XmiPoint3D(x=0.0, y=0.0, z=0.0)
    end_point = XmiPoint3D(x=10.0, y=0.0, z=0.0)
    center_point = XmiPoint3D(x=5.0, y=5.0, z=0.0)

    data = {
        "start_point": start_point,
        "end_point": end_point,
        "center_point": center_point
    }

    arc, error_logs = XmiArc3D.from_dict(data)

    # Should have error logs for missing attributes but still create instance
    assert arc.start_point == start_point
    assert arc.end_point == end_point
    assert arc.center_point == center_point


def test_xmi_arc_3d_with_kwargs():
    """Test creating XmiArc3D with additional kwargs"""
    start_point = XmiPoint3D(x=0.0, y=0.0, z=0.0)
    end_point = XmiPoint3D(x=10.0, y=0.0, z=0.0)
    center_point = XmiPoint3D(x=5.0, y=5.0, z=0.0)

    arc = XmiArc3D(
        start_point=start_point,
        end_point=end_point,
        center_point=center_point,
        id="arc_1",
        extra_param="should_be_ignored"
    )

    assert arc.start_point == start_point
    assert arc.end_point == end_point
    assert arc.center_point == center_point
    assert arc.id == "arc_1"


def test_xmi_arc_3d_3d_coordinates():
    """Test XmiArc3D with full 3D coordinates (not just in XY plane)"""
    start_point = XmiPoint3D(x=0.0, y=0.0, z=5.0)
    end_point = XmiPoint3D(x=10.0, y=10.0, z=15.0)
    center_point = XmiPoint3D(x=5.0, y=5.0, z=10.0)

    arc = XmiArc3D(
        start_point=start_point,
        end_point=end_point,
        center_point=center_point,
        id="arc_3d"
    )

    assert arc.start_point.z == 5.0
    assert arc.end_point.z == 15.0
    assert arc.center_point.z == 10.0


def test_xmi_arc_3d_property_getters():
    """Test that property getters work correctly"""
    start_point = XmiPoint3D(x=0.0, y=0.0, z=0.0, id="start_1", name="Start Point")
    end_point = XmiPoint3D(x=10.0, y=0.0, z=0.0, id="end_1", name="End Point")
    center_point = XmiPoint3D(x=5.0, y=5.0, z=0.0, id="center_1", name="Center Point")

    arc = XmiArc3D(
        start_point=start_point,
        end_point=end_point,
        center_point=center_point,
        id="arc_getter_test"
    )

    # Access properties multiple times
    assert arc.start_point.name == "Start Point"
    assert arc.start_point.id == "start_1"
    assert arc.end_point.name == "End Point"
    assert arc.end_point.id == "end_1"
    assert arc.center_point.name == "Center Point"
    assert arc.center_point.id == "center_1"
