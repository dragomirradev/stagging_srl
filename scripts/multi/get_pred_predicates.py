import sys
import io

input_file = sys.argv[1]
out_file = 'pred.txt'
with io.open(input_file, encoding='utf-8') as fin:
    with io.open(out_file, 'wt', encoding='utf-8') as fout:
        for line in fin:
            tokens = line.split()
            if len(tokens) > 10:
                fout.write(tokens[13])
                fout.write(u'\n')
            else:
                fout.write(u'\n')
