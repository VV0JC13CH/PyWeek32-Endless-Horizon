"""
Example code showing how to create a button,
and the three ways to process button events.
"""
import arcade
import assets


class ViewVictory(arcade.View):
    def __init__(self):
        super().__init__()

        # Set background color
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    def on_draw(self):
        arcade.draw_texture_rectangle(center_x=self.window.width /2,
                                      center_y=self.window.height/2,
                                      width=assets.bg_victory.width * self.window.height/assets.bg_victory.height,
                                      height=self.window.height,
                                      texture=assets.bg_victory)
        arcade.draw_text("VICTORY",
                         self.window.width // 2, self.window.height - 150,
                         arcade.color.BLACK, 80,
                         anchor_x="center")

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.window.view_menu)
        elif symbol == arcade.key.ENTER:
            self.window.show_view(self.window.view_menu)
        elif symbol == arcade.key.SPACE:
            self.window.show_view(self.window.view_menu)



