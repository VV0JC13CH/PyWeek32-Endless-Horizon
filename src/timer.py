import arcade


class Timer:
    def __init__(self):
        self.total_time = 0.0
        self.game_cycle = 0.0
        self.output = "00:00:00"
        self.game_hour = 0
        self.game_hour_counter_started = False
        self.night_is_coming = True

    def on_setup(self):
        self.total_time = 0.0
        self.game_cycle = 0.0
        self.game_hour = 0
        self.night_is_coming = True
        self.game_hour_counter_started = False

    def on_draw(self, pos_x, pos_y):
        arcade.draw_text(self.output,
                         pos_x, pos_y - 50,
                         arcade.color.WHITE, 100,
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

        # Calculate 100s of a second
        seconds_100s = int((self.total_time - seconds) * 100)

        # "Game-hours"
        # New background every 12s? So progress will be visible for a player
        if int(self.game_cycle) // 12 >= 1 and self.game_hour_counter_started:
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
        self.output = f"{minutes:02d}:{seconds:02d}:{seconds_100s:02d}"