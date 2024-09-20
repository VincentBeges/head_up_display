from head_up_display import constants
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Union
import os


class GenerationConfig(BaseSettings):
    """ Storing the hud generation process configuration

    What is writen in the overlay is defined using templates elements.
    The way we process media before writing hud is defined in this class.
    """
    model_config = SettingsConfigDict(env_prefix=constants.GENERATION_CONFIG_ENV_PREFIX)

    # Configuration to resize the input media
    do_resize: bool = True
    resize_width: int = 1920
    resize_height: int = 1920

    # Configuration to add a black bar to the media
    add_black_bar: bool = True
    black_bar_height: Union[int, str] = 20  # Fixed int pixel size or string percent size

    # Configuration to automatically scale all elements to fit in the black bars
    auto_scale_hud_elements: bool = True
    override_existing_size_values: bool = False  # False will override size values only if font_size is 0

    # Configuration to store the command in a file
    ffmpeg_command_as_file: bool = False  # True to write it in a pickle file to execute command (to keep history)
    #TODO: make this feature


if __name__ == '__main__':
    # Example to override default value using environment variables
    os.environ['hud_generation_config__do_resize'] = 'False'
    os.environ['hud_generation_config__resize_width'] = '1200'

    config = GenerationConfig()
    print(config.model_dump())
