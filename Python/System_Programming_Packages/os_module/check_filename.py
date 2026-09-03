import os
import sys
from collections import Counter

# - os.system() allows us to execute a shell command.
# - os.listdir(path) returns a list with the contents of the directory 
#   passed as an argument.
# - os.walk(path) navigates all the directories in the provided path 
#   directory, and returns three values: the path directory, the names of 
#   the subdirectories, and a list of filenames in the current directory 
#   path.


if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        if not os.path.isfile(filename):
            print('[-] ' + filename + ' does not exist.')
        if not os.access(filename, os.R_OK):
            print('[-] ' + filename + ' access denied.')

    pwd = os.getcwd()

    # Return a list containing the names of the files in the directory.
    list_directory = os.listdir(pwd) 

    for directory in list_directory:
        print('[+] ',directory)


    for root, directories, files in os.walk('.', topdown=False):
        # Iterate over the files in the current "root"
        for file in files:
            # Create Relative Path
            print('[+] ', os.path.join(root, file))
            for name in directory:
                print('[++] ', name)
            print('root => ',root)
            print('directories => ',directory)
            print('files =>',files)

    for currentdir, dirnames, filenames in os.walk('.'):
        print(filenames)


    counter = Counter()

    for currentdir, dirnames, filename in os.walk('.'):
        for file in filename:
            file_name , extension = os.path.splitext(file)
            counter[extension] += 1

    for ext, count in counter.items():
        print(f"{extension} => {count}")


    print("Get the environment variables in the operating system")

    # 'os.getcwd()' returns a string representing the current absolute working
    #  directory path.
    # Utility: Crucial for locating relative files, datasets, scripts, or 
    # project root folders.
    print('Current Working directory => ',os.getcwd())

    # 'os.getuid()' returns the numerical real user ID (UID) of the current 
    # running process.
    # Utility: Useful for process identity checks, permission validation, or 
    # security auditing on Kali Linux/POSIX systems.
    # Note: This function only exists on Unix/Linux/macOS platforms 
    # (raises AttributeError on Windows).
    print('Get the procces ID running => ',os.getuid())

    # 'os.getenv("PATH")' retrieves the value of the "PATH" system environment 
    # variable.
    # Utility: Safe variable lookup. Unlike dict access (os.environ["PATH"]), 
    # os.getenv() returns None 
    # (or a specified default value) instead of raising a KeyError if 
    # the variable does not exist.
    print('System environment variablee => ',os.getenv("PATH"))


    # 'os.environ' is a mapping object representing all active system 
    # environment variables.
    # Printing it directly outputs the full os._Environ dictionary 
    # representation containing all key-value pairs.
    print('active system environment variables => ',os.environ)

    for environ in os.environ:
        print(environ)

    for key, value in os.environ.items():
        print(key,value)