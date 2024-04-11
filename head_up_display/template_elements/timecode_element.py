from head_up_display.template_elements import text_element
from pydantic import Field, computed_field


class TimecodeElement(text_element.BaseTextElement):
    """ Represent a Timecode in the hud

    https://ffmpeg.org/ffmpeg-filters.html#toc-Syntax
    """
    type: str = Field(default='timecode', frozen=True)
    value: str = r''  # This string will be added before the timecode

    # Custom time format, see https://ffmpeg.org/ffmpeg-filters.html#Text-expansion
    pts_format: str = 'hms'
    timecode_format: str = f'%{{pts\:{pts_format}}}'
    timecode_rate: int = Field(default=24, gt=0)

    @computed_field
    def text_value(cls) -> str:
        """ Format the text """
        return f'{cls.value}{cls.timecode_format}'

    def get_filter(self):
        """ Get filter to generate frame number value """
        text_filter = 'drawtext='
        text_filter += f'fontfile={self.police_file}:'

        if self.value:
            # Used to add text before the timecode
            text_filter += f'text=\'{self.value}\':'

        # Custom element with timecode
        text_filter += f'text=\'{self.timecode_format}\':'
        text_filter += f'rate={self.timecode_rate}:'

        text_filter += f'fontcolor={self.color}:'
        text_filter += f'fontsize={str(self.font_size)}:'
        text_filter += f'{self.get_position_filter()}'

        return text_filter


if __name__ == '__main__':
    timecode_element = TimecodeElement()
    print(timecode_element.get_filter())
