# SUCCESS THREAD CLASS

from threading import Thread
import time
import schedule
import datetime


class MyThread(Thread):
    def job(self):
        x = 0
        while 1:
            x = x + 1
            print("follow %s" % datetime.datetime.now())
            time.sleep(1)
            return 1/0

    def job2(self):
        # while 1:
        print("unfollow")
        #     time.sleep(1)

    def run_threaded(self, job_func):
        job_thread = Thread(target=job_func)
        job_thread.start()

    def loop_follow(self):
        try:
            print("self.job")
            self.job()
        except:
            print("going to loop")
            self.loop_follow()

    def run(self):
        self.run_threaded(self.loop_follow)
        schedule.every(5).seconds.do(self.run_threaded, self.job2)

        while 1:
            schedule.run_pending()
            time.sleep(1)

MyThread().start()
