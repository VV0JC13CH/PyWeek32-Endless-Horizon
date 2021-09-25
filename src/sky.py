import arcade
import assets


def setup_clouds(sprite_list):
    cloud = assets.clouds_sprite
    cloud.center_y = 300
    cloud.scale = 2
    sprite_list.append(cloud)


def change_clouds(sprite_list, game_hour, window, camera):
    cloud = sprite_list[0]
    cloud.center_x = window.width / 2.5 + camera.position[0]
    cloud.texture = cloud.textures[game_hour]


def change_sky(game_hour):
    arcade.set_background_color(assets.backgrounds[game_hour])