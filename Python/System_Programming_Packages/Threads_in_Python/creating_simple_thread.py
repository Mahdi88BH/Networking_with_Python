import threading


def my_task():
    print("Hello Threads : {}".format(threading.current_thread()))

myFirstThreads = threading.Thread(target=my_task)
myFirstThreads.start()