
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV


def determine_best_model_probabilities(x, y, cv, random_state = None):
    """ Uses stepwise backward feature selection with a cross validation metric used for
    determining the best set of features

    Args:
        x (pandas.DataFrame): The data in a pandas dataframe
        y (list like object): The response variable
        cv (int): The number of cross validations to use
        random_state (int): random seed to use to get consistent results for testing

    Returns:
        (float): The best cross validation score
        (list): List of probabilities for data belonging to best cluster
    """

    # Create the parameter grid of suitable parameters to search
    param_grid = {
        'max_depth': [30, 90, 180],
        'max_features': [2, 3],
        'n_estimators': [100, 300, 1000]
    }

    # Create a based model
    model = RandomForestClassifier(random_state=random_state)

    # Instantiate the grid search model
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid,
                               cv=cv, n_jobs=-1)

    # Fit the grid search to the data
    grid_search.fit(x, y)

    # Get the best cross val score
    best_score = grid_search.best_score_

    # Create the model with the best params
    model = grid_search.best_estimator_

    # Fit on training data
    model.fit(x, y)

    # Make predictions on probability
    prob = model.predict_proba(x)
    prob_success = prob[:, 1]

    return best_score, prob_success








