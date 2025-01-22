from head_up_display.constants import POLICE_TEXT_PATH
from head_up_display.template_elements.text_element import TextElement, BaseTextElement
import os
import pytest

@pytest.fixture
def base_text_element():
    return BaseTextElement(value='Sample Text')

@pytest.fixture
def text_element():
    return TextElement(value='Sample Text', text_id='sample_id')

def test_base_text_element_initialization(base_text_element):
    # Test the default initialization of the BaseTextElement object
    assert base_text_element.type == 'base_text'
    assert base_text_element.value == 'Sample Text'
    assert base_text_element.color == 'black'
    assert base_text_element.font_size == 0
    assert os.path.exists(base_text_element.police_file)
    assert base_text_element.bold is False
    assert base_text_element.underline is False
    assert base_text_element.italic is False

def test_text_element_initialization(text_element):
    # Test the default initialization of the TextElement object
    assert text_element.type == 'text'
    assert text_element.value == 'Sample Text'
    assert text_element.text_id == 'sample_id'

def test_validate_and_conform_value():
    # Test to validate and conform input text
    value = 'Sample:Text;'
    conformed_value = BaseTextElement.validate_and_conform_value(value, None)
    assert conformed_value == 'Sample\\:Text\\;'

def test_get_draw_text(base_text_element):
    # Test the _get_draw_text method of the BaseTextElement object
    base_text_element.color = 'white'
    base_text_element.font_size = 24
    expected_filter = (
        f"drawtext=fontfile={POLICE_TEXT_PATH}:"
        "text='Sample Text':"
        "fontcolor=white:"
        "fontsize=24:"
        "x=main_w/2-(text_w/2):y=main_h/2-(text_h/2)"
    )
    result = base_text_element._get_draw_text('Sample Text')
    assert isinstance(result, str)
    assert result == expected_filter

def test_get_filter(base_text_element):
    # Test the get_filter method of the BaseTextElement object
    base_text_element.value = 'Sample Text'
    assert isinstance(base_text_element.get_filter(), str)

def test_text_element_check_inputs():
    # Test the check_inputs method of the TextElement object
    with pytest.raises(ValueError):
        TextElement(value='', text_id='')
