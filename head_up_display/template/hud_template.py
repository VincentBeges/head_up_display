from head_up_display.template_elements import base_element
from head_up_display.template.template_elements import TemplateElements
import string
import json
import logging

logger = logging.getLogger(__name__)


class HudTemplate(object):
    """ Represent a template used to generate head up display over a media.

    Can instantiate it dynamically:
        - from a given dict of template elements
        - from a list of template elements
    or statically:
        - from a json file
    """

    FILTER_COMPLEX = '-filter_complex "{filters}"'
    FILTERS_INCREMENT = list(string.ascii_lowercase)
    #TODO: remove limits to the number of filters in the complex filter

    def __init__(self, template_elements: list[base_element.TemplateElement]):
        """ Init a HudTemplate instance used by HudGenerator to create a head up display over a media.

        :param template_elements: List of template elements
        """
        self.template_elements = template_elements

        #TODO: additional inputs property
        #TODO: complex filter parts property

    @classmethod
    def from_template_json_file(cls, json_file: str) -> 'HudTemplate':
        """ Get HudTemplate from a json file

        :param json_file: json file with template data inside (a list of dict. Each dict is a template element)
        :return: class instance
        """
        with open(json_file, 'r') as stream:
            template_list = json.load(stream)

        template_elements = list(TemplateElements.from_json_data_list(json_data_list=template_list))

        return cls(template_elements=template_elements)

    def export_template_to_json_file(self, json_file: str) -> None:
        """ Export current template as a json file

        :param json_file: json filepath to export
        """
        json_template_list = []

        for template_element in self.template_elements:
            json_template_list.append(template_element.dict())

        with open(json_file, 'w+', encoding='utf-8') as stream:
            json.dump(json_template_list, stream, ensure_ascii=False, indent=4)

        logger.info(f'Dumped template data into:\n'
                    f'{json_file}')

    def add_template_element(self, element: base_element.TemplateElement):
        """ Add given element in the template

        :param element: Template element (inherit from TemplateElement)
        """
        if len(self.template_elements) == len(self.FILTERS_INCREMENT):
            raise RuntimeError(f'Trying to add too much filters > {len(self.template_elements)}.'
                               f'See "HudTemplate.FILTERS_INCREMENT" list')

        self.template_elements.append(element)

    def resize_elements_from_black_bar_size(self,
                                            black_bar_height: int,
                                            override_existing_values: bool = True,
                                            ):
        """ Update the font_size of any text element (text, datetime, frame, ...) to fit in the black bars.
        Result will be:   black bar height size - margin in percent

        :param black_bar_height: The black bar height used in resize calcul
        :param override_existing_values: True to override any font_size existing value. False if you want to resize
            font_size only if existing value is 0
        """
        # 1 point = 1.07 pixel
        # Note that this value is coming from tests to have the text fitting in the black bar
        pixel_point_ratio = 1.07

        for element in self.template_elements:

            # Resize text elements (text, datetime, etc)
            size = getattr(element, 'font_size', None)
            if size is None:
                # Not a text element to auto resize
                continue

            if not override_existing_values and size > 0:
                continue

            margin = element.vertical_margin

            # Update the font size based on black bar height and margin
            new_size_value_px = black_bar_height - (black_bar_height * (2 * margin) / 100)
            new_size_value_pt = new_size_value_px * pixel_point_ratio

            setattr(element, 'font_size', new_size_value_pt)

            # Update the vertical margin (will be based on the text size but text has been resized so margin
            # should be)
            resize_ratio = black_bar_height / new_size_value_px
            new_vertical_margin = margin * resize_ratio

            setattr(element, 'vertical_margin', new_vertical_margin)

    def get_filter_complex_content(self, text_elements_data: dict = None) -> str:
        """ Get the filter complex string to use in ffmpeg content.
        This will not include -filter_complex "..." only what's inside "..."

        ..note::
            Note about the source and destination groups.
            In FFMPEG filter_complex, you have multiple following filters to execute. For each filter (except first and
            last one) you have to define the name of the source input group used and the name of the destination output
            group.

            We use simple alphabetical letters to do it:
            -filter_complex "first filter [a];[a] second filter [b];[b] third and last filter"
            May be not the best but it makes complex filter simple to read

        :param text_elements_data: a dict used to fill template text elements values according "text_id" attributes
        :return: FFMPEG filter_complex string content (to use in FFMPEG -filter_complex "..." command)
        """
        # Create the filter_complex used to add the hud in overlay using ffmpeg command

        text_elements_data = text_elements_data or {}

        filters = []

        i = -1
        max_i = len(self.template_elements)
        # Add each hud element into the command list
        for filter_element in self.template_elements:

            # For text elements using dynamic values input
            if hasattr(filter_element, 'text_id') and text_elements_data.get(filter_element.text_id):
                filter_element.value = text_elements_data[filter_element.text_id].replace('\'', '\\\'')
            else:
                logger.warning(f'Failed to find related value for hud dynamic text element: \n'
                               f'{filter_element}')

            # First element of filter has no source group value like "[a]"
            if i == -1:
                group_prefix = ''
            else:
                group_prefix = f'[{self.FILTERS_INCREMENT[i]}]'

            # Last element of filter has no destination group value like "[b]"
            if i+2 == max_i:
                group_suffix = ''
            else:
                group_suffix = f'[{self.FILTERS_INCREMENT[i + 1]}]'

            # If element is about adding additional image in overlay (see ImageElement)
            if hasattr(filter_element, '_image_id'):
                filters.append(f'{group_prefix}[{filter_element._image_id}:v]{filter_element.get_filter()}{group_suffix}')

            # Any other element
            else:
                filters.append(f'{group_prefix}{filter_element.get_filter()}{group_suffix}')

            i += 1

        return ';'.join(filters)

    def get_filter_complex(self, text_elements_data: dict = None) -> str:
        """ Get the filter_complex argument. For debug or test purpose

        :param text_elements_data: dict used to fill templates text elements values dynamically
        :return: filter_complex complete argument (to use in ffmpeg command)
        """
        return self.FILTER_COMPLEX.format(
            filters=self.get_filter_complex_content(text_elements_data=text_elements_data))

    def get_additional_inputs(self) -> list[str]:
        """ Get the list of all inputs to use in command. First one is the main media, other inputs will only add
        image in overlay (no audio)

        :return: list of inputs to use
        """

        inputs = []
        input_number = 0

        for filter_element in self.template_elements:

            # Filter out non ImageElement objects
            if not hasattr(filter_element, 'image_path'):
                continue
            inputs.append(getattr(filter_element, 'image_path'))

            # Update the input number id. In the command we may have multiple inputs, this is used to differentiate them
            input_number += 1
            filter_element._image_id = input_number

        return inputs


if __name__ == '__main__':
    # from head_up_display.template_elements import text_element
    # text = text_element.TextElement(value='', text_id='foo')
    # text_elements_data = {'foo': 'Hello fools'}
    #
    # template = HudTemplate(template_elements=[text])
    # # print(template.get_filter_complex_content(text_elements_data=text_elements_data))
    # import os
    # example_directory_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..', 'examples'))
    # json_file_example = os.path.join(example_directory_path, 'hud_template.json')
    # template.export_template_to_json_file(json_file_example)

    test_file = r'C:\Users\Vincent\Documents\PycharmProjects\head_up_display\examples\hud_template.json'
    template = HudTemplate.from_template_json_file(json_file=test_file)
