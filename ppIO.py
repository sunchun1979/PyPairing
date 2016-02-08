import csv
import pandas

def read_round(filename):
    dframe = pandas.read_csv(filename)
    dframe = dframe.fillna("")
    return dframe

# def read_round(filename):
#     pT = []
#     with open(filename) as f:
#         next(f)
#         for i,line in enumerate(f):
#             lis = line.split(",")
#             id = int(lis[0])
#             name = lis[1]
#             rank = float(lis[2])
#             history = convert_history(lis[3].rstrip()[1:-1])
#             pT.append(ppType.PlayerTable(id,name,rank,history))
#     return pT
#
# def convert_history(raw_history):
#     gs = raw_history.split(";")
#     os = set()
#     for item in gs:
#         if (item!=""):
#             if (item.lower() != 'bye'):
#                 os.add(int(item[1:-1]))
#     return ppType.PlayerHistory(gs, os)
#
