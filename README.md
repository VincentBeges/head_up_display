# head_up_display_generator
A simple tool to create head up displays over media using FFMPEG.

The main idea of this tool is to stay pretty simple and limited. For more advanced
overlay creation, FFMPEG is here.

## Tool development
Tool should be able to:
- generate HUD over an image or a movie (keeping codec and quality)
- resize source media and add black bar on top and bottom
- add hud elements using templates defined in a json file or with python classes
- elements we can use in templates are:
    - text
    - date/time
    - frame
    - filename / filepath
    - timecode
- text element can be filled dynamically using an ID in the template and a dict in the generation method
- test all templates without giving input

### Generate "empty" media for tests purpose
Test color bars \
`ffmpeg -f lavfi -i testsrc -t 30 -pix_fmt yuv420p testsrc.mp4`

Test red media \
`ffmpeg -f lavfi -i color=color=red -t 30 red.mp4`

## Requires
- ffmpeg with fontconfig setup at build
- pydantic

