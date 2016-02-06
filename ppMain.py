import pandas

import ppIO
import ppGenRound

dfRound = ppIO.read_round("Round0b.txt")
print dfRound
ppGenRound.generate_new_round(dfRound)

