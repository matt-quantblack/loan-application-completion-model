from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

from sklearn.exceptions import ConvergenceWarning
from sklearn.utils._testing import ignore_warnings


def cv_model(x, y, cv):
    lr = LogisticRegression()
    lr_scores = cross_val_score(lr, x, y, cv=cv)
    av_score = sum(lr_scores) / len(lr_scores)
    return  av_score

@ignore_warnings(category=ConvergenceWarning)
def determine_best_model_probabilities(x, y, cv):
    """ Uses stepwise backward feature selection with a cross validation metric used for
    determining the best set of features

    Args:
        x (pandas.DataFrame): The data in a pandas dataframe
        y (list like object): The response variable

    Returns:
        (float): The best cross validation score
        (list): List of probabilities for data belonging to best cluster
    """

    feature_list = x.columns

    best_score = cv_model(x, y, cv)
    best_list = feature_list.copy()


    improved = True

    while improved is True and len(feature_list) > 1:

        improved = False
        for feature in feature_list:
            temp_list = [f for f in feature_list if f != feature]
            score = cv_model(x[temp_list], y, cv)
            if score > best_score:
                best_score = score
                best_list = temp_list
                improved = True

        feature_list = best_list.copy()

    lr = LogisticRegression()
    lr.fit(x[feature_list], y)
    prob = lr.predict_proba(x[feature_list])
    prob_success = prob[:,1]

    return best_score, prob_success








