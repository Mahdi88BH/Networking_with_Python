import argparse


# Define a class to hold configuration settings or arguments centrally 
# across your script.
class Parameters:
    """Globale Parameters"""

    def __init__(self, **kwargs):
        self.param1 = kwargs.get("param1")
        self.param2 = kwargs.get("param2")

def view_parameters(input_parameters):
    print(input_parameters.param1)
    print(input_parameters.param2)

# Boilerplate check: Ensures this block only executes when running 
# the script directly from the terminal,
# not when importing this file as a module in another script.
if __name__ == "__main__":

    # Create the ArgumentParser object with a description displayed when 
    # running with -h/--help.
    parser = argparse.ArgumentParser(description='Testing Parameters')

    parser.add_argument("-p1", dest="param1", help="parameter1")
    parser.add_argument("-p2", dest="param2", help="parameter2")

    # Read command-line arguments passed at runtime (e.g., python script.py -p1 foo -p2 bar)
    # and store them in the 'params' object.
    params = parser.parse_args()

    input_parameters = Parameters(param1=params.param1, param2=params.param2)

    view_parameters(input_parameters)