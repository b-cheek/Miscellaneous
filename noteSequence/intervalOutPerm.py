# Objectives
# 1. Cover as many intervals as possible
#    a. include intervals of both directions
#    b. minimize the size of the largest jump between numbers in the sequence
#    c. start with smaller jumps progressing larger
#    d. do not repeat intervals
# 2. Cover as many notes as possible
#    a. Do not repeat notes
#    b. Start in the middle and expand outward

from sequence_stats_store import *
from random import randint


seq=(0,)

maxInterval = 24
iterations = 1000 # Select how many times you want to attempt to create a random interval
cur = 0

stats_dict = load_sequence_stats()

print(f"Current best candidate: {find_best_candidates(stats_dict, 24)}")

while (cur<iterations):
    if cur % 1000 == 0:
        print(f"{cur/iterations:.2%} complete")
    cur += 1
    seq = seq + (randint(-maxInterval, maxInterval),)
    if len(seq)>2 and seq not in stats_dict:
        update_sequence_stats(seq, stats_dict)
    if randint(1,24) == 1 or len(seq) == 64:
        seq = (0,)
