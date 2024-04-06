from pydantic import BaseModel, field_validator
import abc

"""
Storing all abstract and base object used to create template elements.
"""


class ElementPosition(BaseModel):
    """ Represent an element position """
    horizontal_position: str = 'center'
    vertical_position: str = 'center'
    horizontal_margin: int = 10  # In % of the overlay width
    vertical_margin: int = 20  # In % of the overlay height

    _LEFT = 'left'
    _CENTER = "center"
    _RIGHT = 'right'
    _TOP = 'top'
    _BOTTOM = 'bottom'

    _H_POS_LIST = [_LEFT, _CENTER, _RIGHT]
    _V_POS_LIST = [_TOP, _CENTER, _BOTTOM]

    # TODO: position element using a dividing value: 3/5 -> will position element at 3/5 of the size

    @field_validator('horizontal_position', mode='before')
    def validate_horizontal_position(cls, value: str, values: dict) -> str:
        """ Conform and validate horizontal position input

        :param value: horizontal_position input
        :param values: all model values
        :return: conformed value
        """
        # Int values are pixel position. Can be positive or negative
        if isinstance(value, int):
            # TODO: should negative values return the main width/height size minus given value ?
            return str(value)

        # String values are "shortcut" automatic values. See H_POS_LIST
        elif isinstance(value, str):
            if value in cls._H_POS_LIST:
                return value
            raise ValueError(f'Given "horizontal_position" value is wrong. Should be {cls._H_POS_LIST} or an integer '
                             f'value, not "{value}"')

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
            if value in cls._V_POS_LIST:
                return value
            raise ValueError(f'Given "vertical_position" value is wrong. Should be {cls._V_POS_LIST} or an integer '
                             f'value, not "{value}"')

        raise TypeError(f'Given "vertical_position" type is wrong, should be an "int" or "str", not {type(value)}')

    def get_position_filter(self):
        """ Returns the correct position for current element to use in ffmpeg filter_complex

        x -> horizontal position
        y -> vertical position
        x=0 y=0 -> top left

        The x, and y expressions can contain the following parameters.
            main_w, W
            main_h, H
            -> The main input width and height

            overlay_w, w
            overlay_h, h
            -> The overlay input width and height.

        Check documentation about overlay position here:
        https://ffmpeg.org/ffmpeg-filters.html#overlay-1
        """
        # Getting x position (horizontal) filter part

        x = '0'

        if isinstance(self.horizontal_position, int):
            x = str(self.horizontal_position)
            # TODO: not happening because we convert int to string in the validator

        if isinstance(self.horizontal_position, str):
            if self.horizontal_position == self._LEFT:
                x = f'overlay_w*{self.horizontal_margin}/100'
            if self.horizontal_position == self._RIGHT:
                x = f'main_w-overlay_w-(overlay_w*{self.horizontal_margin}/100)'
            if self.horizontal_position == self._CENTER:
                x = 'main_w/2-(overlay_w/2)'

        # Getting y position (vertical) filter part
        # Vertical position value is the top left of the text

        y = '0'

        if isinstance(self.vertical_position, int):
            y = str(self.vertical_position)

        if isinstance(self.vertical_position, str):
            if self.vertical_position == self._TOP:
                y = f'overlay_h*{self.vertical_margin}/100'
            if self.vertical_position == self._BOTTOM:
                y = f'main_h-overlay_h-(text_h*{self.vertical_margin}/100)'
            if self.vertical_position == self._CENTER:
                y = 'main_h/2'

        # Getting the filter using x and y value
        return f'x={x}:y={y}'


class TemplateElement(ElementPosition, abc.ABC):
    """ Base of all template elements (any template element type should inherit from this class) """

    type: str = ''  # Element type (text, date, frame, etc)
    value: str = ''  # Element value. Set by user (text, etc) or automatic process (date, frame, etc)

    def __repr__(self):
        return f'<TemplateElement:{self.type}:"{self.value}">'

    @abc.abstractmethod
    def get_filter(self):
        """ In the end, an element is used to generate a FFMPEG filter.
        This method should convert current object and return a ffmpeg string filter used in a complex filter
        Example:
        >> drawtext=fontfile=/Windows/fonts/arial.ttf:text=\'Helloworld\':fontcolor=white:fontsize=24:x=(w-text_w)/2:y=8
        """
        pass


if __name__ == '__main__':
    position = ElementPosition()
    element = TemplateElement()
