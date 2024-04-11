from head_up_display.hud.hud_generator import HudGenerator
from head_up_display.template.hud_template import HudTemplate
from head_up_display.template_elements.text_element import TextElement
from head_up_display.template_elements.filepath_element import FilepathElement
from head_up_display.template_elements.frame_element import FrameElement
from head_up_display.template_elements.datetime_element import DatetimeElement
from head_up_display.template_elements.timecode_element import TimecodeElement
import os

EXAMPLE_FILES_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'examples'))


if __name__ == '__main__':

    ## Prepare objects

    # A fixed text element to use in the template hud
    text_filter = TextElement(value='this is my text', color='red', horizontal_position='center', vertical_position='center')

    # A dynamic text element
    text_filter_dynamic = TextElement(text_id='foo', color='white', horizontal_position='center', vertical_position='bottom')

    # A filepath element
    filename_element = FilepathElement(type='filename', horizontal_position='center', vertical_position='top')
    filepath_element = FilepathElement(type='filepath', horizontal_position='center', vertical_position='center', font_size=16)

    # A hud object storing all hud elements
    hud_template = HudTemplate(template_elements=[
        text_filter,
        text_filter_dynamic,
        filename_element,
        filepath_element,
    ])

    # Dynamic text input data
    text_elements_data = {
        'foo': 'Hello foo'
    }

    # The main class to apply the hud over a media
    hud_generator = HudGenerator(hud_template=hud_template)

    ## Execute hud generation
    source_file = os.path.join(EXAMPLE_FILES_DIR, r'testsrc.mp4')
    filename, ext = os.path.splitext(source_file)
    destination_file = '{filename}_result{ext}'.format(filename=filename, ext=ext)

    hud_generator.generate(source_file=source_file,
                           destination_file=destination_file,
                           text_elements_data=text_elements_data,
                           dry_run=False,
                           )

    # TODO: Add settings to the generator and regroup settings by types: ffmpeg, audio, image, movie
    # Modify settings before generating
    # settings = hud_generator.settings

