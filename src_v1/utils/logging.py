from datetime import datetime
from pathlib import Path

log_dir = "logs"
logfile = None

output_mode = "terminal"    # terminal = print to terminal, file = write to file
halt_threshold = None       # warning = halt on warning, error = halt on error
verbosity = 1               # 0 = silent, 1 = normal, 2 = diagnostic

class Logger:
    def __init__(self):
        Exception("ERROR: do not instantiate logger")

    @staticmethod
    def configure(mode, halt_on=None, conf_verbosity=1, log_path="log.txt"):
        global output_mode, halt_threshold, verbosity, logfile

        if mode in ["terminal", "file", "exception"]:
            output_mode = mode
        else:
            raise Exception("ERROR: '" + mode + "' not a valid Logger mode")

        if halt_on in ["warning", "error", None]:
            halt_threshold = halt_on
        else:
            raise Exception("ERROR: '" + halt_on + "' not a valid Logger mode")

        if conf_verbosity in [0, 1, 2]:
            verbosity = conf_verbosity
        else:
            raise Exception("ERROR: '" + conf_verbosity + "' not a valid verbosity")

        if mode == "file":
            if isinstance(log_path, str):
                Path(log_dir).mkdir(exist_ok=True)
                Path(log_dir + "/" + log_path).touch()
                logfile = open(log_dir + "/" + log_path, "a")
            else:
                raise Exception("ERROR: '" + log_path + "' not a valid logfile path")

    @staticmethod
    def log(volume, message):
        global output_mode, halt_threshold, verbosity, logfile

        if volume > verbosity:
            return

        if output_mode == "terminal":
            print(message)
        elif output_mode == "file":
            if logfile == None:
                raise Exception("ERROR: no logfile specified")
            else:
                logfile.write(Logger.timestamp() + " " + message + "\n")

    @staticmethod
    def warn(message):
        global halt_threshold
        Logger.log(1, "WARNING: " + message)

        if halt_threshold == "warning":
            raise Exception("halting on warning")

    @staticmethod
    def error(message):
        global halt_threshold
        Logger.log(1, "ERROR: " + message)

        if halt_threshold == "error":
            print("")
            exit(1)

    @staticmethod
    def trace(message):
        Logger.log(2, message)

    @staticmethod
    def timestamp():
        return "[" + str(datetime.now()) + "]"
