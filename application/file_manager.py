import os
from io import StringIO
import csv


def csv_to_list(filepath):
    """Reads a list from a csv file

        Args:
            filepath: Full path of file to write to

        Returns:
            list: the list of rows as a list of cells
        """
    rows = []

    # Open the file and use csv reader to parse
    with open(filepath, newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')

        # Build into a list of rows
        for row in reader:
            rows.append(row)

    # Return the csv file as a list
    return rows


def csv_to_list_from_bin_file(file, header=True):
    """Reads a list from a binary stream

        Args:
            file: The file object
            header (bool): indicates if the file has a header line

        Returns:
            list: the list of rows as a list of cells
        """

    # Read the file decoding with utf-8
    as_str = file.read().decode("utf-8")

    # Create a string IO
    fp = StringIO(as_str)

    # Read the file using the csv reader
    reader = csv.reader(fp, delimiter=',', quotechar='"')

    rows = []

    # Append each row as a list of cells to the rows list
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

    # Uses the csv writer to write the list to file storage
    with open(filepath, 'w', newline='') as csv_file:
        wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        for line in data:
            wr.writerow(line)


def remove_ga_credentials_file(filepath):
    """ Removes a file that exists at filepath

        Args:
            filepath: Full path of file to remove
        """
    os.remove(filepath)


def update_ga_credentials_file(file, filepath):
    """ Replaces the file at filepath

        Args:
            file (file): File object to save
            filepath (string): Full path of file to remove
        """
    file.save(filepath)


def file_exists(filepath):
    """ Checks if the file exists at the filepath

        Args:
            filepath: Full path of file to check

        Returns (bool): True if found
        """
    return os.path.isfile(filepath)
