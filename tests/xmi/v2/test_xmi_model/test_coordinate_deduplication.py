"""Tests for coordinate deduplication factory in XmiModel (Phase 5)."""

from xmi.v2.models.xmi_model.xmi_model import XmiModel
from xmi.v2.models.entities.xmi_structural_point_connection import XmiStructuralPointConnection
from xmi.v2.models.geometries.xmi_line_3d import XmiLine3D


def test_create_point_3d_reuses_coordinates_within_tolerance():
    model = XmiModel()
    point_a = model.create_point_3d(0.0, 0.0, 0.0, tolerance=1e-6)
    point_b = model.create_point_3d(0.0, 0.0, 5e-7, tolerance=1e-6)
    assert point_a is point_b

    point_c = model.create_point_3d(0.0, 0.0, 0.0, tolerance=1e-9)
    assert point_c is not point_a


def test_structural_point_connections_share_deduplicated_points():
    data = {
        "Entities": [
            {
                "ID": "spc-001",
                "Name": "SPC1",
                "EntityType": "XmiStructuralPointConnection",
                "Point": {"X": 10.0, "Y": 20.0, "Z": 30.0},
            },
            {
                "ID": "spc-002",
                "Name": "SPC2",
                "EntityType": "XmiStructuralPointConnection",
                "Point": {"X": 10.0, "Y": 20.0, "Z": 30.0},
            },
        ],
        "Relationships": [],
        "Histories": [],
        "Errors": [],
    }

    model = XmiModel()
    model.load_from_dict(data)

    connections = [e for e in model.entities if isinstance(e, XmiStructuralPointConnection)]
    assert len(connections) == 2
    assert connections[0].point is connections[1].point


def test_line_geometry_uses_deduplicated_points_from_model():
    data = {
        "Entities": [
            {
                "ID": "spc-003",
                "Name": "SPC3",
                "EntityType": "XmiStructuralPointConnection",
                "Point": {"X": 0.0, "Y": 0.0, "Z": 0.0},
            },
            {
                "ID": "line-001",
                "EntityType": "XmiLine3D",
                "start_point": {"X": 0.0, "Y": 0.0, "Z": 0.0},
                "end_point": {"X": 1000.0, "Y": 0.0, "Z": 0.0},
            },
        ],
        "Relationships": [],
        "Histories": [],
        "Errors": [],
    }

    model = XmiModel()
    model.load_from_dict(data)

    connection = next(e for e in model.entities if isinstance(e, XmiStructuralPointConnection))
    line = next(e for e in model.entities if isinstance(e, XmiLine3D))

    assert connection.point is line.start_point
    assert connection.point is not line.end_point
