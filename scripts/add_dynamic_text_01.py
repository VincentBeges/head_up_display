from head_up_display.hud.hud_generator import HudGenerator
from head_up_display.template.hud_template import HudTemplate
from head_up_display.template_elements.text_element import TextElement
from head_up_display.hud.generation_config import GenerationConfig
import os

EXAMPLE_FILES_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'examples'))

"""
This example is creating a HUD with one dynamic text positioned at static position

- Text has no value in the HUD definition
- Value is set dynamically generation using a dict

"""


if __name__ == '__main__':

    ## 1 PREPARE TEMPLATE

    text_filter_01 = TextElement(text_id='foo',
                                 color='red',
                                 horizontal_position='center',
                                 vertical_position='top',
                                 )

    hud_template = HudTemplate(template_elements=[
        text_filter_01,
    ])

    ## 2 PREPARE GENERATION

    config = GenerationConfig()
    # Don't resize the input media
    config.do_resize = False
    # Define the black bar height
    config.black_bar_height = 20

    hud_generator = HudGenerator(hud_template=hud_template,
                                 generation_config=config,
                                 )

    ## 3 EXECUTE GENERATION

    source_file = os.path.join(EXAMPLE_FILES_DIR, r'testsrc.mp4')
    filename, ext = os.path.splitext(source_file)
    destination_file = '{filename}_result_{test_name}{ext}'.format(filename=filename,
                                                                   test_name=os.path.basename(__file__),
                                                                   ext=ext)

    # Defining the dynamic value for text element
    text_elements_data = {'foo': 'This will be my text in hud'}

    hud_generator.generate(source_file=source_file,
                           destination_file=destination_file,
                           text_elements_data=text_elements_data,
                           dry_run=False,
                           )
