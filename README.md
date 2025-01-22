# Head up display generator
This is a simple tool to create head up displays (HUD) over media using FFMPEG.

ADD IMAGE EXAMPLES

Adding a head up display is a process used in movie/animation/VFX industries to apply in overlay of an input media some visual 
data (text, frame number, logo, etc), mostly for reviewing purpose.

# Table of contents

## Tool Features

The HUD generator tool can be used to :
- modify the input media
  - resize the media
  - add black bar on top and bottom
- add data in overlay
- batch process
  - create templates

## Installation

### Use custom ffmpeg path
Setup `FFMPEG_PATH` environment variable

## Dependencies

## Simple usage

## Advanced usage

### Hud generation
Automatic size scaling

#### Generation configuration defined per project / environment
The GenerationConfig class is based on pydantic Settings Management : \
https://docs.pydantic.dev/latest/concepts/pydantic_settings/

The settings will be loaded from environment variables through `prefix` + `class attribute`.
The default prefix name is defined in `head_up_display/constants.py` file.
```python
from head_up_display.hud.generation_config import GenerationConfig
import os

# Example to set up a specific value in the environment variable
os.environ['hud_generation_config__do_resize'] = 'False'
os.environ['hud_generation_config__resize_width'] = '1200'

# Init the configuration will load environment variables values if defined
# Default value will be used if the environment variable is not set
config = GenerationConfig()

print(config.model_dump())
# >>> {'do_resize': False, 'resize_width': 1200, 'resize_height': 1920, 'add_black_bar': True, 'black_bar_height': 20, 'auto_scale_hud_elements': True, 'override_existing_size_values': False, 'ffmpeg_command_as_file': False}
```
Note that the environment variable type is automatically converted (from string to bool, int, etc)

/



~~The HUD generation is done using a template and an input media.
It can:
- process modification on input media
- add static/dynamic overlay data using a template

The templates are used to define what we want to add in overlay. It can be defined by:
- Python objects
- json files~~



The HUD generation is divided in two step:
- Process the source media
- Create the HUD in overlay

### Source media process features
This step is used to modify the source media mostly for conformation aspects. You can:
- Resize media
- Add black bar to the top and bottom

### Adding HUD features
HUD elements you can use in overlay are next one:
- Adding static text
- Adding dynamic text (you can change the value for each generation using a dict)
- Adding datetime, date or time
- Adding filepath or filename
- Adding frame number
- Adding image
- Adding timecode

Each HUD element position can be defined
- Automatically with keywords like "top", "center"
- Manually with pixel position

Each HUD element size can be defined
- Automatically to fit in the black bar size (with a margin)
- Manually in point size

## How to use tool

## How to create HUD template


## Tool Architecture
Generate a schema explaining structure with automatic tool

- FFMPEGWrapper
- HudGenerator
- Hud template
- Template elements
   - ElementPosition
      - TemplateElement
         - BaseTextElement
            - TextElement
            - FrameElement
            - TimecodeElement
            - FilepathElement
            - DatetimeElement
         - ImageElement


### Generate "empty" media for tests purpose
Test color bars \
`ffmpeg -f lavfi -i testsrc -t 30 -pix_fmt yuv420p testsrc.mp4`

Test red media \
`ffmpeg -f lavfi -i color=color=red -t 30 red.mp4`

Extract a single frame from a media \
`ffmpeg -i input.mp4 -frames:v 1 first.jpg`

## Requires
- ffmpeg with fontconfig setup at build
- pydantic


