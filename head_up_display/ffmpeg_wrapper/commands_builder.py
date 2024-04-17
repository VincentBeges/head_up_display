from dataclasses import dataclass
import os


# cmd = f'ffmpeg -y -hide_banner -i {source_file} -q:v 1 -qmin 1 -filter_complex ' \
#       f'"scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:{1080 + (BLACK_BAR_HEIGHT * 2)}
#       :(ow-iw)/2:(oh-ih)/2,setsar=1" ' \
#       f'{destination_file}'


@dataclass
class FFMPEGCommandsBuilder(object):
    """ Storing ffmpeg commands elements """
    ffmpeg: str = os.getenv('FFMPEG_PATH', 'ffmpeg')  #TODO: to explain in documentation
    override_files: str = '-y'
    hide_banner: str = '-hide_banner'
    add_input: str = '-i {0}'
    keep_video_quality = '-q:v 1 -qmin 1'
    complex_filters: str = '-filter_complex "{0}"'
    output: str = '{0}'

    @staticmethod
    def _build_command(*args):
        """ Build command with given elements (current class attributes) """
        return ' '.join(args)

    def get_command_to_create_hud_using_filters(self,
                                                input_file: str,
                                                output_file: str,
                                                filters: str
                                                ) -> str:
        """ Get the FFMPEG command used to create hud over a given media

        ..note::
            The function name could be more generic but I wanted a precise name to know which function we use to
            get the ffmpeg command to create hud

        :param input_file: input file to process
        :param output_file: output file to save media with hud
        :param filters: complex filters used to generate the hud (coming from HudTemplate object)
        :return: The ffmpeg command ready to execute
        """
        return self._build_command(
            self.ffmpeg,
            self.override_files,
            self.hide_banner,
            self.add_input.format(input_file),
            self.complex_filters.format(filters),
            self.output.format(output_file)
        )
