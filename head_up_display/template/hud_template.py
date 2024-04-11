from head_up_display.template_elements import base_element
from head_up_display import constants
import string


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

    @classmethod
    def from_template_json_file(cls):
        # TODO: create method to read template from a json file
        pass

    def add_template_element(self, element: base_element.TemplateElement):
        """ Add given element in the template

        :param element: Template element (inherit from TemplateElement)
        """
        if len(self.template_elements) == len(self.FILTERS_INCREMENT):
            raise RuntimeError(f'Trying to add too much filters > {len(self.template_elements)}.'
                               f'See "HudTemplate.FILTERS_INCREMENT" list')

        self.template_elements.append(element)

    def get_filter_complex_content(self, text_elements_data: dict = None) -> str:
        """ Get the filter complex string to use in ffmpeg content.
        This will not include -filter_complex "..." only what's inside "..."

        ..note::
            Note about the source and destination groups.
            In FFMPEG filter_complex, you have multiple following filters to execute. For each filter (except first and
            last one) you have to define the name of the source input group used and the name of the destination output.

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
        for filter_element in self.template_elements:

            # For text elements using dynamic values input
            if hasattr(filter_element, 'text_id') and text_elements_data.get(filter_element.text_id):
                filter_element.value = text_elements_data[filter_element.text_id].replace('\'', '\\\'')

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


if __name__ == '__main__':
    from head_up_display.template_elements import text_element
    text = text_element.TextElement(value='', text_id='foo')
    text_elements_data = {'foo': 'Hello fools'}

    template = HudTemplate(template_elements=[text])
    print(template.get_filter_complex_content(text_elements_data=text_elements_data))
