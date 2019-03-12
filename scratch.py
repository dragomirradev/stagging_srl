# Miscellaneous scripts
import sys
import os
import json
from util.conll_io import CoNLL09_Sent


def make_frames_file():
    fn_in = '../neural-dep-srl/data/nombank_descriptions-1.0+prop3.1.json'
    with open(fn_in, 'r') as f_in:
        data = json.load(f_in)
        
    role_cats = ['Core', 'Core-Unexpressed', 'Extra-Thematic',
                 'Peripheral', 'Modifiers']

    fn_out = 'data/frames.txt'
    with open(fn_out, 'w') as f_out:
        for i, pred in enumerate(data):
            line = [pred]
            for cat in role_cats:
                if cat in data[pred]["FEs"]:
                    line += [l[0] for l in data[pred]["FEs"][cat]]
            line.append('_')
            f_out.write(' '.join(line) + '\n')

    

def remove_non_pred_sents(fn_in):
    fn_out = '.'.join(fn_in.split('.')[:-1] + ['clean', 'txt'])
    out = open(fn_out, 'w')
    sent_count = 0
    no_pred_count = 0
    with open(fn_in, 'r') as f:
        lines = []
        for line in f:
            if line == '\n':
                sent_count += 1
                sys.stdout.write('\r{}'.format(sent_count))
                sys.stdout.flush()
                
                preds = [line[13] for line in lines]
                if all(pred == '_' for pred in preds):
                    no_pred_count += 1
                else:
                    out.write('\n'.join(
                        ['\t'.join(l) for l in lines]) + '\n\n')

                lines = []
            else:
                lines.append(line.strip().split('\t'))
        
    print('\nRemoved {}/{} sentences'.format(no_pred_count, sent_count))
    out.close()

def get_predicate_info(fn):
    d = {}
    with open(fn, 'r') as f:
        for line in f:
            if line == '\n':
                continue
            parts = line.split('\t')
            if parts[12] == 'Y':
                lemma = parts[3]
                predicate = parts[13]
                if lemma not in d:
                    d[lemma] = set()
                d[lemma].add(predicate)
    return d
    

# if __name__ == '__main__':
    # fn_in = sys.argv[1]
    # print fn_in
    # remove_non_pred_sents(fn_in)
    # make_frames_file()
