import collections
import sys

def rplc(line):
    line = line.replace('.', ' ')
    line = line.replace(',', ' ')
    line = line.replace('?', ' ')
    line = line.replace('!', ' ')
    line = line.replace(':', ' ')
    line = line.replace(';', ' ')
    line = line.replace('"', ' ')
    line = line.replace('(', ' ')
    line = line.replace(')', ' ')
    line = line.replace('1', ' ')
    line = line.replace('2', ' ')
    line = line.replace('3', ' ')
    line = line.replace('4', ' ')
    line = line.replace('5', ' ')
    line = line.replace('6', ' ')
    line = line.replace('7', ' ')
    line = line.replace('8', ' ')
    line = line.replace('9', ' ')
    line = line.replace('\n', ' ')
    line = line.replace('_', ' ')
    return line.strip()

def create_prefixes(d):
    prefixes = {}
    for w in d:
        word = w[0]
        if not prefixes.get(word, None):
            prefixes[word] = [w]
        else:
            prefixes[word].append(w)
        for let in w[1:]:
            word += let
            if not prefixes.get(word, None):
                prefixes[word] = [w]
            else:
                prefixes[word].append(w)
    return prefixes

def get_available_words(d, words_prefixes, seq):
    keyboard = {2:['a','b','c'], 3:['d','e','f'], 4:['g','h','i'], 5:['j','k','l'], 6:['m','n','o'],
                7:['p','q','r','s'], 8:['t','u','v'], 9:['w','x','y','z']}
    if '1' in seq:
        return []
    seq_idx = 0
    next_prefixes = keyboard.get(int(seq[seq_idx]), None)
    last_prefixes = None
    avaliable_words = []
    for p in next_prefixes:
        if words_prefixes.get(p, None):
            avaliable_words.extend(words_prefixes[p])
    while (seq_idx < len(seq)-1) and (len(avaliable_words) > 0):
        last_prefixes = next_prefixes
        next_prefixes = keyboard[int(seq[seq_idx+1])]
        avalable_prefixes = [l+n for l in last_prefixes for n in next_prefixes]
        new_available_words = []
        remained_prefixes = []
        for prefix in avalable_prefixes: 
            for word in avaliable_words:
                if word.startswith(prefix) and word not in new_available_words:
                    new_available_words.append(word)
                    if not prefix in remained_prefixes:
                        remained_prefixes.append(prefix)
        avaliable_words = new_available_words
        next_prefixes = remained_prefixes
        seq_idx += 1
    return avaliable_words

def main(seqs):
    with open('t9Dictionary', 'r') as dict_file:
        t9_dict = [line.strip() for line in dict_file.readlines()]
    with open('t9TextCorpus', 'r') as corpus_file:
        t9_corp = ''
        line = rplc(corpus_file.readline())
        while not line == 'END-OF-CORPUS':
            t9_corp += line + ' ' 
            line = rplc(corpus_file.readline())
    simple_tokens = [w.strip() for w in t9_corp.split(' ') if not w.strip() == '']
    simple_tokens.extend(list(set(t9_dict)))
    simple_tokens = [t[:-1] if t.endswith("'") else t for t in simple_tokens]
    cnts_dict = collections.Counter(simple_tokens)
    weigted_dict = {}
    for w in t9_dict:
        weigted_dict[w] = cnts_dict[w]
    prefixes = create_prefixes(t9_dict)
    for seq in seqs:
        words = get_available_words(t9_dict, prefixes, seq)
        words_f = sorted([(w, weigted_dict[w]) for w in words], key=lambda x: (-x[1], x[0]))
        if len(words_f) > 0:
            print(';'.join([x[0] for x in words_f[:5]]))
        else:
            print('No Suggestions')

seqs = [line.strip() for line in sys.stdin]
main(seqs[1:])