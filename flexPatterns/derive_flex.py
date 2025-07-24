
def rotate(l, n):
    return l[n:] + l[:n]

sequence_length = 2  # Maximum length of the sequences to generate
number_range = 2     # Range of numbers to use in the sequences (from -m to m, excluding 0)

sequences = []

for i in range (1, number_range + 1):
    sequences += [(i,)]

for seq_len in range(2,sequence_length+1):
    new_seq = []
    for seq in sequences:
        for num in range(1, number_range + 1):
            new_seq += [seq + (num,), seq + (-num),]
            for rotation_distance in range(1, seq_len):
                new_seq += [rotate(seq + (num,), rotation_distance),
                            rotate(seq + (-num,), rotation_distance)]
    sequences += new_seq

for seq in list(set(sequences)):
    print(seq)