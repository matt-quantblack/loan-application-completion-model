from io import BytesIO

from xlsxwriter import Workbook

from application.file_manager import list_to_csv, csv_to_list, csv_to_list_from_bin_file
import pandas as pd

def update_data_template(data_template_path, fields):
    """Ensures the data template csv file stays updated with any changes or additions to data fields and types

        Args:
            data_template_path (string): filepath for the data template csv
            fields (list): The list of fields names and data types

        Returns:
            list: a list of customers and contact details
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
        #check for a matching field name in current fields
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


def build_and_predict(file, data_template_path, fields, connect_ga):
    """This function starts by updating the data_templates with new field names if the exist
        then builds the model then predicts what are the best customers to follow up on

            Args:
                file (file): A csv file object
                data_template_path (string): filepath for the data template csv
                fields (list): The list of fields names and data types
                connect_ga (string): string representing the Google Analytics profile to use or 'Exclude' for none

            Returns:
                list: a list of customers and contact details
            """

    # Update data templates
    update_data_template(data_template_path, fields)

    # Get the names of the fields
    field_names = [x[0] for x in fields]
    contact_fields = [x[0] for x in fields if x[1] == "Contact Details"]

    # Get the file contents as a list
    data = csv_to_list_from_bin_file(file, header=False)
    df = pd.DataFrame(data, columns=field_names)

    #hack to generate a fake list of customers for testing
    from random import random
    r = []
    for i in range(len(df.index)):
        r.append(round(random(), 2))
    df["Prob"] = r
    df = df.sort_values(by="Prob", ascending=False)
    df = df[:35]

    #Select only the contact details and probabilty scores from the dataframe
    df = df[contact_fields + ["Prob"]]

    #return the dataframe
    return df

def export_to_excel(customers):

    output = BytesIO()

    book = Workbook(output)
    sheet = book.add_worksheet('Customer List')

    fields = []

    #write the details of each customer in a row
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

    book.close()

    output.seek(0)

    return output