from pydantic import BaseModel
from typing import Union

class GenerationConfig(BaseModel):
    """ Storing the hud generation process configuration

    What is writen in the overlay is defined using templates elements.
    The way we process media before writing hud is defined in this class.
    """

    # Configuration to resize the input media
    do_resize: bool = True
    resize_width: int = 1920
    resize_height: int = 1080

    # Configuration to add a black bar to the media
    add_black_bar: bool = True
    black_bar_height: Union[int, str] = 20  # Fixed int pixel size or string percent size

    # Configuration to scale all elements to fit in the black bars
    auto_scale_hud_elements: bool = True
    override_existing_size_values: bool = False  # False will override size values only if font_size is 0

    # Configuration to store the command in a file
    ffmpeg_command_as_file: bool = False  # True to write it in a pickle file and read it, easiest debug
    #TODO: make this feature
    #TODO: we need to be able to setup it for a full projet / environment