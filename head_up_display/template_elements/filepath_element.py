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
    def _reduce_length(text: str, max_length: int = 20, separator: str = '...'):
        """ Reduce given text by giving max_length + separator

        :param text: text to reduce
        :param max_length: max character length to keep
        :param separator: separator characters to replace the removed part
        :return: reduced text
        """
        if len(text) <= max_length:
            # Nothing to reduce
            return text

        if max_length < len(separator) + 2:
            raise RuntimeError('Cannot reduce length of given text because max_length is too short compared to '
                               'separator length. Please increase max_length or reduce separator length. '
                               )

        start_length = int(max_length / 2 - (len(separator) / 2))
        end_length = -1 * start_length

        if len(separator) % 2 != 0 and max_length % 2 == 0:
            end_length -= 1

        return text[:start_length] + separator + text[end_length:]

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


if __name__ == '__main__':
    # filepath = FilepathElement(value=r'C:\Documents\Tests\file.mov')
    text = r'C:\Documents\Tests\file.mov'
    r = FilepathElement._reduce_length(text=text, max_length=10)
    print(r)
    print(len(r))

    # print(text[5:-5])
