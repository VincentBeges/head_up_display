from head_up_display.hud.hud_generator import HudGenerator
from head_up_display.template.hud_template import HudTemplate
from head_up_display.template_elements.text_element import TextElement
import os

EXAMPLE_FILES_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'examples'))


if __name__ == '__main__':

    ## Prepare objects

    # A text element to use in the template hud
    text_filter = TextElement(value='this is my text', text_id='foo', color='red')
    text_filter.horizontal_position = 'center'
    text_filter.vertical_position = 'center'

    # A hud object storing all hud elements
    hud_template = HudTemplate(template_elements=[text_filter])

    # The main class to apply the hud over a media
    hud_generator = HudGenerator(hud_template=hud_template)

    ## Execute hud generation
    source_file = os.path.join(EXAMPLE_FILES_DIR, r'testsrc.mp4')
    filename, ext = os.path.splitext(source_file)
    destination_file = '{filename}_result{ext}'.format(filename=filename, ext=ext)

    hud_generator.generate(source_file=source_file,
                           destination_file=destination_file,
                           text_elements_data=None,  # No data for this simple test
                           dry_run=False,
                           )

    # TODO: Add settings to the generator and regroup settings by types: ffmpeg, audio, image, movie
    # Modify settings before generating
    # settings = hud_generator.settings

