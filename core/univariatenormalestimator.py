from sys import float_info
import math
from core import utils

class UnivariateNormalEstimator(object):
    """docstring for UnivariateNormalEstimator"""
    def __init__(self):
        self._weighted_sum = 0
        self._weighted_sum_squared = 0
        self._sum_of_weights = 0
        self._mean = 0
        self._variance = float_info.max
        self._min_var = 1e-12
        self.CONST = math.log(2 * math.pi)

    def __str__(self):
        self.update_mean_and_variance()
        return 'Mean: {0}, Variance: {1}'.format(self._mean, self._variance)

    def add_value(self, value, weight):
        self._weighted_sum += value * weight
        self._weighted_sum_squared += value * value * weight
        self._sum_of_weights += weight

    def update_mean_and_variance(self):
        self._mean = 0
        if self._sum_of_weights > 0:
            self._mean = self._weighted_sum / self._sum_of_weights

        self._variance = float_info.max
        if self._sum_of_weights > 0:
            self._variance = self._weighted_sum_squared / self._sum_of_weights - self._mean * self._mean

        if self._variance <= self._min_var:
            self._variance = self._min_var

    def predict_intervals(self, conf):
        self.update_mean_and_variance()
        val = utils.normal_inverse(1.0 - (1.0 - conf) / 2.0)
        arr = [[self._mean + val * math.sqrt(self._variance)],
            [self._mean - val * math.sqrt(self._variance)]]
        return arr

    def predict_quantile(self, percentage):
        self.update_mean_and_variance()
        return self._mean + utils.normal_inverse(percentage) * math.sqrt(self._variance)

    def log_density(self, value):
        self.update_mean_and_variance()
        val = -0.5 * (self.CONST + math.log(self._variance) + (value - self._mean) *
            (value - self._mean) / self._variance)
        return val
