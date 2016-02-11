import csv
import pandas

def read_round(filename):
    rawframe = pandas.read_csv(filename)
    rawframe = rawframe.fillna("")
    dframe = []
    begin = 0
    handicap = 0
    for i in range(0,len(rawframe)):
        if (rawframe['id'][i]=='='):
            dframe.append((handicap, rawframe.loc[begin:i-1].reset_index(drop=True)))
            begin = i+1
            handicap = 0
        elif (rawframe['id'][i]=='&'):
            dframe.append((handicap, rawframe.loc[begin:i-1].reset_index(drop=True)))
            begin = i+1
            handicap = 1
    dframe.append((handicap,rawframe.loc[begin:].reset_index(drop=True)))
    for df in dframe:
        df[1]['id'] = df[1]['id'].astype(int)
        df[1]['rank'] = df[1]['rank'].astype(float)
    return dframe

def print_pairing(pairing, dframe):
    pframe = pandas.DataFrame(columns=['Black','White'])
    for i in range(0, len(pairing)/2):
        bname = dframe['name'][pairing[2*i]]
        wname = dframe['name'][pairing[2*i+1]]
        pframe.loc[len(pframe)] = [bname,wname]
    return pframe