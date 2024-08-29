import logging.config

LOGGING_CONFIG_DICT = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "basic": {
            "format": "[%(levelname)s] %(asctime)s %(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "basic",
  
        }
    },
    "loggers": {
        "": {"handlers": ["console"],"level": "INFO",},
        },
}


logging.config.dictConfig(LOGGING_CONFIG_DICT)
