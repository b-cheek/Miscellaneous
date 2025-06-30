# sequence_stats_store.py
import pickle
import os

STATS_FILE = os.path.join(os.path.dirname(__file__), 'sequence_stats.pkl')

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
    center = seq[0]
    increments = 0
    max_distance = 0
    for i in range(1, len(seq)):
        if abs(seq[i] - center) > max_distance:
            increments += 1
            max_distance = abs(seq[i] - center)
    return increments

def load_sequence_stats():
    """
    Loads the sequence statistics dictionary from file.
    Returns an empty dict if file does not exist.
    """
    if not os.path.exists(STATS_FILE):
        return {}
    with open(STATS_FILE, 'rb') as f:
        return pickle.load(f)

def save_sequence_stats(stats_dict):
    """
    Saves the sequence statistics dictionary to file.
    """
    with open(STATS_FILE, 'wb') as f:
        pickle.dump(stats_dict, f)

def update_sequence_stats(seq, stats_dict=None):
    """
    Updates the stats_dict with the given sequence and stats.
    seq: tuple of ints (including 0)
    stats: dict with keys: 'largest_jump', 'direction_changes', 'unique_intervals',
           'distance_from_center_increments', 'num_unique_intervals', 'sum_abs_intervals'
    stats_dict: optional, if not provided, will load from file
    """
    if stats_dict is None:
        stats_dict = load_sequence_stats()
    stats_dict[tuple(seq)] = {
        'largest_jump': largestJump(seq),
        'direction_changes': directionChanges(seq),
        'unique_intervals': uniqueIntervals(seq),
        'distance_from_center_increments': distance_from_center_increments(seq),
        'num_unique_intervals': len(uniqueIntervals(seq)),
        'sum_abs_intervals': sum(abs(seq[i] - seq[i+1]) for i in range(len(seq) - 1))
    }
    save_sequence_stats(stats_dict)
    return stats_dict

# Find best candidates inside pickle
def find_best_candidates(stats_dict, length):
    
    candidates = []
    for seq, stats in stats_dict.items():
        if len(seq) == length:
            candidates.append((seq, stats))

    return max(
        candidates,
        key = lambda x: (
            x[1]['num_unique_intervals'],
            x[1]['distance_from_center_increments'],
            -x[1]['sum_abs_intervals']
        )
    )
