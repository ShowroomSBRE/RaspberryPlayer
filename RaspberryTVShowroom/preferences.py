from apscheduler.schedulers.background import BackgroundScheduler
from Queue import Queue
from socket import gethostname
import yaml


class Preferences:
    def __init__(self, config_path):
        self.video_list = Queue()
        self.time_on_off = Queue()
        self.configuration_file = config_path
        self._scheduler = BackgroundScheduler()
        self._scheduler.add_job(self.update, "interval", seconds=20)

    def update(self):
        try:
            data = self.decode_file(self.configuration_file)
            video_list = data["videos"]
            times = data["time"]
            time_on, time_off = times.split("-")
            self.video_list.put(video_list)
            self.time_on_off.put((time_on, time_off))
        except Exception as e:
            print "Error checking preferences: ", str(e)

    def start(self):
        self._scheduler.start()

    def stop(self):
        self._scheduler.pause()

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



