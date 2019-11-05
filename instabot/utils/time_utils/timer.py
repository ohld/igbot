
from threading import Timer


class RepeatTimer(Timer):

    def __init__(self, interval, function):
        super().__init__(interval, function)
        self.daemon = True

    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

    def stop(self):
        self.cancel()
