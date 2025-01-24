# Tool development
## Features
**Done**
- [x] generate HUD over a movie (keeping codec and quality)
- [x] resize source media and add black bar on top and bottom
- [x] add hud elements using templates defined in a json file or with python classes
-  elements we can use in templates are:
    - [x] text
    - [x] date/time
    - [x] filename / filepath
    - [x] frame
    - [x] timecode
    - [x] another image (logo or other) 
- [x] text element can be filled dynamically using an ID in the template and a dict in the generation method
- [x] test all templates without giving input
- [x] unit testing of all objects
- [x] fill the constants file to make it easy to update
- [x] Use a logger instead of print
- [x] We need to be able to set up configuration for a project
- [x] store the ffmpeg command in a file

**To do**
- [ ] setup with pip install
- [ ] ensure it's working on Linux
- [ ] add usage of FFMPEG fontconfig if available
- [ ] automatic test with Github actions
- [ ] print CICD badge in README
- [ ] documentation for all elements + examples
- [ ] generate HUD over an image (Use Path or File object ?) -> a tester
- [ ] batch process multiple media in a folder
- [ ] add command line for the generation
- [ ] setup tool for FFFMPEG font path
- [ ] automatic resize for image elements
- [ ] add negative values to position in pixel from the other side instead of x and y coordinate (-10 -> main_w - 10 for example)


## Bugs
- [ ] In text auto resize : Not fit perfectly for uppercase text
- [ ] In text : auto align can feel wrong when we don't have low letter like y, p, etc. See frame script
- [ ] Image can be wrongly positioned due to black bar positioning
- [ ] Fix police file
