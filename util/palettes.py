from dataclasses import dataclass
import random
from pygame import Color


@dataclass
class BoidFramePalette:
    name: str
    background_color: Color
    obstacle_color: Color
    boid_palette: list


class PaletteSelector:
    # Class to abstract away the selection of a palette
    def __init__(self):
        self.current_palette_index = 0
        self.current_palette = all_palettes[0]

    def nxt(self):
        self.current_palette_index += 1
        self.current_palette_index %= len(all_palettes)
        self.current_palette = all_palettes[self.current_palette_index]

    def prv(self):
        self.current_palette_index -= 1
        self.current_palette_index %= len(all_palettes)
        self.current_palette = all_palettes[self.current_palette_index]

    def random(self):
        self.current_palette = get_random_color_palette()

    def palette(self):
        return self.current_palette


color_palette_clown = BoidFramePalette(
    name="Clown",
    background_color=Color(26, 81, 115),
    obstacle_color=Color(140, 40, 40),
    boid_palette=[
        Color(242, 194, 48),
        Color(242, 138, 128),
        Color(191, 48, 48),
        Color(60, 166, 97),
    ],
)

color_palette_sunny = BoidFramePalette(
    name="Sunny",
    background_color=Color(255, 195, 0),
    obstacle_color=Color(40, 26, 13),
    boid_palette=[
        Color(199, 0, 57),
        Color(255, 87, 51),
        Color(87, 24, 69),
        Color(144, 12, 62),
    ],
)

color_palette_neon = BoidFramePalette(
    name="Neon",
    background_color=Color(0, 0, 0),
    obstacle_color=Color(176, 6, 214),
    boid_palette=[
        Color(250, 134, 246),
        Color(105, 5, 237),
        Color(17, 6, 214),
        Color(250, 0, 154),
    ],
)

color_palette_red_grey = BoidFramePalette(
    name="Red",
    background_color=Color(63, 0, 0),
    obstacle_color=Color(30, 31, 128),
    boid_palette=[
        Color(254, 34, 48),
        Color(154, 41, 48),
        Color(135, 5, 70),
        Color(244, 68, 72),
    ],
)

color_palette_hackergreen = BoidFramePalette(
    name="Hacker Green",
    background_color=Color(0, 3, 0),
    obstacle_color=Color(220, 230, 70),
    boid_palette=[
        Color(2, 89, 81),
        Color(29, 115, 75),
        Color(22, 140, 64),
        Color(130, 217, 43),
        Color(6, 47, 64),
    ],
)

color_palette_sand = BoidFramePalette(
    name="Sand",
    background_color=Color(194, 178, 128),
    obstacle_color=Color(245, 242, 208),
    boid_palette=[
        Color(228, 208, 179),
        Color(162, 138, 109),
        Color(211, 203, 172),
        Color(160, 112, 72),
    ],
)

color_palette_holland = BoidFramePalette(
    name="Holland",
    background_color=Color(5, 5, 5),
    obstacle_color=Color(128, 0, 32),
    boid_palette=[
        Color(230, 230, 230),
        Color(33, 70, 139),
        Color(255, 140, 0),
        Color(174, 28, 40),
    ],
)

color_palette_summer = BoidFramePalette(
    name="Summer",
    background_color=Color(200, 200, 200),
    obstacle_color=Color(255, 216, 61),
    boid_palette=[
        Color(156, 157, 151),
        Color(71, 79, 82),
        Color(29, 28, 33),
        Color(255, 140, 0),
    ],
)

color_palette_greyscale = BoidFramePalette(
    name="Greyscale",
    background_color=Color(10, 10, 10),
    obstacle_color=Color(200, 200, 200),
    boid_palette=[
        Color(202,180,32),
        Color(170, 170, 170),
        Color(120, 120, 120),
        Color(80, 80, 80),
        Color(50, 50, 50),
        Color(220, 220, 220),
    ],
)

color_palette_icy = BoidFramePalette(
    name="Icy",
    background_color=Color(10, 10, 30),
    obstacle_color=Color(230, 230, 255),
    boid_palette=[
        Color(187, 222, 251),
        Color(144, 202, 249),
        Color(100, 181, 246),
        Color(130, 177, 255),
        Color(227, 242, 253),
    ],
)

color_palette_durag_activity = BoidFramePalette(
    name="Durag Activity",
    background_color=Color(40, 25, 25),
    obstacle_color=Color(188, 170, 164),
    boid_palette=[
        Color(121, 85, 72),
        Color(109, 76, 65),
        Color(93, 64, 55),
        Color(141, 110, 99),
    ],
)

color_palette_monochrome = BoidFramePalette(
    name="Monochrome",
    background_color=Color(0, 110, 0),
    obstacle_color=Color(0, 60, 0),
    boid_palette=[
        Color(0, 210, 40),
        Color(51, 255, 30),
        Color(20, 150, 0),
    ],
)

color_palette_terminal = BoidFramePalette(
    name="Terminal",
    background_color=Color(48, 10, 38),
    obstacle_color=Color(220, 220, 220),
    boid_palette=[
        Color(123, 154, 255),
        Color(231, 30, 216),
        Color(111, 208, 52),
    ],
)

color_palette_the_grand_budapest = BoidFramePalette(
    name="The Grand Budapest",
    background_color=Color(191, 124, 142),
    obstacle_color=Color(183, 17, 16),
    boid_palette=[
        Color(114, 148, 212),
        Color(198, 205, 247),
        Color(221, 126, 146),
        Color(246, 171, 178),
        Color(90, 44, 90),
    ],
)

color_palette_Microsoft = BoidFramePalette(
    name="Microsoft",
    background_color=Color(247, 247, 240),
    obstacle_color=Color(150, 150, 140),
    boid_palette=[
        Color(242, 80, 34),
        Color(127, 186, 0),
        Color(0, 164, 239),
        Color(255, 185, 0),
    ],
)

all_palettes = [
    color_palette_sand,
    color_palette_red_grey,
    color_palette_greyscale,
    color_palette_icy,
    color_palette_durag_activity,
    color_palette_monochrome,
    color_palette_terminal,
    color_palette_the_grand_budapest,
    color_palette_Microsoft,
]

# Get one of the above palettes randomly:
def get_random_color_palette():
    return random.choice(all_palettes)
