from Queue import Empty
from os import name
from threading import Thread
from logging import getLogger, INFO, StreamHandler
import time
if name != "nt":
    from omxplayer.player import OMXPlayer


class VideoPlayer:
    def __init__(self):
        self.is_running = False
        self._current_player = None
        self._thread = Thread()
        self._logger = getLogger("Video Player")
        self._logger.setLevel(INFO)

        self._logger.addHandler(StreamHandler())

    def start(self, video_list_queue):
        self._thread = Thread(target=self._run, args=(video_list_queue,))
        self._thread.start()

    def stop(self):
        self.is_running = False
        if self._current_player:
            self._current_player.quit()
        self._thread.join()

    def _run(self, video_list_queue):
        """
        :type video_list_queue: Queue.Queue
        """
        self.is_running = True
        video_list = []
        self._logger.info("waiting for a playlist...")
        while self.is_running:
            try:
                video_list = video_list_queue.get(block=True, timeout=5)
                self._logger.info("got a playlist!")
                break
            except Empty:
                continue

        current_video = 0
        while self.is_running:
            if self.play_video(video_list[current_video]):
                current_video = (current_video + 1) % len(video_list)
            else:
                self._logger.info("Removing from the playlist")
                del video_list[current_video]
                if len(video_list) > 0:
                    current_video = current_video % len(video_list)

            if len(video_list) == 0 or not video_list_queue.empty():
                self._logger.info("waiting for a new playlist...")
                video_list = video_list_queue.get()
                self._logger.info("new playlist!")
                current_video = 0

    def play_video(self, path):
        """
        :type path: str
        """
        # print "[video player] Playing video %s" % path
        try:
            self._current_player = OMXPlayer(path, args=['-r','--no-osd'],
                                             dbus_name='org.mpris.MediaPlayer2.omxplayer1')
            self._current_player.play()
            while self._current_player.is_playing:
                time.sleep(1)
            return True
        except Exception as e:
            self._logger.info("Error playing %s : %s" % (path, str(e)))
            return False
