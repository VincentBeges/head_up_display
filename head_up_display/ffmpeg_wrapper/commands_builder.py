from dataclasses import dataclass
from head_up_display import constants
import os


@dataclass
class FFMPEGCommandsBuilder(object):
    """ Storing ffmpeg commands elements """

    ffmpeg: str = os.getenv('FFMPEG_PATH', constants.FFMPEG_CMD)
    override_files: str = '-y'
    hide_banner: str = '-hide_banner'
    add_input: str = '-i {0}'
    keep_video_quality = '-q:v 1 -qmin 1'
    complex_filters: str = '-filter_complex "{0}"'
    output: str = '{0}'

    @staticmethod
    def _build_command(*args) -> str:
        """ Build command with given elements (current class attributes) """
        return ' '.join(args)
    
    @classmethod
    def get_command_to_create_hud_using_filters(cls,
                                                input_files: list[str],
                                                output_file: str,
                                                filters: str,
                                                ) -> str:
        """ Get the FFMPEG command used to create hud over a given media.

        :param input_files: list of input files to process. First one the background element.
        :param output_file: output file to save media with hud
        :param filters: complex filters used to generate the hud (coming from HudTemplate object)
        :return: The ffmpeg command ready to execute
        """

        return cls._build_command(
            cls.ffmpeg,
            cls.override_files,
            cls.hide_banner,
            *[cls.add_input.format(input_file) for input_file in input_files],
            cls.complex_filters.format(filters),
            cls.output.format(output_file)
        )
