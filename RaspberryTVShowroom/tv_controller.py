from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from Queue import Empty
from threading import Thread
import subprocess
from logging import getLogger
import time


class TVController:
    def __init__(self):
        self._logger = getLogger("raspberry.tvcontroller")
        self._thread = Thread()
        self.is_running = False
        self._logger.info("ready")

    def start(self, schedule_queue):
        self._thread = Thread(target=self._run, args=(schedule_queue,))
        self._thread.start()

    def stop(self):
        self.is_running = False
        self._logger.info("Waiting for all actions to terminate")
        self._thread.join()
        self._logger.info("Finished")

    def _run(self, schedule_queue):
        """
        :type schedule_queue: Queue.Queue
        """
        self._logger.info("waiting for a schedule...")

        self.is_running = True

        scheduler = BackgroundScheduler()
        scheduler.start()

        time_on = "12:00"
        time_off = "13:00"
        while self.is_running:
            try:
                schedule = schedule_queue.get(block=True, timeout=5)
                time_on, time_off = schedule
                self._logger.info("new schedule: %s to %s." % (time_on, time_off))
                break

            except Empty:
                continue

        while self.is_running:
            self._logger.info("got a new schedule: %s to %s." % (time_on, time_off))
            time_on = datetime.strptime(time_on, "%H:%M").time()
            time_off = datetime.strptime(time_off, "%H:%M").time()

            job_switch_on = scheduler.add_job(self.switch_on, 'cron',
                                              hour=time_on.hour,
                                              minute=time_on.minute,
                                              day_of_week='mon-fri')
            job_switch_off = scheduler.add_job(self.switch_off, 'cron',
                                               hour=time_off.hour,
                                               minute=time_off.minute,
                                               day_of_week='mon-fri')
            while self.is_running:
                try:
                    schedule = schedule_queue.get(block=True, timeout=5)
                    time_on, time_off = schedule
                except Empty:
                    continue

            job_switch_on.remove()
            job_switch_off.remove()

        scheduler.shutdown()

    def switch_on(self):
        self._logger.info("switching TV on")
        for i in range(5):
            command = "echo on 0 | cec-client -s -d 1"
            subprocess.call(command, shell=True)
            time.sleep(2)

    def switch_off(self):
        self._logger.info("switching TV off")
        for i in range(5):
            command = "echo standby 0 | cec-client -s -d 1"
            subprocess.call(command, shell=True)
            time.sleep(2)


if __name__ == "__main__":
    tv = TVController()
    tv.switch_on()
    tv.switch_off()
    tv.switch_on()
    tv.switch_off()