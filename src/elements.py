import arcade
import pymunk


def make_duck(x, y, space, sprite_list):
    # With right mouse button, shoot a heavy coin fast.
    mass = 500
    radius = 10
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
    body = pymunk.Body(mass, inertia)
    body.position = x, y
    # Speed of duck
    body.velocity = -1200, 0
    shape = pymunk.Circle(body, radius, pymunk.Vec2d(0, 0))
    shape.friction = 0.3
    # Make duck zero-gravity:
    body.velocity_func = (body, space.gravity, space.damping)
    space.add(body, shape)
    sprite = CircleSprite(shape, ":resources:images/items/coinGold.png")
    sprite_list.append(sprite)

def make_ballon(x, y, space, sprite_list):
    size = 20
    mass = 3.0
    moment = pymunk.moment_for_circle(mass, 0, size, (0, 0))
    body = pymunk.Body(mass, moment)
    body.position = pymunk.Vec2d(x, y)
    shape = pymunk.Circle(body, size, pymunk.Vec2d(0, 0))
    shape.friction = 0.3
    space.add(body, shape)
    sprite = CircleSprite(shape, ":resources:images/items/coinGold.png")
    sprite_list.append(sprite)


def make_crate(x, y, space, sprite_list):
    size = 45
    mass = 12.0
    moment = pymunk.moment_for_box(mass, (size, size))
    body = pymunk.Body(mass, moment)
    body.position = pymunk.Vec2d(x, y)
    shape = pymunk.Poly.create_box(body, (size, size))
    shape.friction = 0.3
    space.add(body, shape)
    sprite = CrateSprite(shape, ":resources:images/tiles/boxCrate_double.png", width=size, height=size)
    sprite_list.append(sprite)


class PhysicsSprite(arcade.Sprite):
    def __init__(self, pymunk_shape, filename):
        super().__init__(filename, center_x=pymunk_shape.body.position.x, center_y=pymunk_shape.body.position.y)
        self.pymunk_shape = pymunk_shape


class CircleSprite(PhysicsSprite):
    def __init__(self, pymunk_shape, filename):
        super().__init__(pymunk_shape, filename)
        self.width = pymunk_shape.radius * 2
        self.height = pymunk_shape.radius * 2


class CrateSprite(PhysicsSprite):
    def __init__(self, pymunk_shape, filename, width, height):
        super().__init__(pymunk_shape, filename)
        self.width = width
        self.height = height


