# greedy_sequence_maximizer.py
"""
Greedy algorithm to construct a sequence of length n (starting with 0) that attempts to maximize:
- number of unique intervals
- distance from center increments
- minimize sum of absolute intervals

Runs in O(n^2) time (much better than O(n!)).
"""

def greedy_maximize_sequence(n, max_interval=24):
    """
    Construct a sequence of length n (starting with 0) maximizing unique intervals, etc.
    Args:
        n: int, length of sequence
        max_interval: int, max jump allowed in either direction
    Returns:
        list of ints: the constructed sequence
    """
    seq = [0]
    used_notes = set(seq)
    unique_intervals = set()
    center = 0
    max_distance = 0
    distance_increments = 0
    
    for i in range(1, n):
        best_candidates = []
        best_score = None
        # Try all possible next notes within allowed interval
        for next_note in range(seq[-1] - max_interval, seq[-1] + max_interval + 1):
            if next_note in used_notes:
                continue
            interval = next_note - seq[-1]
            new_unique_intervals = unique_intervals | {interval}
            new_distance = abs(next_note - center)
            new_distance_increments = distance_increments + (1 if new_distance > max_distance else 0)
            new_sum_abs_intervals = sum(abs(x) for x in new_unique_intervals)
            score = (
                len(new_unique_intervals),
                new_distance_increments,
                -new_sum_abs_intervals
            )
            if best_score is None or score > best_score:
                best_candidates = [(next_note, new_unique_intervals, new_distance, new_distance_increments, new_sum_abs_intervals)]
                best_score = score
            elif score == best_score:
                best_candidates.append((next_note, new_unique_intervals, new_distance, new_distance_increments, new_sum_abs_intervals))
        # Pick one of the best candidates (e.g., the smallest next_note for determinism)
        if not best_candidates:
            break  # No valid next note
        next_note, unique_intervals, max_distance, distance_increments, _ = min(best_candidates, key=lambda x: abs(x[0]))
        seq.append(next_note)
        used_notes.add(next_note)
    return seq

if __name__ == "__main__":
    n = 12
    seq = greedy_maximize_sequence(n)
    print(f"Greedy maximized sequence of length {n}: {seq}")
    print(f"Unique intervals: {set(seq[i+1]-seq[i] for i in range(len(seq)-1))}")
    print(f"Number of unique intervals: {len(set(seq[i+1]-seq[i] for i in range(len(seq)-1)))}")
    print(f"Distance from center increments: ...")
    print(f"Sum of abs intervals: {sum(abs(seq[i+1]-seq[i]) for i in range(len(seq)-1))}")
