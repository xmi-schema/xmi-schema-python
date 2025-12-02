import pytest
from xmi.v1.relationships.xmi_has_line_3d import XmiHasLine3D
from xmi.v1.geometries.xmi_line_3d import XmiLine3D
from xmi.v1.geometries.xmi_point_3d import XmiPoint3D
from xmi.v1.xmi_base import XmiBaseEntity


def test_xmi_has_line_3d_creation_valid():
    """Test creating a valid XmiHasLine3D relationship"""
    # Create source entity (use base entity for simplicity)
    start_point = XmiPoint3D(x=0.0, y=0.0, z=0.0, id="start_1")
    end_point = XmiPoint3D(x=10.0, y=0.0, z=0.0, id="end_1")

    source = XmiBaseEntity(
        id="segment_1",
        name="Segment 1"
    )

    # Create target entity (line geometry)
    target = XmiLine3D(
        start_point=start_point,
        end_point=end_point,
        id="line_1"
    )

    # Create relationship
    relationship = XmiHasLine3D(source=source, target=target)

    assert relationship.source == source
    assert relationship.target == target
    assert relationship.name == "hasLine3D"
    assert relationship.entity_type == "XmiRelHasLine3D"


def test_xmi_has_line_3d_creation_with_kwargs():
    """Test creating XmiHasLine3D with additional kwargs"""
    start_point = XmiPoint3D(x=0.0, y=0.0, z=0.0)
    end_point = XmiPoint3D(x=10.0, y=0.0, z=0.0)

    source = XmiBaseEntity(
        id="segment_1",
        name="Segment 1"
    )

    target = XmiLine3D(
        start_point=start_point,
        end_point=end_point
    )

    relationship = XmiHasLine3D(
        source=source,
        target=target,
        is_begin=True,
        is_end=False
    )

    assert relationship.source == source
    assert relationship.target == target
    assert relationship.is_begin == True
    assert relationship.is_end == False


def test_xmi_has_line_3d_is_begin_setter():
    """Test is_begin property setter"""
    start_point = XmiPoint3D(x=0.0, y=0.0, z=0.0)
    end_point = XmiPoint3D(x=10.0, y=0.0, z=0.0)

    source = XmiBaseEntity(
        id="segment_1",
        name="Segment 1"
    )

    target = XmiLine3D(
        start_point=start_point,
        end_point=end_point
    )

    relationship = XmiHasLine3D(source=source, target=target)

    # Set is_begin
    relationship.is_begin = True
    assert relationship.is_begin == True

    relationship.is_begin = False
    assert relationship.is_begin == False


def test_xmi_has_line_3d_is_end_setter():
    """Test is_end property setter"""
    start_point = XmiPoint3D(x=0.0, y=0.0, z=0.0)
    end_point = XmiPoint3D(x=10.0, y=0.0, z=0.0)

    source = XmiBaseEntity(
        id="segment_1",
        name="Segment 1"
    )

    target = XmiLine3D(
        start_point=start_point,
        end_point=end_point
    )

    relationship = XmiHasLine3D(source=source, target=target)

    # Set is_end
    relationship.is_end = True
    assert relationship.is_end == True

    relationship.is_end = False
    assert relationship.is_end == False


def test_xmi_has_line_3d_is_begin_invalid_type():
    """Test that TypeError is raised when is_begin is not bool"""
    start_point = XmiPoint3D(x=0.0, y=0.0, z=0.0)
    end_point = XmiPoint3D(x=10.0, y=0.0, z=0.0)

    source = XmiBaseEntity(
        id="segment_1",
        name="Segment 1"
    )

    target = XmiLine3D(
        start_point=start_point,
        end_point=end_point
    )

    relationship = XmiHasLine3D(source=source, target=target)

    with pytest.raises(TypeError, match="is_begin should be of type bool"):
        relationship.is_begin = "True"


def test_xmi_has_line_3d_is_end_invalid_type():
    """Test that TypeError is raised when is_end is not bool"""
    start_point = XmiPoint3D(x=0.0, y=0.0, z=0.0)
    end_point = XmiPoint3D(x=10.0, y=0.0, z=0.0)

    source = XmiBaseEntity(
        id="segment_1",
        name="Segment 1"
    )

    target = XmiLine3D(
        start_point=start_point,
        end_point=end_point
    )

    relationship = XmiHasLine3D(source=source, target=target)

    with pytest.raises(TypeError, match="is_end should be of type bool"):
        relationship.is_end = 1


def test_xmi_has_line_3d_property_getters():
    """Test that property getters work correctly"""
    start_point = XmiPoint3D(x=0.0, y=0.0, z=0.0)
    end_point = XmiPoint3D(x=10.0, y=0.0, z=0.0)

    source = XmiBaseEntity(
        id="segment_1",
        name="Segment 1"
    )

    target = XmiLine3D(
        start_point=start_point,
        end_point=end_point
    )

    relationship = XmiHasLine3D(
        source=source,
        target=target,
        is_begin=True,
        is_end=False
    )

    # Test getters
    assert relationship.is_begin == True
    assert relationship.is_end == False
    assert relationship.source.id == "segment_1"
    assert relationship.target.entity_type == "XmiLine3D"


def test_xmi_has_line_3d_name_override():
    """Test that name is always 'hasLine3D' even if passed differently"""
    start_point = XmiPoint3D(x=0.0, y=0.0, z=0.0)
    end_point = XmiPoint3D(x=10.0, y=0.0, z=0.0)

    source = XmiBaseEntity(
        id="segment_1",
        name="Segment 1"
    )

    target = XmiLine3D(
        start_point=start_point,
        end_point=end_point
    )

    # Try to pass different name
    relationship = XmiHasLine3D(source=source, target=target, name="differentName")

    # Should still be 'hasLine3D'
    assert relationship.name == "hasLine3D"


def test_xmi_has_line_3d_both_flags():
    """Test setting both is_begin and is_end flags"""
    start_point = XmiPoint3D(x=0.0, y=0.0, z=0.0)
    end_point = XmiPoint3D(x=10.0, y=0.0, z=0.0)

    source = XmiBaseEntity(
        id="segment_1",
        name="Segment 1"
    )

    target = XmiLine3D(
        start_point=start_point,
        end_point=end_point
    )

    relationship = XmiHasLine3D(
        source=source,
        target=target,
        is_begin=True,
        is_end=True
    )

    assert relationship.is_begin == True
    assert relationship.is_end == True


def test_xmi_has_line_3d_with_different_entities():
    """Test XmiHasLine3D with different types of entities"""
    from xmi.v1.xmi_base import XmiBaseEntity

    start_point = XmiPoint3D(x=0.0, y=0.0, z=0.0)
    end_point = XmiPoint3D(x=10.0, y=0.0, z=0.0)

    # Use generic base entity as source
    source = XmiBaseEntity(id="generic_1", name="Generic Source")

    target = XmiLine3D(
        start_point=start_point,
        end_point=end_point,
        id="line_1"
    )

    relationship = XmiHasLine3D(source=source, target=target)

    assert relationship.source == source
    assert relationship.target == target
    assert relationship.name == "hasLine3D"


def test_xmi_has_line_3d_unrelated_kwargs_ignored():
    """Test that unrelated kwargs are ignored"""
    start_point = XmiPoint3D(x=0.0, y=0.0, z=0.0)
    end_point = XmiPoint3D(x=10.0, y=0.0, z=0.0)

    source = XmiBaseEntity(
        id="segment_1",
        name="Segment 1"
    )

    target = XmiLine3D(
        start_point=start_point,
        end_point=end_point
    )

    # Pass extra kwargs that are not in _attributes_needed
    relationship = XmiHasLine3D(
        source=source,
        target=target,
        is_begin=True,
        extra_param="should_be_ignored",
        another_param=123
    )

    assert relationship.is_begin == True
    # Extra params should not be set as they're not in _attributes_needed
    assert not hasattr(relationship, 'extra_param')
    assert not hasattr(relationship, 'another_param')
