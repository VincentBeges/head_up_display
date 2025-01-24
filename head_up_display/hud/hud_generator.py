from head_up_display import constants
from head_up_display.ffmpeg_wrapper import commands_builder
from head_up_display.hud.generation_config import GenerationConfig
from head_up_display.template.hud_template import HudTemplate
from head_up_display.template.resize_filter import ResizeAndPadFilter
import os
import subprocess
import tempfile
import logging

logger = logging.getLogger(__name__)


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
    def test_given_hud_template(cls,
                                hud_template: HudTemplate,
                                generation_config: GenerationConfig = None,
                                text_elements_data: dict = None,
                                output_file: str = None,
                                source_width: int = 720,
                                source_height: int = 480,
                                ):
        """ Generate an example media with given hud template

        :param hud_template: HudTemplate object to test
        :param generation_config: GenerationConfig object to used to modify input file
        :param text_elements_data: dynamic data to use with template
        :param output_file: A filepath for the exported test file
        :param source_width: Size of the source media generated (used mainly to test the resize process)
        :param source_height: Size of the source media generated (used mainly to test the resize process)
        """

        input_file = tempfile.NamedTemporaryFile(mode='w+', prefix='test_movie_input', suffix='.mp4').name
        output_file = output_file or input_file.replace('input', 'output')

        # Generate a test movie to apply HUD over
        command = f'ffmpeg -f lavfi -i testsrc -t 30 -s {source_width}x{source_height} -pix_fmt yuv420p {input_file}'
        os.system(command=command)

        if not os.path.exists(input_file):
            raise OSError(f'Failed to create a test movie to apply HUD over:\n {input_file}')

        # Don't resize the generated movie, just add black bar
        config = generation_config or GenerationConfig(add_black_bar=True,
                                                       black_bar_height=int(source_height * 0.1),
                                                       do_resize=False,
                                                       )

        generator = cls(hud_template=hud_template,
                        generation_config=config,
                        )
        generator.generate(source_file=input_file,
                           destination_file=output_file,
                           text_elements_data=text_elements_data,
                           dry_run=False,
                           )
        try:
            os.remove(input_file)
        except OSError:
            logger.error(f'Failed to remove temporary generated source file. Not a big deal\n {input_file}')

        logger.info('## Generated a test media for hud template ##')
        logger.info(output_file)

    @classmethod
    def test_given_hud_template_from_file(cls,
                                          hud_template_filepath:str,
                                          generation_config: GenerationConfig = None,
                                          text_elements_data: dict = None,
                                          output_file: str = None,
                                          source_width: int = 720,
                                          source_height: int = 480,
                                          ):
        """ Test the given template file without giving input

        :param hud_template_filepath: template as a json file
        :param generation_config: GenerationConfig object to used to modify input file
        :param text_elements_data: dynamic data to use with template
        :param output_file: A filepath for the exported test file
        :param source_width: Size of the source media generated (used mainly to test the resize process)
        :param source_height: Size of the source media generated (used mainly to test the resize process)
        """
        # Load template
        hud_template = HudTemplate.from_template_json_file(json_file=hud_template_filepath)
        # Test template
        cls.test_given_hud_template(hud_template=hud_template,
                                    generation_config=generation_config,
                                    text_elements_data=text_elements_data,
                                    output_file=output_file,
                                    source_height=source_height,
                                    source_width=source_width,
                                    )

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
                # The "ResizeAndPagFilter.from_generation_config()" class method return None if we don't want to
                # do_resize the media or add black bar. In this case we don't need to use it
                self.hud_template.template_elements.insert(0, resize_and_pad_filter)

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
            logger.info('Dry run generate HUD:')
            logger.info(command)

            logger.info('Generation settings:')
            self.generation_config.print_settings()

        else:
            res = subprocess.call(command, shell=True)
            logger.debug(command)
            if self.generation_config.ffmpeg_command_as_file:
                command_file = tempfile.NamedTemporaryFile(dir=self.generation_config.temp_directory,
                                                           prefix='hud_command_',
                                                           suffix='.txt'
                                                           )
                with open(command_file.name, 'w') as stream:
                    stream.write(command)
                logger.info(f'Written command in: {command_file.name}')

            if res != 0:
                raise RuntimeError('Failed to process HUD generation')
            logger.info('## Processed HUD generation ##')
