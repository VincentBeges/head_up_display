from head_up_display.hud.hud_generator import HudGenerator
from head_up_display.template.hud_template import HudTemplate
from head_up_display.template_elements.text_element import TextElement
from head_up_display.hud.generation_config import GenerationConfig
import os

EXAMPLE_FILES_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'examples'))

"""
This example is creating a HUD with two static text with dynamic font_size to fit in the black bar

- We define a precise black bar height
- We don't setup the font_size argument in the TextElement (value is 0 by default)
- We setup to execution config object to allow override
- Whatever the black bar size we have, the text will fit in but keeping "vertical_margin" (in percent of the black 
bar size, above and bellow)

"""

#TODO: to correct, make it dynamic

if __name__ == '__main__':

    ## 1 PREPARE TEMPLATE

    text_filter_01 = TextElement(value='this is my text',
                                 color='yellow',
                                 horizontal_position='center',
                                 vertical_position='top',
                                 vertical_margin=30,  # keep 30% free space above and bellow the text
                                 )

    text_filter_02 = TextElement(value='another text yo',
                                 color='red',
                                 horizontal_position='left',
                                 vertical_position='bottom',
                                 vertical_margin=0,  # keep 0% free space above and bellow the text
                                 horizontal_margin=5,  # keep 5% free space on the left size
                                 )

    hud_template = HudTemplate(template_elements=[
        text_filter_01,
        text_filter_02,
    ])

    ## 2 PREPARE GENERATION

    config = GenerationConfig()
    # Don't resize input media
    config.do_resize = False

    config.black_bar_height = 30

    # Config setup for auto font_size
    config.auto_scale_hud_elements = True  # Necessary to scale any hud elements. Default value is True.
    config.override_existing_size_values = False  # False will override the text element with font_size=0 only. True
                                                  # will override all text elements

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
