import logging 

LOG_FORMAT = "%(Levelname)s %(asctime)s - %(message)s"

def setup_logger(name, log_file,  level= logging.INFO):


    handler = logging.FileHandler(log_file)
    handler.setFormatter(LOG_FORMAT)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
    