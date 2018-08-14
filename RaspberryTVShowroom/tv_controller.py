from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from Queue import Empty
from threading import Thread
import subprocess


class TVController:
    def __init__(self):
        self._thread = Thread()
        self.is_running = False

    def start(self, schedule_queue):
        self._thread = Thread(target=self._run, args=(schedule_queue,))
        self._thread.start()

    def stop(self):
        self.is_running = False
        self._thread.join()

    def _run(self, schedule_queue):
        """
        :type schedule_queue: Queue.Queue
        """

        self.is_running = True

        scheduler = BackgroundScheduler()
        scheduler.start()

        time_on = "9:00"
        time_off = "19:00"
        print "[tv controller] waiting for a schedule..."
        while self.is_running:
            try:
                schedule = schedule_queue.get(block=True, timeout=5)
                time_on, time_off = schedule
                print "[tv controller] new schedule: %s to %s." % (time_on, time_off)
                break

            except Empty:
                continue

        while self.is_running:
            print "[tv controller] got a new schedule: %s to %s." % (time_on, time_off)
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
                    schedule = schedule_queue.get(block=True, timeout=300)
                    time_on, time_off = schedule
                except Empty:
                    continue

            job_switch_on.remove()
            job_switch_off.remove()

        scheduler.shutdown()

    def switch_on(self):
        print "[tv controller] switching TV on"
        command = "echo on 0 | cec-client -s -d 1"
        subprocess.call(command, shell=True)

    def switch_off(self):
        print "[tv controller] switching TV off"
        command = "echo standby 0 | cec-client -s -d 1"
        subprocess.call(command, shell=True)
