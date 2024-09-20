# Features
## Global
- [ ] Setup pip install
## Configuration
- [ ] Store ffmpeg command in a file and then execute it
- [x] We need to be able to set up configuration for a project



# Bugs



---

## Tool development [OLD]
Tool should be able to:
- [x] generate HUD over a movie (keeping codec and quality)
- [ ] generate HUD over an image (Use Path or File object ?)
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
- [ ] unit testing of all objects
- [ ] accessible with pip install
- [ ] documentation for all elements + examples
- [ ] fill the constants file to make it easy to update
- [ ] store the ffmpeg command in a file

Tool structure should be:
- [ ] HUD and template are used to define what we will see in overlay
- [ ] Generator settings are used to process source media before applying the HUD
