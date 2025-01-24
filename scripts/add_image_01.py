from head_up_display.hud.hud_generator import HudGenerator
from head_up_display.template.hud_template import HudTemplate
from head_up_display.template_elements.image_element import ImageElement
from head_up_display.hud.generation_config import GenerationConfig
import os

EXAMPLE_FILES_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'examples'))

"""
This example is creating a HUD with two static text positioned at dynamic position

- We define a precise black bar height
- Whatever the black bar size we have, the text will fit in but keeping "vertical_margin" (in percent of the black 
bar size, above and bellow)

"""

#TODO: in positioning we have a problem of order if we add black bar

if __name__ == '__main__':

    image_filter = ImageElement(
        image_path=os.path.join(EXAMPLE_FILES_DIR, r'testlogo.png'),
        horizontal_position='center',
        vertical_position='top',
    )

    hud_template = HudTemplate(template_elements=[
        image_filter,
    ])

    config = GenerationConfig()
    config.do_resize = True
    # config.auto_scale_hud_elements = True  # Necessary to scale any hud elements
    config.black_bar_height = 30

    hud_generator = HudGenerator(hud_template=hud_template,
                                 generation_config=config,
                                 )

    ## Execute hud generation
    source_file = os.path.join(EXAMPLE_FILES_DIR, r'testsrc.mp4')
    filename, ext = os.path.splitext(source_file)
    destination_file = '{filename}_result_{test_name}{ext}'.format(filename=filename,
                                                                   test_name=os.path.basename(__file__),
                                                                   ext=ext)
    hud_generator.generate(source_file=source_file,
                           destination_file=destination_file,
                           dry_run=False,
                           )
