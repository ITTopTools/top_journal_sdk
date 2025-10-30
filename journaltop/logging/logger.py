import logging.config
import os


def setup_logging():

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    log_dir = os.path.join(base_dir, "src", "logging", "logs")
    os.makedirs(log_dir, exist_ok=True)

    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,

        'formatters': {
            'default': {
                'format': "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                'datefmt': "%H:%M:%S"
            },
            'full': {
                'format': (
                    "%(asctime)s.%(msecs)03d "
                    "[%(levelname)s] "
                    "%(name)s | %(module)s.%(funcName)s():%(lineno)d "
                    "[PID:%(process)d | TID:%(threadName)s] — %(message)s"
                ),
                'datefmt': "%Y-%m-%d %H:%M:%S"
            }
        },

        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
            },
            'file': {
                'class': 'logging.FileHandler',
                'filename': os.path.join(log_dir, 'app.log'),
                'formatter': 'default',
                'encoding': 'utf-8',
            },
            'file-verbose': {
                'class': 'logging.FileHandler',
                'filename': os.path.join(log_dir, 'app-verbose.log'),
                'formatter': 'full',
                'encoding': 'utf-8',
            },
        },

        'root': {
            'handlers': ['console', 'file', 'file-verbose'],
            'level': 'DEBUG',
        },
    }

    logging.config.dictConfig(LOGGING_CONFIG)
    logging.getLogger(__name__).debug("Logging initialized (logs in ./src/logging/logs)")
