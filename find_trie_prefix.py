# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 01:23:38 2018

@author: Afnan
"""

# BEGIN PART FROM https://towardsdatascience.com/implementing-a-trie-data-structure-in-python-in-less-than-100-lines-of-code-a877ea23c1a1

from typing import Tuple

class TrieNode(object):
    """
    Trie node implementation.
    """
    
    def __init__(self, char: str):
        self.char = char
        self.children = []
        # Is it the last character of the word.
        self.word_finished = False
        # How many times this character appeared in the addition process
        self.counter = 1
    

def add(root, word: str):
    """
    Adding a word in the trie structure
    """
    node = root
    for char in word:
        found_in_child = False
        # Search for the character in the children of the present `node`
        for child in node.children:
            if child.char == char:
                # We found it, increase the counter by 1 to keep track that another
                # word has it as well
                child.counter += 1
                # And point the node to the child that contains this char
                node = child
                found_in_child = True
                break
        # We did not find it so add a new chlid
        if not found_in_child:
            new_node = TrieNode(char)
            node.children.append(new_node)
            # And then point node to the new child
            node = new_node
    # Everything finished. Mark it as the end of a word.
    node.word_finished = True


def find_prefix(root, prefix: str) -> Tuple[bool, int]:
    """
    Check and return 
      1. If the prefix exsists in any of the words we added so far
      2. If yes then how may words actually have the prefix
    """
    node = root
    # If the root node has no children, then return False.
    # Because it means we are trying to search in an empty trie
    if not root.children:
        return False, 0
    for char in prefix:
        char_not_found = True
        # Search through all the children of the present `node`
        for child in node.children:
            if child.char == char:
                # We found the char existing in the child.
                char_not_found = False
                # Assign node as the child containing the char and break
                node = child
                break
        # Return False anyway when we did not find a char.
        if char_not_found:
            return False, 0
    # Well, we are here means we have found the prefix. Return true to indicate that
    # And also the counter of the last node. This indicates how many words have this
    # prefix
    return True, node.counter

# END PART FROM https://towardsdatascience.com/implementing-a-trie-data-structure-in-python-in-less-than-100-lines-of-code-a877ea23c1a1

if __name__ == "__main__":
    root = TrieNode('*')
    
    # Here my algorithm for splitting off and counting the body words is my own
    # Here the sources were hard coded. This can be easily changed to accept user input or to 
    # search through a list of files given a directory if needed
    distinct_words = []
    sources = ["files/reut2-000.sgm", "files/reut2-001.sgm", "files/reut2-002.sgm", \
               "files/reut2-003.sgm", "files/reut2-004.sgm", "files/reut2-005.sgm", \
               "files/reut2-006.sgm", "files/reut2-007.sgm", "files/reut2-008.sgm", \
               "files/reut2-009.sgm", "files/reut2-010.sgm", "files/reut2-011.sgm", \
               "files/reut2-012.sgm", "files/reut2-013.sgm", "files/reut2-014.sgm", \
               "files/reut2-015.sgm", "files/reut2-016.sgm", "files/reut2-017.sgm", \
               "files/reut2-018.sgm", "files/reut2-019.sgm", "files/reut2-020.sgm", \
               "files/reut2-021.sgm"]
    for source in sources:
        print("Parsing " + source[-13:])
        with open(source) as f: # Open the file and read line by line into array
            array = []
            for line in f:
                array.append(line)
        words = []
        body_on = False
        # Since there was no separator like the "<D>" used for TOPICS and PLACES,
        # extracting the body text of the article only needed a standard strng split along one delimiter.
        for index in array:
            if "<BODY>" in index:
                index = index.split("<BODY>",1)[1]
                body_on = True # flag is used to track when to start and stop adding lines to the body text
                words.append(index)
            if "</BODY>" in index:
                index = index.split("</BODY>",1)[0]
                body_on = False
            if body_on == True:
                words.append(index)
        distinct_words.extend(words) 
        # Words are then added to the prefix trie using the add function above in a loop
    distinct_words = set(distinct_words) # list casted as set to get rid of duplicates
    print("Adding words to prefix trie...")
    for word in distinct_words:
        try:
            int(word) # here I try to filter out integers that would not be useful in the future.
        except:
            add(root,word)
    print("Done!")
    # counts of words can be found and printed using the find_prefix methods as shown below
    print(find_prefix(root, 'limited'))
    print(find_prefix(root, '8'))
