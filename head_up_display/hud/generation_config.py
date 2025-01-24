from head_up_display import constants
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Union
from pprint import pprint
import tempfile
import os


class GenerationConfig(BaseSettings):
    """ Storing the hud generation process configuration

    What is writen in the overlay is defined using templates elements.
    The way we process media before writing hud is defined in this class.

    Any of the attributes bellow can be override using env variable (except model_config).
    >>> import os
    >>> os.environ['hud_generation_config__do_resize'] = 'False'
    >>> config = GenerationConfig()
    >>> print(config.do_resize)
    >>> # False
    The environment variable name is composed of env_prefix (defined in current model_config) + attribute name

    https://docs.pydantic.dev/latest/concepts/pydantic_settings/#usage
    """
    model_config = SettingsConfigDict(env_prefix=constants.GENERATION_CONFIG_ENV_PREFIX)

    temp_directory: str = os.path.join(tempfile.gettempdir(), 'hud_generation')

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
    ffmpeg_command_as_file: bool = False  # True to write the command in a file during hud generation

    def print_settings(self):
        """ Print the generation config settings (used in dryrun mode) """
        pprint(self.model_dump())
