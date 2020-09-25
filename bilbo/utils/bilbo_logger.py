import logging 

def get_logger(verbosity=1, name = 'BILBO'):
    logger = logging.getLogger(name)
    level = logging_level(verbosity)
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=level, datefmt='%d-%b-%y %H:%M:%S')
    return logger


def logging_level(verbosity):
    """ Converts a verbosity number to a logging level

    Args:
    verbosity - a number, possibly collected from ``argparse``'s ``count``
    action. If ``verbosity`` is out of the range of possible logging levels
    it will be normalized to the nearest level. Does not take into
    consideration custom levels.
    """
    levels = [
        logging.CRITICAL,
        logging.ERROR,
        logging.WARNING,
        logging.INFO,
        logging.DEBUG
    ]
    return levels[max(min(len(levels) - 1, verbosity), 0)]
