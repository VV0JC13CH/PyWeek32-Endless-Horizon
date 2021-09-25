"""
Example code showing how to create a button,
and the three ways to process button events.
"""
import arcade
import arcade.gui
import assets


class ViewSettings(arcade.View):
    def __init__(self):
        super().__init__()

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()

        # Set background color
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        screen_button = arcade.gui.UIFlatButton(text="Screen mode", width=200)
        self.v_box.add(screen_button.with_space_around(bottom=20))

        volume_up_button = arcade.gui.UIFlatButton(text="Sounds +", width=200)
        self.v_box.add(volume_up_button.with_space_around(bottom=20))

        volume_down_button = arcade.gui.UIFlatButton(text="Sounds -", width=200)
        self.v_box.add(volume_down_button.with_space_around(bottom=20))

        music_up_button = arcade.gui.UIFlatButton(text="Music +", width=200)
        self.v_box.add(music_up_button.with_space_around(bottom=20))

        music_down_button = arcade.gui.UIFlatButton(text="Music -", width=200)
        self.v_box.add(music_down_button.with_space_around(bottom=20))

        menu_button = arcade.gui.UIFlatButton(text="Back to menu", width=200)
        self.v_box.add(menu_button.with_space_around(bottom=20))

        # assign buttons:
        screen_button.on_click = self.on_click_screen
        volume_up_button.on_click = self.on_click_volume_up
        volume_down_button.on_click = self.on_click_volume_down
        music_up_button.on_click = self.on_click_music_up
        music_down_button.on_click = self.on_click_music_down
        menu_button.on_click = self.on_click_menu

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_click_screen(self, event):
        print("on_click_screen_button:", event)
        arcade.get_window().switch_screen_mode()

    def on_click_volume_up(self, event):
        print("on_click_volume_up_button:", event)
        self.window.change_volume_sounds()

    def on_click_volume_down(self, event):
        print("on_click_volume_down_button:", event)
        arcade.get_window().change_volume_sounds(add=False)

    def on_click_music_up(self, event):
        print("on_click_music_up_button:", event)
        arcade.get_window().change_volume_music()

    def on_click_music_down(self, event):
        print("on_click_music_down_button:", event)
        arcade.get_window().change_volume_music(add=False)

    def on_click_menu(self, event):
        print("on_click_menu_button:", event)
        arcade.get_window().show_view(arcade.get_window().view_menu)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(center_x=self.window.width / 2,
                                      center_y=self.window.height / 2,
                                      width=assets.bg_menu.width * self.window.height / assets.bg_menu.height,
                                      height=self.window.height,
                                      texture=assets.bg_menu)
        self.manager.draw()

    def on_show_view(self):
        # Registers handlers for GUI button clicks, etc.
        # We don't really use them in this example.
        self.manager.enable()
        self.window.set_mouse_visible(visible=True)


    def on_hide_view(self):
        # This unregisters the manager's UI handlers,
        # Handlers respond to GUI button clicks, etc.
        self.manager.disable()
