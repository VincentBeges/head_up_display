from head_up_display.ffmpeg_wrapper import commands_builder
from head_up_display import constants
from shutil import which
import pytest

def test_ffmpeg_is_installed():
    """ Check that ffmpeg is existing on current computer """
    builder = commands_builder.FFMPEGCommandsBuilder
    if builder.ffmpeg is constants.FFMPEG_CMD:
        # Check if `ffmpeg` command is a valid program
        if not which(builder.ffmpeg):
            raise RuntimeError('ffmpeg is not installed on current computer')
