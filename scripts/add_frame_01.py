from head_up_display.hud.hud_generator import HudGenerator
from head_up_display.template.hud_template import HudTemplate
from head_up_display.template_elements.frame_element import FrameElement
from head_up_display.hud.generation_config import GenerationConfig
import os

EXAMPLE_FILES_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'examples'))

"""
This example is creating a HUD with two static text positioned at static position

- We define a precise black bar height
- We define the font size for the text 

"""


if __name__ == '__main__':

    ## 1 PREPARE TEMPLATE

    frame_element = FrameElement(horizontal_position='left',
                                 vertical_position='top',
                                 color='red',
                                 )

    hud_template = HudTemplate(template_elements=[
        frame_element,
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
