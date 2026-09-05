import threading
import logging
import time

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] - %(threadName)-10s : %(message)s')

def thread(name):
    logging.debug('Starting Thread '+ name)
    time.sleep(5)
    print("%s: %s" % (name, time.ctime(time.time())))
    logging.debug('Stopping Thread '+ name)


def check_state(thread):
    if thread.is_alive():
        print(f'Thread {thread.name} is alive.')
    else:
        print(f'Thread {thread.name} it not alive.')

th1 = threading.Thread(target=thread, args=('MyThread',))
th2 = threading.Thread(target=thread, args=('MyThread2',))

# Daemon threads are background tasks that do NOT prevent the main program 
# from exiting.
th1.daemon = True

th1.start()
th2.start()

check_state(th1)
check_state(th2)

# Poll 'th1' status every 1 second while it sleeps/executes.
while(th1.is_alive()):
    logging.debug('Thread is executing...')
    time.sleep(1)

# .join() blocks the main thread until th1 and th2 complete 
# their execution cleanly.
th1.join()
th2.join()