from head_up_display import constants
from head_up_display.ffmpeg_wrapper import commands_builder
from head_up_display.hud.generation_config import GenerationConfig
from head_up_display.template.hud_template import HudTemplate
from head_up_display.template.resize_filter import ResizeAndPadFilter
import subprocess


class HudGenerator(object):
    """ Main object used to generate the head up display """

    def __init__(self,
                 hud_template: HudTemplate,
                 generation_config: GenerationConfig = None,
                 ):
        """ Init a HudGenerator instance

        :param hud_template: template to use in generation
        :param generation_config: config used during generation to modify input media
        """
        self.hud_template = hud_template

        self.ffmpeg_commands = commands_builder.FFMPEGCommandsBuilder()

        self.generation_config = generation_config or GenerationConfig()

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
        ## 1 Prepare text elements data
        text_elements_data = text_elements_data or {}

        # Necessary for the FilepathElement objects
        text_elements_data[constants.OUTPUT_PATH_TEXT_ID] = destination_file

        ## 2 Resize source media and add black bar (or not according generation config)
        if self.generation_config.do_resize or self.generation_config.add_black_bar:
            resize_and_pad_filter = ResizeAndPadFilter.from_generation_config(generation_config=self.generation_config)

            if resize_and_pad_filter:
                # The "from_generation_config" class method from ResizeAndPagFilter return None if we don't want to
                # do_resize the media or add black bar. In this case we don't need to use it
                self.hud_template.template_elements.insert(0, resize_and_pad_filter) #TODO: correct the type

        ## 3 Resize all elements to fit in the black bars
        if self.generation_config.auto_scale_hud_elements:
            self.hud_template.resize_elements_from_black_bar_size(
                black_bar_height=self.generation_config.black_bar_height,
                override_existing_values=self.generation_config.override_existing_size_values,
            )

        ## 4 Prepare the input files. First one is the main media, any other are additional image added in overlay
        input_files = [source_file]
        input_files.extend(self.hud_template.get_additional_inputs())

        command = self.ffmpeg_commands.get_command_to_create_hud_using_filters(
            input_files=input_files,
            output_file=destination_file,
            filters=self.hud_template.get_filter_complex_content(text_elements_data=text_elements_data))

        if dry_run:
            print('Dry run generate HUD:')
            print(command)
            #TODO: print generator settings

        else:
            res = subprocess.call(command, shell=True)
            print(command)


if __name__ == '__main__':

    """
    On a tel HUD
    Quand on process on lui dit, c'est tel HUD et voila la conf a utiliser (do_resize, etc)
    Permet de batch process, permet de process un meme hud sur differents media        
    Permet de process pour differentes conf (projets)
    """