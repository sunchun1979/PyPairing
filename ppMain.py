import pandas
import itertools
import ppIO
import ppGenRound

dfRound = ppIO.read_round("Round0.txt")
print dfRound
finalPairing = ppGenRound.generate_new_round(dfRound, 4, 1)
print finalPairing[0]
