import csv
import pandas

def read_round(filename):
    rawframe = pandas.read_csv(filename)
    rawframe = rawframe.fillna("")
    dframe = []
    handicapInfo = [0]
    begin = 0
    for i in range(0,len(rawframe)):
        if (rawframe['id'][i]=='='):
            dframe.append(rawframe.loc[begin:i-1].reset_index(drop=True))
            begin = i+1
            handicapInfo.append(0)
        elif (rawframe['id'][i]=='&'):
            dframe.append(rawframe.loc[begin:i-1].reset_index(drop=True))
            begin = i+1
            handicapInfo.append(1)
    dframe.append(rawframe.loc[begin:].reset_index(drop=True))
    for df in dframe:
        df['id'] = df['id'].astype(int)
        df['rank'] = df['rank'].astype(float)
    return dframe, handicapInfo

def print_pairing(pairing, dframe):
    pframe = pandas.DataFrame(columns=['Black','White'])
    for i in range(0, len(pairing)/2):
        bname = dframe['name'][pairing[2*i]]
        wname = dframe['name'][pairing[2*i+1]]
        pframe.loc[len(pframe)] = [bname,wname]
    return pframe