import winsound
import threading

class Sound:
    def __init__(self, file_path):
        self.file_path = file_path
        self.is_looping = False
        self.thread = None

    def _play_loop(self):
        while self.is_looping:
            winsound.PlaySound(self.file_path, winsound.SND_FILENAME | winsound.SND_ASYNC)

    def play(self):
        winsound.PlaySound(self.file_path, winsound.SND_FILENAME | winsound.SND_ASYNC)

    def play_loop(self):
        if not self.is_looping:
            self.is_looping = True
            self.thread = threading.Thread(target=self._play_loop, daemon=True)
            self.thread.start()

    def stop(self):
        self.is_looping = False
        winsound.PlaySound(None, winsound.SND_PURGE)

if __name__ == "__main__":
    player = Sound("Assets/Audio/type.wav")
    player.play()
    while True:
        pass