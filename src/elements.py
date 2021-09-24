import arcade
import pymunk

import assets


def zero_gravity(body, gravity, damping, dt):
    pymunk.Body.update_velocity(body, (0,0), damping, dt)

# def make_duck(x, y, space, sprite_list):
#     # With right mouse button, shoot a heavy coin fast.
#     mass = 500
#     radius = 32
#     inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
#     body = pymunk.Body(mass, inertia)
#     body.position = x, y
#     # Speed of duck
#     body.velocity = -1200, 0
#     shape = pymunk.Circle(body, radius, pymunk.Vec2d(0, 0))
#     shape.friction = 0.3
#     # Make duck zero-gravity:
#     body.velocity_func = zero_gravity
#     space.add(body, shape)
#     sprite = CircleSprite(shape, "gfx/duck96x32_1.png")
#     sprite_list.append(sprite)


def make_duck(x, y, space, global_sprite_list, instance_sprite_list=None):
    # With right mouse button, shoot a heavy coin fast.
    if instance_sprite_list is None:
        instance_sprite_list = []
    size = 300
    mass = 1500000.0
    moment = pymunk.moment_for_box(mass, (size, size))
    body = pymunk.Body(mass, moment)
    body.position = pymunk.Vec2d(x, y)
    # Speed of duck
    body.velocity = -1200, 0
    shape = pymunk.Poly.create_box(body, (size, size))
    shape.friction = 0.3
    # Make duck zero-gravity:
    body.velocity_func = zero_gravity
    space.add(body, shape)
    sprite = AnimatedSprite(shape, textures=assets.duck_fly_textures, width=96, height=32)
    global_sprite_list.append(sprite)
    instance_sprite_list.append(sprite)


def make_ballon(x, y, space, global_sprite_list, instance_sprite_list=None):
    if instance_sprite_list is None:
        instance_sprite_list = []
    size = 20
    mass = 3.0
    moment = pymunk.moment_for_circle(mass, 0, size, (0, 0))
    body = pymunk.Body(mass, moment)
    body.position = pymunk.Vec2d(x, y)
    shape = pymunk.Circle(body, size, pymunk.Vec2d(0, 0))
    shape.friction = 0.3
    space.add(body, shape)
    sprite = CircleSprite(shape, texture=assets.crates_textures[2])
    global_sprite_list.append(sprite)
    instance_sprite_list.append(sprite)


def make_crate(x, y, space, global_sprite_list, instance_sprite_list=None):
    if instance_sprite_list is None:
        instance_sprite_list = []
    size = 32
    mass = 12.0
    moment = pymunk.moment_for_box(mass, (size, size))
    body = pymunk.Body(mass, moment)
    body.position = pymunk.Vec2d(x, y)
    shape = pymunk.Poly.create_box(body, (size, size))
    shape.friction = 0.3
    space.add(body, shape)
    sprite = CrateSprite(shape, texture=assets.crates_textures[3], width=size, height=size)
    global_sprite_list.append(sprite)
    instance_sprite_list.append(sprite)


class PhysicsSprite(arcade.Sprite):
    def __init__(self, pymunk_shape, texture):
        super().__init__(texture=texture, center_x=pymunk_shape.body.position.x, center_y=pymunk_shape.body.position.y)
        self.pymunk_shape = pymunk_shape


class CircleSprite(PhysicsSprite):
    def __init__(self, pymunk_shape, texture):
        super().__init__(pymunk_shape, texture)
        self.width = pymunk_shape.radius * 2
        self.height = pymunk_shape.radius * 2


class CrateSprite(PhysicsSprite):
    def __init__(self, pymunk_shape, texture, width, height):
        super().__init__(pymunk_shape, texture)
        self.width = width
        self.height = height


class AnimatedSprite(PhysicsSprite):
    def __init__(self, pymunk_shape, textures, width, height, anim_speed=10):
        super().__init__(pymunk_shape, textures[0])
        self.width = width
        self.height = height
        self.anim_speed = anim_speed
        self.anim_speed_counter = anim_speed
        for t in textures:
            self.textures.append(t)
