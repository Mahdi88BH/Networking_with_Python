from ThreadWorker import ThreadWorker

def main():
    thread = ThreadWorker()
    thread.start()
    thread.join()  # Best practice: Wait for worker thread to finish

if __name__ == "__main__":
    main()