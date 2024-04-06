from head_up_display.template_elements import base_element
from pydantic import field_validator


class TextElement(base_element.TemplateElement):
    """ Represent a text in a template

    ..note::
        The "text_id" is used to separate each text element of a template and be able to fill them with dynamic data
        at hud generation.
        Example a "username" text element would have different value according user.
    """

    type: str = 'text'
    text_id: str = ''  # Optional if you don't want dynamic data for this element but only a simple fixed text

    value: str = ''
    color: str = 'black'
    font_size: str = 20

    #TODO: https://stackoverflow.com/questions/43254634/ffmpeg-drawtext-style-bold-italics-underline
    # reinstall ffmpeg with the fontconfig to change police_file and be able to use bold, underline and italic
    police_file: str = '/Windows/fonts/arial.ttf'
    # bold: bool = False
    # underline: bool = False
    # italic: bool = False

    @field_validator('text_id', mode='before')
    def validate_id(cls, value: str, values: dict) -> str:
        """ Ensure we have an id

        :param value: given id value
        :param values: all other Element values
        :return: given value if correct
        """
        if not value:
            raise ValueError('You need to give an ID to this element')
        return value

    def get_filter(self):
        """ Get the text filter used in complex filter """
        text_filter = 'drawtext='
        text_filter += f'fontfile={self.police_file}:'
        text_filter += f'text=\'{self.value}\':'
        text_filter += f'fontcolor={self.color}:'
        text_filter += f'fontsize={self.font_size}:'
        text_filter += f'{self.get_position_filter()}'

        return text_filter

    def __repr__(self):
        return f'<TemplateElement:{self.type}: {self.text_id}="{self.value}">'


if __name__ == '__main__':
    text_filter = TextElement(value='this is my text', text_id='foo')
    text_filter.horizontal_position = 'right'
    print(text_filter.get_filter())
    print(text_filter.__repr__())

