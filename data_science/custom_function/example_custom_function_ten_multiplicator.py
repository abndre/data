import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class TenMultiplier(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X * 10

"""
multiplier = TenMultiplier()

X = np.array([6, 3, 7, 4, 7])
multiplier.transform(X)

array([60, 30, 70, 40, 70])
"""


