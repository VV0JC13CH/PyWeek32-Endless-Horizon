import elements
import arcade

TEXT_EVENTS = [(0, ""), (1, "HELLO"),(2, "THIS IS..."), (3, "PyWeek32 Entry"), (4, "Endless Horizon"),
         (5, "Nice Weather Tho"), (6, "Music also \n sounds fine"), (7, "Where was I?"),
         (8, "You see this \n progress bar above?"), (9, "I think we gonna make it"),
         (10, "This duck is strong."), (11, "but watch out for..."),
         (12, "the disappearing cursor"), (13, "Good luck!"), (14, "")]


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

    def setup(self):
        self.text_event = TEXT_EVENTS[0][1]
        self.game_event_id = 0
        self.last_event_position = self.window.view_game.camera_sprites.position[0]

    def on_update(self):
        print(-self.window.view_game.camera_sprites.position[0] + self.last_event_position)
        if int(-self.window.view_game.camera_sprites.position[0] + self.last_event_position) >= 10000:
            self.game_event_id += 1
            for event in TEXT_EVENTS:
                if self.game_event_id == event[0]:
                    if self.text_event != event[1]:
                        self.text_event = event[1]
                        print("Game text event:", self.game_event_id, event[1])
                        self.last_event_position = self.window.view_game.camera_sprites.position[0]

    def update_mouse_coords(self, x, y):
        self.mouse_world_x = x
        self.mouse_world_y = y

    def on_draw(self):
        arcade.draw_text(text=str(self.text_event),
                         start_x=self.window.width // 2, start_y=self.window.height // 2 - 50,
                         color=arcade.color.BLACK, font_size=50,
                         anchor_x="center")
