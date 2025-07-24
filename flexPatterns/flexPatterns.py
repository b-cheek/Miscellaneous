import itertools

def max_leap(seq):
    return max(abs(i) for i in seq)

def normal_max_leap(seq):
    return max_leap(seq) + len(seq)

def avg_leap(seq):
    return sum(abs(i) for i in seq) / len(seq)

def num_direction_changes_per_jump(seq):
    num_direction_changes = 0
    for i in range(1, len(seq) - 1):
        if (seq[i] - seq[i - 1]) * (seq[i + 1] - seq[i]) < 0:
            num_direction_changes += 1
    return num_direction_changes / len(seq)

def end_partial_difference(seq):
    return abs(sum(seq))

def tessitura(seq):
    max = min = cur = 0
    for i in seq:
        cur += i
        if cur > max:
            max = cur
        if cur < min:
            min = cur
    return max - min

def rotations_with_inversions(l):
    rotations = [l[d:] + l[:d] for d in range(1, len(l))]
    inversions = [tuple(-x for x in rot) for rot in rotations]
    return rotations + inversions

def repeats(l, sequence_length):
    return [l*r for r in range(2,sequence_length//len(l)+1)]

sequence_length = 4  # Maximum length of the sequences to generate
number_range = 2     # Range of numbers to use in the sequences (from -m to m, excluding 0)
possible_numbers = list(range(-number_range, 0)) + list(range(1, number_range + 1))
sequences = []

# Generate sequences of all lengths from 1 to sequence_length
for length in range(1, sequence_length + 1):
    length_sequences = list(itertools.product(possible_numbers, repeat=length))
    sequences += [seq for seq in length_sequences if seq[0] > 0 and end_partial_difference(seq)<=1]

# Remove any rotations or inversions of rotations
cur_seq_idx = 0
while cur_seq_idx < len(sequences):
    remove_seq_idx = cur_seq_idx + 1
    similar = rotations_with_inversions(sequences[cur_seq_idx])
    while remove_seq_idx<len(sequences):
        if sequences[remove_seq_idx] in similar:
            sequences.pop(remove_seq_idx)
        else:
            remove_seq_idx += 1
    cur_seq_idx += 1

# Remove sequences that are an earlier sequence repeated
cur_seq_idx = 0
while cur_seq_idx < len(sequences):
    remove_seq_idx = cur_seq_idx + 1
    similar = repeats(sequences[cur_seq_idx], sequence_length)
    while remove_seq_idx<len(sequences):
        if sequences[remove_seq_idx] in similar:
            sequences.pop(remove_seq_idx)
        else:
            remove_seq_idx += 1
    cur_seq_idx += 1


for seq in sorted(sequences, 
                  key=lambda x: (
                      max_leap(x),
                      avg_leap(x),
                      end_partial_difference(x),
                      num_direction_changes_per_jump(x),
                      tessitura(x),
                  ))[:50]:
    print(seq)
