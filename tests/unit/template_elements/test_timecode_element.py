import pytest
from head_up_display.template_elements.timecode_element import TimecodeElement
from pydantic import ValidationError

@pytest.fixture
def timecode_element():
    return TimecodeElement()

def test_timecode_element_initialization(timecode_element):
    assert timecode_element.type == 'timecode'
    assert timecode_element.value == ''
    assert timecode_element.pts_format == 'hms'
    assert timecode_element.timecode_format == '%{pts\\:hms}'
    assert timecode_element.timecode_rate == 24

def test_text_value(timecode_element):
    assert timecode_element.text_value == '%{pts\\:hms}'

def test_get_filter(timecode_element):
    # Simple tests for get_filter
    timecode_element.color = 'white'
    timecode_element.font_size = 24
    timecode_element.value = 'Timecode: '

    result = timecode_element.get_filter()
    assert isinstance(result, str)
    assert r'Timecode\:' in result

def test_invalid_timecode_rate():
    with pytest.raises(ValidationError):
        TimecodeElement(timecode_rate=-1)