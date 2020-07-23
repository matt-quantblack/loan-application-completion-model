import os
from io import StringIO
import csv

def csv_to_list(filepath):
    """Reads a list from a csv file

        Args:
            filepath: Full path of file to write to
        """
    rows = []

    with open(filepath, newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')

        for row in reader:
            rows.append(row)

    #return the csv file as a list
    return rows

def csv_to_list_from_bin_file(file, header=True):

    str = file.read().decode("utf-8")
    fp = StringIO(str)
    reader = csv.reader(fp, delimiter=',', quotechar='"')

    rows = []

    for row in reader:
        rows.append(row)

    # return the csv file as a list
    if header or len(rows) == 0:
        return rows
    else:
        return rows[1:]

def list_to_csv(data, filepath):
    """Writes a list to a csv file

        Args:
            data: A list of lists
            filepath: Full path of file to write to
        """

    with open(filepath, 'w', newline='') as csv_file:
        wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        for line in data:
            wr.writerow(line)



def update_ga_credentials_file(file, filepath):
    file.save(filepath)


def file_exists(filename):
    return os.path.isfile(filename)
