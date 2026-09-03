# - BaseException: The class from which all exceptions inherit.
# - Exception (BaseException): An exception is a special case of a more 
# general class named BaseException.
# - ZeroDivisionError (ArithmeticError): An exception raised when the second 
# argument of a division is 0. This is a special case of a more general 
# exception class named ArithmeticError.
# - EnvironmentError (StandardError): This is a parent class of errors 
# related to input/output.
# -IOError (EnvironmentError): This is an error in an input/output operation.
# -OSError (EnvironmentError): This is an error in a system call.
# -ImportError (StandardError): The module or the module element that 
# you wanted to import was not found.

def printExceptionsTree(ExceptionClass, level = 0):
    if level > 1:
        print(" |" * (level - 1), end="")
    if level > 0:
        print(" +---", end="")
    print(ExceptionClass.__name__)
    for subclass in ExceptionClass.__subclasses__():
        printExceptionsTree(subclass, level+1)


if __name__ == "__main__":

    try:
        print("10 / 0 = ", str(10/0))
    except Exception as exc:
        print("Error => ",exc)

    try:
        file_handler = open("file1.txt", 'r')
    except IOError as exc:
        print("Exception IOError : Unable to read the file ", exc)
    except Exception as exc:
        print("Exception : ", exc)
    else:
        print("file read Succefuly")
        file_handler.close()
        print("file are closed" if file_handler.closed else "The file are not closed properly")

    printExceptionsTree(BaseException)