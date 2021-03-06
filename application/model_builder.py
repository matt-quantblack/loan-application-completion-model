from io import BytesIO
import gower
from sklearn_extra.cluster import KMedoids
from sklearn.metrics import silhouette_score
from xlsxwriter import Workbook
from application.file_manager import list_to_csv, csv_to_list, csv_to_list_from_bin_file
from application.ga_adapter import get_data
from application import logistic_regression_model
from application import random_forest_model
import pandas as pd
from sklearn.impute import KNNImputer
import numpy as np

MAX_NULL_PERCENT = 0.1  # Maximum number of nulls allowed in feature before it is excluded
MAX_VALUE_SET = 20  # Maximum number of values in a value set to prevent too many columns
CROSS_VAL_FOLDS = 10  # Number of cross validation folds to use
SUCCESS_VALUE = 100  # The value that indicates a success (client has vales from 0 to 100 with 100 being success)
MIN_SUCCESS_PROPORTION = 0.05  # Minimum number of successes in data set required to build a robust model


def update_data_template(data_template_path, fields):
    """Ensures the data template csv file stays updated with any changes or additions to data fields and types

        Args:
            data_template_path (string): filepath for the data template csv
            fields (list): The list of fields names and data types
        """

    # First get the data template csv data
    current_fields = csv_to_list(data_template_path)

    # Compare the data template with the passed fields to see if there are any changes
    changed = False

    # Go through the current fields first
    for index1 in range(len(current_fields)):
        field1 = current_fields[index1]

        # Find same field in the passed fields array
        for field2 in fields:
            if field1[0] == field2[0]:

                # Check the rest of the field line to see if there is a change
                if field1[1:] != field2[1:]:
                    # Update current fields if there is a change
                    current_fields[index1] = field2
                    changed = True

    # Now need to check if there are any new fields
    for field2 in fields:
        found = False

        # Check for a matching field name in current fields
        for field1 in current_fields:
            if field1[0] == field2[0]:
                found = True
                break
        # Append to the current fields because it doesn't exist
        if found is False:
            current_fields.append(field2)
            changed = True

    # If changes write whole file to csv again
    if changed:
        list_to_csv(current_fields, data_template_path)


def validate_types(df, fields):
    """ Validate and convert all data types used for modelling.

        Args:
            df (pandas.DataFrame): The data in a pandas dataframe
            fields (list): The list of fields names and data types

        Returns:
            (pandas.DataFrame): the modified dataframe with converted data types
        """

    # Go through each field and validate data based on the expected field type
    for field_info in fields:

        # Field name and type are stored in a list of length 2
        field_name = field_info[0]
        field_type = field_info[1]

        # First check field type is an accepted field
        if field_type not in ["Exclude", "Contact Details", "Numeric",
                              "Percentage", "Money", "Value Set", "Yes/No",
                              "String", "GA Merge Variable", "Response Variable"]:
            raise ValueError("Unknown variable type {} for field {}"
                             .format(field_type, field_name))

        # Numeric fields are any type of number
        elif field_type == "Numeric":

            # Might be sent as a string so convert to a float
            if df[field_name].dtype == object:
                df[field_name] = df[field_name].where(df[field_name] != '', np.nan)  #  Make sure we have a na for missing data
                df[field_name] = df[field_name].astype(float)

        # Percentage field is a number between 0 and 1 or between 1 and 100
        elif field_type == "Percentage":

            # Remove string representation of percentage
            if df[field_name].dtype == object:
                df[field_name] = df[field_name].str.replace("%", "")
                df[field_name] = df[field_name].where(df[field_name] != '', np.nan)  #  Make sure we have a na for missing data

                # Convert to a float
                df[field_name] = df[field_name].astype(float)

            # Determine if this is represented by a number from 0 to 1 or from 1 to 100
            max_val = max(df[field_name])
            min_val = min(df[field_name])

            # Multiply by 100 if values are between 0 and 1
            if min_val >= 0 and max_val <= 1:
                df[field_name] = df[field_name] * 100

            # Throw an error if values don't match percentage type
            if min_val < 0 or max_val > 100:
                raise ValueError("Percentage values must be between 0 and 1 or between 1 and 100 for field {}"
                                 .format(field_name))

        # Some data is sent as a string with a $ sign but needs to be a number
        elif field_type == "Money":
            # Remove string representation of money
            if df[field_name].dtype == object:
                df[field_name] = df[field_name].str.replace("$", "")
                df[field_name] = df[field_name].str.replace(",", "")
                df[field_name] = df[field_name].where(df[field_name] != '', np.nan)  #  Make sure we have a na for missing data

            # Convert to a float
            df[field_name] = df[field_name].astype(float)

        # Value set is a selection of predefined text values
        elif field_type == "Value Set":
            # Count how many unique values
            unique = len(df[field_name].unique())

            # Limit number of values in a value set to prevent huge number of columns in modelling
            if unique > MAX_VALUE_SET:
                raise ValueError("The maximum number of values in a Value Set is {}. The field {} has {}."
                                 .format(MAX_VALUE_SET, field_type, unique))

        # This is a boolean field but can also contain "No Data"
        elif field_type == "Yes/No":
            # Count how many unique values
            unique = len(df[field_name].unique())

            # Limit number of values in a Yes/No to prevent huge number of columns in modelling
            if unique > 3:
                raise ValueError("The maximum number of values in a Yes/No is 3. The field {} has {}."
                                 .format(field_type, unique))

        elif field_type == "Response Variable":
            if df[field_name].dtype == object:
                df[field_name] = df[field_name].str.replace('', '0')  # make sure we have a zero for missing data
                df[field_name] = df[field_name].astype(float)

    return df


def stripdown_features(df, fields):
    """This function splits the features and the response variable and removes columns that are not
        suitable for modelling.

        Args:
            df (pandas.DataFrame): The data in a pandas dataframe
            fields (list): The list of fields names and data types

        Returns:
            (pandas.DataFrame): the included features of the dataframe to be used for modelling
            (pandas.Series): the response variable
        """

    # Create a list of columns to drop
    cols_to_drop = []

    # Get the name of the response variable - should on be one otherwise throw error
    response_field_names = [x[0] for x in fields if x[1] == "Response Variable"]
    if len(response_field_names) != 1:
        raise ValueError("There must only be one response variable marked for the data set.")
    response_field_name = response_field_names[0]
    cols_to_drop.append(response_field_name)

    # Drop any rows where response variable is missing - response variable is required
    df = df.dropna(subset=[response_field_name])

    # Assign the y series to the response variable
    y = df[response_field_name]

    # Reassign y as a success or fail - success is 100 because application is 100% complete
    # Only if not in binary format
    if np.all(sorted(y.unique()) != [0, 1]):
        y = pd.Series(np.where(y >= SUCCESS_VALUE, 1, 0))

    # Remove contact fields
    contact_fields = [x[0] for x in fields if x[1] == "Contact Details"]
    cols_to_drop = cols_to_drop + contact_fields

    # Remove fields of type string and GA Merge Variable
    string_fields = [x[0] for x in fields if x[1] == "String" or x[1] == "GA Merge Variable" or x[1] == "Exclude"]
    cols_to_drop = cols_to_drop + string_fields

    # Remove fields with > 10% missing values
    # Count nulls in each column
    nulls = df.isna().sum()
    # Iterate through null count series
    for index, value in nulls.items():

        # Only check if not already dropping column
        if index not in cols_to_drop:

            # Calc percentage of nulls
            percent_nulls = value / df.shape[0]

            # Add field to fields to remove more than desired amount
            if percent_nulls > MAX_NULL_PERCENT:
                cols_to_drop.append(index)

    # Remove the fields that should be excluded
    new_df = df.drop(cols_to_drop, axis=1)

    # Remove the fields from the field data types list that we excluded
    fields = [field for field in fields if field[0] in new_df.columns]

    return new_df, y, fields


def impute_nulls(df, fields):
    """This function fills missing categorical data iwth "No Data" and Imputes missing numerical data with
    KNNImputer

        Args:
            df (pandas.DataFrame): The data in a pandas dataframe
            fields (list): The list of fields names and data types

        Returns:
            (pandas.DataFrame): the new imputed dataframe with no missing values
        """

    # Fill Value Set and the Yes/No data types with "No Data" as opposed to imputing categorical
    # data because the category of No Data makes more logical sense

    # Get the columns for categorical data
    cat_types = ["Value Set", "Yes/No"]
    cat_columns = [x[0] for x in fields if x[1] in cat_types]

    # Fill empty cells with NA then fill na with No Data
    df[cat_columns] = df[cat_columns].replace(r'^\s*$', pd.NA, regex=True)
    df[cat_columns] = df[cat_columns].fillna("No Data")

    # Only impute Numeric, Percentage, Money columns
    valid_types = ["Numeric", "Percentage", "Money"]
    valid_columns = [x[0] for x in fields if x[1] in valid_types]

    # Build a dataframe with just these columns
    imputer_df = df[valid_columns]

    # Do nothing if no columns to impute
    if imputer_df.shape[1] == 0:
        return df

    # Create a KNN Imputer with 6 neighbours
    imputer = KNNImputer(n_neighbors=6)

    # Impute the values
    results = imputer.fit_transform(imputer_df)

    # Covert back into a dataFrame so we maintain column mapping
    results_df = pd.DataFrame(results, columns=imputer_df.columns)

    # Overwrite the imputed columns with the results while maintaining untouched columns
    new_df = pd.DataFrame()
    for col_name in df.columns:
        if col_name in results_df.columns:
            new_df[col_name] = results_df[col_name]
        else:
            new_df[col_name] = df[col_name]

    return new_df


def encode_categorical(x, fields):
    """Uses pandas get_dummies to encode categorical data (Value Set and Yes/No)
    into more columns with  0 and 1

        Args:
            x (pandas.DataFrame): The data in a pandas dataframe
            fields (list): The list of fields names and data types

        Returns:
            (pandas.DataFrame): the new dataframe with encoded values
        """

    # Only encode fields that are Value Set or Yes/No
    # NOTE: Yes/No may also have a "Not Given" value
    columns = []
    for field in fields:
        if field[1] == "Value Set" or field[1] == "Yes/No":
            columns.append(field[0])

    # Encode categorical variables
    enc_df = pd.get_dummies(x, columns=columns, prefix=columns)

    return enc_df


def cluster(df, random_state=None):
    """Use Gower distances and K Medioids to cluster the data from between 2 to 8 clusters.
    Uses silhouette analysis to determine optimal number of clusters

        Args:
            df (pandas.DataFrame): The data in a pandas dataframe
            random_state (int): Can be sued to fix the random state - ideal for testing

        Returns:
            (array): an array of the cluster assignments
            (int): the number of clusters used
        """
    # Compute the Gower distance matrix
    # NOTE:large datasets will cause slow processing since array size is n2
    matrix = gower.gower_matrix(df)

    # Use silhouette analysis to determine the optimal number of clusters
    # between 2 and 8 clusters
    res = []
    for k in range(2, 9):

        #must have enough samples ie. k-1
        if k < len(matrix) - 1:
            k_medoids = KMedoids(n_clusters=k, random_state=random_state).fit(matrix)

            # Catch exceptions here and set the score to -1 (worst)
            try:
                silhouette_avg = silhouette_score(df, k_medoids.labels_)
                res.append([k, silhouette_avg])

            # If only one cluster causes an error so give worst score to this k
            except ValueError:
                res.append([k, -1])

    # Best cluster has the value closest to 1 from the range -1 to 1
    best_cluster = max(res, key=lambda x: x[1])

    # Refit with the best number of clusters
    k_medoids = KMedoids(n_clusters=best_cluster[0], random_state=random_state).fit(matrix)

    return k_medoids.labels_, best_cluster[0]


def determine_target_cluster(success_labels, cluster_labels, cluster_count):
    """Determines the target cluster by calculating % of successes (response variable) for each
    cluster. Returns the cluster index with the higher % success.

        Args:
            success_labels (numpy array): The response variable column
            cluster_labels (numpy array): the cluster labelling
            cluster_count (int): the number of clusters

        Returns:
            (int): the cluster with the highest successes
        """
    # Variables to remember which is the current highest cluster
    max_percentage = 0
    cluster_index = None

    # Iterate through all clusters
    for i in range(cluster_count):

        # Extract only the cases related to this cluster
        partial = success_labels[cluster_labels == i]

        # Determine successes ie. response variable equal to 1
        successes = len(partial[partial == 1])

        # Percentage of successes
        percentage = successes / len(partial)

        # Replace the current max if this is higher
        if percentage > max_percentage:
            max_percentage = percentage
            cluster_index = i

    # Return the cluster index that has the highest % Successes
    return cluster_index


def best_model_probabilities(x, cluster_labels, target_cluster, cv=CROSS_VAL_FOLDS, random_state=None):
    """Optimises a logistic regression model and a random forest model to determine which has the best
    cross validation score. The best model is used to predict the probabilities that a customer
    belongs to the cluster with the highest success in application completions

        Args:
            x (Pandas.DataFroma): The features
            cluster_labels (numpy array): the cluster labelling
            target_cluster (int): the cluster with the highes % application completions
            cv (int): the number of cross validation folds
            random_state (int): The random seed can be used for testing for consistent results

        Returns:
            (list): the probabilities that a customer belongs to the cluster with the highest success
        """

    # Adjust the response variable to be either 1 belongs to target cluster or 0 does not belong
    y = np.where(cluster_labels == target_cluster, 1, 0)

    # Try the logistic regression model
    lr_score, lr_prob = logistic_regression_model.determine_best_model_probabilities(x, y, cv)

    # Try the Random forest model
    rf_score, rf_prob = random_forest_model.determine_best_model_probabilities(x, y, cv, random_state)

    # Determine the best one and return the probabilities
    if rf_score > lr_score:
        return rf_prob
    else:
        return lr_prob


def merge_google_analytics(df, fields, ga_profile_id, ga_cred_file_location):
    """This function connects to the Hello API platform for google analytics, downloads and merges the data
    based on matching the dimension1 custom Google Analytics column and the Merge Data variable in the csv data set

            Args:
                df (pandas.DataFrame): the uploaded csv file in a dataframe
                fields (list): The list of fields and the field types that match the columns in df
                ga_profile_id (string): The google analytics profile id to extract the data from
                ga_cred_file_location (string): Location of the credentials file for Google Analytics

            Returns:
                (pandas.DataFrame): the merged data frame
                fields (list): updated fields list to include the new field items
            """

    # Check we have only one merge variable
    merge_fields = [x[0] for x in fields if x[1] == "GA Merge Variable"]

    if len(merge_fields) != 1:
        raise ValueError(
            "The supplied data must have exactly one field marked as GA Merge Variable or the Google Analytics \
            connection must be set to Exclude.")
    else:
        merge_field = merge_fields[0]

    # Get the data from the google analytics API
    results = get_data(ga_cred_file_location, ga_profile_id,
                       dimensions='ga:dimension1, ga:userType, ga:sessionCount, ga:sessionDurationBucket',
                       start_date='7daysAgo')

    # Convert into a dataframe
    cols = ["GA Merge Variable", "User Type", "Session Count", "Session Duration"]
    ga_df = pd.DataFrame(columns=cols)
    # Exclude the last column as this is just user_count metric
    for row in results["rows"]:
        ga_df = ga_df.append(pd.Series(row[:-1], index=cols), ignore_index=True)

    # Merge the data frame on the merge variable ie. user id
    df = pd.merge(df, ga_df, how="left", left_on=[merge_field], right_on=["GA Merge Variable"])
    df = df.drop(["GA Merge Variable"], axis=1)

    # Update the fields list to incorporate the datatypes of the new fields
    fields = fields + [["User Type", "Value Set"],
                       ["Session Count", "Numeric"],
                       ["Session Duration", "Numeric"]]

    return df, fields


def build_and_predict(file, data_template_path, fields, ga_profile_id, ga_cred_file_location = None):
    """This function starts by updating the data_templates with new field names if the exist
        then builds the model then predicts what are the best customers to follow up on

        Args:
            file (file): A csv file object
            data_template_path (string): filepath for the data template csv
            fields (list): The list of fields names and data types
            ga_profile_id (string): string representing the Google Analytics profile id to use or '0' for none
            ga_cred_file_location (string): storage location of the google analytics credentials file

        Returns:
            list: a list of customers and contact details
        """

    # Update data templates
    update_data_template(data_template_path, fields)

    # Get the names of the fields
    field_names = [x[0] for x in fields]
    contact_fields = [x[0] for x in fields if x[1] == "Contact Details"]

    # Throw an error if we don't have any contact details
    if len(contact_fields) == 0:
        raise ValueError("The supplied data must have at least one field marked as \
        Contact Details to identify customers")

    # Get the file contents as a dataframe
    data = csv_to_list_from_bin_file(file, header=False)
    df = pd.DataFrame(data, columns=field_names)

    # Merge data from Google Analytics if selected
    if ga_profile_id != '0' and ga_cred_file_location is not None:
        df, fields = merge_google_analytics(df, fields, ga_profile_id, ga_cred_file_location)

    # Convert data columns to correct type and check all types are valid
    df = validate_types(df, fields)

    # Determine what features to remove (if String type or if too many nulls)
    x, y, fields = stripdown_features(df, fields)

    # Make sure we have a number of successes to be able to run model
    if len(y[y == 1]) / len(y) < MIN_SUCCESS_PROPORTION:
        raise ValueError("There needs to be a minimum of {0:.0f}% completed applications\
         in the data set to build a robust model."
                         .format(MIN_SUCCESS_PROPORTION*100))

    # Fill missing Categorical data with "No Data" and use KNNImpute on numerical data
    x = impute_nulls(x, fields)

    # One hot encode categorical variables
    x = encode_categorical(x, fields)

    # Cluster Analysis to determine groups (including determining cluster count)
    cluster_labels, cluster_count = cluster(x)

    # Calculate cluster with highest % completion of applications
    best_cluster = determine_target_cluster(y, cluster_labels, cluster_count)

    # Build the best prediction model to predict which cluster client belongs to
    # The higher the probability the client belongs to the target cluster
    # the closer they are to the being the type of customer to complete an application
    prob = best_model_probabilities(x, cluster_labels, best_cluster)

    # Select only the contact details and probabilty scores from the dataframe
    df = df[contact_fields]
    df["Prob"] = prob

    # Select only the customers that have not completed the application
    df = df[y == 1]

    # Order the df by probability
    df = df.sort_values(by=["Prob"], axis=0, ascending=False)

    # Return the dataframe
    return df

def export_to_excel(customers):
    """Converts customer list data into a Microsoft Excel file and
    returns the file stream for downloading

        Args:
            customers (list): A list of customers with customer details on each line

        Returns:
            filestream: The excel file as a filestream for downloading
        """

    # Create an Microsoft Excel workbook and sheet
    output = BytesIO()
    book = Workbook(output)
    sheet = book.add_worksheet('Customer List')
    fields = []

    # Write the details of each customer in a row
    for row in range(len(customers)):
        customer = customers[row]

        if row == 0:
            fields = customer.keys()

            col = 0
            for field in fields:
                sheet.write(0, col, field)
                col += 1

        col = 0
        for field in fields:
            sheet.write(row+1, col, customer[field])
            col += 1

    # Set the columns width so it's easier to read.
    sheet.set_column('A:Z', 48)

    # Close the file and seek back to start of file
    book.close()
    output.seek(0)

    # Return the file stream
    return output
