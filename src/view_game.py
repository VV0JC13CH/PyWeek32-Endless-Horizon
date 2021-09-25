"""
Rod of Madness
pyWeek 32 endless game
"""
import arcade
import pymunk
import timeit
import timer
import math
import os

import elements
import connection
import fisher
import sky

SCREEN_TITLE = "Endless Horizon"

"""
Key bindings:

F1 - Drag mode
F2 - Make crate mode
F3 - Make baloon mode
F4 - Make PinJoint mode
F5 - Make DampedSpring mode

F6 - No gravity or friction
F7 - Layout, no gravity, lots of friction
F8 - Gravity, little bit of friction
F9 - Fullscreen on/off
F12- Developer mode

Right-click, fire duck

"""

# How fast the camera pans to the player. 1.0 is instant.
CAMERA_SPEED = 0.2


class ViewGame(arcade.View):
    """ Main application class. """

    def __init__(self):
        super().__init__()

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # -- Pymunk
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -900.0)

        # Lists of sprites or lines
        self.sprite_list_pymunk = None
        self.sprite_list_pymunk_static = None
        self.sprite_list_static = None
        self.sprite_list_sea = None
        self.sprite_list_clouds = None
        self.sprite_list_progress_bar = None
        self.static_lines_pymunk = []
        self.floor_height = 0
        self.bridge_position = (0.0, 0.0)

        self.victory = False
        self.game_over = False

        #
        self.progress = 0

        # Camera
        self.viewport_margin = 0
        self.camera_sprites = arcade.Camera(self.window.width, self.window.height)
        self.camera_gui = arcade.Camera(self.window.width, self.window.height)

        # Set the viewport boundaries
        # These numbers set where we have 'scrolled' to.
        self.view_left = 0
        self.view_bottom = 0

        # Used for dragging shapes around with the mouse
        self.shape_being_dragged = None
        self.last_mouse_position = 0, 0

        self.player_dragged = None
        self.force_position = 0, 0

        self.processing_time_text = None
        self.draw_time = 0
        self.draw_time_text = None
        self.processing_time = 0

        self.draw_mode_text = None
        self.shape_1 = None
        self.shape_2 = None

        self.joints = []

        self.game_started = False

        self.mode_developer = False
        self.physics = "Normal"
        self.mode = "Make Crate"

        # Timer
        self.timer = timer.Timer()

        # Player
        self.fisher = fisher.Fisher()
        self.private_duck_list = None

    def on_setup(self, sandbox=False):
        self.mode_developer = sandbox
        self.game_started = False
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -900.0)
        self.sprite_list_pymunk: arcade.SpriteList[elements.PhysicsSprite] = arcade.SpriteList()
        self.sprite_list_pymunk_static = arcade.SpriteList()
        self.sprite_list_static = arcade.SpriteList()
        self.sprite_list_sea = arcade.SpriteList()
        elements.make_ground(self.sprite_list_static, self.window)
        self.sprite_list_progress_bar = arcade.SpriteList()
        self.bridge_position = elements.make_bridge(self.sprite_list_static, self.window, self.space)

        self.player_dragged = self.fisher

        self.static_lines_pymunk = []

        self.victory = False
        self.game_over = False

        # Timer
        self.timer.on_setup()
        # Camera
        self.camera_sprites = arcade.Camera(self.window.width, self.window.height)
        self.camera_gui = arcade.Camera(self.window.width, self.window.height)
        if self.window.fullscreen:
            self.viewport_margin = 200
        else:
            self.viewport_margin = 100

        # Set the viewport boundaries
        # These numbers set where we have 'scrolled' to.
        self.view_left = 0
        self.view_bottom = 0

        self.progress = 1

        # Clouds
        self.sprite_list_clouds = arcade.SpriteList()
        sky.setup_clouds(self.sprite_list_clouds)

        # Setup sea:
        elements.setup_sea(self.window, self.space,
                           self.sprite_list_sea, self.static_lines_pymunk)

        # Setup player:
        self.fisher.on_setup(bridge_x=self.bridge_position[0],
                             bridge_y=self.bridge_position[1],
                             space=self.space)
        self.private_duck_list = arcade.SpriteList()

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Start timing how long this takes
        draw_start_time = timeit.default_timer()

        # Select the (unscrolled) camera for our GUI
        self.camera_sprites.use()

        # Draw clouds:
        self.sprite_list_clouds.draw()

        # Draw player
        self.fisher.on_draw()

        # Draw all the sprites
        self.sprite_list_pymunk.draw()
        self.sprite_list_pymunk_static.draw()
        self.sprite_list_sea.draw()

        # Draw the lines that aren't sprites
        for line in self.static_lines_pymunk:
            body = line.body

            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            arcade.draw_line(pv1.x, pv1.y, pv2.x, pv2.y, arcade.color.LIGHT_SKY_BLUE, 2)

        # Draw f.e. ground:
        self.sprite_list_static.draw()

        if self.mode_developer:
            for joint in self.joints:
                color = arcade.color.WHITE
                if isinstance(joint, pymunk.DampedSpring):
                    color = arcade.color.DARK_GREEN
                arcade.draw_line(joint.a.position.x, joint.a.position.y, joint.b.position.x, joint.b.position.y, color,
                                 3)

        # GUI BELOW:
        # Select the (unscrolled) camera for our GUI
        self.camera_gui.use()
        self.sprite_list_progress_bar.draw()
        elements.draw_progress_bar(self.fisher, self.window, self.progress)

        # Display timings
        if self.mode_developer:
            # Camera
            output = f"Processing time: {self.processing_time:.3f}"
            arcade.draw_text(output, 20, self.window.height - 20, arcade.color.SILVER)
            output = f"Drawing time: {self.draw_time:.3f}"
            arcade.draw_text(output, 20, self.window.height - 40, arcade.color.SILVER)
            self.draw_time = timeit.default_timer() - draw_start_time
            output = f"Mode: {self.mode}"
            arcade.draw_text(output, 20, self.window.height - 60, arcade.color.SILVER)
            output = f"Physics: {self.physics}"
            arcade.draw_text(output, 20, self.window.height - 80, arcade.color.SILVER)
            # Draw the GUI
            arcade.draw_rectangle_filled(self.window.width // 2, 20, self.window.width, 40, arcade.color.ALMOND)
            text = f"Camera position: ({self.camera_sprites.position[0]:5.1f}, {self.camera_sprites.position[1]:5.1f})"
            arcade.draw_text(text, 10, 10, arcade.color.BLACK_BEAN, 20)

            # Draw the box that we work to make sure the user stays inside of.
            # This is just for illustration purposes. You'd want to remove this
            # in your game.
            left_boundary = self.viewport_margin
            right_boundary = self.window.width - self.viewport_margin
            top_boundary = self.window.height - self.viewport_margin
            bottom_boundary = self.viewport_margin
            arcade.draw_lrtb_rectangle_outline(left_boundary, right_boundary, top_boundary, bottom_boundary,
                                               arcade.color.GREEN, 2)

        self.timer.on_draw(self.window.width // 2, self.window.height - 80)

    def on_mouse_press(self, x, y, button, modifiers):

        if button == 1 and self.mode == "Drag":
            self.last_mouse_position = x + self.camera_sprites.position[0], y + self.camera_sprites.position[1],
            self.shape_being_dragged = connection.get_shape(
                x + self.camera_sprites.position[0], y + self.camera_sprites.position[1], self.space)

        elif button == 1 and self.mode == "Make Crate":
            elements.make_crate(x + self.camera_sprites.position[0],
                                y + self.camera_sprites.position[1],
                                self.space, self.sprite_list_pymunk)

        elif button == 1 and self.mode == "Make Ballon":
            elements.make_ballon(x + self.camera_sprites.position[0],
                                 y + self.camera_sprites.position[1],
                                 self.space, self.sprite_list_pymunk)

        elif button == 1 and self.mode == "Make Connection by PinJoint":
            self.shape_1, self.shape_2 = connection.make_pin_joint_connection(x + self.camera_sprites.position[0],
                                                                              y + self.camera_sprites.position[1],
                                                                              self.space, self.joints,
                                                                              self.shape_1, self.shape_2)

        elif button == 1 and self.mode == "Make Connection by DampedSpring":
            self.shape_1, self.shape_2 = connection.make_damped_spring_connection(x + self.camera_sprites.position[0],
                                                                                  y + self.camera_sprites.position[1],
                                                                                  self.space, self.joints,
                                                                                  self.shape_1, self.shape_2)

        elif button == 4 and self.mode_developer:
            elements.make_duck(x + self.camera_sprites.position[0],
                               y + self.camera_sprites.position[1],
                               self.space, self.sprite_list_pymunk,
                               self.window)

    def on_mouse_release(self, x, y, button, modifiers):
        if button == 1:
            # Release the item we are holding (if any)
            self.shape_being_dragged = None

    def on_mouse_motion(self, x, y, dx, dy):
        if self.shape_being_dragged is not None:
            # If we are holding an object, move it with the mouse
            self.last_mouse_position = x + self.camera_sprites.position[0], y + self.camera_sprites.position[1]
            self.shape_being_dragged.shape.body.position = self.last_mouse_position
            self.shape_being_dragged.shape.body.velocity = dx * 20, dy * 20

    def on_key_press(self, symbol: int, modifiers: int):
        if self.mode_developer:
            if symbol == arcade.key.F1:
                self.mode = "Drag"
            elif symbol == arcade.key.F2:
                self.mode = "Make Crate"
            elif symbol == arcade.key.F3:
                self.mode = "Make Ballon"
            elif symbol == arcade.key.F4:
                self.mode = "Make Connection by PinJoint"
            elif symbol == arcade.key.F5:
                self.mode = "Make Connection by DampedSpring"
            elif symbol == arcade.key.F6:
                self.space.gravity = (0.0, 0.0)
                self.space.damping = 1
                self.physics = "Space gravity"
            elif symbol == arcade.key.F7:
                self.space.gravity = (0.0, 0.0)
                self.space.damping = 0
                self.physics = "Freeze gravity"
            elif symbol == arcade.key.F8:
                self.space.damping = 0.95
                self.space.gravity = (0.0, -900.0)
                self.physics = "Normal gravity"
        if symbol == arcade.key.F12:
            self.mode_developer = not self.mode_developer
            if not self.mode_developer:
                self.mode = "Play"
            else:
                self.mode = "Drag"
            print("Developer mode:", self.mode_developer)
        elif symbol == arcade.key.SPACE:
            if not self.game_started:
                self.game_started = True
                self.timer.start()
                elements.make_duck(self.window.width-self.viewport_margin, self.window.height * 0.75, self.space,
                                   self.sprite_list_pymunk, self.private_duck_list, self.window)
                self.fisher.start(duck=self.private_duck_list, space=self.space, joints=self.joints)
                # Setup progress bar
                elements.setup_progress_bar(self.sprite_list_progress_bar)
                print("Game started!")
        elif symbol == arcade.key.UP:
            pass
        elif symbol == arcade.key.DOWN:
            pass
        elif symbol == arcade.key.LEFT:
            pass
        elif symbol == arcade.key.RIGHT:
            pass

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            pass
        elif symbol == arcade.key.DOWN:
            pass
        elif symbol == arcade.key.LEFT:
            pass
        elif symbol == arcade.key.RIGHT:
            pass

    def on_update(self, delta_time):
        start_time = timeit.default_timer()

        # Check for sprites that are behind the screen
        for sprite in self.sprite_list_pymunk:
            if sprite.pymunk_shape.body.position.x > self.camera_sprites.position[0] + self.window.width:
                elements.kill_old_instances(sprite, self.space)
        # Same for lines
        for sprite in self.sprite_list_pymunk_static:
            if sprite.pymunk_shape.body.position.x > self.camera_sprites.position[0] + self.window.width:
                elements.kill_old_instances(sprite, self.space)

        # Sea chunks updates:
        for sprite in self.sprite_list_sea:
            if sprite.center_x >= self.camera_sprites.position[0] + self.window.width * 2 + sprite.width:
                elements.update_sea(sprite, self.window, self.space, self.camera_sprites)
        # Update physics
        self.space.step(1 / 80.0)

        # If we are dragging an object, make sure it stays with the mouse. Otherwise
        # gravity will drag it down.
        if self.shape_being_dragged is not None:
            self.shape_being_dragged.shape.body.position = self.last_mouse_position
            self.shape_being_dragged.shape.body.velocity = 0, 0

        self.fisher.during_update(self.window)
        if self.game_started and len(self.sprite_list_pymunk) > 0:
            self.scroll_to_player(self.sprite_list_pymunk[0])

        # Move sprites to where physics objects are
        for sprite in self.sprite_list_pymunk:
            sprite.center_x = sprite.pymunk_shape.body.position.x
            sprite.center_y = sprite.pymunk_shape.body.position.y
            sprite.angle = math.degrees(sprite.pymunk_shape.body.angle)
            if len(sprite.textures) > 1:
                sprite.anim_speed_counter -= 1
                if sprite.anim_speed_counter == 0:
                    if sprite.cur_texture_index == len(sprite.textures) - 1:
                        sprite.cur_texture_index = 0
                    else:
                        sprite.cur_texture_index += 1
                elif sprite.anim_speed_counter < 0:
                    sprite.anim_speed_counter = sprite.anim_speed
                sprite.texture = sprite.textures[sprite.cur_texture_index]
        sky.change_sky(self.timer.game_hour)
        sky.change_clouds(self.sprite_list_clouds, self.timer.game_hour, self.window, self.camera_sprites)
        elements.update_progress_bar(self.progress)

        # Save the time it took to do this.
        self.timer.on_update(delta_time)
        if self.camera_sprites.position[0] < 0:
            self.progress = (5333333 + self.camera_sprites.position[0]) / 5333333

        if self.progress < 0.1:
            self.victory = True
        if self.victory and self.progress < 0.0:
            self.window.show_view(self.window.view_victory)

        self.processing_time = timeit.default_timer() - start_time

    def scroll_to_player(self, target_sprite):
        """
        if CAMERA_SPEED is 1, the camera will immediately move to the desired position.
        """

        # --- Manage Scrolling ---

        # Scroll left
        left_boundary = self.view_left + self.viewport_margin
        if target_sprite.left < left_boundary:
            self.view_left -= left_boundary - target_sprite.left

        # Scroll right
        right_boundary = self.view_left + self.window.width - self.viewport_margin
        if target_sprite.right > right_boundary:
            self.view_left += target_sprite.right - right_boundary

        # Scroll up
        top_boundary = self.view_bottom + self.window.height - self.viewport_margin
        if target_sprite.top > top_boundary:
            self.view_bottom += target_sprite.top - top_boundary

        # Scroll down
        bottom_boundary = self.view_bottom + self.viewport_margin
        if target_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - target_sprite.bottom

        # Scroll to the proper location
        position = self.view_left, self.view_bottom
        self.camera_sprites.move_to(position, CAMERA_SPEED)

    def on_resize(self, width, height):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        self.camera_sprites.resize(int(width), int(height))
        self.camera_gui.resize(int(width), int(height))
