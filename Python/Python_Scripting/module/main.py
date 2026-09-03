import sys
import my_function
from my_function import message


def main():
    message("Mahdi")


if __name__ == "__main__":
    main()
    print(dir(my_function)) # get all name entities from a module
    print(sys.path) # Indicate the path to the other modules