from application import model_builder
import pandas as pd

def test_ga_data_extraction_intergration():


    # Arrange
    fields = [["User Id", "GA Merge Variable"],
              ["Dependants", "Numeric"],
              ["Another Feature", "Numeric"]]
    profile_id = '224136010'
    cred_file = 'google_analytics_cred.json'
    cols = ["User Id", "Dependants", "Another Feature"]
    df = pd.DataFrame(columns=cols)
    df = df.append(pd.Series(["55", 4, 5], index=cols), ignore_index=True)
    df = df.append(pd.Series(["1598233913226", 4, 6], index=cols), ignore_index=True)
    df = df.append(pd.Series(["15", 4, 6], index=cols), ignore_index=True)

    # Act
    df, fields = model_builder.merge_google_analytics(df, fields, profile_id, cred_file)

    # Assert
    assert list(df.shape) == [3, 6]
    assert len(fields) == 6

