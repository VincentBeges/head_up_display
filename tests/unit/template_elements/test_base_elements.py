import pytest
from pydantic import ValidationError
from head_up_display.template_elements.base_element import ElementPosition
from head_up_display.template_elements.base_element import TemplateElement


def test_validate_horizontal_position():
    # Test valid horizontal positions
    assert ElementPosition(horizontal_position='left').horizontal_position == 'left'
    assert ElementPosition(horizontal_position='center').horizontal_position == 'center'
    assert ElementPosition(horizontal_position='right').horizontal_position == 'right'
    assert ElementPosition(horizontal_position='100').horizontal_position == '100'
    assert ElementPosition(horizontal_position=100).horizontal_position == '100'

    # Test invalid horizontal position
    with pytest.raises(ValidationError):
        ElementPosition(horizontal_position='invalid')

def test_validate_vertical_position():
    # Test valid vertical positions
    assert ElementPosition(vertical_position='top').vertical_position == 'top'
    assert ElementPosition(vertical_position='center').vertical_position == 'center'
    assert ElementPosition(vertical_position='bottom').vertical_position == 'bottom'
    assert ElementPosition(vertical_position='100').vertical_position == '100'
    assert ElementPosition(vertical_position=100).vertical_position == '100'

    # Test invalid vertical position
    with pytest.raises(ValidationError):
        ElementPosition(vertical_position='invalid')

def test_get_position_filter():
    # Test position filter generation
    element = ElementPosition(horizontal_position='center', vertical_position='top')
    assert element.get_position_filter() == 'x=main_w/2-(overlay_w/2):y=overlay_h*20.0/100'

    element = ElementPosition(horizontal_position=50, vertical_position=100)
    assert element.get_position_filter() == 'x=50:y=100'


class ConcreteTemplateElement(TemplateElement):
    """ Concrete implementation of TemplateElement for testing purposes """
    def get_filter(self):
        return f'drawtext=text=\'{self.value}\':x={self.get_position_filter()}'

@pytest.fixture
def element():
    return ConcreteTemplateElement(type='text', value='Hello World', horizontal_position='center', vertical_position='top')

def test_template_element_initialization(element):
    # Test element initialization
    assert element.type == 'text'
    assert element.value == 'Hello World'
    assert element.horizontal_position == 'center'
    assert element.vertical_position == 'top'

def test_template_element_get_filter(element):
    # Test element filter generation
    expected_filter = 'drawtext=text=\'Hello World\':x=x=main_w/2-(overlay_w/2):y=overlay_h*20.0/100'
    assert element.get_filter() == expected_filter

def test_template_element_invalid_type():
    # Test invalid type input
    with pytest.raises(ValidationError):
        ConcreteTemplateElement(type=None, value='Hello World')

def test_template_element_invalid_value():
    # Test invalid value input
    with pytest.raises(ValidationError):
        ConcreteTemplateElement(type='text', value=None)
