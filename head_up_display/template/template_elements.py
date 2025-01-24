from head_up_display.template_elements import datetime_element, filepath_element, frame_element, image_element, \
    text_element, timecode_element
from dataclasses import dataclass


@dataclass
class TemplateElements:
    """ Storing all available elements """

    datetime: datetime_element.DatetimeElement = datetime_element.DatetimeElement
    date: datetime_element.DatetimeElement = datetime_element.DatetimeElement
    time: datetime_element.DatetimeElement = datetime_element.DatetimeElement

    filepath: filepath_element.FilepathElement = filepath_element.FilepathElement
    filename: filepath_element.FilepathElement = filepath_element.FilepathElement

    frame: frame_element.FrameElement = frame_element.FrameElement

    image: image_element.ImageElement = image_element.ImageElement

    text: text_element.TextElement = text_element.TextElement

    timecode: timecode_element.TimecodeElement = timecode_element.TimecodeElement

    @classmethod
    def from_json_data_list(cls, json_data_list: list):
        """ This method is used to read a template from a json file.
        It will loop over the json data list (your template, storing multiple elements) and yield the correct element
        instance for each element of the json file list.

        Example of valid json data list:
            [
            {'type': 'datetime'},
            {'type': 'filepath', 'max_length': 15},
            {'type': 'frame', 'start_number': 101, 'digits_number': 3},
            {'type': 'image', 'path': 'path/to/image.jpg'}, # The path should exist
            {'type': 'text', 'value': 'Hello World'},
            {'type': 'text', 'value': 'Another text'},
            {'type': 'timecode'},
            ]


        """

        for element_data in json_data_list:
            # Find related element object
            element = getattr(cls, element_data['type'])
            if not element:
                raise ValueError(f'The given json data list has a wrong element type: "{element_data["type"]}"')

            # Yield instance with template data
            yield element.from_dict(element_data)


if __name__ == '__main__':
    elements = list(TemplateElements.from_json_data_list(
        [
            {'type': 'datetime'},
            {'type': 'filepath', 'max_length': 15},
            {'type': 'frame', 'start_number': 101, 'digits_number': 3},
            {'type': 'image', 'path': 'path/to/image.jpg'}, # The path should exists
            {'type': 'text', 'value': 'Hello World'},
            {'type': 'timecode'}],
    ))
    print(elements)
