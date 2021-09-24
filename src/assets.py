import arcade
# we love Windows users:
from pathlib import Path


def path_to_string(directory, file):
    return str(Path.cwd().joinpath(directory, file).resolve())


duck_fly_textures = [arcade.load_texture(path_to_string('gfx', 'duck96x32_1.png')),
                     arcade.load_texture(path_to_string('gfx', 'duck96x32_2.png')),
                     arcade.load_texture(path_to_string('gfx', 'duck96x32_3.png'))]

crates_textures = [arcade.load_texture(path_to_string('gfx', 'crate16x16a.png'), width=16, height=16),
                   arcade.load_texture(path_to_string('gfx', 'crate16x16b.png'), width=16, height=16),
                   arcade.load_texture(path_to_string('gfx', 'crate16x16c.png'), width=16, height=16),
                   arcade.load_texture(path_to_string('gfx', 'crate32x32.png'), width=32, height=32)]

# Pallet: https://colorswall.com/palette/24326/
backgrounds = [
    (225, 245, 254),
    (179, 229, 252),
    (129, 212, 250),
    (79, 195, 247),
    (41, 182, 246),
    (0, 172, 230),
    (0, 153, 204),
    (0, 153, 204),
    (0, 153, 204),
    (0, 134, 179),
    (0, 134, 179),
    (0, 115, 153),
    (0, 115, 153),
    (0, 96, 128),
    (0, 96, 128),
    (0, 76, 102),
    (0, 76, 102),
    (0, 57, 77),
    (0, 57, 77),
    (0, 57, 77),
    (0, 38, 51),
    (0, 38, 51),
    (0, 38, 51),
    (0, 19, 25),
    (0, 19, 25),
    (0, 19, 25)
]
