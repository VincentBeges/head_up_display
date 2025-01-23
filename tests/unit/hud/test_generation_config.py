from head_up_display.hud import generation_config
from  head_up_display import constants
import os

def test_config_settings():
    # Test class init
    config = generation_config.GenerationConfig()
    assert config

    # Test settings a setting
    tmp_dir = '/temp_dir'
    config.temp_directory = tmp_dir

def test_config_settings_with_env_variables():
    # Test config setting using env variables
    env_variable_name = f'{constants.GENERATION_CONFIG_ENV_PREFIX}temp_directory'
    env_variable_value = 'another_temp_dir'
    os.environ[env_variable_name] = env_variable_value

    config = generation_config.GenerationConfig()
    assert config.temp_directory == env_variable_value

def test_config_print(capfd):
    config = generation_config.GenerationConfig()
    config.print_settings()

    out, err = capfd.readouterr()
    assert out
