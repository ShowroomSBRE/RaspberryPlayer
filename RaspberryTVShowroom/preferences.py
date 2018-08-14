from apscheduler.schedulers.background import BackgroundScheduler
from Queue import Queue
from socket import gethostname
import yaml
from logging import getLogger


class Preferences:
    def __init__(self, config_path):
        self._logger = getLogger("raspberry.preferences")
        self.video_list = Queue()
        self.time_on_off = Queue()
        self.configuration_file = config_path
        self._scheduler = BackgroundScheduler()
        self._scheduler.add_job(self.update, "interval", seconds=300)
        self._logger.info("ready")

    def update(self):
        self._logger.info("Checking for new preferences")
        try:
            data = self.decode_file(self.configuration_file)
            video_list = data["videos"]
            times = data["time"]
            time_on, time_off = times.split("-")
            self.video_list.put(video_list)
            self.time_on_off.put((time_on, time_off))
        except Exception as e:
            self._logger.error("Error checking preferences: %s " % str(e))

    def start(self):
        self.update()
        self._scheduler.start()

    def stop(self):
        self._scheduler.pause()
        self._logger.info("Finished")

    @staticmethod
    def decode_file(path):
        data = {}
        with open(path, 'r') as stream:
            try:
                data = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        hostname = gethostname()
        if hostname in data.keys():
            return data[hostname]
        else:
            return None



