import pytest
from head_up_display.template.resize_filter import ResizeAndPadFilter
from head_up_display.hud.generation_config import GenerationConfig
from pydantic import ValidationError

@pytest.fixture
def resize_and_pad_filter():
    return ResizeAndPadFilter()

def test_resize_and_pad_filter_initialization(resize_and_pad_filter):
    # Ensure we have unchanged default values
    assert resize_and_pad_filter.width == 1920
    assert resize_and_pad_filter.height == 1080
    assert resize_and_pad_filter.force_original_aspect_ratio == 'decrease'
    assert resize_and_pad_filter.black_bar_height == 20
    assert resize_and_pad_filter.display_aspect_ratio == 1.0

@pytest.mark.parametrize('height,expected', [('10%', '1080*10.0/100'),
                                             (20, '20'),
                                             ('15', '15'),
                                             ])
def test_conform_black_bar_height(height, expected):
    # Test the conform_black_bar_height method with various inputs
    resize_filter = ResizeAndPadFilter(black_bar_height=height)
    assert resize_filter.black_bar_height == expected

def test_conform_black_bar_height_invalid():
    # Test with invalid input
    with pytest.raises(ValueError):
        ResizeAndPadFilter(black_bar_height='invalid%')

def test_conform_width():
    assert ResizeAndPadFilter.conform_width(1920, None) == '1920'
    assert ResizeAndPadFilter.conform_width(-1, None) == 'in_w'

def test_conform_height():
    assert ResizeAndPadFilter.conform_height(1080, None) == '1080'
    assert ResizeAndPadFilter.conform_height(-1, None) == 'in_h'

def test_get_filter(resize_and_pad_filter):
    assert isinstance(resize_and_pad_filter.get_filter(), str)

def test_from_generation_config():
    generation_config = GenerationConfig(do_resize=True,
                                         resize_width=1280,
                                         resize_height=720,
                                         add_black_bar=True,
                                         black_bar_height='10')
    resize_and_pad_filter = ResizeAndPadFilter.from_generation_config(generation_config)
    assert resize_and_pad_filter.width == '1280'
    assert resize_and_pad_filter.height == '720'
    assert resize_and_pad_filter.black_bar_height == '10'

# def test_invalid_black_bar_height():
#     with pytest.raises(ValidationError):
#         ResizeAndPadFilter(black_bar_height='invalid%')