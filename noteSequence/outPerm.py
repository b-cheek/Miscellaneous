from itertools import permutations
from math import factorial
import matplotlib.pyplot as plt

def largestJump(seq):
    """
    Returns the largest jump in a sequence.
    
    Parameters:
    seq (list): A list of integers representing the input sequence.
    
    Returns:
    int: The largest jump in the sequence.
    """
    return max(abs(seq[i] - seq[i+1]) for i in range(len(seq) - 1))

def directionChanges(seq):
    """
    Returns the number of direction changes in a sequence.
    """
    return sum(1 for i in range(1, len(seq) - 1) if (seq[i] - seq[i - 1]) * (seq[i + 1] - seq[i]) < 0)

def uniqueIntervals(seq):
    """
    Returns the number of unique intervals in a sequence.
    """
    # Remove abs to include intervals of both directions
    return set(seq[i] - seq[i+1] for i in range(len(seq)-1))

def distance_from_center_increments(seq):
    """
    the number of times the absolute distance from the center of the sequence increases
    """
    center = len(seq) // 2
    increments = 0
    max_distance = 0
    for i in range(1, len(seq)):
        if abs(seq[i] - center) > max_distance:
            increments += 1
            max_distance = abs(seq[i] - center)
    return increments

def outPerm(seqLen):
    """
    Returns the output permutation of a list.
    
    Parameters:
    l (list): A list of integers representing the input permutation.
    
    Returns:
    list: The output permutation of the input list.

    Requirements:
    The permutation begins at the center of the sequence
    The permutation generally expands outward from the center
    The size of the largest jump between numbers in the sequence is minimized
    """

    center = seqLen // 2
    initial = [i for i in range(seqLen)]
    stripped = initial[0:center] + initial[center+1:]
    # Use generator to avoid storing all permutations at once
    perm_stats = []
    total_permutations = factorial(len(stripped))
    current_permutation = 0
    for perm in permutations(stripped):
        # track progress
        current_permutation += 1
        if current_permutation % 100000 == 0:
            print(f"{current_permutation/total_permutations:.2%} complete")
        candidate = [initial[center]] + list(perm)
        lj = largestJump(candidate)
        dc = directionChanges(candidate)
        ui = uniqueIntervals(candidate)
        di = distance_from_center_increments(candidate) # A greater value here means the sequence is more likely to be expanding outward from the center (reaching higher/lower notes later in sequence)
        num_unique_intervals = len(ui)
        sum_abs_intervals = sum(abs(i) for i in ui) # A lesser value here means that the intervals covered will be more compact, i.e. the sequence will not jump around as far (smaller intervals hit before larger)
        perm_stats.append((candidate, lj, dc, ui, di, num_unique_intervals, sum_abs_intervals))

    _, _, _, unique_intervals, most_distance_increments, num_unique_intervals, sum_abs_intervals = max(
        perm_stats,
        key=lambda x: (x[5], x[4], -x[1], -x[6])
    )

    print(f"Max Unique Intervals: {num_unique_intervals}, Most Distance Increments: {most_distance_increments}, Sum of Absolute Intervals: {sum_abs_intervals}")

    # smallest_jump_with_max_dc = max(perm_stats, key=lambda x: (x[2], -x[1]))
    # best_candidates = [x for x in perm_stats if x[1] == smallest_jump_with_max_dc[1] and x[2] == smallest_jump_with_max_dc[2]]
    # for candidate in [i for i in perm_stats if len(i[3]) == len(unique_intervals) and i[4] == most_distance_increments]:
    for candidate in [i for i in perm_stats if (i[5]) == num_unique_intervals and i[4] == most_distance_increments and i[6] == sum_abs_intervals]:
        print(f"Candidate: {candidate[0]}, Unique Intervals: {candidate[3]}")

    # Graph the candidates with the largest jump and direction changes using matplotlib;
    # the x-axis is the largest jump and the y-axis is the direction changes
    # plt.scatter([x[1] for x in perm_stats], [x[2] for x in perm_stats], s=1)
    # plt.xlabel('Largest Jump')
    # plt.ylabel('Direction Changes')
    # plt.show()

# for i in range(3, 12, 2):
#     print(f"Processing sequence length {i}...")
#     outPerm(i)
#     print(f"Finished processing sequence length {i}.\n")

outPerm(12) # All notes!