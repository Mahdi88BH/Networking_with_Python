import threading

class MyThread(threading.Thread):

    def __init__(self, message):
        threading.Thread.__init__(self)
        self.message = message

    # The run() method defines the entry point for the thread when 
    # .start() is called.
    def run(self): print(self.message)

def test():
    for num in range(0, 10):
        thread = MyThread(f"I am the {num} Thread")
        thread.name = num
        thread.start()


if __name__ == "__main__":
    import timeit

    # timeit.timeit() measures the time taken to execute statement 
    # 'test()' 5 times (number=5).
    # 'setup' imports 'test' from the current execution namespace 
    # (__main__).
    print(timeit.timeit(
        "test()", 
        setup="from __main__ import test", 
        number=5)
        )