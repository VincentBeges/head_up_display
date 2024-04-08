from pydantic import BaseModel, field_validator, ValidationInfo, PrivateAttr, Field, ConfigDict
import abc

"""
Storing all abstract and base objects used to create template elements.
"""


class ElementPosition(BaseModel):
    """ Represent an element position """
    model_config = ConfigDict(validate_assignment=True)

    _LEFT = PrivateAttr(default='left')
    _CENTER = PrivateAttr(default='center')
    _RIGHT = PrivateAttr(default='right')
    _TOP = PrivateAttr(default='top')
    _BOTTOM = PrivateAttr(default='bottom')

    _H_POS_LIST = PrivateAttr(default=[_LEFT.default, _CENTER.default, _RIGHT.default])
    _V_POS_LIST = PrivateAttr(default=[_TOP.default, _CENTER.default, _BOTTOM.default])

    # TODO: position element using a dividing value: 3/5 -> will position element at 3/5 of the size

    # All filters are not using overlay_h or overlay_w to get the size of the overlay. Text will use text_h, text_w
    # Giving the attribute access here allow to modify it dynamically
    _OVERLAY_H = PrivateAttr(default='overlay_h')
    _OVERLAY_W = PrivateAttr(default='overlay_w')

    horizontal_position: str = Field(default='center', validate_default=True)
    vertical_position: str = Field(default='center', validate_default=True)
    horizontal_margin: int = 10  # In % of the overlay width
    vertical_margin: int = 20  # In % of the overlay height

    @field_validator('horizontal_position')
    def validate_horizontal_position(cls, value: str, info: ValidationInfo) -> str:
        """ Conform and validate horizontal position input

        :param value: horizontal_position input
        :param info: accessing already validated data
        :return: conformed value
        """

        # Int values are pixel position. Can be positive or negative
        if isinstance(value, int):
            # TODO: should negative values return the main width/height size minus given value ?
            return str(value)

        # String values are "shortcut" automatic values. See _H_POS_LIST
        elif isinstance(value, str):
            if value in cls._H_POS_LIST.default:
                return value
            raise ValueError(f'Given "horizontal_position" value is wrong. Should be {cls._H_POS_LIST.default} or an '
                             f'integer value, not "{value}"')

        raise TypeError(f'Given "horizontal_position" type is wrong, should be an "int" or "str", not {type(value)}')

    @field_validator('vertical_position', mode='before')
    def validate_vertical_position(cls, value: str, values: dict) -> str:
        """ Conform and validate vertical position input

        :param value: vertical_position input
        :param values: all model values
        :return: conformed value
        """
        # Int values are pixel position. Can be positive or negative
        if isinstance(value, int):
            return str(value)

        # String values are "shortcut" automatic values. See V_POS_LIST
        elif isinstance(value, str):
            if value in cls._V_POS_LIST.default:
                return value
            raise ValueError(f'Given "vertical_position" value is wrong. Should be {cls._V_POS_LIST.default} or an '
                             f'integer value, not "{value}"')

        raise TypeError(f'Given "vertical_position" type is wrong, should be an "int" or "str", not {type(value)}')

    def get_position_filter(self):
        """ Returns the correct position for current element to use in ffmpeg filter_complex

        x -> horizontal position
        y -> vertical position
        x=0 y=0 -> top left

        The x and y expressions can contain the following parameters.
            main_w, W
            main_h, H
            -> The main input width and height

            overlay_w, w
            overlay_h, h
            -> The overlay input width and height.

        Note that x and y expressions accept different values for text
            text_w, tw
            text_h, th
            (instead of overlay_w and overlay_h)

        Check documentation about overlay position here:
        https://ffmpeg.org/ffmpeg-filters.html#overlay-1

        Check documentation about text position and syntax here:
        https://ffmpeg.org/ffmpeg-filters.html#toc-Syntax
        """
        # Getting x position (horizontal) filter part

        x = '0'

        if isinstance(self.horizontal_position, int):
            x = str(self.horizontal_position)
            # TODO: not happening because we convert int to string in the validator

        if isinstance(self.horizontal_position, str):
            if self.horizontal_position == self._LEFT:
                x = f'{self._OVERLAY_W}*{self.horizontal_margin}/100'
            if self.horizontal_position == self._RIGHT:
                x = f'main_w-{self._OVERLAY_W}-({self._OVERLAY_W}*{self.horizontal_margin}/100)'
            if self.horizontal_position == self._CENTER:
                x = f'main_w/2-({self._OVERLAY_W}/2)'

        # Getting y position (vertical) filter part
        # Vertical position value is the top left of the text

        y = '0'

        if isinstance(self.vertical_position, int):
            y = str(self.vertical_position)

        if isinstance(self.vertical_position, str):
            if self.vertical_position == self._TOP:
                y = f'{self._OVERLAY_H}*{self.vertical_margin}/100'
            if self.vertical_position == self._BOTTOM:
                y = f'main_h-{self._OVERLAY_H}-({self._OVERLAY_H}*{self.vertical_margin}/100)'
            if self.vertical_position == self._CENTER:
                y = 'main_h/2'

        # Getting the filter using x and y value
        return f'x={x}:y={y}'


class TemplateElement(ElementPosition, abc.ABC):
    """ Base of all template elements (any template element type should inherit from this class) """

    # Element type (text, date, frame, etc)
    type: str
    # Element value. Set by user (text, etc) or automatic process (date, frame, etc)
    value: str

    def __repr__(self):
        return f'<TemplateElement:{self.type}: "{self.value}">'

    @abc.abstractmethod
    def get_filter(self):
        """ In the end, an element is used to generate a FFMPEG filter.
        This method should convert current object and return a ffmpeg string filter used in a complex filter
        Example:
        >> drawtext=fontfile=/Windows/fonts/arial.ttf:text=\'Helloworld\':fontcolor=white:fontsize=24:x=(w-text_w)/2:y=8
        """
        pass


if __name__ == '__main__':
    position = ElementPosition(horizontal_position='center')
    element = TemplateElement()
