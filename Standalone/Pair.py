import getopt
import random
import sys

import pandas

import MMS


def main(argv):
    inputFile = ''
    outputFile = '_output.txt'
    round = -1
    try:
        opts, args = getopt.getopt(argv, "hr:i:o:",["help","round=","input=","output="])
    except getopt.GetoptError:
        print "Pair.py -i <standing file> -o <pairing file>"
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print "Pair.py -i <standing file> -o <pairing file>"
            sys.exit()
        elif opt in ("-i", "--input"):
            inputFile = arg
        elif opt in ("-o", "--output"):
            outputFile = arg
        elif opt in ("-r", "--round"):
            round = int(arg)

    if (round == -1):
        print "Please specify round by -r"
        sys.exit(2)
    if (inputFile==""):
        print "Please specify input file by -i"
        sys.exit(2)
    print "input", inputFile
    print "output", outputFile

    dataframe1 = pandas.read_csv(inputFile)
    result = azureml_main(dataframe1, round-1)
    print result.to_string(index=False)
    result.to_csv(outputFile, index=False)

# Import-Csv .\P1.txt | ConvertTo-Html | Out-File 1.html

# The script MUST contain a function named azureml_main
# which is the entry point for this module.
#
# The entry point function can contain up to two input arguments:
#   Param<dataframe1>: a pandas.DataFrame
#   Param<dataframe2>: a pandas.DataFrame

def azureml_main(dataframe1, currentRound):

    # Execution logic goes here
    result = pandas.DataFrame(columns=['Table','Black','White','Handicap','Komi','Result'])
    if (dataframe1 is None):
        return result

    dframe, handicapInfo = read_round(dataframe1)

    for i in range(0, len(dframe)-1):
        finalPairing, sortedFrame = generate_new_round(dframe, i, currentRound, handicapInfo[i])
        resTable = print_pairing(finalPairing[0][1], sortedFrame, handicapInfo[i])
        # if handicapInfo[i]:
        #     result.loc[len(result)] = ['&','&','&','&','&']
        # else:
        #     result.loc[len(result)] = ['=','=','=','=','=']
        result = result.append(resTable)
	
	for i in range(0, len(result)):
		result.set_value(i,0,str(int(i+1)), True)

    # Return value must be of a sequence of pandas.DataFrame
    return result



######################################################
# data processing
######################################################
def read_round(rawframe): # with manual banding
    rawframe = rawframe.fillna("")
    dframe = []
    handicapInfo = [False]
    begin = 0
    for i in range(0,len(rawframe)):
        if (rawframe['id'][i]=='='):
            dframe.append(rawframe.loc[begin:i-1].reset_index(drop=True))
            begin = i+1
            handicapInfo.append(False)
        elif (rawframe['id'][i]=='&'):
            dframe.append(rawframe.loc[begin:i-1].reset_index(drop=True))
            begin = i+1
            handicapInfo.append(True)
    dframe.append(rawframe.loc[begin:].reset_index(drop=True))
    dframe.append(rawframe.loc[[]].reset_index(drop=True))
    for df in dframe:
        df['id'] = df['id'].astype(int)
        df['rank'] = df['rank'].astype(float)
    return dframe, handicapInfo

def print_pairing(pairing, dframe, handicapInfo=False):
    pframe = pandas.DataFrame(columns=['Table','Black','White','Handicap','Komi','Result'])
    for i in range(0, len(pairing)/2):
        bindex = pairing[2*i]
        windex = pairing[2*i+1]
        bname = dframe['name'][bindex]
        wname = dframe['name'][windex]
        if (not handicapInfo):
            komi = "7.5"
            handicap = "0"
        else:
            brank = dframe['rank'][bindex]
            wrank = dframe['rank'][windex]
            if (brank > wrank):
                bname, wname = wname, bname
                brank, wrank = wrank, brank
            rdiff = int(wrank-brank)
            if (rdiff == 0):
                komi = "7.5"
                handicap = "0"
            elif (rdiff == 1):
                komi = "0.5"
                handicap = "0"
            else:
                komi = "0.5"
                handicap = str(rdiff)
        pframe.loc[len(pframe)] = ["0",bname,wname,handicap,komi,'']
    return pframe

######################################################
# pairing logic
######################################################
def get_mutation(df, pos, finalPairing, currentIndex, currentSet, oppSet, totalCount):
    if (not finalPairing):
        lowest = sys.maxint
    else:
        lowest = min(finalPairing, key=finalPairing.get)
    N = len(df)
    # only approximation for large groups; performance concern
    if (N>12 and totalCount[0]>N*(N-1)*(N-2)):
        return

    if (pos >= N):
        penalty = get_penalty(df, currentIndex)
        if (not finalPairing.has_key(penalty)):
            finalPairing[penalty] = []
        if (penalty>lowest):
            return
        finalPairing[penalty].append(currentIndex[:])
        totalCount[0] += 1
        return
    else:
        for p1 in range(0, N):
            if (p1 not in currentSet):
                currentIndex.append(p1)
                currentSet.add(p1)
                for p2 in range(0, N):
                    if (p2 not in currentSet):
                        if (df['id'][p2] not in oppSet[df['id'][p1]]):
                            currentIndex.append(p2)
                            currentSet.add(p2)
                            penalty = get_penalty(df, currentIndex)
                            if (penalty<=lowest):
                                get_mutation(df, pos + 2, finalPairing, currentIndex, currentSet, oppSet, totalCount)
                                currentIndex[pos], currentIndex[pos+1] = currentIndex[pos+1], currentIndex[pos]
                                get_mutation(df, pos + 2, finalPairing, currentIndex, currentSet, oppSet, totalCount)
                                currentIndex[pos], currentIndex[pos+1] = currentIndex[pos+1], currentIndex[pos]
                            currentSet.remove(p2)
                            currentIndex.pop()
                currentSet.remove(p1)
                currentIndex.pop()
                return

def get_foldpairing(n):
    pairing = [None]*n
    if (n%4 != 0):
        mid = n/2-1
    else:
        mid = n/2
    for i in range(0,mid/2):
        pairing[2*i] = mid/2 + i
        pairing[2*i + 1] = i
    left = n - mid
    for i in range(0,left/2):
        pairing[2*i + mid] = mid + i + left/2
        pairing[2*i + 1 + mid] = mid + i
    return pairing

def generate_new_round(dframeList, currentBand, this_round, handicap = False):
    dframe = dframeList[currentBand]
    sortedFrame = MMS.sort_by_mms(dframeList, currentBand, False, handicap)
    oppset = {}
    for i,item in sortedFrame['history'].iteritems():
        os=set()
        if (item!=""):
            for opp in item.split(";"):
                if (opp.lower() != 'bye'):
                    os.add(int(opp[1:-1]))
        oppset[sortedFrame['id'][i]]=os

    finalPairing = {}
    currentIndex = []
    currentSet = set()
    finalList = []
    if (this_round == 0): #special treatment for the very first round for performance consideration
        first_pairing = get_foldpairing(len(sortedFrame))
        finalList.append((0, first_pairing))
    else:
        totalCount = [0]
        get_mutation(sortedFrame, 0, finalPairing, currentIndex, currentSet, oppset, totalCount)
        topPairings = sorted(finalPairing.iteritems())[0]
        random.shuffle(topPairings[1])
        for item in topPairings[1]:
            finalList.append((topPairings[0], item))

    return finalList, sortedFrame

######################################################
# penalty function
######################################################
def get_penalty(dframe, pairing):
    penalty = 0;
    for p in range(0, len(pairing)/2):
        i = pairing[p*2];
        j = pairing[p*2+1];
        dm = dframe['mms'][i]-dframe['mms'][j]
        dp = dframe['rank'][i]-dframe['rank'][j]
        iw = dframe['history'][i].upper().count('W')
        ib = dframe['history'][i].upper().count('B') - dframe['history'][i].upper().count('y') + 1
        jw = dframe['history'][j].upper().count('W') + 1
        jb = dframe['history'][j].upper().count('B') - dframe['history'][j].upper().count('y')
        ic = iw-ib
        jc = jw-jb
        penalty += (10000 * dm*dm + 100 * dp*dp + ic*ic + jc*jc)
    return penalty

if __name__ == '__main__':
    main(sys.argv[1:])