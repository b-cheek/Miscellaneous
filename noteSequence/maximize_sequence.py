import music21 as m21

def unique_intervals(seq):
    """
    Calculates the number of unique intervals in a sequence.
    An interval is the difference between an element and the next.
    """
    if len(seq) < 2:
        return 0
    # Use a set comprehension to find all unique intervals.
    # The interval is defined as seq[i] - seq[i+1].
    intervals = {seq[i] - seq[i+1] for i in range(len(seq)-1)}
    return len(intervals)

def distance_from_center_increments(seq):
    """
    Calculates the number of times the absolute distance from the center (0)
    of the sequence increases as the sequence progresses.
    """
    if not seq:
        return 0
        
    center = 0
    increments = 0
    # The first element establishes the initial max distance.
    max_distance = abs(seq[0] - center)
    
    for i in range(1, len(seq)):
        current_distance = abs(seq[i] - center)
        if current_distance > max_distance:
            increments += 1
            max_distance = current_distance
    return increments

def sum_abs_intervals(seq):
    """
    Calculates the sum of the absolute values of all intervals in the sequence.
    This is the metric to be minimized.
    """
    if len(seq) < 2:
        return 0
    return sum(abs(seq[i] - seq[i+1]) for i in range(len(seq)-1))

def generate_sequence(n: int):
    """
    Generates a sequence of length n using a balanced approach that prioritizes
    maximizing unique intervals while secondarily minimizing the interval sum.

    Args:
        n: The desired length of the sequence (must be an integer > 2).

    Returns:
        A list of integers representing the generated sequence.
    
    The algorithm iteratively builds the sequence with a multi-layered greedy strategy:
    1. At each step, it considers all available numbers.
    2. It prioritizes choices that create a NEW interval (one not used before).
    3. Among those choices, it picks the one that creates the smallest absolute interval.
    4. Ties are broken by picking the number closer to 0.
    5. If no choice creates a new interval, it falls back to picking the move with the
       smallest absolute interval among the used ones.
    
    This results in a sequence that achieves a high number of unique intervals
    while keeping the interval sum lower than a purely expansive approach.
    """
    if not isinstance(n, int) or n <= 2:
        raise ValueError("Input must be an integer greater than 2.")

    # 1. Determine the continuous range of integers for the sequence.
    if n % 2 != 0: # Odd n
        k = (n - 1) // 2
        numbers = range(-k, k + 1)
    else: # Even n
        k = n // 2
        numbers = range(-(k - 1), k + 1) # Asymmetrical range
        
    available_numbers = set(numbers)
    
    # 2. Initialize the sequence and tracking sets.
    sequence = [0]
    available_numbers.remove(0)
    used_intervals = set()

    # 3. Iteratively build the sequence.
    while len(sequence) < n:
        last_num = sequence[-1]
        
        new_interval_candidates = []
        used_interval_candidates = []
        
        # Categorize all possible next moves.
        for num in available_numbers:
            interval = last_num - num
            candidate_info = {
                'num': num,
                'interval': interval,
                'abs_interval': abs(interval)
            }
            if interval in used_intervals:
                used_interval_candidates.append(candidate_info)
            else:
                new_interval_candidates.append(candidate_info)

        # Determine which list of candidates to use (prefer new intervals).
        if new_interval_candidates:
            target_candidates = new_interval_candidates
        else:
            # This is a fallback, rarely needed with this strategy.
            target_candidates = used_interval_candidates

        # Find the best candidate from the chosen list.
        # First, find the minimum absolute interval in the list.
        min_abs_interval = min(c['abs_interval'] for c in target_candidates)
        
        # Filter to only those candidates that achieve this minimum.
        best_candidates = [c for c in target_candidates if c['abs_interval'] == min_abs_interval]
        
        # Apply tie-breaking rules:
        # 1st: by the absolute value of the number itself (closer to zero is better).
        # 2nd: by the value of the number itself (smaller is better).
        best_candidates.sort(key=lambda c: (abs(c['num']), c['num']))
        
        best_choice = best_candidates[0]

        # Update state with the chosen number and interval.
        sequence.append(best_choice['num'])
        available_numbers.remove(best_choice['num'])
        used_intervals.add(best_choice['interval'])
        
    return sequence

# --- Main execution block to demonstrate the function ---
if __name__ == '__main__' and False:
    # --- Example 1: Odd length (n=7) ---
    n_odd = 7
    print(f"--- Generating sequence for n = {n_odd} ---")
    try:
        odd_sequence = generate_sequence(n_odd)
        print(f"Generated Sequence: {odd_sequence}")

        # The set of numbers used should be a continuous range.
        print(f"Set of numbers used: {sorted(list(set(odd_sequence)))}")
        
        # Analyze the sequence based on the given criteria.
        unique_count = unique_intervals(odd_sequence)
        distance_increments = distance_from_center_increments(odd_sequence)
        interval_sum = sum_abs_intervals(odd_sequence)
        
        print(f"1. Starts with 0: {odd_sequence[0] == 0}")
        print(f"2. Number of Unique Intervals: {unique_count}")
        print(f"3. Outward Expansions: {distance_increments}")
        print(f"4. Sum of Absolute Intervals: {interval_sum}")

    except ValueError as e:
        print(f"Error: {e}")
        
    print("\n" + "="*40 + "\n")
    
    # --- Example 2: Even length (n=10) ---
    n_even = 10
    print(f"--- Generating sequence for n = {n_even} ---")
    try:
        even_sequence = generate_sequence(n_even)
        print(f"Generated Sequence: {even_sequence}")

        # The set of numbers used should be a continuous range.
        print(f"Set of numbers used: {sorted(list(set(even_sequence)))}")

        # Analyze the sequence based on the given criteria.
        unique_count = unique_intervals(even_sequence)
        distance_increments = distance_from_center_increments(even_sequence)
        interval_sum = sum_abs_intervals(even_sequence)

        print(f"1. Starts with 0: {even_sequence[0] == 0}")
        print(f"2. Number of Unique Intervals: {unique_count}")
        print(f"3. Outward Expansions: {distance_increments}")
        print(f"4. Sum of Absolute Intervals: {interval_sum}")

    except ValueError as e:
        print(f"Error: {e}")

def showSequence(length):
    """
    Generates a sequence of the specified length and display as sheet music,
    where each number added to 60 (C4 in midi) to be displayed as a quarter note.
    """
    sequence = generate_sequence(length)
    stream = m21.stream.Stream()
    for num in sequence:
        num *= 1
        midi_note = m21.note.Note(num + 50)
        stream.append(midi_note)
    stream.show()
if __name__ == "__main__":
    # Example usage of showSequence function
    showSequence(48)  # Generates a sequence and displays it as sheet music