from typing import Optional 
import logging.config
import logging

def setup_logging(
    level: Optional[int] = logging.DEBUG, formater: str | None = "default"
) -> None:

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
                'formatter': formater , 
            }
            
        },
        'root': {
            'handlers': 'console',
            'level': level,
        },
    }
    
    logging.config.dictConfig(LOGGING_CONFIG)
    logging.getLogger(__name__).info("Logging initialized")
