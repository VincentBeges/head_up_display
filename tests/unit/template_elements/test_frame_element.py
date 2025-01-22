import pytest
from head_up_display.template_elements.frame_element import FrameElement
from pydantic import ValidationError


@pytest.fixture
def frame_element():
    return FrameElement()


def test_frame_element_initialization(frame_element):
    # Check the default values
    assert frame_element.type == 'frame'
    assert frame_element.value == r'Frame\: '
    assert frame_element.start_number == 0
    assert frame_element.digits_number == 4


def test_text_value(frame_element):
    # Check we keep the same pattern for frame
    assert frame_element.text_value == 'Frame\: %{expr_int_format\\:n\\:u\\:4}'


def test_invalid_digits_number():
    # Check that negative digits number will raise
    with pytest.raises(ValidationError):
        FrameElement(digits_number=-1)
