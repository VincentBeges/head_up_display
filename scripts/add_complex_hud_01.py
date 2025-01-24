from head_up_display.hud.hud_generator import HudGenerator
from head_up_display.template.hud_template import HudTemplate
from head_up_display.template_elements.filepath_element import FilepathElement
from head_up_display.template_elements.frame_element import FrameElement
from head_up_display.template_elements.image_element import ImageElement
from head_up_display.template_elements.text_element import TextElement
from head_up_display.template_elements.timecode_element import TimecodeElement

from head_up_display.hud.generation_config import GenerationConfig
import os

EXAMPLE_FILES_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'examples'))

"""
This example is an example of a complex hud generation with multiple hud elements.
"""


if __name__ == '__main__':

    ## 1 PREPARE TEMPLATE

    text_filter_01 = TextElement(value='Project Test',
                                 color='red',
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
                                       color='white',
                                       )

    image_filter = ImageElement(image_path=os.path.join(EXAMPLE_FILES_DIR, r'testlogo.png'),
                                horizontal_position='left',
                                vertical_position='bottom',
                                )

    hud_template = HudTemplate(template_elements=[
        text_filter_01,
        text_filter_02,
        frame_element,
        filename_element,
        timecode_element,
        image_filter,
    ])

    ## 2 PREPARE GENERATION

    config = GenerationConfig()
    # Don't resize the input media
    config.do_resize = True
    # Define the black bar height
    config.black_bar_height = 50

    hud_generator = HudGenerator(hud_template=hud_template,
                                 generation_config=config,
                                 )

    ## 3 EXECUTE GENERATION

    source_file = os.path.join(EXAMPLE_FILES_DIR, r'testsrc.mp4')
    filename, ext = os.path.splitext(source_file)
    destination_file = '{filename}_result_{test_name}{ext}'.format(filename=filename,
                                                                   test_name=os.path.basename(__file__),
                                                                   ext=ext)

    text_element_data = {'username': 'User Name'}

    hud_generator.generate(source_file=source_file,
                           destination_file=destination_file,
                           text_elements_data=text_element_data,
                           dry_run=False,
                           )
