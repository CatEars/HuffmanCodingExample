# Henrik Adolfsson
# henad221@student.liu.se

"""
A short example of how to do huffman encoding
The huffman algorithm consists of the huffman tree, which is just a
binary tree with chars and weights as data members
It consists of a Frequency table, that show how important each encountered letter is.
And a coder that does the whole huffman encoding
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


class FrequencyTable:
    """ A table that contains the weights of each character """
    
    def __init__(self, text):
        self._table = defaultdict(int)
        self.build_frequency(text)

    def build_frequency(self, text):
        """ Builds the frequency table """
        for letter in text:
            self._table[letter] += 1

    def __getitem__(self, letter):
        return self._table[letter]

    def __iter__(self):
        return iter(self._table)


def populate(table, huffman_tree, now=""):
    """ Populates a table from a huffman tree """
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
        
    def build_table(self, text):
        """
        Takes an input string and calculates frequencies to make a huffman tree.
        creates the table for a huffman tree
        """
        assert len(text) > 1
    
        freq = FrequencyTable(text)
        
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
        """ Encodes the string with the current table """
        return "".join(self.table[letter] for letter in text)
        
    def decode(self, text):
        """ Decodes a string with the current table """
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
    text = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum"
    coder = HuffmanCoder()
    coder.build_table(text)
    
    print("Original:", text)
    print()
    print("Encoded:", coder.encode(text))
    print()
    print("Decoded:", coder.decode(coder.encode(text)))
    print()
    print("Bytes:", len(text)*8, " vs. ", len(coder.encode(text))) # Assume ASCII coding with 1 byte per char
    print("Compression ratio (without overhead):", len(coder.encode(text)) / (len(text)*8.0) )
    assert text == coder.decode(coder.encode(text))
