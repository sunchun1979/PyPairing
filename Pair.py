import sys
import ppGenRound
import ppIO
import getopt
import pandas

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

    allResults = []
    allPairing = []
    allSortedFrame = []

    dfRound, handicapInfo = ppIO.read_round(inputFile)
    for i in range(0, len(dfRound)-1):
        finalPairing, sortedFrame = ppGenRound.generate_new_round(dfRound, i, round-1, handicapInfo[i])
        allPairing.append(finalPairing)
        allSortedFrame.append(sortedFrame)
    for i in range(0, len(dfRound)-1):
        finalPairing = allPairing[i]
        resTable = ppIO.print_pairing(finalPairing[0][1], dfRound[i], handicapInfo[i])
        allResults.append(resTable)
    print "Round " + str(round) + " Pairing:"
    pf = pandas.concat(allResults, ignore_index=True)
    pf['Result'] = ''
    pf.to_csv(outputFile, index=False)

# Import-Csv .\P1.txt | ConvertTo-Html | Out-File 1.html

if __name__ == '__main__':
    main(sys.argv[1:])