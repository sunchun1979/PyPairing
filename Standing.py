import sys
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
    dataframe1 = pandas.read_csv(inputFile)
    result = pandas.read_csv(resultFile)
    standing = azureml_main(dataframe1, result)
    print standing
    standing.to_csv(outputFile, index=False)

# Import-Csv .\P1.txt | ConvertTo-Html | Out-File 1.html
# The script MUST contain a function named azureml_main
# which is the entry point for this module.
#
# The entry point function can contain up to two input arguments:
#   Param<dataframe1>: a pandas.DataFrame
#   Param<dataframe2>: a pandas.DataFrame


def azureml_main(dataframe1 = None, results = None):

    # Execution logic goes here
    if (dataframe1 is None):
        return pandas.DataFrame(columns=['id','name','rank','history'])
    rawframe = dataframe1.fillna("")
    newframe = update_round(rawframe, results)

    # If a zip file is connected to the third input port is connected,
    # it is unzipped under ".\Script Bundle". This directory is added
    # to sys.path. Therefore, if your zip file contains a Python file
    # mymodule.py you can import it using:
    # import mymodule

    # Return value must be of a sequence of pandas.DataFrame
    return newframe


def update_round(dframe, previous):
    ndict = {}
    for i in range(0, len(dframe)):
        ndict[dframe['name'][i]] = i
    for i in range(0, len(previous)):
        win = ndict[previous['Result'][i]]
        if (previous['Result'][i] == previous['Black'][i]):
            c = 'B'
            loss = ndict[previous['White'][i]]
        else:
            c = 'W'
            loss = ndict[previous['Black'][i]]
        if (dframe['history'][win]!=""):
            delim = ';'
        else:
            delim = ''
        dframe.set_value(win, 'history', dframe['history'][win] + delim + c + str(dframe['id'][loss]) + '+')
        if (dframe['history'][loss]!=""):
            delim = ';'
        else:
            delim = ''
        dframe.set_value(loss, 'history', dframe['history'][loss] + delim + c + str(dframe['id'][win]) + '-')
    return dframe

# Import-Csv .\P1.txt | ConvertTo-Html | Out-File 1.html

if __name__ == '__main__':
    main(sys.argv[1:])