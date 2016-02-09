import csv
import pandas

def read_round(filename):
    dframe = pandas.read_csv(filename)
    dframe = dframe.fillna("")
    return dframe
