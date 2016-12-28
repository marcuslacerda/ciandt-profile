"""Logger Util."""
import logging


def initLogger(levelname='INFO'):
    """Init logger and setting log level."""
    FORMAT = '%(name)s %(levelname)-5s %(message)s'
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger('profile')
    logger.addHandler(logging.NullHandler())
    logger.setLevel(logging.getLevelName(levelname))
    logging.getLogger('elasticsearch').setLevel(logging.ERROR)
    logging.getLogger('googleapiclient.http').setLevel(logging.ERROR)
    logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

    return logger
