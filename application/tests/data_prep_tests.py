import pandas as pd
import pytest
from pandas.testing import assert_frame_equal, assert_series_equal
from application import model_builder


def test_validate_types_numeric_success():

    # Arrange
    df = pd.DataFrame()
    new_expect = pd.DataFrame()
    new_expect["Some Feature"] = [3, 4, 5]
    new_expect["Answer"] = [1, 2, 3]
    df["Some Feature"] = new_expect["Some Feature"]
    df["Answer"] = new_expect["Answer"]
    fields = [["Some Feature", "Numeric"],
              ["Answer", "Response Variable"]]

    # Act
    x = model_builder.validate_types(df, fields)

    # Assert
    assert_frame_equal(x, new_expect, check_dtype=False)

def test_validate_types_numeric_string_converts_success():

    # Arrange
    df = pd.DataFrame()
    new_expect = pd.DataFrame()
    new_expect["Some Feature"] = [3, 4, 5]
    new_expect["Answer"] = [1, 2, 3]
    df["Some Feature"] = ["3", "4", "5"]
    df["Answer"] = new_expect["Answer"]
    fields = [["Some Feature", "Numeric"],
              ["Answer", "Response Variable"]]

    # Act
    x = model_builder.validate_types(df, fields)

    # Assert
    assert_frame_equal(x, new_expect, check_dtype=False)

def test_validate_types_numeric_string_converts_throws_error():

    # Arrange
    df = pd.DataFrame()
    df["Some Feature"] = ["3d", "4d", "5d"]
    df["Answer"] = [1, 2, 3]
    fields = [["Some Feature", "Numeric"],
              ["Answer", "Response Variable"]]

    # Act and Assert
    with pytest.raises(ValueError):
        model_builder.validate_types(df, fields)


def test_validate_types_percentage_converts_throws_value_error():

    # Arrange
    df = pd.DataFrame()
    df["Some Feature"] = ["0.3s c", "0.4", "0.5"]
    df["Answer"] = [1, 2, 3]
    fields = [["Some Feature", "Percentage"],
              ["Answer", "Response Variable"]]

    # Act and Assert
    with pytest.raises(ValueError):
        model_builder.validate_types(df, fields)


def test_validate_types_percentage_converts_success():

    # Arrange
    df = pd.DataFrame()
    new_expect = pd.DataFrame()
    new_expect["Some Feature"] = [30.0, 40.0, 50.0]
    new_expect["Some Feature 2"] = [30.0, 40.0, 50.0]
    new_expect["Some Feature 3"] = [30.0, 40.0, 50.0]
    new_expect["Answer"] = [1, 2, 3]
    df["Some Feature"] = [0.3, 0.4, 0.5]
    df["Some Feature 2"] = ["0.3%", "0.4 %", " 0.5  %"]
    df["Some Feature 3"] = ["30", "40", " 50"]
    df["Answer"] = new_expect["Answer"]
    fields = [["Some Feature", "Percentage"],
              ["Some Feature 2", "Percentage"],
              ["Some Feature 3", "Percentage"],
              ["Answer", "Response Variable"]]

    # Act
    x = model_builder.validate_types(df, fields)

    # Assert
    assert_frame_equal(x, new_expect, check_dtype=False)


def test_validate_types_money_converts_throws_value_error():
    # Arrange
    df = pd.DataFrame()
    df["Some Feature"] = ["0.3s$", "$0.4", "0.5"]
    df["Answer"] = [1, 2, 3]
    fields = [["Some Feature", "Money"],
              ["Answer", "Response Variable"]]

    # Act and Assert
    with pytest.raises(ValueError):
        model_builder.validate_types(df, fields)


def test_validate_types_percentage_converts_success():
    # Arrange
    df = pd.DataFrame()
    new_expect = pd.DataFrame()
    new_expect["Some Feature"] = [30.0, 40.0, 50.0]
    new_expect["Some Feature 2"] = [30.0, 40.0, 50.0]
    new_expect["Some Feature 3"] = [50000, 40000.0, 50000]
    new_expect["Answer"] = [1, 2, 3]
    df["Some Feature"] = [30, 40, 50]
    df["Some Feature 2"] = ["$30", "$  40 ", "   $50 "]
    df["Some Feature 3"] = ["$50,000", "40000", " 50,000"]
    df["Answer"] = new_expect["Answer"]
    fields = [["Some Feature", "Money"],
              ["Some Feature 2", "Money"],
              ["Some Feature 3", "Money"],
              ["Answer", "Response Variable"]]

    # Act
    x = model_builder.validate_types(df, fields)

    # Assert
    assert_frame_equal(x, new_expect, check_dtype=False)


def test_validate_types_value_set_success():
    # Arrange
    df = pd.DataFrame()
    new_expect = pd.DataFrame()
    new_expect["Some Feature"] = ["Married", "Single", "Married"]
    new_expect["Answer"] = [1, 2, 3]
    df["Some Feature"] = new_expect["Some Feature"]
    df["Answer"] = new_expect["Answer"]
    fields = [["Some Feature", "Value Set"],
              ["Answer", "Response Variable"]]

    # Act
    x = model_builder.validate_types(df, fields)

    # Assert
    assert_frame_equal(x, new_expect, check_dtype=False)


def test_validate_types_value_set_throws_value_exception_too_many_values():
    # Arrange
    df = pd.DataFrame()
    df["Some Feature"] = range(1, 2000)
    df["Answer"] = range(1, 2000)
    fields = [["Some Feature", "Value Set"],
              ["Answer", "Response Variable"]]

    # Act and Assert
    with pytest.raises(ValueError):
        model_builder.validate_types(df, fields)


def test_validate_types_yes_no_success():
    # Arrange
    df = pd.DataFrame()
    new_expect = pd.DataFrame()
    new_expect["Some Feature"] = ["Yes", "No", "No Data"]
    new_expect["Answer"] = [1, 2, 3]
    df["Some Feature"] = new_expect["Some Feature"]
    df["Answer"] = new_expect["Answer"]
    fields = [["Some Feature", "Yes/No"],
              ["Answer", "Response Variable"]]

    # Act
    x = model_builder.validate_types(df, fields)

    # Assert
    assert_frame_equal(x, new_expect, check_dtype=False)


def test_validate_types_yes_no_throws_value_exception_too_many_values():

    # Arrange
    df = pd.DataFrame()
    df["Some Feature"] = range(1, 5)
    df["Answer"] = range(1, 5)
    fields = [["Some Feature", "Yes/No"],
              ["Answer", "Response Variable"]]

    # Act and Assert
    with pytest.raises(ValueError):
        model_builder.validate_types(df, fields)


def test_validate_types_invalid_field_type():

    # Arrange
    df = pd.DataFrame()
    df["Some Feature"] = range(1, 5)
    df["Answer"] = range(1, 5)
    fields = [["Some Feature", "Invalid Type"],
              ["Answer", "Response Variable"]]

    # Act and Assert
    with pytest.raises(ValueError):
        model_builder.validate_types(df, fields)

def test_stripdown_splits_x_variables():

    # Arrange
    df = pd.DataFrame()
    x_expect = pd.DataFrame()
    x_expect["Some Feature"] = [3, 4, 5]
    df["Some Feature"] = x_expect["Some Feature"]
    df["Answer"] = [1, 2, 3]
    fields = [["Some Feature", "Numeric"], ["Answer", "Response Variable"]]

    # Act
    x, y = model_builder.stripdown_features(df, fields)

    # Assert
    assert_frame_equal(x, x_expect)

def test_stripdown_splits_response_variable_works():

    # Arrange
    df = pd.DataFrame()
    y_expect = pd.Series([1, 2, 3], name="Answer")
    df["Some Feature"] = [3, 4, 5]
    df["Answer"] = y_expect
    fields = [["Some Feature", "Numeric"], ["Answer", "Response Variable"]]

    # Act
    x, y = model_builder.stripdown_features(df, fields)

    # Assert
    assert_series_equal(y, y_expect)


def test_stripdown_removes_contact_details():

    # Arrange
    df = pd.DataFrame()
    x_expect = pd.DataFrame()
    x_expect["Some Feature"] = [3, 4, 5]
    df["Some Feature"] = x_expect["Some Feature"]
    df["Contacts1"] = ["tom", "john", "sarah"]
    df["Contacts2"] = ["tom", "john", "sarah"]
    df["Answer"] = [1, 2, 3]
    fields = [["Some Feature", "Numeric"], ["Answer", "Response Variable"],
              ["Contacts1", "Contact Details"], ["Contacts2", "Contact Details"]]

    # Act
    x, y = model_builder.stripdown_features(df, fields)

    # Assert
    assert_frame_equal(x, x_expect)


def test_stripdown_removes_string_fields():

    # Arrange
    df = pd.DataFrame()
    x_expect = pd.DataFrame()
    x_expect["Some Feature"] = [3, 4, 5]
    df["Some Feature"] = x_expect["Some Feature"]
    df["Postcodes"] = ["2104", "2000", "2756"]
    df["Answer"] = [1, 2, 3]
    fields = [["Some Feature", "Numeric"], ["Answer", "Response Variable"],
              ["Postcodes", "String"]]

    # Act
    x, y = model_builder.stripdown_features(df, fields)

    # Assert
    assert_frame_equal(x, x_expect)


def test_stripdown_removes_columns_with_many_nulls_fields():

    # Arrange
    df = pd.DataFrame()
    x_expect = pd.DataFrame()
    x_expect["Some Feature"] = range(1, 12)
    df["Some Feature"] = x_expect["Some Feature"]
    df["A lot of Nulls"] = [None, 1, 2, 3, 4, 5, 6, 7, 8, None, 9]
    df["Answer"] = range(1, 12)
    fields = [["Some Feature", "Numeric"], ["Answer", "Response Variable"],
              ["A lot of Nulls", "Numeric"]]

    # Act
    x, y = model_builder.stripdown_features(df, fields)

    # Assert
    assert_frame_equal(x, x_expect)


def test_stripdown_doesnt_remove_columns_with_some_nulls():

    # Arrange
    df = pd.DataFrame()
    x_expect = pd.DataFrame()
    x_expect["Some Feature"] = range(1, 12)
    x_expect["A lot of Nulls"] = [None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    df["Some Feature"] = x_expect["Some Feature"]
    df["A lot of Nulls"] = x_expect["A lot of Nulls"]
    df["Answer"] = range(1, 12)
    fields = [["Some Feature", "Numeric"], ["Answer", "Response Variable"],
              ["A lot of Nulls", "Numeric"]]

    # Act
    x, y = model_builder.stripdown_features(df, fields)

    # Assert
    assert_frame_equal(x, x_expect)


def test_knn_imputer_fills_nulls_on_numeric():

    # Arrange
    df = pd.DataFrame()
    df["Some Feature"] = range(1, 12)
    df["A lot of Nulls"] = [None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    df["Answer"] = range(1, 12)
    fields = [["Some Feature", "Numeric"], ["Answer", "Response Variable"],
              ["A lot of Nulls", "Numeric"]]

    # Act
    new_df = model_builder.impute_nulls(df, fields)

    # Assert
    assert new_df["A lot of Nulls"].isna().sum() == 0


def test_knn_imputer_does_nothing_if_not_numeric():

    # Arrange
    df = pd.DataFrame()
    df["Some Feature"] = range(1, 12)
    df["Some Feature 2"] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    df["Answer"] = range(1, 12)
    fields = [["Some Feature", "Value Set"], ["Answer", "Response Variable"],
              ["Some Feature 2", "Value Set"]]

    # Act
    new_df = model_builder.impute_nulls(df, fields)

    # Assert
    assert_frame_equal(df, new_df)


def test_knn_imputer_with_value_set():

    # Arrange
    df = pd.DataFrame()
    df["Some Feature"] = ["Single", None, "", "Married", "Married", "Married", pd.NA, "Married"]
    df["Numeric Feature"] = [None, 1, 2, 3, 4, 5, 6, 7]
    df["Answer"] = range(1, 9)
    fields = [["Some Feature", "Value Set"], ["Answer", "Response Variable"],
              ["Numeric Feature", "Numeric"]]

    # Act
    new_df = model_builder.impute_nulls(df, fields)

    # Assert
    assert new_df["Some Feature"].isna().sum() == 0
    assert len(new_df[new_df["Some Feature"] == '']) == 0
    assert new_df["Numeric Feature"].isna().sum() == 0


def test_knn_imputer_with_yes_no():

    # Arrange
    df = pd.DataFrame()
    df["Some Feature"] = ["Yes", None, "", "No", pd.NA, "Yes"]
    df["Numeric Feature"] = [None, 1, 2, 3, 4, 5]
    df["Answer"] = range(1, 7)
    fields = [["Some Feature", "Yes/No"], ["Answer", "Response Variable"],
              ["Numeric Feature", "Numeric"]]

    # Act
    new_df = model_builder.impute_nulls(df, fields)

    # Assert
    assert new_df["Some Feature"].isna().sum() == 0
    assert len(new_df[new_df["Some Feature"] == '']) == 0
    assert new_df["Numeric Feature"].isna().sum() == 0


def test_categorical_encoding():

    # Arrange
    fields = [["Cat", "Yes/No"], ["Cat2", "Value Set"],
              ["Some Feature 3", "Numeric"]]
    df = pd.DataFrame()
    df["Cat"] = ["Yes", "No", "Maybe", "Yes", "Yes", "No"]
    df["Cat2"] = ["Yes2", "No2", "Maybe2", "Yes2", "Yes2", "No2"]
    df["Some Feature 3"] = [100, 90, 90, 91, 90, 101]

    # Act
    x = model_builder.encode_categorical(df, fields)

    # Assert
    assert list(x.columns) == ["Some Feature 3", "Cat_Maybe", "Cat_No", "Cat_Yes", "Cat2_Maybe2", "Cat2_No2", "Cat2_Yes2"]
