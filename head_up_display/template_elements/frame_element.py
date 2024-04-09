from head_up_display.template_elements import text_element
from pydantic import Field, PrivateAttr, computed_field


class FrameElement(text_element.BaseTextElement):
    """ Represent a Frame in the hud

    It will print the frame number of each frame
    """
    type: str = Field(default='frame', frozen=True)
    value: str = r'Frame\: '  # This string will be added before the frame
    start_number: int = 1
    _frame_pattern = PrivateAttr(default='%{frame_num}')

    @computed_field
    def text_value(cls) -> str:
        """ Format the text """
        return f'{cls.value}{cls._frame_pattern}'

    def get_filter(self):
        """ Get filter to generate frame number value """
        text_filter = 'drawtext='
        text_filter += f'fontfile={self.police_file}:'

        text_filter += f'text=\'{self.text_value}\':'
        # Custom element with frame_num
        text_filter += f'start_number={self.start_number}:'

        text_filter += f'fontcolor={self.color}:'
        text_filter += f'fontsize={str(self.font_size)}:'
        text_filter += f'{self.get_position_filter()}'

        return text_filter


if __name__ == '__main__':
    frame_element = FrameElement()
    print(frame_element.get_filter())
