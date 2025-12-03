import pytest
from xmi.v2.utils.xmi_errors import (
    XmiError,
    XmiInconsistentDataTypeError,
    XmiMissingReferenceInstanceError,
    XmiMissingRequiredAttributeError
)


def test_xmi_error_basic():
    """Test XmiError with just a message"""
    error = XmiError("Something went wrong")
    assert str(error) == "Something went wrong"
    assert error.error_code is None
    assert error.problem_data is None


def test_xmi_error_with_error_code():
    """Test XmiError with message and error code"""
    error = XmiError("Data validation failed", error_code="E001")
    assert "Data validation failed" in str(error)
    assert "(Error Code: E001)" in str(error)
    assert error.error_code == "E001"


def test_xmi_error_with_problem_data():
    """Test XmiError with message and problem data"""
    problem_data = {"field": "material_type", "value": "invalid"}
    error = XmiError("Invalid value", problem_data=problem_data)
    assert "Invalid value" in str(error)
    assert "(Problem Data:" in str(error)
    assert "material_type" in str(error)
    assert error.problem_data == problem_data


def test_xmi_error_with_all_params():
    """Test XmiError with all parameters"""
    problem_data = {"field": "id", "expected": "str", "got": "int"}
    error = XmiError(
        "Type mismatch",
        error_code="E002",
        problem_data=problem_data
    )

    error_str = str(error)
    assert "Type mismatch" in error_str
    assert "(Error Code: E002)" in error_str
    assert "(Problem Data:" in error_str
    assert error.error_code == "E002"
    assert error.problem_data == problem_data


def test_xmi_error_is_exception():
    """Test that XmiError is an Exception subclass"""
    assert issubclass(XmiError, Exception)

    error = XmiError("Test error")
    assert isinstance(error, Exception)


def test_xmi_error_can_be_raised():
    """Test that XmiError can be raised and caught"""
    with pytest.raises(XmiError) as exc_info:
        raise XmiError("Test error", error_code="E003")

    assert "Test error" in str(exc_info.value)
    assert exc_info.value.error_code == "E003"


def test_xmi_inconsistent_datatype_error():
    """Test XmiInconsistentDataTypeError subclass"""
    error = XmiInconsistentDataTypeError(
        "Expected float, got string",
        error_code="DT001"
    )

    assert isinstance(error, XmiError)
    assert isinstance(error, Exception)
    assert "Expected float, got string" in str(error)


def test_xmi_inconsistent_datatype_error_can_be_raised():
    """Test XmiInconsistentDataTypeError can be raised"""
    with pytest.raises(XmiInconsistentDataTypeError):
        raise XmiInconsistentDataTypeError("Data type mismatch")


def test_xmi_missing_reference_instance_error():
    """Test XmiMissingReferenceInstanceError subclass"""
    problem_data = {"reference": "material_id", "entity": "XmiStructuralMaterial"}
    error = XmiMissingReferenceInstanceError(
        "Required material reference not found",
        error_code="REF001",
        problem_data=problem_data
    )

    assert isinstance(error, XmiError)
    assert "Required material reference not found" in str(error)
    assert error.problem_data == problem_data


def test_xmi_missing_reference_instance_error_can_be_raised():
    """Test XmiMissingReferenceInstanceError can be raised"""
    with pytest.raises(XmiMissingReferenceInstanceError):
        raise XmiMissingReferenceInstanceError("Missing cross-section reference")


def test_xmi_missing_required_attribute_error():
    """Test XmiMissingRequiredAttributeError subclass"""
    problem_data = {"attribute": "material_type", "entity": "XmiStructuralMaterial"}
    error = XmiMissingRequiredAttributeError(
        "Required attribute material_type is missing",
        error_code="ATTR001",
        problem_data=problem_data
    )

    assert isinstance(error, XmiError)
    assert "Required attribute material_type is missing" in str(error)
    assert error.problem_data == problem_data


def test_xmi_missing_required_attribute_error_can_be_raised():
    """Test XmiMissingRequiredAttributeError can be raised"""
    with pytest.raises(XmiMissingRequiredAttributeError):
        raise XmiMissingRequiredAttributeError("Missing id attribute")


def test_error_hierarchy():
    """Test that all error classes inherit correctly"""
    inconsistent_error = XmiInconsistentDataTypeError("test")
    reference_error = XmiMissingReferenceInstanceError("test")
    attribute_error = XmiMissingRequiredAttributeError("test")

    # All should be instances of XmiError
    assert isinstance(inconsistent_error, XmiError)
    assert isinstance(reference_error, XmiError)
    assert isinstance(attribute_error, XmiError)

    # All should be instances of Exception
    assert isinstance(inconsistent_error, Exception)
    assert isinstance(reference_error, Exception)
    assert isinstance(attribute_error, Exception)


def test_catch_specific_error_types():
    """Test that specific error types can be caught separately"""
    # Can catch specific type
    with pytest.raises(XmiInconsistentDataTypeError):
        raise XmiInconsistentDataTypeError("type error")

    # Can catch as parent XmiError
    with pytest.raises(XmiError):
        raise XmiInconsistentDataTypeError("type error")

    # Can catch as Exception
    with pytest.raises(Exception):
        raise XmiInconsistentDataTypeError("type error")


def test_error_with_empty_problem_data():
    """Test XmiError with empty problem data dict"""
    error = XmiError("Test", problem_data={})
    error_str = str(error)
    assert "Test" in error_str
    assert "(Problem Data: {})" in error_str


def test_error_with_complex_problem_data():
    """Test XmiError with complex nested problem data"""
    problem_data = {
        "entity": "XmiCrossSection",
        "errors": [
            {"field": "material_id", "issue": "not_found"},
            {"field": "dimensions", "issue": "invalid_format"}
        ],
        "metadata": {"timestamp": "2025-12-02", "severity": "high"}
    }

    error = XmiError(
        "Multiple validation errors",
        error_code="MULTI001",
        problem_data=problem_data
    )

    error_str = str(error)
    assert "Multiple validation errors" in error_str
    assert "(Error Code: MULTI001)" in error_str
    assert "(Problem Data:" in error_str
    # Check that complex data is represented
    assert str(problem_data) in error_str


# .venv/bin/python -m pytest tests/xmi/v2/test_utils/test_xmi_errors.py
