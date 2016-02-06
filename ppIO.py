import pandas
import csv


def read_round(filename):

    df = pandas.read_csv(filename)
    df = df.fillna("")
    return df

