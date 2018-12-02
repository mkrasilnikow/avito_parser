import logging
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class Statistic(object):
    def __init__(self, skip_objects=None):
        self.skip_objects = skip_objects

    def perform_statistic(self, file):
        pass
