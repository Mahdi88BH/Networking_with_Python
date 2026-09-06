import threading

class ThreadWorker(threading.Thread):
    def __init__(self):
        super().__init__()

    # The run() method defines what code executes when .start() is called.
    def run(self):
        for i in range(10): print(i)