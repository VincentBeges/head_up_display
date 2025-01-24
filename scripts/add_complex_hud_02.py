from head_up_display.hud.hud_generator import HudGenerator
from head_up_display.template.hud_template import HudTemplate
from head_up_display.template_elements.filepath_element import FilepathElement
from head_up_display.template_elements.frame_element import FrameElement
from head_up_display.template_elements.datetime_element import DatetimeElement
from head_up_display.template_elements.text_element import TextElement
from head_up_display.template_elements.timecode_element import TimecodeElement

from head_up_display.hud.generation_config import GenerationConfig
import os

from tests.unit.template_elements.test_datetime_element import datetime_element

EXAMPLE_FILES_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'examples'))

"""
This example is another example of complex utilisation

"""


if __name__ == '__main__':

    ## 1 PREPARE TEMPLATE

    text_filter_01 = TextElement(value='',
                                 color='red',
                                 text_id='movie_step',
                                 horizontal_position='center',
                                 vertical_position='top',
                                 font_size=0,  # Automatic size
                                 )

    text_filter_02 = TextElement(value='',
                                 text_id='username',
                                 color='white',
                                 horizontal_position='right',
                                 vertical_position='top',
                                 )

    frame_element = FrameElement(horizontal_position='left',
                                 vertical_position='top',
                                 color='yellow',
                                 )

    filename_element = FilepathElement(type='filename',
                                       horizontal_position='center',
                                       vertical_position='bottom',
                                       color='white',
                                       )

    timecode_element = TimecodeElement(vertical_position='bottom',
                                       horizontal_position='right',
                                       pts_format='ms',
                                       color='white',
                                       )

    datetime_element = DatetimeElement(type='date',
                                       vertical_position='bottom',
                                       horizontal_position='left',
                                       color='white',
                                       )

    hud_template = HudTemplate(template_elements=[
        text_filter_01,
        text_filter_02,
        frame_element,
        filename_element,
        timecode_element,
        datetime_element
    ])

    ## 2 PREPARE GENERATION

    config = GenerationConfig()
    # We keep the size of the media
    config.resize_width = 2048
    config.resize_height = 872

    # Don't resize the input media
    config.do_resize = True
    # Define the black bar height
    config.black_bar_height = 50

    hud_generator = HudGenerator(hud_template=hud_template,
                                 generation_config=config,
                                 )

    ## 3 EXECUTE GENERATION

    source_file = os.path.realpath(os.path.join('..', 'examples', 'Eugene_S02_sh004_2_INPUT.mov'))
    destination_file = source_file.replace('_INPUT', '_OUTPUT')

    text_element_data = {'username': 'Vincent B.',
                         'movie_step': 'Eugene - Compositing',
                         }

    hud_generator.generate(source_file=source_file,
                           destination_file=destination_file,
                           text_elements_data=text_element_data,
                           dry_run=False,
                           )
