import sys
import ppIO
import ppGetMMS
import ppUpdateRound
import getopt
import pandas

def main(argv):
    inputFile = ''
    resultFile = ''
    outputFile = '_standing.txt'
    try:
        opts, args = getopt.getopt(argv, "hi:r:o:",["help","input=","result=","output="])
    except getopt.GetoptError:
        print "Standing.py -i <old standing file> -r <result file> -o <new standing file>"
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print "Standing.py -i <old standing file> -r <result file> -o <new standing file>"
            sys.exit()
        elif opt in ("-i", "--input"):
            inputFile = arg
        elif opt in ("-o", "--output"):
            outputFile = arg
        elif opt in ("-r", "--result"):
            resultFile = arg

    if (round == -1):
        print "Please specify round by -r"
        sys.exit(2)
    if (inputFile==""):
        print "Please specify input file by -i"
        sys.exit(2)
    print "input", inputFile
    print "output", outputFile

    allResults = []
    allPairing = []
    allSortedFrame = []
    allStanding = []

    dfRound, handicapInfo = ppIO.read_round(inputFile)
    result = pandas.read_csv(resultFile)
    print result
    for i in range(0, len(dfRound)-1):
        dfRound[i] = ppUpdateRound.update_round(dfRound[i], result)
        dfRound[i] = ppGetMMS.sort_by_mms(dfRound, i, dropAux=False, handicap=handicapInfo[i])
        allStanding.append(dfRound[i].copy())
    pf = pandas.concat(allStanding, ignore_index=True)
    print pf

# Import-Csv .\P1.txt | ConvertTo-Html | Out-File 1.html

if __name__ == '__main__':
    main(sys.argv[1:])