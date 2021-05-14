import random
from pygame import Color


color_palette_clown = [ Color(26, 81, 115),
                        Color(60, 166, 97),
                        Color(242, 194, 48),
                        Color(242, 138, 128),
                        Color(191, 48, 48),
                        Color(140, 40, 40) ]

color_palette_sunny = [ Color(255, 195, 0),
                        Color(144, 12, 62),
                        Color(199, 0, 57),
                        Color(255, 87, 51),
                        Color(87, 24, 69),
                        Color(40, 26, 13) ]

color_palette_purple = [ Color(0,0,0),
                       Color(250, 0, 154),
                       Color(176, 6, 214),
                       Color(105, 5, 237),
                       Color(17, 6, 214),
                       Color(250, 134, 246)]

color_palette_red_grey = [Color(186, 195, 202),
                       Color(244, 68, 72),
                       Color(254, 34, 48),
                       Color(154, 41, 48),
                       Color(135, 5, 70),
                       Color(40, 70, 90)]

color_palette_hackergreen = [ Color(0, 3, 0),
                              Color(6, 47, 64),
                              Color(2, 89, 81),
                              Color(29, 115, 75),
                              Color(22, 140, 64),
                              Color(130, 217, 43),
                              Color(220, 230, 70)]

color_palette_sand = [Color(20, 12, 4),
                       Color(160, 112, 72),
                       Color(228, 208, 179),
                       Color(162, 138, 109),
                       Color(211, 203, 172),
                       Color(245, 242, 208)]

color_palette_holland = [Color(5, 5, 5),
                        Color(174, 28, 40),
                        Color(230, 230, 230),
                        Color(33, 70, 139),
                        Color(255, 140, 0),
                        Color(128, 0, 32)]

color_palette_summer = [Color(200, 200, 200),
                        Color(255, 140, 0),
                        Color(156, 157, 151),
                        Color(71, 79, 82),
                        Color(29, 28, 33),
                        Color(255, 216, 61)]

color_palette_greyscale = [Color(10, 10, 10),
                        Color(220, 220, 220),
                        Color(170, 170, 170),
                        Color(120, 120, 120),
                        Color(80, 80, 80),
                        Color(40, 40, 40),
                        Color(220, 200, 60),]

color_palette_ice = [Color(10, 10, 45),
                        Color(227, 242, 253),
                        Color(187, 222, 251),
                        Color(144, 202, 249),
                        Color(100, 181, 246),
                        Color(130, 177, 255),
                        Color(13, 71, 161),]

color_palette_durag_activity = [Color(40, 25, 25),
                        Color(141, 110, 99),
                        Color(121, 85, 72),
                        Color(109, 76, 65),
                        Color(93, 64, 55),
                        Color(188, 170, 164),]


all_palettes = [
    color_palette_clown,
    color_palette_sunny, 
    color_palette_purple, 
    color_palette_hackergreen,
    color_palette_sand,
    color_palette_red_grey,
    color_palette_holland,
    color_palette_summer,
    color_palette_greyscale,
    color_palette_ice,
    color_palette_durag_activity,
]

# Get one of the above palettes randomly:
def get_random_color_palette():
    return random.choice(all_palettes)

