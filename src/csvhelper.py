import csv


def readdata(filepath, type):
    "Reads data from a CSV file into a named tuple, expecting the first line to be the header."
    with open(filepath) as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # skip header
        return [type(*row) for row in reader]

