from datetime import datetime
from enum import Enum, IntEnum
from pathlib import Path

log_dir: str = "./logs/"          # Directory that logs will be written to
default_logfile: str = "log.txt"  # Filename for log file

class OutputMode(Enum):
    """The type of output the logger should produce"""
    terminal = 0
    file = 1

class MessageType(IntEnum):
    """The type of message logged"""
    trace = 0
    warning = 1
    error = 2

    def __str__(self):
        match self:
            case MessageType.trace:
                return "trace"
            case MessageType.warning:
                return "warning"
            case MessageType.error:
                return "error"

class Logger:
    """Logs messages to a specific output source and with a particular configuration."""
    def __init__(
            self,
            output_mode: OutputMode = OutputMode.terminal, # What output stream to log to
            halt_on: MessageType = MessageType.error,      # Program halts when any message of this type is logged
            verbosity: MessageType = MessageType.warning,  # The minimum message level to log
            log_path: str = default_logfile                # File where messages will be logged in file logging mode
    ):
        self.output_mode = output_mode
        self.halt_on = halt_on
        self.verbosity = verbosity

        if output_mode == OutputMode.file:
            Path(log_dir).mkdir(exist_ok=True)
            Path(log_dir + "/" + log_path).touch()
            self.logfile = open(log_dir + "/" + log_path, "a")
        else:
            self.logfile = None

    def log(self, message_type: MessageType, message: str):
        """Logs the given message if its volume is greater than the configured verbosity."""
        if message_type < self.verbosity:
            return

        if self.output_mode == OutputMode.terminal:
            print(Logger.prefix(message_type) + message)
        elif self.output_mode == OutputMode.file:
            if self.logfile is None:
                self.log(MessageType.error, "no open logfile")
            else:
                self.logfile.write("[" + str(datetime.now()) + "] " + Logger.prefix(message_type) + message + "\n")

    def will_halt(self, message_type: MessageType):
        """Called when execution is about to halt due to logged message above the threshold"""
        self.log(MessageType.trace, f"- HALTING ON {str(message_type).upper()}\n")
        if self.logfile is not None: self.logfile.close();

    @staticmethod
    def prefix(message_type: MessageType) -> str:
        """String prefix for messages of the given type"""
        if message_type == MessageType.warning:
            return "WARNING: "
        elif message_type == MessageType.error:
            return "ERROR: "

        return ""

# Base public logging functions

active_loggers: list[Logger] = [] # Loggers which will be logged to be public functions

def log_message(message_type: MessageType, message: str):
    """Logs a message of the given type and content to all loggers."""
    for logger in active_loggers:
        logger.log(message_type, message)

def log_exception(message_type: MessageType, exception: Exception):
    """Logs the given exception's string to all loggers and raises it if configuration indicates."""

    exc_string = exception.__class__.__name__ + ": " + str(exception)
    raise_exc: bool = False # Whether to raise the given exception or only log it
    for logger in active_loggers:
        logger.log(message_type, exc_string)
        if logger.halt_on <= message_type:
            raise_exc = True

    if raise_exc:
        for logger in active_loggers:
            logger.will_halt(message_type)

        raise exception

# Convenience logging functions

def trace(message: str):
    """Log a trace message."""
    log_message(MessageType.trace, message)

def warn(message: str):
    """Log a warning message."""
    log_message(MessageType.warning, message)

def error(exception: Exception):
    """Log an error with an exception."""
    log_exception(MessageType.error, exception)

# Default configurations

def configure_for_test(verbose: bool = False):
    """Assigns default logging configuration for test execution."""
    global active_loggers

    active_loggers = [
        Logger(OutputMode.terminal, MessageType.error, MessageType.trace if verbose else MessageType.warning),
        Logger(OutputMode.file, MessageType.error, MessageType.trace)
    ]

def configure_for_publish():
    """Assigns default logging configuration for publish execution"""
    global active_loggers

    active_loggers = [
        Logger(OutputMode.file, MessageType.error, MessageType.trace)
    ]
