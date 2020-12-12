import logging

def set_logger(string, stream=True, file=False):
    logger = logging.getLogger(string) 
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #fh = logging.FileHandler('debug.log')
    #fh.setLevel(logging.DEBUG)
    #logger.addHandler(fh)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger 