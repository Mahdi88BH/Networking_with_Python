# NOTE: 'optparse' is deprecated since Python 3.2 in favor of 'argparse', 
# but it is frequently encountered in legacy security and networking 
# scripts/tools.
from optparse import OptionParser

# Define a container class to hold configuration parameters centrally.
class Parameters:
    """Global parameters"""

    def __init__(self, **kwargs):
        self.param1 = kwargs.get("param1")
        self.param2 = kwargs.get("param2")

def view_parameters(input_parameters):
    print(input_parameters.param1)
    print(input_parameters.param2)


if __name__ == "__main__":
    parser = OptionParser()

    parser.add_option("--p1", dest="param1", help="parameter1")
    parser.add_option("--p2", dest="param2", help="parameter2")

    # 'options' is an object containing flag values (e.g., options.param1).
    # 'args' is a list of positional arguments left over after options 
    # are parsed.
    (options, args) = parser.parse_args()

    input_parameters = Parameters(param1=options.param1, param2=options.param2)

    view_parameters(input_parameters)



# |         Feature      |                              `optparse`                              
# |                      |                                                                  
# | Status               | Deprecated (since Python 3.2). Kept only for backward compatibility.
# | Positional Arguments | Cannot parse positional arguments directly; handles only options (`-f`, `--flag`). Unmatched arguments spill into a raw list (`args`). 
# | Parsing Return       | Returns a two-element tuple: `(options, args)`.
# | Subcommands          | No native support (building `git clone` or `docker run` style interfaces is difficult).
# | Action Types         | Supports basic types like `string`, `int`, `choice`. Custom types require complex extensions.
# | Help Output          | Basic help generation.


# |         Feature       |                 `argparse` 
# |                       | 
# | Status                | Active standard. Recommended for all new Python development. |
# | Positional Arguments  | Native support for positional arguments alongside flags via `add_argument()`. |
# | Parsing Return        | Returns a single `Namespace` object containing both options and positional arguments. |
# | Subcommands           |  Built-in support for sub-parsers via `add_subparsers()`. |
# | Action Types          | Directly accepts any Callable (e.g., `type=int`, `type=Path`, `type=open`) to validate or convert input automatically. |
# | Help Output           |  Richer, customizable help generation with support for argument groups and mutally exclusive flags. |
    
