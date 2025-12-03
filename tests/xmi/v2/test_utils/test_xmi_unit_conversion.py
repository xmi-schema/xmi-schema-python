"""
Tests for XMI unit conversion utilities.
"""

import pytest
from xmi.v2.models.enums.xmi_unit_enum import XmiUnitEnum
from xmi.v2.utils.xmi_unit_conversion import (
    convert_value,
    convert_dict,
    get_conversion_factor,
    get_common_length_units,
    get_recommended_unit_for_value,
)


class TestConvertValue:
    """Tests for convert_value function."""

    def test_convert_millimeter_to_meter(self):
        """Test converting millimeters to meters."""
        result = convert_value(1000.0, XmiUnitEnum.MILLIMETER, XmiUnitEnum.METER)
        assert result == pytest.approx(1.0)

    def test_convert_meter_to_millimeter(self):
        """Test converting meters to millimeters."""
        result = convert_value(1.0, XmiUnitEnum.METER, XmiUnitEnum.MILLIMETER)
        assert result == pytest.approx(1000.0)

    def test_convert_inch_to_millimeter(self):
        """Test converting inches to millimeters."""
        result = convert_value(1.0, XmiUnitEnum.INCH, XmiUnitEnum.MILLIMETER)
        assert result == pytest.approx(25.4)

    def test_convert_inch_to_foot(self):
        """Test converting inches to feet."""
        result = convert_value(12.0, XmiUnitEnum.INCH, XmiUnitEnum.FOOT)
        assert result == pytest.approx(1.0)

    def test_convert_millimeter2_to_centimeter2(self):
        """Test converting mm² to cm²."""
        result = convert_value(100.0, XmiUnitEnum.MILLIMETER2, XmiUnitEnum.CENTIMETER2)
        assert result == pytest.approx(1.0)

    def test_convert_inch2_to_millimeter2(self):
        """Test converting in² to mm²."""
        result = convert_value(1.0, XmiUnitEnum.INCH2, XmiUnitEnum.MILLIMETER2)
        assert result == pytest.approx(645.16, rel=1e-2)

    def test_convert_same_unit_returns_same_value(self):
        """Test that converting to the same unit returns the same value."""
        result = convert_value(42.0, XmiUnitEnum.MILLIMETER, XmiUnitEnum.MILLIMETER)
        assert result == 42.0

    def test_convert_incompatible_units_raises_error(self):
        """Test that converting between incompatible units raises an error."""
        with pytest.raises(ValueError, match="Cannot convert between different unit types"):
            convert_value(1.0, XmiUnitEnum.MILLIMETER, XmiUnitEnum.MILLIMETER2)


class TestConvertDict:
    """Tests for convert_dict function."""

    def test_convert_dict_millimeter_to_meter(self):
        """Test converting a dictionary from mm to m."""
        params = {"H": 500.0, "B": 300.0, "T": 10.0}
        result = convert_dict(params, XmiUnitEnum.MILLIMETER, XmiUnitEnum.METER)

        assert result["H"] == pytest.approx(0.5)
        assert result["B"] == pytest.approx(0.3)
        assert result["T"] == pytest.approx(0.01)

    def test_convert_dict_inch_to_millimeter(self):
        """Test converting a dictionary from inches to mm."""
        params = {"D": 4.0, "T": 0.5}
        result = convert_dict(params, XmiUnitEnum.INCH, XmiUnitEnum.MILLIMETER)

        assert result["D"] == pytest.approx(101.6)
        assert result["T"] == pytest.approx(12.7)

    def test_convert_dict_empty(self):
        """Test converting an empty dictionary."""
        result = convert_dict({}, XmiUnitEnum.MILLIMETER, XmiUnitEnum.METER)
        assert result == {}


class TestGetConversionFactor:
    """Tests for get_conversion_factor function."""

    def test_get_conversion_factor_mm_to_m(self):
        """Test getting conversion factor from mm to m."""
        factor = get_conversion_factor(XmiUnitEnum.MILLIMETER, XmiUnitEnum.METER)
        assert factor == pytest.approx(0.001)

    def test_get_conversion_factor_inch_to_mm(self):
        """Test getting conversion factor from inches to mm."""
        factor = get_conversion_factor(XmiUnitEnum.INCH, XmiUnitEnum.MILLIMETER)
        assert factor == pytest.approx(25.4)

    def test_get_conversion_factor_same_unit(self):
        """Test that same unit has conversion factor of 1.0."""
        factor = get_conversion_factor(XmiUnitEnum.METER, XmiUnitEnum.METER)
        assert factor == 1.0

    def test_get_conversion_factor_incompatible_units(self):
        """Test that incompatible units raise an error."""
        with pytest.raises(ValueError, match="Cannot get conversion factor"):
            get_conversion_factor(XmiUnitEnum.MILLIMETER, XmiUnitEnum.MILLIMETER2)


class TestGetCommonLengthUnits:
    """Tests for get_common_length_units function."""

    def test_get_common_length_units_metric(self):
        """Test getting common metric length units."""
        units = get_common_length_units(metric=True)
        assert XmiUnitEnum.MILLIMETER in units
        assert XmiUnitEnum.CENTIMETER in units
        assert XmiUnitEnum.METER in units

    def test_get_common_length_units_imperial(self):
        """Test getting common imperial length units."""
        units = get_common_length_units(metric=False)
        assert XmiUnitEnum.INCH in units
        assert XmiUnitEnum.FOOT in units
        assert XmiUnitEnum.YARD in units


class TestGetRecommendedUnitForValue:
    """Tests for get_recommended_unit_for_value function."""

    def test_recommend_mm_for_small_meter_values(self):
        """Test that small meter values are recommended as mm."""
        # 0.5 mm displayed as meters would be 0.0005 m (too small)
        recommended = get_recommended_unit_for_value(0.0005, XmiUnitEnum.METER, metric=True)
        assert recommended == XmiUnitEnum.MILLIMETER

    def test_recommend_cm_for_large_mm_values(self):
        """Test that large mm values are recommended as cm or m."""
        # 5000 mm = 500 cm = 5 m (algorithm chooses cm as it's in good range)
        recommended = get_recommended_unit_for_value(5000, XmiUnitEnum.MILLIMETER, metric=True)
        assert recommended in (XmiUnitEnum.CENTIMETER, XmiUnitEnum.METER)

    def test_recommend_keeps_good_range(self):
        """Test that values in good range keep their unit."""
        # 500 mm is in a good display range
        recommended = get_recommended_unit_for_value(500, XmiUnitEnum.MILLIMETER, metric=True)
        assert recommended == XmiUnitEnum.MILLIMETER


class TestUnitEnumHelpers:
    """Tests for XmiUnitEnum helper methods."""

    def test_get_base_unit_type_length(self):
        """Test getting base unit type for length units."""
        assert XmiUnitEnum.get_base_unit_type(XmiUnitEnum.MILLIMETER) == "length"
        assert XmiUnitEnum.get_base_unit_type(XmiUnitEnum.METER) == "length"
        assert XmiUnitEnum.get_base_unit_type(XmiUnitEnum.INCH) == "length"
        assert XmiUnitEnum.get_base_unit_type(XmiUnitEnum.FOOT) == "length"

    def test_get_base_unit_type_area(self):
        """Test getting base unit type for area units."""
        assert XmiUnitEnum.get_base_unit_type(XmiUnitEnum.MILLIMETER2) == "area"
        assert XmiUnitEnum.get_base_unit_type(XmiUnitEnum.METER2) == "area"
        assert XmiUnitEnum.get_base_unit_type(XmiUnitEnum.INCH2) == "area"

    def test_get_base_unit_type_volume(self):
        """Test getting base unit type for volume units."""
        assert XmiUnitEnum.get_base_unit_type(XmiUnitEnum.MILLIMETER3) == "volume"
        assert XmiUnitEnum.get_base_unit_type(XmiUnitEnum.METER3) == "volume"

    def test_get_base_unit_type_inertia(self):
        """Test getting base unit type for inertia units."""
        assert XmiUnitEnum.get_base_unit_type(XmiUnitEnum.MILLIMETER4) == "inertia"
        assert XmiUnitEnum.get_base_unit_type(XmiUnitEnum.METER4) == "inertia"
        assert XmiUnitEnum.get_base_unit_type(XmiUnitEnum.INCH4) == "inertia"

    def test_get_base_unit_type_time(self):
        """Test getting base unit type for time units."""
        assert XmiUnitEnum.get_base_unit_type(XmiUnitEnum.SECOND) == "time"

    def test_is_metric_true_for_si_units(self):
        """Test that SI units are identified as metric."""
        assert XmiUnitEnum.is_metric(XmiUnitEnum.MILLIMETER) is True
        assert XmiUnitEnum.is_metric(XmiUnitEnum.METER) is True
        assert XmiUnitEnum.is_metric(XmiUnitEnum.CENTIMETER) is True
        assert XmiUnitEnum.is_metric(XmiUnitEnum.MILLIMETER2) is True

    def test_is_metric_false_for_imperial_units(self):
        """Test that imperial units are identified as not metric."""
        assert XmiUnitEnum.is_metric(XmiUnitEnum.INCH) is False
        assert XmiUnitEnum.is_metric(XmiUnitEnum.FOOT) is False
        assert XmiUnitEnum.is_metric(XmiUnitEnum.INCH2) is False
