from head_up_display.template.template_elements import TemplateElements
from head_up_display.template_elements.datetime_element import DatetimeElement
from head_up_display.template_elements.filepath_element import FilepathElement
from head_up_display.template_elements.frame_element import FrameElement
from head_up_display.template_elements.image_element import ImageElement
from head_up_display.template_elements.text_element import TextElement
from head_up_display.template_elements.timecode_element import TimecodeElement
from tempfile import NamedTemporaryFile
import pytest

def test_template_elements_initialization():
    # Test we have all elements in the class initialization
    elements = TemplateElements()
    assert elements.datetime == DatetimeElement
    assert elements.date == DatetimeElement
    assert elements.time == DatetimeElement
    assert elements.filepath == FilepathElement
    assert elements.filename == FilepathElement
    assert elements.frame == FrameElement
    assert elements.image == ImageElement
    assert elements.text == TextElement
    assert elements.timecode == TimecodeElement

def test_from_json_data_list():
    # Test loading a template stored as json file into objects
    with NamedTemporaryFile(suffix='image.png') as image_temp_file:
        json_data_list = \
            [
                {'type': 'datetime'},
                {'type': 'filepath', 'max_length': 15},
                {'type': 'frame', 'start_number': 101, 'digits_number': 3},
                {'type': 'image', 'image_path': image_temp_file.name},
                {'type': 'text', 'value': 'Hello World'},
                {'type': 'timecode'},
            ]
        elements = list(TemplateElements.from_json_data_list(json_data_list))
        assert len(elements) == 6
        assert isinstance(elements[0], DatetimeElement)
        assert isinstance(elements[1], FilepathElement)
        assert isinstance(elements[2], FrameElement)
        assert isinstance(elements[3], ImageElement)
        assert isinstance(elements[4], TextElement)
        assert isinstance(elements[5], TimecodeElement)

def test_from_json_data_list_invalid_type():
    # Test loading a wrong template element
    json_data_list = [{'type': 'invalid_type'}]
    with pytest.raises(AttributeError):
        list(TemplateElements.from_json_data_list(json_data_list))

    json_data_list = [{'type': 'image', 'image_path': 'not_existing/path/to/image.png'}]
    with pytest.raises(OSError):
        list(TemplateElements.from_json_data_list(json_data_list))