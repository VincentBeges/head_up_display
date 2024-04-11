from head_up_display import constants
from head_up_display.template_elements import text_element
from pydantic import field_validator, ValidationInfo
import os

VALID_FILENAME_TYPES = ('filename', 'filepath')


class FilepathElement(text_element.BaseTextElement):
    """ Represent filepath in the HUD
    Can be filepath or filename
    """
    type: str = 'filename'
    value: str = ''
    # We use the
    text_id: str = constants.OUTPUT_PATH_TEXT_ID

    # TODO: argument to reduce length of path value

    @field_validator('type')
    def validate_type(cls, value, info: ValidationInfo) -> str:
        """ Ensure we have a valid type in input """
        if value not in VALID_FILENAME_TYPES:
            raise TypeError(f'Given FilepathElement has wrong type "{value}" should be any of {VALID_FILENAME_TYPES}')
        return value

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

    def get_filter(self):
        """ Get filter to write path in HUD """

        if not self.value:
            raise RuntimeError('Failed to get the filepath filter value')

        if self.type is 'filename':
            text = os.path.basename(self.value)
        else:
            text = self.value

        return self._get_draw_text(text_value=text)
