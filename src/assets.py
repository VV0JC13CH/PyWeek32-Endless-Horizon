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