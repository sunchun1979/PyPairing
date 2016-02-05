import pandas

def readRound(filename):
    df = pandas.read_csv(filename)
    df = df.fillna("")
    return df