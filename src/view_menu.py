"""
Example code showing how to create a button,
and the three ways to process button events.
"""
import arcade
import arcade.gui
import assets


class ViewMenu(arcade.View):
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
        start_button = arcade.gui.UIFlatButton(text="New game", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))

        resume_button = arcade.gui.UIFlatButton(text="Resume game", width=200)
        self.v_box.add(resume_button.with_space_around(bottom=20))

        sandbox_button = arcade.gui.UIFlatButton(text="Sandbox", width=200)
        self.v_box.add(sandbox_button.with_space_around(bottom=20))

        settings_button = arcade.gui.UIFlatButton(text="Settings", width=200)
        self.v_box.add(settings_button.with_space_around(bottom=20))

        quit_button = arcade.gui.UIFlatButton(text="Quit", width=200)
        self.v_box.add(quit_button.with_space_around(bottom=20))

        # assign buttons:
        start_button.on_click = self.on_click_start
        resume_button.on_click = self.on_click_resume
        sandbox_button.on_click = self.on_click_sandbox
        settings_button.on_click = self.on_click_settings
        quit_button.on_click = self.on_click_quit

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_click_start(self, event):
        print("Start:", event)
        arcade.get_window().view_game.on_setup()
        arcade.get_window().show_view(arcade.get_window().view_game)

    def on_click_resume(self, event):
        print("Resume:", event)
        if not arcade.get_window().view_game.timer.game_hour_counter_started:
            arcade.get_window().view_game.on_setup()
        arcade.get_window().show_view(arcade.get_window().view_game)

    def on_click_sandbox(self, event):
        print("Sandbox:", event)
        arcade.get_window().view_game.on_setup(sandbox=True)
        arcade.get_window().show_view(arcade.get_window().view_game)

    def on_click_settings(self, event):
        print("Settings:", event)
        arcade.get_window().show_view(arcade.get_window().view_settings)

    def on_click_quit(self, event):
        print("Quit:", event)
        arcade.exit()

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(center_x=self.window.width / 2,
                                      center_y=self.window.height / 2,
                                      width=assets.bg_menu.width * self.window.height / assets.bg_menu.height,
                                      height=self.window.height,
                                      texture=assets.bg_menu)
        arcade.draw_text("Endless Horizon",
                         self.window.width // 2, self.window.height - 250,
                         arcade.color.BLACK, 80,
                         anchor_x="center")
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

