from preferences import Preferences
from video_player import VideoPlayer
from tv_controller import TVController
from sys import argv
import time
from logging import getLogger, INFO, StreamHandler, Formatter


class TVApp:
    def __init__(self, config_path):
        self._logger = getLogger("raspberry")
        self._logger.setLevel(INFO)
        formatter = Formatter('%(asctime)s [%(name)s] %(levelname)s : %(message)s')
        stream_handler = StreamHandler()
        stream_handler.setLevel(INFO)
        stream_handler.setFormatter(formatter)
        self._logger.addHandler(stream_handler)

        self._logger.info("Initializing...")
        self.preference_checker = Preferences(config_path)
        self.video_player = VideoPlayer()
        self.tv_controller = TVController()

        self._logger.info("Ready")

    def run(self):
        self._logger.info("Waiting 1 min if you want to stop me before I go full screen...")
        time.sleep(60)

        self._logger.info("Starting all components now...")
        self.tv_controller.start(self.preference_checker.time_on_off)
        self.video_player.start(self.preference_checker.video_list)
        self.preference_checker.start()

        try:
            a = raw_input()
        except KeyboardInterrupt:
            pass

        self._logger.info("Key pressed, exiting")
        self.tv_controller.stop()
        self.video_player.stop()
        self.preference_checker.stop()

        self._logger.info("End")


if __name__ == "__main__":
    path = argv[1]
    print path
    app = TVApp(path)
    app.run()
