from head_up_display.template_elements import base_element
from pydantic import Field, model_validator


class BaseTextElement(base_element.TemplateElement):
    """ Base object for all sub object printing text in the end """

    type: str = Field(default='base_text', frozen=True)
    value: str
    #TODO: add a validator to ensure we espace all special characters

    color: str = 'black'
    font_size: int = 20
    #TODO: https://stackoverflow.com/questions/43254634/ffmpeg-drawtext-style-bold-italics-underline
    # reinstall ffmpeg with the fontconfig to change police_file and be able to use bold, underline and italic
    police_file: str = '/Windows/fonts/arial.ttf'
    bold: bool = False
    underline: bool = False
    italic: bool = False

    # Replaced "overlay_h" by "text_h" and "overlay_w" by "text_w" used in positioning expressions (drawtext)
    # Won't work for text if we use default overlay_{} value
    _OVERLAY_H = 'text_h'
    _OVERLAY_W = 'text_w'

    def _get_draw_text(self, text_value):
        """ Get the draw text to write text with complex_filter """
        text_filter = 'drawtext='
        text_filter += f'fontfile={self.police_file}:'
        text_filter += f'text=\'{text_value}\':'
        text_filter += f'fontcolor={self.color}:'
        text_filter += f'fontsize={str(self.font_size)}:'
        text_filter += f'{self.get_position_filter()}'

        return text_filter

    def get_filter(self):
        """ Get current element complex_filter part """
        return self._get_draw_text(text_value=self.value)


class TextElement(BaseTextElement):
    """ Represent a text in a template

    ..note::
        The "text_id" is used to fill TextElement value with dynamic data at hud generation.

        Example using a fixed string input
        >>> text_element = TextElement(value='MyUsername')
        -> will always show 'Myusername' in the hud

        Example using a text_id to fill data dynamically
        >>> text_element = TextElement(text_id='username')
        -> See HudTemplate.get_filter_complex_content() you can see we give a dict with {text_id: new_value} used to
        fill the text_element dynamically

        "text_id" is optional if you just want to have a fixed string value
    """

    type: str = Field(default='text', frozen=True)
    text_id: str = ''  # Optional. See docstring.
    value: str = ''

    @model_validator(mode='after')
    def check_inputs(self) -> 'TextElement':
        """ Ensure we have a "value" or a "text_id" """

        if not self.text_id and not self.value:
            raise ValueError('You need to give a "value" or a "text_id" at TextElement creation')
        return self

    def __repr__(self):
        return f'<TemplateElement:{self.type}: "{self.text_id}"="{self.value}">'


if __name__ == '__main__':
    text_filter = TextElement(value='this is my text', text_id='foo')
    text_filter.horizontal_position = 'right'
    print(text_filter.get_filter())
    print(text_filter.__repr__())

