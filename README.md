# head_up_display_generator
A simple tool to create head up displays over media using FFMPEG.

The main idea of this tool is to stay pretty simple and limited. For more advanced
overlay creation, FFMPEG is here.

## Tool development
Tool should be able to:
- [x] generate HUD over a movie (keeping codec and quality)
- [ ] generate HUD over an image (Use Path or File object ?)
- [ ] generate HUD over a sequence
- [ ] resize source media and add black bar on top and bottom
- [ ] add hud elements using templates defined in a json file or with python classes
-  elements we can use in templates are:
    - [x] text
    - [x] date/time
    - [x] filename / filepath
    - [x] frame
    - [x] timecode
    - [ ] another image (logo or other) 
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


### Generate "empty" media for tests purpose
Test color bars \
`ffmpeg -f lavfi -i testsrc -t 30 -pix_fmt yuv420p testsrc.mp4`

Test red media \
`ffmpeg -f lavfi -i color=color=red -t 30 red.mp4`

## Requires
- ffmpeg with fontconfig setup at build
- pydantic

