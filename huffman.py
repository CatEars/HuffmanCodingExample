# Henrik Adolfsson
# henad221@student.liu.se

"""
Do not use this in production.
It is not usefull at all.
Lots of overhead
It encodes/decodes not to a byte object but to a string object
Only usefull as an example of how this huffman stuff works
"""

import heapq
from collections import defaultdict

class HuffmanTree:
    """ A huffman tree """
    
    def __init__(self, left=None, right=None, char="", weight=0):
        self.left = left
        self.right = right
        self.char = char
        self.weight = weight

    def is_leaf(self):
        return self.left == None and self.right == None

    def __lt__(self, other):
        return self.weight < other.weight

    def __str__(self):
        if self.leaf:
            return "Leaf: " + str(self.char) + ", weight: " + str(self.weight)
        else:
            return "Internal: weight " + str(self.weight) 


def populate(table, huffman_tree, now=""):
    # Leaf case
    if huffman_tree.is_leaf():
        table[huffman_tree.char] = now
        table[now] = huffman_tree.char

    # internal node
    else:
        if huffman_tree.left:
            populate(table, huffman_tree.left, now + "0")
        if huffman_tree.right:
            populate(table, huffman_tree.right, now + "1")
    

class HuffmanCoder:
    """ A class that codes huffman, mostly for example use """

    def __init__(self):
        # The conversion table, contains both from "bits" to chars and from chars to bits
        self.table = dict()
        

    def build_frequency(self, text):
        """ Builds the frequency table for a text """
        freq = defaultdict(int)
        for letter in text:
            freq[letter] += 1
            
        return freq
        
    def build_table(self, text):
        """
        Takes an input string and calculates frequencies to make a huffman tree.
        creates the table for a huffman tree
        """
        assert len(text) > 1
    
        freq = self.build_frequency(text)
        
        # Construct beginning heaps
        heap = []
        for key in freq:            
            heapq.heappush(heap, HuffmanTree(char=key, weight=freq[key]))
        
        # Merge all heaps to get ultimate tree
        while len(heap) > 1:
            low1 = heapq.heappop(heap)
            low2 = heapq.heappop(heap)
            new = HuffmanTree(left=low1, right=low2, weight=low1.weight + low2.weight)
            heapq.heappush(heap, new)
        
        tree = heapq.heappop(heap)
        populate(self.table, tree)
        return self.table


    def encode(self, text):
        """
        Encodes the string with the current table        
        """
        if not text:
            return ""

        letter = text[0]
        assert letter in self.table        
        return self.table[letter] + self.encode(text[1:])

    def decode(self, text):
        """
        Decodes a string with the current table
        """
        if not text:
            return ""

        # Assume the next prefix has length 1
        # until you find the correct prefix, add another letter 
        
        size = 1
        prefix = text[:size]
        while prefix not in self.table:
            size += 1
            assert size <= len(text)                
            prefix = text[:size]
            
        return self.table[prefix] + self.decode(text[size:])

if __name__ == "__main__":
    # Here is a DNA sequence, its quite long
    text = "I love to take a stroll in the park"
    #text = "ACAAGATGCCATTGTCCCCCGGCCTCCTGCTGCTGCTGCTCTCCGGGGCCACGGCCACCGCTGCCCTGCCCCTGGAGGGTGGCCCCACCGGCCGAGACAGCGAGCATATGCAGGAAGCGGCAGGAATAAGGAAAAGCAGCCTCCTGACTTTCCTCGCTTGGTGGTTTGAGTGGACCTCCCAGGCCAGTGCCGGGCCCCTCATAGGAGAGGAAGCTCGGGAGGTGGCCAGGCGGCAGGAAGGCGCACCCCCCCAGCAATCCGCGCGCCGGGACAGAATGCCCTGCAGGAACTTCTTCTGGAAGACCTTCTCCTCCTGCAAATAAAACCTCACCCATGAATGCTCACGCAAGTTTAATTACAGACCTGAA"    
    coder = HuffmanCoder()
    coder.build_table(text)
    print(coder.encode(text))
    print(len(text)*8, len(coder.encode(text)), len(text)*8.0 / len(coder.encode(text)))
    assert text == coder.decode(coder.encode(text))
    
