from head_up_display.template_elements import base_element
from pydantic import field_validator, ValidationInfo
from typing import Literal
import os


class ImageElement(base_element.TemplateElement):
    type: Literal['image'] = 'image'
    value: str = None
    image_path: str

    width: int = 0  # In pixel
    height: int = 0  # In pixel

    _image_id = 1

    @field_validator('image_path')
    def validate_image_path(cls, value: str, info: ValidationInfo) -> str:
        """ Ensure we have a valid image_path

        :param value: path to check
        :param info: storing already validated info
        :return: validated path
        """
        if not os.path.exists(value):
            raise OSError(f'Given additional image to use does not exists:\n'
                          f'{value}')
        return value

    def get_filter(self) -> str:
        """ Get the filter to use in complex_filter"""
        text_filter = f'overlay={self.get_position_filter()}'
        return text_filter
