### utf-8 Support for Preprocessing
### Place CoNLL09 Style files
import sys
import os
import io

item2idx = {'words': 1, 'lemmas': 2, 'plemmas': 3, 'pos': 4, 'predicates': 13}

def normalize(token):
    """From Marcheggiani et al"""
    penn_tokens = {
        '-LRB-': '(',
        '-RRB-': ')',
        '-LSB-': '[',
        '-RSB-': ']',
        '-LCB-': '{',
        '-RCB-': '}'
    }
    if token in penn_tokens:
        return penn_tokens[token]

    token = token.lower()
    try:
        int(token)
        return "<NUM>"
    except:
        pass
    try:
        float(token.replace(',', ''))
        return "<FLOAT>"
    except:
        pass
    return token
   

def to_vocab(data, lan):
    for item in data.keys():
        out_file = os.path.join('data', lan, 'vocab', item+'.txt')
        counts = {}
        item_data = data[item]
        for token in item_data:
            if item == 'words':
                token = unicode(normalize(token))
            if token in counts:
                counts[token] += 1
            else:
                counts[token] = 1 
        counts = sorted(counts.items(), key=lambda x: -x[1])
        with io.open(out_file, 'wt', encoding='utf-8') as fout:
            for stag, count in counts:
                out = [stag, str(count)]
                fout.write(' '.join(out))
                fout.write(u'\n')
def to_vocab_lab(lab_data, lan):
    out_file = os.path.join('data', lan, 'vocab', 'labels.txt')
    counts = {}
    item_data = lab_data
    for token in item_data:
        if token in counts:
            counts[token] += 1
        else:
            counts[token] = 1 
    counts = sorted(counts.items(), key=lambda x: -x[1])
    with io.open(out_file, 'wt', encoding='utf-8') as fout:
        for stag, count in counts:
            out = [stag, str(count)]
            fout.write(' '.join(out))
            fout.write(u'\n')
 
 
def read_conll09(conll_file):
    items = ['words', 'pos', 'lemmas', 'plemmas', 'predicates']
    ### 'labels' is more complicated
    data = {item: [] for item in items}
    data['labels'] = []
    lens = []
    length = 0
    with io.open(conll_file, encoding='utf-8') as fin:
        for line in fin:
            tokens = line.split()
            if len(tokens) > 10:
                for item in items:
                    data[item].append(tokens[item2idx[item]])
                ## for labels
                data['labels'].extend(tokens[14:])
                length += 1
            else:
                if lens > 0: ## avoid consecutive blank lines
                    lens.append(length)
                length = 0
    return data, lens
                    
def output_data(data, data_type, lens, lan):
    #items = ['words', 'pos', 'lemmas', 'plemmas', 'predicates']
    items = ['predicates']
    for item in items:
        out_file = os.path.join('data/{}/conll09/gold/'.format(lan), data_type+'_'+item+'.txt')
        sent_idx = 0
        word_idx = 0
        tokens = data[item]
        sent_len = lens[sent_idx]
        with io.open(out_file, 'wt', encoding='utf-8') as fout:
            for token in tokens:
                sent_len = lens[sent_idx]
                fout.write(token)
                fout.write(u'\n')
                word_idx += 1
                if word_idx == sent_len:
                    sent_idx += 1
                    word_idx = 0
                    fout.write(u'\n')

def preprocess(conll_file, data_type, lan):
    data, lens = read_conll09(conll_file)
    print(len(lens))
    output_data(data, data_type, lens, lan)
    if data_type == 'train':
        to_vocab(data, lan)
    return data
                
if __name__ == '__main__':
    #lan = 'zh'
    lan = 'de'
    #lan = 'es'
    #lan = 'eng'
    data_types = ['train', 'dev', 'test', 'ood'] 
    #data_types = ['train', 'dev', 'test'] 
    lab_data = []
    for data_type in data_types:
        conll_file = os.path.join('data', lan, 'conll09', data_type+'.txt')
        data = preprocess(conll_file, data_type, lan)
        lab_data.extend(data['labels'])
    to_vocab_lab(lab_data, lan)
    
