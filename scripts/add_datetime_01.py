from head_up_display.hud.hud_generator import HudGenerator
from head_up_display.template.hud_template import HudTemplate
from head_up_display.template_elements.datetime_element import DatetimeElement
from head_up_display.hud.generation_config import GenerationConfig
import os

EXAMPLE_FILES_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'examples'))

"""
This example is creating a HUD with datetime data

- We can have the full datetime, the date only or the time only  

"""


if __name__ == '__main__':

    ## 1 PREPARE TEMPLATE

    datetime_element = DatetimeElement(type='datetime',
                                       vertical_position='top',
                                       horizontal_position='center',
                                       color='yellow',
                                       )

    date_element = DatetimeElement(type='date',
                                   vertical_position='center',
                                   horizontal_position='center',
                                   )

    time_element = DatetimeElement(type='time',
                                   vertical_position='bottom',
                                   horizontal_position='center',
                                   color='red'
                                   )

    hud_template = HudTemplate(template_elements=[
        datetime_element,
        date_element,
        time_element,
    ])

    ## 2 PREPARE GENERATION

    config = GenerationConfig()
    # Don't resize the input media
    config.do_resize = False
    # Define the black bar height
    config.black_bar_height = 30
    config.auto_scale_hud_elements = False,

    hud_generator = HudGenerator(hud_template=hud_template,
                                 generation_config=config,
                                 )

    ## 3 EXECUTE GENERATION

    source_file = os.path.join(EXAMPLE_FILES_DIR, r'testsrc.mp4')
    filename, ext = os.path.splitext(source_file)
    destination_file = '{filename}_result_{test_name}{ext}'.format(filename=filename,
                                                                   test_name=os.path.basename(__file__),
                                                                   ext=ext)
    hud_generator.generate(source_file=source_file,
                           destination_file=destination_file,
                           dry_run=False,
                           )
