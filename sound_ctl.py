from pydub import AudioSegment
from pydub.playback import play
import simpleaudio as sa
import threading

class SoundController:
    def __init__(self, filepath):
        self.filepath = filepath
        self.audio = AudioSegment.from_file(filepath)
        self.playback_object = None
        self.is_paused = False
        self.stop_flag = False
        self.play_thread = None

    def play_song(self):
        if not self.playback_object or self.playback_object.is_playing() == False:
            self.stop_flag = False
            self.is_paused = False
            self.play_thread = threading.Thread(target=self._play)
            self.play_thread.start()
        elif self.is_paused:
            self.is_paused = False
            self.playback_object.stop()
            self.playback_object = sa.play_buffer(self.audio.raw_data, num_channels=self.audio.channels, bytes_per_sample=self.audio.sample_width, sample_rate=self.audio.frame_rate)
            self.playback_object.wait_done()

    def _play(self):
        self.playback_object = sa.play_buffer(self.audio.raw_data, num_channels=self.audio.channels, bytes_per_sample=self.audio.sample_width, sample_rate=self.audio.frame_rate)
        while self.playback_object.is_playing() and not self.stop_flag:
            pass
        if self.stop_flag:
            self.playback_object.stop()

    def toggle_pause(self):
        if self.playback_object and self.playback_object.is_playing():
            self.playback_object.stop()
            self.is_paused = True
        elif self.is_paused:
            self.play_song()

    def stop(self):
        self.stop_flag = True
        if self.playback_object:
            self.playback_object.stop()

if __name__ == "__main__":
    filepath = "Queencards.mp3"  # Change to your file path
    controller = SoundController(filepath)
    
    controller.play_song()
    input("Press Enter to toggle pause/play...")
    controller.toggle_pause()

    input("Press Enter to toggle pause/play again...")
    controller.toggle_pause()

    input("Press Enter to stop and exit...")
    controller.stop()
