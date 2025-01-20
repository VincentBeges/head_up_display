import pytest
from head_up_display.ffmpeg_wrapper.commands_builder import FFMPEGCommandsBuilder

@pytest.fixture
def builder():
    return FFMPEGCommandsBuilder()

def test_build_command(builder):
    cmd = builder._build_command('a', 'b')
    assert isinstance(cmd, str)
    assert cmd == 'a b'

def test_get_command_to_create_hud_using_filters(builder):
    builder.ffmpeg = 'ffmpeg'  # For test purpose, to avoid the dynamic value
    input_file = 'root/input_file.mp4'
    output_file = 'root/output_file.mp4'
    filters = 'drawtext=text=\'this is my text\':fontcolor=black:fontsize=10:x=50:y=50'
    cmd = builder.get_command_to_create_hud_using_filters(
        input_files=[input_file],
        output_file=output_file,
        filters=filters,
    )
    expected_cmd = (
        f'ffmpeg -y -hide_banner -i {input_file} -filter_complex '
        f'"drawtext=text=\'this is my text\':fontcolor=black:fontsize=10:x=50:y=50" '
        f'{output_file}'
    )
    assert cmd == expected_cmd