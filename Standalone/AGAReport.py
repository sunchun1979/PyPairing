import sys
import getopt
import pandas
import urllib2

def main(argv):
    agaidFile = ''
    resultFile = ''
    outputFile = 'toAGA.txt'
    try:
        opts, args = getopt.getopt(argv, "ha:r:o:",["help","agaid=","result=","output="])
    except getopt.GetoptError:
        print "AGAReport.py -a <aga id file> -r <result file> -o <aga report file>"
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print "AGAReport.py -a <aga id file> -r <result file> -o <aga report file>"
            sys.exit()
        elif opt in ("-a", "--agaid"):
            agaidFile = arg
        elif opt in ("-o", "--output"):
            outputFile = arg
        elif opt in ("-r", "--result"):
            resultFile = arg

    outfile = open(outputFile, 'w')

    aga_id = pandas.read_table(agaidFile)
    nameMap = {}
    for i in range(0, len(aga_id)):
        nameMap[aga_id['name'][i]] = aga_id['agaid'][i]
    for i in range(0, len(aga_id)):
        currentId = aga_id['agaid'][i]
        rank = aga_id['rank'][i]
        reqstr = "http://www.usgo.org/ratings-lookup-id?PlayerID=" + str(currentId)
        response = urllib2.urlopen(reqstr)
        html = response.read()
        key1 = "<td>" + str(currentId) + "</td>"
        p1 = html.find(key1)
        p2 = html.find("<td>", p1+5)
        p3 = html.find("</td>",p2)
        pname = html[p2+4:p3]
        print >> outfile, currentId, pname, rank

    games = pandas.read_csv(resultFile)
    #print games
    for i in range(0, len(games)):
        whiteid = nameMap[games['White'][i]]
        blackid = nameMap[games['Black'][i]]
        result = '-'
        if (games['Result'][i]==games['Black'][i]):
            result = 'b'
        elif (games['Result'][i]==games['White'][i]):
            result = 'w'
        handicap = games['Handicap'][i]
        komi = int(games['Komi'][i] - 0.5)
        print >> outfile, whiteid, blackid, result, handicap, komi

if __name__ == "__main__":
    main(sys.argv[1:])