import pytest
import os
import tempfile
from unittest.mock import patch, MagicMock
from head_up_display.hud.hud_generator import HudGenerator
from head_up_display.template.hud_template import HudTemplate
from head_up_display.hud.generation_config import GenerationConfig
from head_up_display.template.resize_filter import ResizeAndPadFilter

@pytest.fixture
def hud_template():
    return MagicMock(spec=HudTemplate)

@pytest.fixture
def generation_config():
    return MagicMock(spec=GenerationConfig)

@pytest.fixture
def hud_generator(hud_template, generation_config):
    return HudGenerator(hud_template=hud_template, generation_config=generation_config)

def test_hud_generator_initialization(hud_template, generation_config):
    # Test basic class init
    generator = HudGenerator(hud_template=hud_template, generation_config=generation_config)
    assert generator.hud_template == hud_template
    assert generator.generation_config == generation_config

@patch('head_up_display.hud.hud_generator.tempfile.NamedTemporaryFile')
@patch('head_up_display.hud.hud_generator.os.system')
@patch('head_up_display.hud.hud_generator.os.path.exists')
@patch('head_up_display.hud.hud_generator.HudGenerator.generate')
def test_test_given_hud_template(mock_generate, mock_exists, mock_system, mock_tempfile, hud_template, generation_config):
    # Test the "test_given_hud_template" method used to generate an example media from a hud template
    mock_tempfile.return_value.name = 'temp_file.mp4'
    mock_exists.return_value = True

    HudGenerator.test_given_hud_template(hud_template=hud_template, generation_config=generation_config)

    mock_system.assert_called_once()
    mock_generate.assert_called_once()
    mock_exists.assert_called_once()

@patch('head_up_display.hud.hud_generator.HudTemplate.from_template_json_file')
@patch('head_up_display.hud.hud_generator.HudGenerator.test_given_hud_template')
def test_test_given_hud_template_from_file(mock_test_given_hud_template, mock_from_template_json_file):
    # Test the "test_given_hud_template_from_file" method used to generate an example media from a hud template file
    mock_from_template_json_file.return_value = MagicMock(spec=HudTemplate)

    HudGenerator.test_given_hud_template_from_file(hud_template_filepath='dummy_path')

    mock_from_template_json_file.assert_called_once_with(json_file='dummy_path')
    mock_test_given_hud_template.assert_called_once()
