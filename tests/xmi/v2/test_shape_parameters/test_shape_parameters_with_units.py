"""
Tests for shape parameters with unit support.
"""

import pytest
from xmi.v2.models.enums.xmi_unit_enum import XmiUnitEnum
from xmi.v2.models.shape_parameters import (
    CircularShapeParameters,
    RectangularShapeParameters,
    IShapeParameters,
    CircularHollowShapeParameters,
)


class TestShapeParametersWithUnits:
    """Tests for shape parameters with unit specifications."""

    def test_rectangular_params_with_default_unit(self):
        """Test rectangular parameters with no unit specified."""
        params = RectangularShapeParameters(H=500, B=300)
        assert params.unit is None  # No default unit set
        assert params.H == 500
        assert params.B == 300

    def test_rectangular_params_with_millimeter_unit(self):
        """Test rectangular parameters with millimeter unit."""
        params = RectangularShapeParameters(
            H=500, B=300, unit=XmiUnitEnum.MILLIMETER
        )
        assert params.unit == XmiUnitEnum.MILLIMETER
        assert params.H == 500
        assert params.B == 300

    def test_rectangular_params_with_meter_unit(self):
        """Test rectangular parameters with meter unit."""
        params = RectangularShapeParameters(
            H=0.5, B=0.3, unit=XmiUnitEnum.METER
        )
        assert params.unit == XmiUnitEnum.METER
        assert params.H == pytest.approx(0.5)
        assert params.B == pytest.approx(0.3)

    def test_rectangular_params_with_inch_unit(self):
        """Test rectangular parameters with inch unit."""
        params = RectangularShapeParameters(
            H=20, B=12, unit=XmiUnitEnum.INCH
        )
        assert params.unit == XmiUnitEnum.INCH
        assert params.H == 20
        assert params.B == 12

    def test_circular_params_with_unit(self):
        """Test circular parameters with unit."""
        params = CircularShapeParameters(
            D=400, unit=XmiUnitEnum.MILLIMETER
        )
        assert params.unit == XmiUnitEnum.MILLIMETER
        assert params.D == 400

    def test_circular_hollow_params_with_unit(self):
        """Test circular hollow parameters with unit."""
        params = CircularHollowShapeParameters(
            D=400, t=10, unit=XmiUnitEnum.MILLIMETER
        )
        assert params.unit == XmiUnitEnum.MILLIMETER
        assert params.D == 400
        assert params.t == 10

    def test_i_shape_params_with_unit(self):
        """Test I-shape parameters with unit."""
        params = IShapeParameters(
            D=400, B=200, T=15, t=10, r=12,
            unit=XmiUnitEnum.MILLIMETER
        )
        assert params.unit == XmiUnitEnum.MILLIMETER
        assert params.D == 400
        assert params.B == 200


class TestShapeParameterConversion:
    """Tests for converting shape parameters between units."""

    def test_convert_rectangular_mm_to_m(self):
        """Test converting rectangular parameters from mm to m."""
        params_mm = RectangularShapeParameters(
            H=500, B=300, unit=XmiUnitEnum.MILLIMETER
        )
        params_m = params_mm.convert_to(XmiUnitEnum.METER)

        assert params_m.unit == XmiUnitEnum.METER
        assert params_m.H == pytest.approx(0.5)
        assert params_m.B == pytest.approx(0.3)

        # Original should be unchanged
        assert params_mm.H == 500
        assert params_mm.B == 300

    def test_convert_circular_inch_to_mm(self):
        """Test converting circular parameters from inches to mm."""
        params_in = CircularShapeParameters(
            D=4, unit=XmiUnitEnum.INCH
        )
        params_mm = params_in.convert_to(XmiUnitEnum.MILLIMETER)

        assert params_mm.unit == XmiUnitEnum.MILLIMETER
        assert params_mm.D == pytest.approx(101.6)

    def test_convert_circular_hollow_cm_to_mm(self):
        """Test converting circular hollow parameters from cm to mm."""
        params_cm = CircularHollowShapeParameters(
            D=40, t=1, unit=XmiUnitEnum.CENTIMETER
        )
        params_mm = params_cm.convert_to(XmiUnitEnum.MILLIMETER)

        assert params_mm.unit == XmiUnitEnum.MILLIMETER
        assert params_mm.D == pytest.approx(400)
        assert params_mm.t == pytest.approx(10)

    def test_convert_same_unit_returns_copy(self):
        """Test that converting to the same unit returns a copy."""
        params1 = RectangularShapeParameters(
            H=500, B=300, unit=XmiUnitEnum.MILLIMETER
        )
        params2 = params1.convert_to(XmiUnitEnum.MILLIMETER)

        assert params2.unit == params1.unit
        assert params2.H == params1.H
        assert params2.B == params1.B
        assert params2 is not params1  # Different objects

    def test_convert_without_unit_raises_error(self):
        """Test that converting without a unit raises an error."""
        params = RectangularShapeParameters(H=500, B=300)  # No unit
        with pytest.raises(ValueError, match="Cannot convert parameters without a unit"):
            params.convert_to(XmiUnitEnum.METER)

    def test_convert_i_shape_mm_to_inch(self):
        """Test converting I-shape parameters from mm to inches."""
        params_mm = IShapeParameters(
            D=400, B=200, T=15, t=10, r=12,
            unit=XmiUnitEnum.MILLIMETER
        )
        params_in = params_mm.convert_to(XmiUnitEnum.INCH)

        assert params_in.unit == XmiUnitEnum.INCH
        assert params_in.D == pytest.approx(15.748, rel=1e-3)
        assert params_in.B == pytest.approx(7.874, rel=1e-3)
        assert params_in.T == pytest.approx(0.591, rel=1e-3)


class TestGetUnitDisplayString:
    """Tests for get_unit_display_string method."""

    def test_get_unit_display_string_millimeter(self):
        """Test getting unit display string for millimeters."""
        params = RectangularShapeParameters(
            H=500, B=300, unit=XmiUnitEnum.MILLIMETER
        )
        assert params.get_unit_display_string() == "mm"

    def test_get_unit_display_string_meter(self):
        """Test getting unit display string for meters."""
        params = RectangularShapeParameters(
            H=0.5, B=0.3, unit=XmiUnitEnum.METER
        )
        assert params.get_unit_display_string() == "m"

    def test_get_unit_display_string_inch(self):
        """Test getting unit display string for inches."""
        params = CircularShapeParameters(
            D=4, unit=XmiUnitEnum.INCH
        )
        assert params.get_unit_display_string() == "in"

    def test_get_unit_display_string_no_unit(self):
        """Test getting unit display string when no unit is set."""
        params = RectangularShapeParameters(H=500, B=300)
        assert params.get_unit_display_string() == "mm"  # Default


class TestShapeParametersFromDict:
    """Tests for creating shape parameters from dictionaries."""

    def test_rectangular_from_dict(self):
        """Test creating rectangular parameters from dictionary."""
        data = {"H": 500, "B": 300}
        params = RectangularShapeParameters.from_dict(data)

        assert params.H == 500
        assert params.B == 300
        assert params.unit is None  # No unit in dict

    def test_circular_from_dict(self):
        """Test creating circular parameters from dictionary."""
        data = {"D": 400}
        params = CircularShapeParameters.from_dict(data)

        assert params.D == 400
        assert params.unit is None

    def test_circular_hollow_from_dict(self):
        """Test creating circular hollow parameters from dictionary."""
        data = {"D": 400, "t": 10}
        params = CircularHollowShapeParameters.from_dict(data)

        assert params.D == 400
        assert params.t == 10


class TestShapeParametersToDict:
    """Tests for converting shape parameters to dictionaries."""

    def test_rectangular_to_dict(self):
        """Test converting rectangular parameters to dictionary."""
        params = RectangularShapeParameters(
            H=500, B=300, unit=XmiUnitEnum.MILLIMETER
        )
        data = params.to_dict()

        assert data == {"H": 500, "B": 300}
        # Note: unit is not included in to_dict()

    def test_circular_to_dict(self):
        """Test converting circular parameters to dictionary."""
        params = CircularShapeParameters(
            D=400, unit=XmiUnitEnum.MILLIMETER
        )
        data = params.to_dict()

        assert data == {"D": 400}

    def test_circular_hollow_to_dict(self):
        """Test converting circular hollow parameters to dictionary."""
        params = CircularHollowShapeParameters(
            D=400, t=10, unit=XmiUnitEnum.MILLIMETER
        )
        data = params.to_dict()

        assert data == {"D": 400, "t": 10}
