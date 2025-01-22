import pytest
from head_up_display.template_elements.image_element import ImageElement
from tempfile import NamedTemporaryFile
from pydantic import ValidationError
import os

@pytest.fixture
def image_element():
    with NamedTemporaryFile(suffix='image.png') as image_temp_file:
        return ImageElement(image_path=image_temp_file.name)

def test_image_element_initialization(image_element):
    assert image_element.type == 'image'
    assert image_element.value is None
    assert image_element.width == 0
    assert image_element.height == 0

def test_image_element_path_valid():
    with NamedTemporaryFile(suffix='image.png') as image_temp_file:
        image_element = ImageElement(image_path=image_temp_file.name)
        assert os.path.exists(image_element.image_path)

def test_validate_image_path_invalid():
    with pytest.raises(OSError):
        ImageElement(image_path='invalid/path/to/image.png')

def test_get_filter(image_element):
    assert isinstance(image_element.get_filter(), str)