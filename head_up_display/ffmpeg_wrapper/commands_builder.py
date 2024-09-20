from dataclasses import dataclass
import os


@dataclass
class FFMPEGCommandsBuilder(object):
    """ Storing ffmpeg commands elements """

    ffmpeg: str = os.getenv('FFMPEG_PATH', 'ffmpeg')
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

    def get_command_to_create_hud_using_filters(self,
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

        return self._build_command(
            self.ffmpeg,
            self.override_files,
            self.hide_banner,
            *[self.add_input.format(input_file) for input_file in input_files],
            self.complex_filters.format(filters),
            self.output.format(output_file)
        )
