import elements
import arcade
import random

TEXT_EVENTS = [(0, ""), (1, "HELLO"), (2, "THIS IS..."), (3, "PyWeek32 Entry"), (4, "Endless Horizon"),
               (5, "Nice Weather Tho"), (6, "Music also sounds fine"), (7, "Where was I?"),
               (8, "You see this progress bar above?"), (9, "I think we gonna make it"),
               (10, "This duck is strong."), (11, "but be careful..."),
               (12, "do not lose the cursor"), (13, ""), (16, "Magic."),
               (17, ""), (18, ""), (19, "What was that?"),
               (20, "I didn't mention something before"), (21, "Something important"), (22, "You can't loose"),
               (23, "but!"), (24, "It's possible to win!"), (25, ""),
               (28, "The ducks have found you"), (29, "Don't move mouse"), (30, ""),
               (31, "Yeah...you still wanna play?"), (32, "This game is unfinished"),
               (33, "But at the end"), (34, "There is nice image"), (35, "I mean"),
               (36, "victory screen"), (37, ""), (38, "No, no more content."),
               (39, "only victory image"), (40, "to be honest"),
               (41, "you won't see it "), (42, "you won't last"), (43, "but"),
               (44, "time will show"), (45, ""),
               (46, "btw"), (47, "Thanks for playing."), (48, "I appreciate it"),
               (49, ""), (50, "It took me one hour"), (51, "To make this cursor disappearing"),
               (52, "It's not magic"), (53, "only hard work"), (54, ""), (56, "More boxes"),
               (57, ""), (58, ""), (62, "One day"), (63, "I will finish this game"),
               (64, ""), (75, "Still here?"), (76, ""), (82, "THE END"), (84, "Joke"),
               (85, ""), (87, "Road is long"), (88, "or maybe the sea?"), (89, ""),
               (90, "for sure"), (91, "sea is the limit"), (92, ""), (100, "no more content ahead"),
               (101, "really"), (102, ""), (105, "only boxes"), (106, ""), (109, "and ducks"),
               (110, ""), (120, ""), (121, "I have to go"), (122, "Once again, thanks for playing."),
               (123, "")]


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
        self.font_color = arcade.color.BLACK

    def setup(self):
        self.text_event = TEXT_EVENTS[0][1]
        self.game_event_id = 0
        self.font_color = arcade.color.BLACK
        self.last_event_position = self.window.view_game.camera_sprites.position[0]
        self.last_scripted_event_position = self.window.view_game.camera_sprites.position[0]
        self.mouse_visible = True
        self.script_executed = False
        self.spawn_ducks = False
        self.scripted_events = [(12, "1_CURSOR"),
                                (13, "1_CURSOR"),
                                (14, "1_CURSOR"),
                                (15, "1_CURSOR"),
                                (18, "2_SPAWN_BOXES"),
                                (19, "4_SPAWN_BOXES_MORE"),
                                (29, "3_SPAWN_DUCKS"),
                                (51, "1_CURSOR"),
                                (53, "1_CURSOR"),
                                (56, "4_SPAWN_BOXES_MORE"),
                                (105, "4_SPAWN_BOXES_MORE"),
                                (110, "3_SPAWN_DUCKS")
                                ]

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
                    elif event[1] == "4_SPAWN_BOXES_MORE":
                        self.spawn_more_boxes()
                    print("Game scripted event:", event[1])
                    self.script_executed = True
                    self.last_scripted_event_position = self.window.view_game.camera_sprites.position[0]
                elif self.game_event_id != event[0]:
                    # None of the scripts was executed
                    self.script_executed = False
        if self.window.view_game.timer.game_hour > 16:
            self.font_color = arcade.color.WHITE_SMOKE
        else:
            self.font_color = arcade.color.BLACK

    def update_mouse_coords(self, x, y):
        self.mouse_world_x = x
        self.mouse_world_y = y

    def on_draw(self):
        arcade.draw_text(text=str(self.text_event),
                         start_x=self.window.width // 2, start_y=self.window.height // 2 - 50,
                         color=self.font_color, font_size=50,
                         anchor_x="center")

    def cursor_disappearing(self):
        self.mouse_visible = not self.mouse_visible
        print("Mouse:", self.mouse_visible)
        self.window.set_mouse_visible(visible=self.mouse_visible)
        self.window._mouse_visible = self.mouse_visible

    def spawn_boxes(self):
        elements.make_crate(self.window.view_game.camera_sprites.position[0],
                            self.mouse_world_y + 100,
                            self.space, self.global_sprite_list)
        elements.make_crate(self.window.view_game.camera_sprites.position[0],
                            self.mouse_world_y - 100,
                            self.space, self.global_sprite_list)
        elements.make_crate(self.window.view_game.camera_sprites.position[0],
                            self.mouse_world_y - 100,
                            self.space, self.global_sprite_list)
        elements.make_crate(self.window.view_game.camera_sprites.position[0],
                            self.mouse_world_y + 100,
                            self.space, self.global_sprite_list)
        elements.make_crate(self.window.view_game.camera_sprites.position[0],
                            self.mouse_world_y,
                            self.space, self.global_sprite_list)

    def spawn_more_boxes(self):
        for i in range(0,50):
            elements.make_crate(random.randrange(int(self.window.view_game.camera_sprites.position[0]-100),
                                                 int(self.window.view_game.camera_sprites.position[0])),
                                random.randrange(int(self.window.height * 0.2), int(self.window.height * 0.6)),
                                self.space, self.global_sprite_list)

    def spawn_duck(self, velocity):
        elements.make_duck(x=self.window.view_game.camera_sprites.position[0],
                           y=int(random.randrange(self.window.height * 0.2, self.window.height * 0.5)),
                           global_sprite_list=self.global_sprite_list,
                           space=self.space,
                           window=self.window, velocity=velocity)

    def on_mouse_motion(self):
        if self.spawn_ducks:
            self.spawn_duck(velocity=200)
            self.spawn_duck(velocity=300)
            self.spawn_duck(velocity=400)
            self.spawn_duck(velocity=200)
            self.spawn_ducks = False
