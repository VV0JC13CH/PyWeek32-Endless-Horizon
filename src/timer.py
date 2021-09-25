import arcade
import datetime


class Timer:
    def __init__(self):
        self.total_time = 0.0
        self.game_cycle = 0.0
        self.game_event_time = 0
        self.output = "Press space, click mouse or whatever."
        self.game_hour = 0
        self.game_hour_counter_started = False
        self.night_is_coming = True
        self.minutes_total = 0
        self.seconds_total = 0

    def on_setup(self):
        self.total_time = 0.0
        self.game_cycle = 0.0
        self.game_hour = 0
        self.night_is_coming = True
        self.game_hour_counter_started = False
        self.seconds_total = 0
        self.game_event_time = 0

    def on_draw(self, pos_x, pos_y):
        arcade.draw_text(self.output,
                         pos_x, pos_y + 10,
                         arcade.color.BROWN_NOSE, 20,
                         anchor_x="center")

    def start(self):
        self.game_hour_counter_started = True

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        """
        if self.game_hour_counter_started:
            self.total_time += delta_time
            self.game_cycle += delta_time

        # Calculate minutes
        minutes = int(self.total_time) // 60

        # Calculate seconds by using a modulus (remainder)
        seconds = int(self.total_time) % 60

        # "Game-hours"
        # New background every 20s? So progress will be visible for a player
        if int(self.game_cycle) // 10 >= 1 and self.game_hour_counter_started:
            print("game cycle", self.game_hour)
            if self.night_is_coming and self.game_hour <= 23:
                self.game_hour += 1
            elif not self.night_is_coming and self.game_hour >= 1:
                self.game_hour -= 1
            elif self.game_hour >= 24:
                self.night_is_coming = False
            elif self.game_hour <= 0:
                self.night_is_coming = True
            self.game_cycle = 0

        # Output to draw:
        if self.game_hour_counter_started:
            self.output = f"{minutes:02d}:{seconds:02d}"
