import os

FFMPEG_CMD = 'ffmpeg'

## HUD GENERATION ##
GENERATION_CONFIG_ENV_PREFIX = 'hud_generation_config__'

## HUD TEMPLATES ##
TEXT_ELEMENT_TYPE = 'text'
FILEPATH_ELEMENT_TYPE = 'filepath'
FILENAME_ELEMENT_TYPE = 'filename'

TEMPLATE_ELEMENTS_TYPES = [TEXT_ELEMENT_TYPE]

OUTPUT_PATH_TEXT_ID = 'output_path'

POLICE_TEXT_PATH = os.getenv('POLICE_TEXT_PATH',
                             os.path.realpath(os.path.join(__file__, '..', 'fonts', 'Roboto', 'Roboto-VariableFont_wdth_wght.ttf')))
POLICE_TEXT_PATH = POLICE_TEXT_PATH.replace('\\', '/')
if POLICE_TEXT_PATH[1] == ':':
    POLICE_TEXT_PATH = POLICE_TEXT_PATH[2:]
#TODO: Find a better solution to load the police, it's only working in Windows and is not very clean
