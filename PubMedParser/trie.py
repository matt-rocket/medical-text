__author__ = 'matias'

import os.path
import pickle


class TokenTrie(object):
    def __init__(self,name):
        self.path = {}
        self.cache_filename = name+".trie.cache"
        # try to load from cache
        if os.path.isfile(name+".trie.cache"):
            try:
                print "loading trie cache.."
                self.path = pickle.load(open(self.cache_filename))
            except:
                raise IOError("not good!")
            print "succesfully loaded trie cache.."

    def is_empty(self):
        return self.path == {}

    def add(self,seq):
        head = self.path
        for token in seq:
            if head.get(token):
                head = head[token]
            else:
                head[token] = {}
                head = head[token]
        head[True] = True

    def save_to_cache(self):
        with open(self.cache_filename, 'w') as outfile:
            pickle.dump(self.path, outfile)

    def scan(self,seq):
        found_seqs = []
        while seq:
            token = seq.pop(0)
            if token in self.path:
                # try to find a match
                match = [token]
                step = 0
                head = self.path[token]
                if True in head and match:
                    # pass list by value
                    found_seqs.append(match[:])
                while len(seq)>step and seq[step] in head:
                    match.append(seq[step])
                    head = head[seq[step]]
                    step += 1
                    if True in head:
                        found_seqs.append(match)
        # get longest sequence
        return found_seqs

