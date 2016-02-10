import csv
import pandas

def read_round(filename):
    dframe = pandas.read_csv(filename)
    dframe = dframe.fillna("")
    return dframe

def print_pairing(pairing, dframe):
    pframe = pandas.DataFrame(columns=['Black','White'])
    for i in range(0, len(pairing)/2):
        bname = dframe['name'][pairing[2*i]]
        wname = dframe['name'][pairing[2*i+1]]
        pframe.loc[len(pframe)] = [bname,wname]
    return pframe