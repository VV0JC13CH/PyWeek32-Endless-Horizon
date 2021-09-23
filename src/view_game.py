"""
Rod of Madness
pyWeek 32 endless game
"""
import arcade
import pymunk
import timeit
import math
import os

import elements
import connection

SCREEN_TITLE = "Rod of Madness"

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

Right-click, fire coin

"""


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

        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

        # -- Pymunk
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -900.0)

        # Lists of sprites or lines
        self.sprite_list: arcade.SpriteList[elements.PhysicsSprite] = arcade.SpriteList()
        self.static_lines = []

        # Used for dragging shapes around with the mouse
        self.shape_being_dragged = None
        self.last_mouse_position = 0, 0

        self.processing_time_text = None
        self.draw_time = 0
        self.draw_time_text = None
        self.processing_time = 0

        self.draw_mode_text = None
        self.shape_1 = None
        self.shape_2 = None

        self.joints = []

        self.physics = "Normal"
        self.mode = "Make Crate"

        # Create the floor
        self.floor_height = 80
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Segment(body, [0, self.floor_height], [self.window.width, self.floor_height], 0.0)
        shape.friction = 10
        self.space.add(shape, body)
        self.static_lines.append(shape)

    def on_setup(self):
        pass

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Start timing how long this takes
        draw_start_time = timeit.default_timer()

        # Draw all the sprites
        self.sprite_list.draw()

        # Draw the lines that aren't sprites
        for line in self.static_lines:
            body = line.body

            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            arcade.draw_line(pv1.x, pv1.y, pv2.x, pv2.y, arcade.color.WHITE, 2)

        for joint in self.joints:
            color = arcade.color.WHITE
            if isinstance(joint, pymunk.DampedSpring):
                color = arcade.color.DARK_GREEN
            arcade.draw_line(joint.a.position.x, joint.a.position.y, joint.b.position.x, joint.b.position.y, color, 3)

        # arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)
        # Display timings
        output = f"Processing time: {self.processing_time:.3f}"
        arcade.draw_text(output, 20, self.window.height - 20, arcade.color.WHITE)

        output = f"Drawing time: {self.draw_time:.3f}"
        arcade.draw_text(output, 20, self.window.height - 40, arcade.color.WHITE)

        self.draw_time = timeit.default_timer() - draw_start_time

        output = f"Mode: {self.mode}"
        arcade.draw_text(output, 20, self.window.height - 60, arcade.color.WHITE)

        output = f"Physics: {self.physics}"
        arcade.draw_text(output, 20, self.window.height - 80, arcade.color.WHITE)

    def on_mouse_press(self, x, y, button, modifiers):

        if button == 1 and self.mode == "Drag":
            self.last_mouse_position = x, y
            self.shape_being_dragged = connection.get_shape(x, y, self.space)

        elif button == 1 and self.mode == "Make Crate":
            elements.make_crate(x, y, self.space, self.sprite_list)

        elif button == 1 and self.mode == "Make Ballon":
            elements.make_ballon(x, y, self.space, self.sprite_list)

        elif button == 1 and self.mode == "Make Connection by PinJoint":
            self.shape_1, self.shape_2 = connection.make_pin_joint_connection(x, y, self.space, self.joints,
                                                                              self.shape_1, self.shape_2)

        elif button == 1 and self.mode == "Make Connection by DampedSpring":
            self.shape_1, self.shape_2 = connection.make_damped_spring_connection(x, y, self.space, self.joints,
                                                                                  self.shape_1, self.shape_2)

        elif button == 4:
            elements.make_duck(x, y, self.space, self.sprite_list)

    def on_mouse_release(self, x, y, button, modifiers):
        if button == 1:
            # Release the item we are holding (if any)
            self.shape_being_dragged = None

    def on_mouse_motion(self, x, y, dx, dy):
        if self.shape_being_dragged is not None:
            # If we are holding an object, move it with the mouse
            self.last_mouse_position = x, y
            self.shape_being_dragged.shape.body.position = self.last_mouse_position
            self.shape_being_dragged.shape.body.velocity = dx * 20, dy * 20

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.F1:
            self.mode = "Drag"
        elif symbol == arcade.key.F2:
            self.mode = "Make Crate"
        elif symbol == arcade.key.F3:
            self.mode = "Make Ballon"

        elif symbol == arcade.key.F4:
            self.mode = "Make PinJoint"
        elif symbol == arcade.key.F5:
            self.mode = "Make DampedSpring"

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

    def on_update(self, delta_time):
        start_time = timeit.default_timer()

        # Check for sprites that are behind the screen
        for sprite in self.sprite_list:
            if sprite.pymunk_shape.body.position.x > self.window.width:
                # Remove balls from physics space
                self.space.remove(sprite.pymunk_shape, sprite.pymunk_shape.body)
                # Remove balls from physics list
                sprite.kill()

        # Update physics
        self.space.step(1 / 80.0)

        # If we are dragging an object, make sure it stays with the mouse. Otherwise
        # gravity will drag it down.
        if self.shape_being_dragged is not None:
            self.shape_being_dragged.shape.body.position = self.last_mouse_position
            self.shape_being_dragged.shape.body.velocity = 0, 0

        # Move sprites to where physics objects are
        for sprite in self.sprite_list:
            sprite.center_x = sprite.pymunk_shape.body.position.x
            sprite.center_y = sprite.pymunk_shape.body.position.y
            sprite.angle = math.degrees(sprite.pymunk_shape.body.angle)

        # Save the time it took to do this.
        self.processing_time = timeit.default_timer() - start_time
