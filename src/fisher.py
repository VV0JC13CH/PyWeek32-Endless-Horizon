import arcade
import pymunk
import assets


class Fisher(arcade.SpriteList):
    def __init__(self):
        super().__init__()
        self.position = (0, 0)
        self.space = None
        self.sprite_dynamic = arcade.Sprite()
        self.sprite_static = arcade.Sprite()
        self.game_started = False
        self.static_animations_finished = False
        self.dynamic_animations_started = False
        self.connected_to_duck = False

        self.private_duck = None
        self.space = None
        self.joints = None

        self.anim_speed = 0
        self.anim_speed_counter = 0

        self.rod_angle = 45
        self.shape = None

    def on_setup(self, bridge_x, bridge_y, space, anim_speed=20):
        for sprite in self:
            sprite.kill()
        self.position = bridge_x, bridge_y
        self.space = space
        self.sprite_static = assets.fisher_static_sprite
        self.sprite_static.position = self.position[0], self.position[1] + self.sprite_static.height / 4
        self.sprite_dynamic = assets.fisher_dynamic_sprite
        # Somewhere outside screen:
        self.sprite_dynamic.center_y = -200

        self.anim_speed = anim_speed
        self.anim_speed_counter = anim_speed
        self.sprite_static.cur_texture_index = 0
        self.append(self.sprite_static)
        self.game_started = False
        self.static_animations_finished = False
        self.dynamic_animations_started = False
        self.connected_to_duck = False

    def start(self, duck, space, joints):
        self.game_started = True
        self.private_duck = duck
        self.space = space
        self.joints = joints

    def on_draw(self):
        if self.connected_to_duck:
            arcade.draw_line(self.private_duck[0].center_x,
                             self.private_duck[0].center_y,
                             (self.sprite_dynamic.center_x - 23),
                             (self.sprite_dynamic.center_y + 23),
                             arcade.color.SILVER,
                             4)
        self.draw()

    def during_update(self, window):
        if self.game_started and not self.static_animations_finished:
            # Move static sprites from texture 3-19 before launch of game
            for sprite in self:
                self.anim_speed = 4
                self.anim_speed_counter -= 1
                if self.anim_speed_counter == 0:
                    if sprite.cur_texture_index in range(0,1):
                        sprite.cur_texture_index = 3
                    elif sprite.cur_texture_index < len(sprite.textures) - 1:
                        sprite.cur_texture_index += 1
                    else:
                        self.static_animations_finished = True
                elif self.anim_speed_counter < 0:
                    self.anim_speed_counter = self.anim_speed
                sprite.texture = sprite.textures[sprite.cur_texture_index]
        elif not self.game_started and not self.static_animations_finished:
            # Move static sprites from texture 1-2 before launch of game
            for sprite in self:
                self.anim_speed_counter -= 1
                if self.anim_speed_counter == 0:
                    if sprite.cur_texture_index == 1:
                        sprite.cur_texture_index = 0
                    else:
                        sprite.cur_texture_index += 1
                elif self.anim_speed_counter < 0:
                    self.anim_speed_counter = self.anim_speed
                sprite.texture = sprite.textures[sprite.cur_texture_index]
        elif self.static_animations_finished and not self.dynamic_animations_started:
            # Replace static sprite with dynamic sprite
            # Prepare link between duck and fisherman
            self.sprite_static.kill()
            # Below line is here, so rod is only visible after start:
            self.sprite_dynamic.position = self.sprite_static.position[0] * 1.1105, self.sprite_static.position[1] / 2.2
            self.append(self.sprite_dynamic)
            self.dynamic_animations_started = True
        elif self.dynamic_animations_started and not self.connected_to_duck:
            self.connected_to_duck = True

            # Create physical model for player:
            size_x = self.sprite_dynamic.width
            size_y = self.sprite_dynamic.height
            mass = 120.0
            moment = pymunk.moment_for_box(mass, (size_x, size_y))
            body = pymunk.Body(mass, moment)
            body.position = pymunk.Vec2d(self.sprite_dynamic.center_x, self.sprite_dynamic.center_y)
            self.shape = pymunk.Poly.create_box(body, (size_x, size_y))
            self.shape.friction = 0.3
            self.space.add(body, self.shape)

            # Create a bond between duck and human 4ever:
            #vein = pymunk.DampedSpring(self.shape.body, self.private_duck[0].pymunk_shape.body, (0, 0), (0, 0), 10, 10, 100)
            vein = pymunk.PinJoint(self.shape.body, self.private_duck[0].pymunk_shape.body)
            self.space.add(vein)
            self.joints.append(vein)
            window.music_manager.start_music_triggered()
            if not window.music_manager.media_player.playing:
                # Yeah I know...but works.
                window.music_manager.start_music_triggered()

        elif self.connected_to_duck:
            # Update position of sprite and shape
            for sprite in self:
                sprite.center_x = self.shape.body.position.x
                sprite.center_y = self.shape.body.position.y
                #Angle doesn't look good:
                #sprite.angle = math.degrees(self.shape.body.angle)
                # Move dynamic sprites between texture 1 and 2
                self.anim_speed_counter -= 1
                if self.anim_speed_counter == 0:
                    if sprite.cur_texture_index == 1:
                        sprite.cur_texture_index = 0
                    else:
                        sprite.cur_texture_index += 1
                elif self.anim_speed_counter < 0:
                    self.anim_speed_counter = self.anim_speed * 3
                sprite.texture = sprite.textures[sprite.cur_texture_index]






