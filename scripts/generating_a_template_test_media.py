from head_up_display.hud.hud_generator import HudGenerator
from head_up_display.template.hud_template import HudTemplate
from head_up_display.template_elements.text_element import TextElement
import os

EXAMPLE_FILES_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'examples'))
EXAMPLE_TEMPLATE_FILE = os.path.join(EXAMPLE_FILES_DIR, 'hud_template.json')

destination_file = os.path.join(EXAMPLE_FILES_DIR, 'template_test_media.mp4')

def generating_a_template_test_media():
    # Create a simple template
    template = HudTemplate(template_elements=[TextElement(vertical_position='bottom',
                                                          horizontal_position='center',
                                                          value='Foo this is my value',
                                                          font_size=0,
                                                          color='yellow'
                                                          )])

    # Test the template on a generated file
    HudGenerator.test_given_hud_template(hud_template=template,
                                         output_file=destination_file,
                                         )

def generating_a_template_test_media_from_file():
    # Load a template file
    # The template is using a dynamic text template element, so we need to give its value
    text_element_data = {'foo': 'This is the printed text'}

    # Test the file template
    HudGenerator.test_given_hud_template_from_file(hud_template_filepath=EXAMPLE_TEMPLATE_FILE,
                                                   text_elements_data=text_element_data,
                                                   output_file=destination_file,
                                                   )


if __name__ == '__main__':
    generating_a_template_test_media_from_file()
