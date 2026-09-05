import time
import logging
# Import multiprocessing to spawn separate OS processes instead of threads.
import multiprocessing

logging.basicConfig(
    level=logging.DEBUG, 
    format='[%(levelname)s] - %(processName)-10s : %(message)s')


def thread(name):
    logging.debug('Starting Process '+ name)
    time.sleep(5)
    print("%s: %s" % (name, time.ctime(time.time())))
    logging.debug('Stopping Process '+ name)

def check_state(process):
    if process.is_alive():
        print(f'Process {process.name} is alive.')
    else:
        print(f'Process {process.name} is not alive.')

if __name__ == "__main__":
    process = multiprocessing.Process(target=thread, args=('MyProcess',))
    process2 = multiprocessing.Process(target=thread, args=('MyProcess2',))

    check_state(process)
    check_state(process2)

    # 2. Trigger OS process creation and start execution 
    # on separate CPU cores.
    process.start()
    process2.start()

    check_state(process)
    check_state(process2)

    # RECOMMENDED: Block the main process until child processes 
    # finish work.
    process.join()
    process2.join()