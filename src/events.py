import elements
import arcade
import random

TEXT_EVENTS = [(0, ""), (1, "HELLO"), (2, "THIS IS..."), (3, "PyWeek32 Entry"), (4, "Endless Horizon"),
               (5, "Nice Weather Tho"), (6, "Music also sounds fine"), (7, "Where was I?"),
               (8, "You see this progress bar above?"), (9, "I think we gonna make it"),
               (10, "This duck is strong."), (11, "but be careful..."),
               (12, "do not lose the cursor"), (13, ""), (16, "Uff. Cursor is back again."),
               (17, ""), (18, "What was that?"), (19, ""),
               (20, "I didn't mention something before"), (21, "Something important"), (22, "You can't loose"),
               (23, "but!"), (24, "It's possible to win!"), (25, ""),
               (28, "Watch out. More ducks!"), (29, ""), (30, "It was close!"),
               (31, "Yeah...you still wanna play?"), (32, "This game is unfinished"),
               (33, "But at the end"), (34, "There is nice image"), (35, "I mean"),
               (36, "victory screen"), (37, ""), (38, "No, no more content."),
               (39, "only victory image"), (40, "you won't see it to be honest"),
               (41, "it's possible, as I said..."), (42, ""),
               (44, "btw"), (45, "Thanks for playing."), (46, "I appreciate it"),
               (47, "And now go try another game!"),(48, "")]


class EventManager:
    def __init__(self, window, timer, space, global_sprite_list, fisher):
        self.window = window
        self.timer = timer
        self.space = space
        self.global_sprite_list = global_sprite_list
        self.fisher = fisher
        self.mouse_world_x = 0
        self.mouse_world_y = 0
        self.text_event = ""
        self.game_event_id = 0
        self.last_event_position = 0
        self.last_scripted_event_position = 0
        self.script_executed = False
        self.scripted_events = []
        self.mouse_visible = True
        self.spawn_ducks = False

    def setup(self):
        self.text_event = TEXT_EVENTS[0][1]
        self.game_event_id = 0
        self.last_event_position = self.window.view_game.camera_sprites.position[0]
        self.last_scripted_event_position = self.window.view_game.camera_sprites.position[0]
        self.mouse_visible = True
        self.script_executed = False
        self.spawn_ducks = False
        self.scripted_events = [(14, "1_CURSOR"),
                                (15, "1_CURSOR"),
                                (17, "2_SPAWN_BOXES"),
                                (29, "3_SPAWN_DUCKS")]

    def on_update(self):
        if int(-self.window.view_game.camera_sprites.position[0] + self.last_event_position) >= 10000:
            self.game_event_id += 1
            for event in TEXT_EVENTS:
                if self.game_event_id == event[0]:
                    if self.text_event != event[1]:
                        self.text_event = event[1]
                        print("Game text event:", self.game_event_id, event[1])
                        self.last_event_position = self.window.view_game.camera_sprites.position[0]
            for event in self.scripted_events:
                if self.game_event_id == event[0] and not self.script_executed:
                    if event[1] == "1_CURSOR":
                        self.cursor_disappearing()
                    elif event[1] == "2_SPAWN_BOXES":
                        self.spawn_boxes()
                    elif event[1] == "3_SPAWN_DUCKS":
                        self.spawn_ducks = True
                    print("Game scripted event:", event[1])
                    self.script_executed = True
                    self.last_scripted_event_position = self.window.view_game.camera_sprites.position[0]
                elif self.game_event_id != event[0]:
                    # None of the scripts was executed
                    self.script_executed = False

    def update_mouse_coords(self, x, y):
        self.mouse_world_x = x
        self.mouse_world_y = y

    def on_draw(self):
        arcade.draw_text(text=str(self.text_event),
                         start_x=self.window.width // 2, start_y=self.window.height // 2 - 50,
                         color=arcade.color.BLACK, font_size=50,
                         anchor_x="center")

    def cursor_disappearing(self):
        self.mouse_visible = not self.mouse_visible
        print("Mouse:", self.mouse_visible)
        self.window.set_mouse_visible(visible=self.mouse_visible)
        self.window.set_mouse_position(x=int(random.randrange(self.window.width * 0.25, self.window.width * 0.5)),
                                       y=int(random.randrange(self.window.height * 0.4, self.window.height * 0.9))
                                       )

    def spawn_boxes(self):
        elements.make_crate(self.mouse_world_x+100-200,
                            self.mouse_world_y+100,
                            self.space, self.global_sprite_list)
        elements.make_crate(self.mouse_world_x-100-200,
                            self.mouse_world_y-100,
                            self.space, self.global_sprite_list)
        elements.make_crate(self.mouse_world_x+100-200,
                            self.mouse_world_y-100,
                            self.space, self.global_sprite_list)
        elements.make_crate(self.mouse_world_x-100-200,
                            self.mouse_world_y+100,
                            self.space, self.global_sprite_list)
        elements.make_crate(self.mouse_world_x-200,
                            self.mouse_world_y,
                            self.space, self.global_sprite_list)

    def spawn_duck(self, velocity):
        elements.make_duck(x=int(self.mouse_world_x),
                           y=int(random.randrange(self.window.height * 0.4, self.window.height * 0.9)),
                           global_sprite_list = self.global_sprite_list,
                           space=self.space,
                           window=self.window, velocity=velocity)

    def on_mouse_motion(self):
        if self.spawn_ducks:
            self.spawn_duck(velocity=200)
            self.spawn_duck(velocity=300)
            self.spawn_duck(velocity=400)
            self.spawn_duck(velocity=200)
            self.spawn_ducks = False
