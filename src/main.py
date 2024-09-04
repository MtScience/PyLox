from argparse import ArgumentParser
from PyLox.pylox import Lox


if __name__ == '__main__':
    options_parser: ArgumentParser = ArgumentParser(prog="pylox.py")
    options_parser.add_argument("script", nargs="?", default=None)
    options_parser.add_argument("-i", "--interactive", action="store_true",
                                help="run in interactive mode after executing a script "
                                     "(if no script is given, does nothing)")
    options_parser.add_argument("-e", "--execute", metavar="FILE",
                                help="run the specified file before executing another"
                                     " script or entering interactive mode")
    options_parser.add_argument("-l", "--load", metavar="FILE", help="synonym to --execute")

    options = options_parser.parse_args()

    lox: Lox = Lox()

    # Processing loading options
    if options.execute is not None:
        lox.run_file(options.execute)
    if options.load is not None:
        lox.run_file(options.load)

    # Processing main script (or lack thereof)
    if options.script is not None:
        lox.run_file(options.script)

        if options.interactive:
            lox.run_repl()
    else:
        lox.run_repl()
