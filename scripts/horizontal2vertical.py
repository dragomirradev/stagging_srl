import sys
with open(sys.argv[1], 'rt') as fin:
    with open('out.txt', 'wt') as fout:
        for line in fin:
            words = line.split()
            for word in words:
                fout.write(word)
                fout.write('\n')
            fout.write('\n')
