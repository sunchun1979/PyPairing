import pandas
import itertools
import ppIO
import ppGenRound

dfRound = ppIO.read_round("Round0.txt")
print dfRound
finalPairing = ppGenRound.generate_new_round(dfRound)
for k,v in itertools.islice(finalPairing, 0, 10):
    print k,v
