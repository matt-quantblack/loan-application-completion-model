from sklearn.datasets import make_friedman1
from application import logistic_regression_model
from application import random_forest_model
import pandas as pd
import numpy as np
import math

def test_logistic_regression():


    # Arrange
    x, y = make_friedman1(n_samples=50, n_features=10, random_state=0)

    df = pd.DataFrame(x)
    y = np.where(y > np.median(y), 1, 0)  # probability of belonging to target cluster

    # Act
    best_score, prob = logistic_regression_model.determine_best_model_probabilities(df, y, 10)

    # Assert
    assert math.isclose(best_score, 0.82, rel_tol=1e-5, abs_tol=0.0)
    assert len(prob) == len(y)


def test_random_forest():

    # Arrange
    x, y = make_friedman1(n_samples=50, n_features=10, random_state=0)

    df = pd.DataFrame(x)
    y = np.where(y > np.median(y), 1, 0)  # probability of belonging to target cluster

    # Act
    best_score, prob = random_forest_model.determine_best_model_probabilities(df, y,
                                                                              cv=10,
                                                                              random_state=0)

    # Assert
    assert math.isclose(best_score, 0.8, rel_tol=1e-5, abs_tol=0.0)
    assert len(prob) == len(y)
