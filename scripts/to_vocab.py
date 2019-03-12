import sys

train_file = sys.argv[1]
out_file = 'vocab.txt'
counts = {}
with open(train_file) as fin:
    for line in fin:
        tokens = line.split()
        if len(tokens) == 1:
            token = tokens[0]
            if token in counts:
                counts[token] += 1
            else:
                counts[token] = 1
counts = sorted(counts.items(), key=lambda x: -x[1])
with open(out_file, 'wt') as fout:
    for stag, count in counts:
        out = [stag, str(count)]
        fout.write(' '.join(out))
        fout.write('\n')

  
