import threading


class MyThread(threading.Thread):
    def __init__(self, message):
        threading.Thread.__init__(self)
        self.message = message

    def run(self): print(self.message)



def test():
    threads = []

    for num in range(0, 10):
        thread = MyThread(f"I am {num} Thread")
        thread.start()
        threads.append(thread)

    # Loop through thread objects and block until each finishes.
    for th in threads:
        # th.join() ensures test() won't return until all threads 
        # have completed.
        th.join()


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(
        "test()", 
        setup="from __main__ import test",
        number=5)
        )