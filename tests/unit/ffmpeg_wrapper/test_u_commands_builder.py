from head_up_display.ffmpeg_wrapper import commands_builder

def test_building_command():
    """ Test the building a command """
    builder = commands_builder.FFMPEGCommandsBuilder()

    # Testing _build_command()
    cmd = builder._build_command('a', 'b')
    assert isinstance(cmd, str)
    assert cmd == 'a b'

    # Testing get_command_to_create_hud_using_filters()
    builder.ffmpeg = 'ffmpeg' # For test purpose, to avoid the dynamic value
    input_file = 'root/input_file.mp4'
    output_file = 'root/output_file.mp4'
    filters = 'drawtext=text=\'this is my text\':fontcolor=black:fontsize=10:x=50:y=50'
    cmd = builder.get_command_to_create_hud_using_filters(input_files=[input_file],
                                                          output_file=output_file,
                                                          filters=filters,
                                                          )
    assert cmd == (f'ffmpeg -y -hide_banner -i {input_file} -filter_complex '
                   f'"drawtext=text=\'this is my text\':fontcolor=black:fontsize=10:x=50:y=50" '
                   f'root/output_file.mp4')