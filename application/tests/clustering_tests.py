import pandas as pd
import numpy as np
from application import model_builder

def test_cluster():

    # Arrange
    df = pd.DataFrame()
    df["Some Feature"] = [30.0, 40.0, 50.0, 50, 49, 29]
    df["Some Feature 2"] = [5, 6, 6, 6, 5.9, 4.9]
    df["Some Feature 3"] = [100, 90, 90, 91, 90, 101]
    df["Answer"] = [0, 1, 1, 1, 1, 0]

    # Act - Data is arranged to have 2 extreme clusters to force predictable results
    cluster_labels, cluster_count = list(model_builder.cluster(df, random_state=0))

    # Assert
    assert list(cluster_labels) == [0, 1, 1, 1, 1, 0]
    assert cluster_count == 2

def test_determine_target_cluster_success():

    # Arrange
    success = pd.Series([0, 1, 1, 1, 0, 1]).to_numpy()
    cluster_labels = np.array([0, 1, 1, 1, 1, 0])

    # Act
    cluster_index = model_builder.determine_target_cluster(success, cluster_labels, 2)

    # Assert
    assert cluster_index == 1




def test_determine_best_prediction_model():
    # Arrange
    cluster_labels = np.array([0, 1, 1, 1, 1, 0])
    df = pd.DataFrame()
    df["Some Feature"] = [30.0, 40.0, 50.0, 50, 49, 29]
    df["Some Feature 2"] = [5, 6, 6, 6, 5.9, 4.9]
    df["Some Feature 3"] = [100, 90, 90, 91, 90, 101]

    # Act
    res = model_builder.best_model_probabilities(df[["Some Feature", "Some Feature 2", "Some Feature 3"]],
                                                 cluster_labels,
                                                 target_cluster=1,
                                                 cv=2,
                                                 random_state=0)

    # Assert
    assert list(res) == [0.022479815774238823,
                         0.9693793666985705,
                         0.9992511098930831,
                         0.9989427243019453,
                         0.9989079413299201,
                         0.011039884561524096]
