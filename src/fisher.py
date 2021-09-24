import arcade
import assets


class Fisher(arcade.SpriteList):
    def __init__(self):
        super().__init__()
        self.position = (0, 0)
        self.space = None
        self.sprite_head = arcade.Sprite()
        self.sprite_head_sprite_list = arcade.SpriteList()
        self.sprite_arm = arcade.Sprite()
        self.sprite_arm_sprite_list = arcade.SpriteList()
        self.sprite_body = arcade.Sprite()
        self.sprite_body_sprite_list = arcade.SpriteList()
        self.sprite_static = arcade.Sprite()
        self.game_started = False
        self.static_animations_finished = False

        self.anim_speed = 0
        self.anim_speed_counter = 0

    def on_setup(self, bridge_x, bridge_y, space, anim_speed=10):
        self.position = bridge_x, bridge_y
        self.space = space
        self.sprite_head = arcade.Sprite(texture=assets.fisher_head_texture)
        self.sprite_arm = arcade.Sprite(texture=assets.fisher_arm_texture)
        self.sprite_body = arcade.Sprite(texture=assets.fisher_body_texture)
        self.sprite_static = assets.fisher_static_sprite
        self.sprite_head_sprite_list.append(self.sprite_head)
        self.sprite_arm_sprite_list.append(self.sprite_arm)
        self.sprite_body_sprite_list.append(self.sprite_body)
        self.sprite_head.position = self.position[0], self.position[1] + self.sprite_head.height / 4
        self.sprite_arm.position = self.position[0], self.position[1]
        self.sprite_body.position = self.position[0], self.position[1] - self.sprite_body.height / 2
        self.sprite_static.position = self.position[0], self.position[1] + self.sprite_static.height / 4
        self.anim_speed = anim_speed
        self.anim_speed_counter = anim_speed
        self.append(self.sprite_static)
        self.game_started = False
        self.static_animations_finished = False

    def start(self):
        self.game_started = True
        self.append(self.sprite_head)
        self.append(self.sprite_arm)
        self.append(self.sprite_body)

    def on_draw(self):
        self.draw()
        #self.sprite_body_sprite_list.draw()
        #self.sprite_arm_sprite_list.draw()
        #self.sprite_head_sprite_list.draw()

    def on_update(self):
        if self.game_started and not self.static_animations_finished:
            # Move static sprites from texture 3-14 before launch of game
            for sprite in self:
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
        elif not self.game_started:
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





