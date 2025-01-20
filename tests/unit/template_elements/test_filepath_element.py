import os
import pytest
from pydantic import ValidationError
from head_up_display.template_elements.filepath_element import FilepathElement
from head_up_display import constants

#TODO: test with linux and windows path

@pytest.fixture
def filepath():
    return r'C:\Documents\Tests\file.mov'

@pytest.fixture
def filepath_element():
    return FilepathElement()

def test_filepath_element_initialization(filepath_element, filepath):
    # Check default values
    assert filepath_element.type == 'filepath'
    assert filepath_element.value == ''
    assert filepath_element.text_id == constants.OUTPUT_PATH_TEXT_ID
    assert filepath_element.max_length == 0

def test_validate_value_as_path():
    # Test we have a valid filepath
    valid_path = r'C\\:\\file.txt'  # The path is used in a command line that's why we need to escape :
    invalid_path = r'C:\file'

    assert FilepathElement(value=valid_path).value == valid_path

    with pytest.raises(ValidationError):
        # Not a file but a directory
        FilepathElement(value=invalid_path)

def test_reduce_length(filepath):
    # Test reduce length
    reduced_text = FilepathElement._reduce_length(filepath, max_length=20)
    assert reduced_text == 'C:\\Docum...\\file.mov'
    assert len(reduced_text) == 20

def test_get_filter_no_value():
    # Test get_filter without value
    with pytest.raises(RuntimeError):
        fe = FilepathElement()
        fe.get_filter()