"""
Example code showing how to create a button,
and the three ways to process button events.
"""
import arcade
import arcade.gui


class ViewMenu(arcade.View):
    def __init__(self):
        super().__init__()

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Set background color
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        start_button = arcade.gui.UIFlatButton(text="New game", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))

        resume_button = arcade.gui.UIFlatButton(text="Resume game", width=200)
        self.v_box.add(resume_button.with_space_around(bottom=20))

        scores_button = arcade.gui.UIFlatButton(text="Leaderboards", width=200)
        self.v_box.add(scores_button.with_space_around(bottom=20))

        settings_button = arcade.gui.UIFlatButton(text="Settings", width=200)
        self.v_box.add(settings_button.with_space_around(bottom=20))

        quit_button = arcade.gui.UIFlatButton(text="Quit", width=200)
        self.v_box.add(quit_button.with_space_around(bottom=20))

        # assign buttons:
        start_button.on_click = self.on_click_start
        resume_button.on_click = self.on_click_resume
        scores_button.on_click = self.on_click_scores
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
        self.manager.disable()
        arcade.get_window().view_game.on_setup()
        arcade.get_window().show_view(arcade.get_window().view_game)

    def on_click_resume(self, event):
        print("Resume:", event)
        self.manager.disable()
        if not arcade.get_window().view_game.timer.game_hour_counter_started:
            arcade.get_window().view_game.on_setup()
        arcade.get_window().show_view(arcade.get_window().view_game)

    def on_click_scores(self, event):
        self.manager.disable()
        print("Scores:", event)

    def on_click_settings(self, event):
        print("Settings:", event)
        self.manager.disable()
        arcade.get_window().view_settings.manager.enable()
        arcade.get_window().show_view(arcade.get_window().view_settings)

    def on_click_quit(self, event):
        print("Quit:", event)
        arcade.exit()

    def on_draw(self):
        arcade.start_render()
        self.manager.draw()