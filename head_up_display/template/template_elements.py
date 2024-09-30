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
        """ Take the json hud template data list in input and, for each element in the file, will yield the correct
        element instance """

        for element_data in json_data_list:
            # Find related element object
            element = getattr(cls, element_data['type'])
            if not element:
                raise ValueError(f'The given json data list has a wrong element type: "{element_data["type"]}"')

            # Yield instance with template data
            yield element.from_dict(element_data)


if __name__ == '__main__':
    elements = list(TemplateElements.from_json_data_list([{'type': 'datetime'}]))
    print(elements)
