from pydantic import computed_field
from head_up_display.template_elements import text_element
from datetime import datetime
from typing import Literal


class DatetimeElement(text_element.BaseTextElement):
    """ Represent a Datetime in the HUD
    Can be date or time or date + time
    """
    type: Literal['datetime', 'date', 'time'] = 'datetime'

    date_time_strftime: str = '%Y-%m-%d %H:%M:%S'
    date_strftime: str = '%Y-%m-%d'
    time_strftime: str = '%H:%M:%S'

    # Empty value is necessary because inherit from BaseTextElement. Value will be computed
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

    def get_filter(self):
        """ Get the text filter used in complex filter """

        return self._get_draw_text(text_value=self.get_date_time_as_str())

    def __repr__(self):
        return f'<TemplateElement:{self.type}: "{self.value}">'


if __name__ == '__main__':
    text_filter = DatetimeElement(type='datetime')
    text_filter.horizontal_position = 'right'
    print(text_filter.get_filter())
    import time
    time.sleep(2)
    print(text_filter.get_filter())

