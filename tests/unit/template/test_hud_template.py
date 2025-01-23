from idlelib.textview import view_text
import pytest
import json
from tempfile import NamedTemporaryFile
from head_up_display.template.hud_template import HudTemplate
from head_up_display.template_elements import base_element
from head_up_display.template_elements.text_element import TextElement
from head_up_display.template_elements.image_element import ImageElement
from unittest.mock import patch, mock_open



class NewTemplate(base_element.TemplateElement):
    # Simulate the creation of a new template element
    type: str = 'dummy_type'
    value: str = 'dummy_value'

    def get_filter(self):
        return 'dummy_filter'

@pytest.fixture
def sample_element():
    return TextElement(value="Sample Text")

@pytest.fixture
def image_element():
    with NamedTemporaryFile(suffix='image.png') as image_temp_file:
        return ImageElement(image_path=image_temp_file.name)

@pytest.fixture
def sample_elements(sample_element):
    return [sample_element]

@pytest.fixture
def hud_template(sample_elements):
    return HudTemplate(template_elements=sample_elements)

def test_hud_template_initialization(hud_template, sample_elements):
    # Test simple initialization
    assert hud_template.template_elements == sample_elements

def test_hud_template_invalid_initialization():
    # Test with invalid template element
    class InvalidTemplate(base_element.TemplateElement):
        type: str = 'dummy_type'
        value: str = 'dummy_value'
        # Don't set up the get_filter method

    with pytest.raises(TypeError):
        InvalidTemplate()

def test_template_from_json_file():
    # Test getting the template from a json file
    json_data = '[{"type": "text", "value": "Sample Text"}]'

    with patch("builtins.open", mock_open(read_data=json_data)):
        template = HudTemplate.from_template_json_file("dummy_path")
        assert len(template.template_elements) == 1
        assert template.template_elements[0].value == "Sample Text"


def test_export_template_to_json_file():
    # Test exporting the template to a json file and then reading it again
    #TODO: write this test with real writing and reading of a file
    pass

def test_add_template_element(hud_template, sample_element):
    # Test adding a new element to the template
    hud_template.add_template_element(sample_element)
    assert sample_element in hud_template.template_elements

def test_add_template_element_too_many(hud_template, sample_element):
    # Test adding too many elements to the template
    hud_template.FILTERS_INCREMENT = ['a']  # Limit to 1 filter for test
    # The hud_template already has one template element stored
    with pytest.raises(RuntimeError):
        hud_template.add_template_element(sample_element)

def test_resize_elements_from_black_bar_size(hud_template, sample_element):
    # Test resizing elements to fit in black bars
    sample_element.font_size = 0
    sample_element.vertical_margin = 10
    hud_template.template_elements = [sample_element]
    hud_template.resize_elements_from_black_bar_size(100)
    assert sample_element.font_size > 0
    assert sample_element.vertical_margin > 0

def test_get_filter_complex_content(hud_template, sample_element):
    # Test getting the filter complex content
    text = 'Another sample text'
    sample_element.value = text
    hud_template.template_elements = [sample_element]
    filter_content = hud_template.get_filter_complex_content()
    assert text in filter_content

def test_get_additional_inputs(hud_template, image_element):
    # Test collecting all input path
    hud_template.template_elements = [image_element]
    inputs = hud_template.get_additional_inputs()
    assert image_element.image_path in inputs
