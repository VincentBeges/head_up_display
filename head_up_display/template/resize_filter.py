from pydantic import BaseModel, field_validator, ValidationInfo, PrivateAttr, Field, ConfigDict, ValidationError
from head_up_display.hud.generation_config import GenerationConfig
from typing import Union
import re

SEARCH_PERCENT = re.compile(r'^([\d+\.\,]+)\s?%$')


class ResizeAndPadFilter(BaseModel):
    """ A complex_filter element used to resize a media and or add black bar on it (pad)

    You can do_resize + add black bar
    You can do_resize only by setting black_bar_height value to 0
    You can add black bar only by setting width and height values to 0
    """
    model_config = ConfigDict(validate_assignment=True)

    width: int = 1920
    height: int = 1080
    force_original_aspect_ratio: str = 'decrease'  # see https://ffmpeg.org/ffmpeg-filters.html#Options-2

    black_bar_height: Union[str, int] = 20  # accept pixel value (int) or percent of the height (str like 2.6%)
    display_aspect_ratio: float = 1.0

    @field_validator('black_bar_height')
    def conform_black_bar_height(cls, value: Union[int, str], info: ValidationInfo) -> str:
        """ We accept pixel value or percent size of the height

        :param value: the black bar value
        :param info: access validation info
        :return: the conformed black bar height
        """
        if isinstance(value, str):
            matched_percent = SEARCH_PERCENT.match(value)
            if matched_percent:
                return f'{info.data['height']}*{str(float(matched_percent.group(1)))}/100'
            if value.isdigit():
                return value
            raise ValueError(f'black_bar_height value should be a digit (pixel size) or a percent value (ex: 2.6%),'
                             f' not: {value}')
        else:
            return str(value)

    @field_validator('width')
    def conform_width(cls, value: int, info: ValidationInfo) -> str:
        """ Conform width or use in_w -> input width

        :param value: new width size
        :param info: access validation info
        :return: the conformed width
        """
        # We accept negative values if we don't want to do_resize the media, then we use the constant
        # see https://ffmpeg.org/ffmpeg-filters.html#Options-2
        if value <= 0:
            return 'in_w'
        return str(value)

    @field_validator('height')
    def conform_height(cls, value: int, info: ValidationInfo) -> str:
        """ Conform height or use in_h -> input height

        :param value: new height size
        :param info: access validation info
        :return: the conformed height
        """
        # We accept negative values if we don't want to do_resize the media, then we use the constant
        # see https://ffmpeg.org/ffmpeg-filters.html#Options-2
        if value <= 0:
            return 'in_h'
        return str(value)

    def get_filter(self) -> str:
        """ Get the filter used to scale and add black bar (pad) """

        text_filter = f'scale={self.width}:{self.height}:force_original_aspect_ratio={self.force_original_aspect_ratio},'

        if self.black_bar_height:
            text_filter += f'pad={self.width}:{self.height}+({self.black_bar_height}*2):(ow-iw)/2:(oh-ih)/2,'
        text_filter += f'setsar={self.display_aspect_ratio}'

        return text_filter

    @classmethod
    def from_generation_config(cls, generation_config: GenerationConfig) -> Union['ResizeAndPadFilter', None]:
        """ Init current filter size from a generation config.
        Note that it can return None if the configuration does not require to resize or add black bar.

        :param generation_config: the GenerationConfig object used to process source media before adding hud
        :return: Current class or None
        """
        if not generation_config.do_resize and not generation_config.add_black_bar:
            # In case we don't want to do_resize or don't want to add black bar there is no sense to use an instance of
            # this class
            return None

        resize_and_pad_filter = cls()

        # Handle resizing

        if not generation_config.do_resize:
            resize_and_pad_filter.width = 0
            resize_and_pad_filter.height = 0
        else:
            resize_and_pad_filter.width = generation_config.resize_width
            resize_and_pad_filter.height = generation_config.resize_height

        # Handle black bar (pad)

        if not generation_config.add_black_bar:
            resize_and_pad_filter.black_bar_height = 0
        else:
            # Accept pixel value as int or percent value as string (ex: 1,3%)
            resize_and_pad_filter.black_bar_height = generation_config.black_bar_height

        return resize_and_pad_filter


if __name__ == '__main__':
    resize_filter = ResizeAndPadFilter(width=0, height=0)
    print(resize_filter.get_filter())
