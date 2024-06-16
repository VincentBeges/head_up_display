# Head up display generator
This is a simple tool to create head up displays (HUD) over media using FFMPEG.
Adding HUD is a process used in movie, animation or VFX industries to apply in overlay of an input media some visual 
data (text, frame number, logo, etc), mostly for reviewing purpose.

The HUD generation is done using a template and an input media.
It can:
- process modification on input media
- add static/dynamic overlay data using a template

The templates are used to define what we want to add in overlay. It can be defined by:
- Python objects
- json files


## Tool Features

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


## Tool development
Tool should be able to:
- [x] generate HUD over a movie (keeping codec and quality)
- [ ] generate HUD over an image (Use Path or File object ?)
- [ ] generate HUD over a sequence
- [x] resize source media and add black bar on top and bottom
- [w] add hud elements using templates defined in a json file or with python classes
-  elements we can use in templates are:
    - [x] text
    - [x] date/time
    - [x] filename / filepath
    - [x] frame
    - [x] timecode
    - [w] another image (logo or other) 
- [x] text element can be filled dynamically using an ID in the template and a dict in the generation method
- [ ] test all templates without giving input
- [ ] unit testing of all objects
- [ ] accessible with pip install
- [ ] documentation for all elements + examples
- [ ] fill the constants file to make it easy to update
- [ ] store the ffmpeg command in a file

Tool structure should be:
- [ ] HUD and template are used to define what we will see in overlay
- [ ] Generator settings are used to process source media before applying the HUD

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

## Requires
- ffmpeg with fontconfig setup at build
- pydantic

