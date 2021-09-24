import arcade
import assets


def change_sky(game_hour):
    arcade.set_background_color(assets.backgrounds[game_hour])