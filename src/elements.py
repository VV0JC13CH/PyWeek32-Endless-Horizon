import arcade
import pymunk

import assets


def zero_gravity(body, gravity, damping, dt):
    pymunk.Body.update_velocity(body, (0, 0), damping, dt)


def make_duck(x, y, space, global_sprite_list, instance_sprite_list=None, window=None, velocity=0):
    # With right mouse button, shoot a heavy coin fast.
    if instance_sprite_list is None:
        instance_sprite_list = []
    size = 96
    mass = 999999999.0
    moment = pymunk.moment_for_box(mass, (size, size))
    body = pymunk.Body(mass, moment)
    body.position = pymunk.Vec2d(x, y)
    # Speed of duck
    if window is not None and velocity == 0:
        if window.fullscreen:
            body.velocity = -1800, 0
        if not window.fullscreen:
            body.velocity = -1700, 0
    elif velocity != 0:
        body.velocity = velocity, 0
    else:
        body.velocity = -1800, 0
    shape = pymunk.Poly.create_box(body, (size, size))
    shape.friction = 0.3
    # Make duck zero-gravity:
    body.velocity_func = zero_gravity
    space.add(body, shape)
    sprite = AnimatedSprite(shape, textures=assets.duck_fly_textures, width=96, height=32)
    global_sprite_list.append(sprite)
    instance_sprite_list.append(sprite)


def make_ballon(x, y, space, global_sprite_list, instance_sprite_list=None):
    # It should be baloon, but it's just next crate
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


def setup_sea(window, space, global_sprite_sea_list, global_static_lines_list):
    # Create the chunks of sea
    image_width = assets.sea_textures[0].width
    sea_chunks_req = int(window.width * 3 / image_width)
    for i in range(0, sea_chunks_req):
        pos_x = window.width - (i * image_width + image_width) + image_width * 2
        sprite = arcade.Sprite(texture=assets.sea_textures[0], center_x=pos_x + image_width / 2,
                               center_y=assets.sea_textures[0].height / 2)
        global_sprite_sea_list.append(sprite)
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    # 5333333 - level width (1h of playing)
    shape = pymunk.Segment(body, (-5333333, sprite.height), (window.width * 4, sprite.height), 0.0)
    shape.friction = 10
    space.add(shape, body)
    global_static_lines_list.append(shape)


def update_sea(sprite, window, space, camera):
    # Moving sprites to left:
    sea_chunks_req = int(window.width * 3 / sprite.width)
    pos_x = sea_chunks_req * sprite.width
    sprite.center_x -= pos_x

    # Generator of static lines:
    # body = pymunk.Body(body_type=pymunk.Body.STATIC)
    # shape = pymunk.Segment(body, (sprite.center_x, sprite.height), (sprite.center_x + sprite.width, sprite.height), 0.0)
    # shape.friction = 10
    # space.add(shape, body)
    # global_static_lines_list.append(shape)


def kill_old_instances(sprite, space):
    # Remove sprites from physics space
    space.remove(sprite.pymunk_shape, sprite.pymunk_shape.body)
    # Remove sprites from physics list
    sprite.kill()


def make_bridge(sprite_list, window, space):
    # Sprite
    bridge = arcade.Sprite(texture=assets.bridge_texture)
    bridge.center_x = window.width - bridge.width * 2
    bridge.center_y = bridge.height * 1.5
    sprite_list.append(bridge)
    # Physic_line
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape = pymunk.Segment(body, (bridge.center_x - bridge.width / 2, bridge.center_y + bridge.height / 6),
                           (bridge.center_x + bridge.width / 2, bridge.center_y + bridge.height / 6), 0.0)
    shape.friction = 10
    space.add(shape, body)
    return bridge.center_x - bridge.width / 2, bridge.center_y + bridge.height


def make_ground(sprite_list, window):
    for i in range(0, 3):
        ground = arcade.Sprite(texture=assets.ground_texture)
        ground.center_x = window.width - ground.width * i
        ground.center_y = 0 + ground.height / 2
        sprite_list.append(ground)
    for i in range(0, 200):
        ground = arcade.Sprite(texture=assets.ground_texture)
        # game is over after -5333333 (its end of level)
        ground.center_x = -5333333 - ground.width * i
        ground.center_y = 0 + ground.height / 2
        sprite_list.append(ground)


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


def setup_progress_bar(sprite_list_progress_bar):
    sprite_list_progress_bar.append(sprite=assets.mini_island_sprite)


def draw_progress_bar(fisher, window, progress):
    if fisher.connected_to_duck:
        arcade.draw_texture_rectangle(center_x=window.width / 2 - (540 - progress * 540) + (270 - progress * 270),
                                      center_y=window.height - 60,
                                      width=540 * progress,
                                      height=30,
                                      texture=assets.progress_bar_fill_texture)
        arcade.draw_texture_rectangle(center_x=window.width / 2,
                                      center_y=window.height - 60,
                                      width=600,
                                      height=60,
                                      texture=assets.progress_bar_texture)
        arcade.draw_texture_rectangle(center_x=window.width / 2 - 265 + progress * 265 * 2,
                                      center_y=window.height - 60,
                                      width=32,
                                      height=64,
                                      texture=assets.log_texture
                                      )
        sprite = assets.mini_island_sprite
        sprite.center_x = window.width / 2 - 350
        sprite.center_y = window.height - 60


def update_progress_bar(progress):
    sprite = assets.mini_island_sprite
    max_index = 6
    if sprite.cur_texture_index < max_index - 1:
        sprite.cur_texture_index += 0.1
    else:
        sprite.cur_texture_index = 0
    sprite.texture = sprite.textures[int(sprite.cur_texture_index)]


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
