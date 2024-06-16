from head_up_display import constants
from head_up_display.template_elements import text_element
from pydantic import field_validator, ValidationInfo
import os
from typing import Literal


class FilepathElement(text_element.BaseTextElement):
    """ Represent filepath in the HUD
    Can be filepath or filename
    """
    type: Literal['filename', 'filepath'] = 'filepath'
    value: str = ''
    # We use a specific text id for this one to set value with generated input filepath or filename
    text_id: str = constants.OUTPUT_PATH_TEXT_ID

    max_length: int = 0  # Used to reduce the filepath string length

    @field_validator('value')
    def validate_value_as_path(cls, value, info: ValidationInfo) -> str:
        """ Ensure we have a potential path """
        path, ext = os.path.splitext(value)
        if not ext:
            raise ValueError(f'Given value does not seems to be a path, no extension:\n'
                             f'{value}')

        #TODO: improve this validator, would like to validate we have a potential path. Part of the splitted path should
        # exist ?

        return value

    @staticmethod
    def _reduce_length(text: str, max_length: int = 10, separator: str = '...'):
        """ Reduce given text by giving max_length + separator

        :param text: text to reduce
        :param max_length: max character length to keep
        :param separator: separator characters to replace the removed part
        :return: reduced text
        """
        #TODO: max_length should include the separator inside ?
        new_text = ''
        text_length = len(text)
        split_length = max_length/2

        for i, char in enumerate(text, start=0):
            if i < split_length or i >= (text_length - split_length):
                new_text += char
            elif i == split_length:
                new_text += separator
            else:
                continue

        return new_text

    def get_filter(self):
        """ Get filter to write path in HUD """

        if not self.value:
            raise RuntimeError('Failed to get the filepath filter value')

        if self.type == 'filename':
            text = os.path.basename(self.value)
        else:
            text = self.value

        # Reduce the path if necessary
        if self.max_length > 0:
            text = self._reduce_length(text, max_length=self.max_length)

        return self._get_draw_text(text_value=text)
