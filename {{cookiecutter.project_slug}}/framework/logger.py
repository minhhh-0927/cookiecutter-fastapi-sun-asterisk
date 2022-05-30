import logging
import os
import sys
from datetime import datetime
from time import gmtime, strftime

from logstash_async.handler import AsynchronousLogstashHandler
from loguru import logger

ENV: str = os.getenv("ENV")
LOGGING_FOLDER: str = os.getenv("LOGGING_FOLDER")
LOGGING_HTTP_FILENAME: str = os.getenv("LOGGING_HTTP_FILENAME")
LOGGING_ERROR_FILENAME: str = os.getenv("LOGGING_ERROR_FILENAME")
LOGGING_DEBUG_FILENAME: str = os.getenv("LOGGING_DEBUG_FILENAME")

# Logstash
LOGGING_LOGSTASH_HOST: str = os.getenv("LOGGING_LOGSTASH_HOST")
LOGGING_LOGSTASH_PORT: str = os.getenv("LOGGING_LOGSTASH_PORT")


class InterceptHandler(logging.Handler):

    def emit(self, record: logging.LogRecord):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def make_filter(name):
    def filter(record):
        return record["extra"].get("name") == name

    return filter


def get_logging_filepath(file_name):
    date = strftime("%Y-%m-%d", gmtime())
    return "{folder}/{env}-{date}-{file_name}".format(folder=LOGGING_FOLDER, env=ENV, date=date, file_name=file_name)


def init_logging_loguru():
    # disable handlers for specific uvicorn loggers
    for name in logging.root.manager.loggerDict:
        if name.startswith("uvicorn."):
            logging.getLogger(name).handlers = []

    # change handler for default uvicorn logger
    intercept_handler = InterceptHandler()
    logging.getLogger("uvicorn").handlers = [intercept_handler]

    logger.configure(
        handlers=[
            {"sink": sys.stdout, "level": logging.DEBUG}
        ]
    )

    http_logging_filepath = get_logging_filepath(LOGGING_HTTP_FILENAME)
    error_logging_filepath = get_logging_filepath(LOGGING_ERROR_FILENAME)
    debug_logging_filepath = get_logging_filepath(LOGGING_DEBUG_FILENAME)

    if http_logging_filepath:
        # logger.add(http_logging_filepath)
        logger.add(http_logging_filepath, rotation="100 MB", filter=make_filter("http"))
        logger.add(error_logging_filepath, rotation="100 MB", filter=make_filter("error"))
        logger.add(debug_logging_filepath, rotation="100 MB", filter=make_filter("debug"))


def init_logging_elk_stack():
    if not LOGGING_LOGSTASH_HOST or not LOGGING_LOGSTASH_PORT:
        raise Exception("Logstash config is not found in .env file!")
    # Get you a test logger
    logger = logging.getLogger('python-logstash-logger')
    # Set it to whatever level you want - default will be info
    logger.setLevel(logging.DEBUG)
    # Create a handler for it
    async_handler = AsynchronousLogstashHandler(LOGGING_LOGSTASH_HOST,
                                                int(LOGGING_LOGSTASH_PORT),
                                                database_path=None)
    # Add the handler to the logger
    logger.addHandler(async_handler)
