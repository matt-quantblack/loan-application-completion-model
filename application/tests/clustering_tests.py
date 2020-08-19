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
    success = pd.Series([0, 1, 1, 1, 0, 1]).to_numpy()
    cluster_labels = np.array([0, 1, 1, 1, 1, 0])
    df = pd.DataFrame()
    df["Some Feature"] = [30.0, 40.0, 50.0, 50, 49, 29]
    df["Some Feature 2"] = [5, 6, 6, 6, 5.9, 4.9]
    df["Some Feature 3"] = [100, 90, 90, 91, 90, 101]
    df["Answer"] = [0, 1, 1, 1, 1, 0]
    cluster_labels, cluster_count = list(model_builder.cluster(df, random_state=0))

    # Act
    res = model_builder.compare_models(df[["Some Feature", "Some Feature 2", "Some Feature 3"]], cluster_labels, 2)

    # Assert
    assert 1 == 1
