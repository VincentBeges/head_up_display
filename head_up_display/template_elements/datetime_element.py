from pydantic import computed_field, ValidationInfo
from head_up_display.template_elements import base_element
from pydantic import field_validator
from datetime import datetime


VALID_TYPES = ('datetime', 'date', 'time')

class DatetimeElement(base_element.TemplateElement):
    type: str = 'datetime'  # See VALID_TYPES

    date_time_strftime: str = '%Y-%m-%d %H:%M:%S'
    date_strftime: str = '%Y-%m-%d'
    time_strftime: str = '%H:%M:%S'

    # Set this value if you want a full custom value
    # Emtpy value = automatic datetime process
    value: str = ''

    color: str = 'black'
    font_size: int = 20
    police_file: str = '/Windows/fonts/arial.ttf'
    # TODO: to fix after setup of ffmpeg fontconfig
    # bold: bool = False
    # underline: bool = False
    # italic: bool = False

    @computed_field
    def now(self) -> datetime:
        """ Get datetime object at each call """
        return datetime.now()

    def get_date_time_as_str(self) -> str:
        """ Format the now datetime according current type """

        if self.type == 'datetime':
            return self.now.strftime(self.date_time_strftime)
        if self.type == 'date':
            return self.now.strftime(self.date_strftime)
        if self.type == 'time':
            return self.now.strftime(self.time_strftime)

        raise RuntimeError('Failed to get date and/or time as string. Wrong type input')

    @field_validator('type')
    def validate_type(cls, value, info: ValidationInfo) -> str:
        """ Ensure we have a valid type in input """
        if value not in VALID_TYPES:
            raise TypeError(f'Given DatetimeElement has wrong type "{value}" should be any of {VALID_TYPES}')
        return value

    def get_filter(self):
        """ Get the text filter used in complex filter """

        text_filter = 'drawtext='
        text_filter += f'fontfile={self.police_file}:'

        if self.value:
            # Full custom input
            text_filter += f'text=\'{self.value}\':'
        else:
            # Using datetime
            text_filter += f'text=\'{self.get_date_time_as_str()}\':'

        text_filter += f'fontcolor={self.color}:'
        text_filter += f'fontsize={str(self.font_size)}:'
        text_filter += f'{self.get_position_filter()}'

        return text_filter

    def __repr__(self):
        return f'<TemplateElement:{self.type}: "{self.value}">'


if __name__ == '__main__':
    text_filter = DatetimeElement(type='datetime')
    text_filter.horizontal_position = 'right'
    print(text_filter.get_filter())
    import time
    time.sleep(2)
    print(text_filter.get_filter())

