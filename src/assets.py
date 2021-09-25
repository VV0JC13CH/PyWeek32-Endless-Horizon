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

sea_textures = [arcade.load_texture(path_to_string('gfx', 'sea96x64.png'), width=96, height=64)]

#
ground_texture = arcade.load_texture(path_to_string('gfx', 'ground288x64.png'), width=288, height=64)
bridge_texture = arcade.load_texture(path_to_string('gfx', 'bridge416x64.png'), width=416, height=64)

# Fisher from head to shoes:
fisher_head_texture = arcade.load_texture(path_to_string('gfx', 'fisher_head32x32.png'), width=32, height=32)
fisher_arm_texture = arcade.load_texture(path_to_string('gfx', 'fisher_arm32x32.png'), width=32, height=32)
fisher_body_texture = arcade.load_texture(path_to_string('gfx', 'fisher_body66x58.png'), width=66, height=58)

fisher_dynamic_textures = [
    arcade.load_texture(path_to_string('gfx', 'fisher_player1.png'), width=68, height=78),
    arcade.load_texture(path_to_string('gfx', 'fisher_player2.png'), width=68, height=78)
]
fisher_dynamic_sprite = arcade.Sprite(texture=fisher_dynamic_textures[0])
fisher_dynamic_sprite.textures = fisher_dynamic_textures

# Static fisher:
fisher_static_textures = []
for x in range(1,19,1):
    texture = arcade.load_texture(path_to_string("gfx", "fisher_static"+str(x)+".png"))
    fisher_static_textures.append(texture)
fisher_static_sprite = arcade.Sprite(texture=fisher_static_textures[0])
fisher_static_sprite.textures = fisher_static_textures

# Clouds:
clouds_textures = []
for x in range(1,6,1):
    for y in range(1,6,1):
        texture = arcade.load_texture(path_to_string("gfx", "clouds"+str(y)+".png"))
        clouds_textures.append(texture)
clouds_sprite = arcade.Sprite(texture=clouds_textures[0])
clouds_sprite.textures = clouds_textures

# Pallet: https://colorswall.com/palette/24326/
# Each index means another game_cycle aka hours
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

# Progress bar related textures:
progress_bar_texture = arcade.load_texture(path_to_string("gfx", "progress_bar300x60.png"))
progress_bar_fill_texture = arcade.load_texture(path_to_string("gfx", "progress_bar_fill270x30.png"))

mini_island_sprite = arcade.Sprite()
mini_island_texture_1 = arcade.load_texture(path_to_string("gfx", "island1.png"))
mini_island_texture_2 = arcade.load_texture(path_to_string("gfx", "island2.png"))
mini_island_texture_3 = arcade.load_texture(path_to_string("gfx", "island3.png"))
mini_island_texture_4 = arcade.load_texture(path_to_string("gfx", "island4.png"))
mini_island_texture_5 = arcade.load_texture(path_to_string("gfx", "island5.png"))
mini_island_texture_6 = arcade.load_texture(path_to_string("gfx", "island6.png"))

mini_island_sprite.textures = [mini_island_texture_1,
                               mini_island_texture_2,
                               mini_island_texture_3,
                               mini_island_texture_4,
                               mini_island_texture_5,
                               mini_island_texture_6]

log_texture = arcade.load_texture(path_to_string("gfx", "log16x32.png"), width=16, height=32)

# music
house_music_path = path_to_string("sfx", "house_loop.wav")
