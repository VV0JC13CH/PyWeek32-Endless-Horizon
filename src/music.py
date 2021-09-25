import arcade
import assets


class MusicPlayer:
    def __init__(self, volume=0.0):
        self.media_player = None
        self.paused = True
        self.songs = [assets.house_music_path]
        self.cur_song_index = 0

        self.my_music = arcade.load_sound(self.songs[self.cur_song_index])

    def music_over(self):
        self.media_player.pop_handlers()
        self.media_player = None
        self.cur_song_index += 1
        if self.cur_song_index >= len(self.songs):
            self.cur_song_index = 0
        self.my_music = arcade.load_sound(self.songs[self.cur_song_index])
        self.media_player = self.my_music.play()
        self.media_player.push_handlers(on_eos=self.music_over)

    def volume_down(self, *_):
        if self.media_player and self.media_player.volume > 0.2:
            self.media_player.volume -= 0.2

    def volume_up(self, *_):
        if self.media_player and self.media_player.volume < 1.0:
            self.media_player.volume += 0.2

    def forward(self, *_):
        skip_time = 10

        if self.media_player and self.media_player.time < self.my_music.get_length() - skip_time:
            self.media_player.seek(self.media_player.time + 10)

    def start_music_triggered(self, *_):
        self.paused = False
        if not self.media_player:
            # Play button has been hit, and we need to start playing from the beginning.
            self.media_player = self.my_music.play()
            self.media_player.push_handlers(on_eos=self.music_over)
        elif not self.media_player.playing:
            # Play button hit, and we need to un-pause our playing.
            self.media_player.play()
        elif self.media_player.playing:
            # We are playing music, so pause.
            self.media_player.pause()

    def on_draw(self):
        if self.media_player:
            seconds = self.media_player.time
            minutes = int(seconds // 60)
            seconds = int(seconds % 60)
            arcade.draw_text(f"Time: {minutes}:{seconds:02}",
                             start_x=10, start_y=10, color=arcade.color.BLACK, font_size=24)
            volume = self.media_player.volume
            arcade.draw_text(f"Volume: {volume:3.1f}",
                             start_x=10, start_y=50, color=arcade.color.BLACK, font_size=24)
