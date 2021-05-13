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

color_palette_mkbhd = [Color(186, 195, 202),
                       Color(244, 68, 72),
                       Color(254, 34, 48),
                       Color(154, 41, 48),
                       Color(135, 5, 70)]

color_palette_hackergreen = [ Color(0, 3, 0),
                              Color(6, 47, 64),
                              Color(2, 89, 81),
                              Color(29, 115, 75),
                              Color(22, 140, 64),
                              Color(130, 217, 43) ]

color_palette_sand = [Color(20, 12, 4),
                       Color(160, 112, 72),
                       Color(228, 208, 179),
                       Color(162, 138, 109),
                       Color(211, 203, 172)]

color_palette_holland = [Color(5, 5, 5),
                       Color(174, 28, 40),
                       Color(230, 230, 230),
                       Color(33, 70, 139),
                       Color(255, 140, 0)]

all_palettes = [
    color_palette_clown,
    color_palette_sunny, 
    color_palette_neon, 
    color_palette_hackergreen,
    color_palette_sand,
    color_palette_mkbhd,
    color_palette_holland,
]

# Get one of the above palettes randomly:
def get_random_color_palette():
    return random.choice(all_palettes)
