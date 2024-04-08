from pydantic import computed_field, ValidationInfo
from head_up_display.template_elements import text_element
from pydantic import field_validator, Field
from datetime import datetime


VALID_DATETIME_TYPES = ('datetime', 'date', 'time')

class DatetimeElement(text_element.BaseTextElement):
    type: str = 'datetime'  # See VALID_DATETIME_TYPES

    date_time_strftime: str = '%Y-%m-%d %H:%M:%S'
    date_strftime: str = '%Y-%m-%d'
    time_strftime: str = '%H:%M:%S'

    # Set this value if you want a full custom value
    # Emtpy value = automatic datetime process
    value: str = ''

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
        if value not in VALID_DATETIME_TYPES:
            raise TypeError(f'Given DatetimeElement has wrong type "{value}" should be any of {VALID_DATETIME_TYPES}')
        return value

    def get_filter(self):
        """ Get the text filter used in complex filter """

        if self.value:
            text = self.value
        else:
            text = self.get_date_time_as_str()

        return self._get_draw_text(text_value=text)

    def __repr__(self):
        return f'<TemplateElement:{self.type}: "{self.value}">'


if __name__ == '__main__':
    text_filter = DatetimeElement(type='datetime')
    text_filter.horizontal_position = 'right'
    print(text_filter.get_filter())
    import time
    time.sleep(2)
    print(text_filter.get_filter())

