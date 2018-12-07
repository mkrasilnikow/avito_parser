import logging

logger = logging.getLogger(__name__)


def convert(distance):
    try:
        dist = int(distance)
        return dist
    except ValueError:
        logger.warning("Cast distance to int")
        dist = float(distance) * 1000
        return int(dist)

