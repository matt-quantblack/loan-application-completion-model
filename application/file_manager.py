import os
import csv

def csv_to_list(template_location):

    rows = []

    with open(template_location, newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')

        for row in reader:
            rows.append(row)

    #return the csv file as a list
    return rows



def update_ga_credentials_file(file, filepath):
    file.save(filepath)


def file_exists(filename):
    return os.path.isfile(filename)
