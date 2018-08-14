from preferences import Preferences
from video_player import VideoPlayer
from tv_controller import TVController
from keyboard_watcher import KeyboardWatcher
from time import sleep
from sys import argv


class TVApp:
    def __init__(self, config_path):
        print "Initializing"
        self.preference_checker = Preferences(config_path)
        self.video_player = VideoPlayer()
        self.tv_controller = TVController()
        self.keyboard_watcher = KeyboardWatcher()

        print "Ready"

    def run(self):
        print "Running all threads!"
        self.keyboard_watcher.start()
        self.tv_controller.start(self.preference_checker.time_on_off)
        self.video_player.start(self.preference_checker.video_list)
        self.preference_checker.start()

        self.keyboard_watcher.key_pressed.get(block=True, timeout=None)

        print "Key pressed, exiting"
        self.keyboard_watcher.stop()
        self.tv_controller.stop()
        self.video_player.stop()
        self.preference_checker.stop()

        print "End"


if __name__ == "__main__":
    path = argv[1]
    print path
    app = TVApp(path)
    app.run()
