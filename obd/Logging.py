import logging 

def setup_logger( log_file,  level= logging.INFO):

    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(levelname)s %(asctime)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(level)
    logger.addHandler(handler)
    
    return logger

def info_logger(txt):
    log = setup_logger("debugging.log")
    log.info(txt)

def debug_logger(txt):
    log = setup_logger("debugging.log", logging.DEBUG)
    log.debug(txt)

def warn_logger(txt):
    log = setup_logger("debugging.log")
    log.warn(txt)

def crit_logger(txt):
    log = setup_logger("debugging.log")
    log.critical(txt)

