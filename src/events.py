import elements
import arcade

TEXT_EVENTS = [(0, ""), (1, "HELLO"), (2, "THIS IS..."), (3, "PyWeek32 Entry"), (4, "Endless Horizon"),
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
        self.last_scripted_event_position = 0
        self.script_executed = False
        self.scripted_events = []
        self.mouse_visible = True

    def setup(self):
        self.text_event = TEXT_EVENTS[0][1]
        self.game_event_id = 0
        self.last_event_position = self.window.view_game.camera_sprites.position[0]
        self.last_scripted_event_position = self.window.view_game.camera_sprites.position[0]
        self.mouse_visible = True
        self.script_executed = False
        self.scripted_events = [(14, "1_CURSOR"),
                                (15, "1_CURSOR")]

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
                        self.script_executed = True
                        print("Game scripted event: 1_CURSOR. Mouse:", self.mouse_visible)
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
        self.window.set_mouse_visible(visible=self.mouse_visible)
