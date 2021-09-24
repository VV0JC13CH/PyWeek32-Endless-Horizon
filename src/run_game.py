"""
Endless Horizon

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.pymunk_joint_builder
"""
import arcade
import os

import assets
from view_game import ViewGame
from view_menu import ViewMenu
from view_settings import ViewSettings

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Endless Horizon"
SOUND = 7
MUSIC = 5


"""
Key bindings:

1 - Drag mode
2 - Make box mode
3 - Make PinJoint mode
4 - Make DampedSpring mode

S - No gravity or friction
L - Layout, no gravity, lots of friction
G - Gravity, little bit of friction

Right-click, fire coin

"""


class GlobalWindow(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True, fullscreen=True)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # views:
        self.view_game = None
        self.view_menu = None
        self.view_settings = None

        # sound
        self.sounds = SOUND
        self.music = MUSIC

    def setup(self):

        # views:
        self.view_game = ViewGame()
        self.view_menu = ViewMenu()
        self.view_settings = ViewSettings()

        # background
        self.background_color = assets.backgrounds[0]

    def on_resize(self, width, height):
        """ This method is automatically called when the window is resized. """

        # Call the parent. Failing to do this will mess up the coordinates, and default to 0,0 at the center and the
        # edges being -1 to 1.
        super().on_resize(width, height)
        print(f"Window resized to: {width}, {height}")

    def switch_screen_mode(self):
        # User hits f. Flip between full and not full screen.
        self.set_fullscreen(not self.fullscreen)

        # Get the window coordinates. Match viewport to window coordinates
        # so there is a one-to-one mapping.
        width, height = self.get_size()
        self.set_viewport(0, width, 0, height)
        print(f"Window resized to: {width}, {height}")

    def change_volume_sounds(self, add=True):
        if add and self.sounds < 10:
            self.sounds += 1
        if not add and self.sounds > 0:
            self.sounds -= 1
        print(f"Volume of sounds: {self.sounds}")

    def change_volume_music(self, add=True):
        if add and self.music < 10:
            self.music += 1
        if not add and self.music > 0:
            self.music -= 1
        print(f"Volume of sounds: {self.music}")

    def go_to_menu(self):
        arcade.get_window().view_menu.manager.enable()
        self.show_view(self.view_menu)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.F9:
            self.switch_screen_mode()
        if key == arcade.key.ESCAPE:
            self.go_to_menu()


window = GlobalWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.setup()
window.show_view(window.view_menu)
arcade.run()