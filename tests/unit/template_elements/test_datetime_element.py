import pytest
from datetime import datetime
from head_up_display.template_elements.datetime_element import DatetimeElement
from pydantic import ValidationError

@pytest.fixture
def datetime_element():
    return DatetimeElement()

def test_datetime_element_initialization(datetime_element):
    # Test element initialization
    assert datetime_element.type == 'datetime'
    assert datetime_element.date_time_strftime == '%Y-%m-%d %H:%M:%S'
    assert datetime_element.date_strftime == '%Y-%m-%d'
    assert datetime_element.time_strftime == '%H:%M:%S'

def test_get_date_time_as_str(datetime_element):
    # Test get_date_time_as_str method
    datetime_element.type = 'datetime'
    assert datetime_element.get_date_time_as_str() == datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    datetime_element.type = 'date'
    assert datetime_element.get_date_time_as_str() == datetime.now().strftime('%Y-%m-%d')

    datetime_element.type = 'time'
    assert datetime_element.get_date_time_as_str() == datetime.now().strftime('%H:%M:%S')

def test_get_date_time_as_str_invalid_type(datetime_element):
    # Test get_date_time_as_str method with invalid type
    with pytest.raises(ValidationError):
        # Pydantic will invalidate this value and raise proper error
        datetime_element.type = 'invalid'

def test_invalid_type():
    # Test invalid type
    with pytest.raises(ValidationError):
        DatetimeElement(type='invalid')

def test_invalid_value():
    # Test invalid value
    with pytest.raises(ValidationError):
        DatetimeElement(value=None)