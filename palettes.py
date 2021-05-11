import random
from pygame import Color


color_palette_clown = [ Color(26, 81, 115),
                        Color(60, 166, 97),
                        Color(242, 194, 48),
                        Color(242, 138, 128),
                        Color(191, 48, 48) ]

color_palette_sunny = [ Color(255, 195, 0),
                        Color(144, 12, 62),
                        Color(199, 0, 57),
                        Color(255, 87, 51),
                        Color(87, 24, 69) ]

color_palette_neon = [ Color(0,0,0),
                       Color(250, 0, 154),
                       Color(176, 6, 214),
                       Color(105, 5, 237),
                       Color(17, 6, 214) ]

color_palette_hackergreen = [ Color(0, 3, 0),
                              Color(6, 47, 64),
                              Color(2, 89, 81),
                              Color(29, 115, 75),
                              Color(22, 140, 64),
                              Color(130, 217, 43) ]

# Get one of the above palettes randomly:
def get_random_color_palette():
    return random.choice((color_palette_clown, color_palette_sunny, color_palette_neon, color_palette_hackergreen))
