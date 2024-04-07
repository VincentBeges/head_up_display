from head_up_display.ffmpeg_wrapper import commands_builder
from head_up_display.template.hud_template import HudTemplate
import subprocess


class HudGenerator(object):
    """ Main object used to generate the head up display """

    def __init__(self, hud_template: HudTemplate):
        """ Init a HudGenerator instance

        :param hud_template: template to use in generation
        """
        self.hud_template = hud_template

        self.ffmpeg_commands = commands_builder.FFMPEGCommandsBuilder()

    @classmethod
    def test_given_hud_template(cls, hud_template: HudTemplate, text_elements_data: dict = None):
        #TODO: test a given template by generating an empty image with given hud data. The ID are used as input
        pass

    def generate(self,
                 source_file: str,
                 destination_file: str = None,
                 text_elements_data: dict = None,
                 dry_run: bool = False,
                 ):
        """ Generate head up display over source file

        :param source_file: media filepath to process
        :param destination_file: media destination path
        :param text_elements_data: dict of {text_element.text_id: value_to_show}
        :param dry_run: True to dry run process and print command
        """
        text_elements_data = text_elements_data or {}

        command = self.ffmpeg_commands.get_command_to_create_hud_using_filters(
            input_file=source_file,
            output_file=destination_file,
            filters=self.hud_template.get_filter_complex_content(text_elements_data=text_elements_data))

        if dry_run:
            print('Dry run generate HUD:')
            print(command)

        else:
            res = subprocess.call(command, shell=True)
            print(command)
