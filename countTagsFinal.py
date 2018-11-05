# -*- coding: utf-8 -*-
"""
@author: Afnan
Note: some of this is carried over from lab 1
"""
from bs4 import BeautifulSoup
from typing import Tuple
import csv
# BEGIN PART FROM https://towardsdatascience.com/implementing-a-trie-data-structure-in-python-in-less-than-100-lines-of-code-a877ea23c1a1
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

# This method works like str.split, but splits for as many times as a delimiter shows up in the doc
# It is also original work based on prior knowledge of how string splits work in Python.
def multi_splitter(input_string, delimiter): 
    out_strings = []
    new_sub = str(input_string).split(delimiter)
    for str_element in new_sub:
        sub = str_element.split("</D>")
        out_strings.append(sub[0])
    return out_strings


def get_text(place, sources, places_bag_vector, t_type):
    # This portion involving reading the body text in from the file mostly done by Kumar
    print (place)
    total_text = ""
    for source in sources:
        with open(source) as f:
            data = f.read()
            soup = BeautifulSoup(data, 'html.parser') # parse using HTML parser, close to structure of these files
            reuters_tags = soup.find_all('reuters')
            for reuter_tag in reuters_tags: # get information stored within each reuters tag
                if t_type == 'topics':
                    p_tag = reuter_tag.topics
                else:
                    p_tag = reuter_tag.places
                d_tags = p_tag.find_all('d') # find all places/topics mentioned
                for d_tag in d_tags:
                    for child in d_tag.children: # find relevant tags to current call and add text to a master string
                        if(place == child):
                            try:
                                total_text += reuter_tag.body.get_text()
                            except:
                                total_text += ""
                            
    # This subsequent section is devoted to removing a few bits of rather unwieldy extra characters in our 
    # output string. We wanted to retain as many words as possible, so more tedious methods of extraction,
    # such as removing '\n' from the MIDDLE of the word was required. This part written by Afnan.
    array = total_text.split()
    new_array = []
    for word in array: # each word gets examined and picked apart if it contains the offending characters
        new_word = ""
        if '\n' in word: # removing line breaks, wherever they may occur
            subword = word.split('\n')
            for part in subword:
                if '\n' not in part:
                    new_word += part
                    word = new_word
        new_word = ""
        if '.' in word: # removing punctuation
            subword = word.split('.')
            for part in subword:
                if '.' not in part:
                    new_word += part
                    word = new_word
        new_word = ""
        if ',' in word: # removing punctuation
            subword = word.split(',')
            for part in subword:
                if ',' not in part:
                    new_word += part
                    word = new_word
        new_word = ""
        if '"' in word: # removing punctuation
            subword = word.split('"')
            for part in subword:
                if '"' not in part:
                    new_word += part
                    word = new_word
        word += " "
        new_array.append(word)
        
    cleaned_text = ""
    for newword in new_array:# now removing some final pesky words as well as any numbers we don't want in our analysis
        if "reuter" not in newword.lower() and "\x03" not in newword and '"' not in newword and newword.isdigit() == False:
            cleaned_text += newword
    # Optionally, add the finished bag of words to a output file
    cleaned_text.rstrip()
    file= open(place+'.txt', "a")
    try:
        file.write(cleaned_text)
    except:
        file.write("")
    file.close();                        
    
    # Create vector and return to calling function
    places_bag_vector[place] = cleaned_text
    # output looks like: {'afghanistan' : 'Pakistan complained to the United Nations today that...', 'algeria' : 'Liquefied natural gas imports from Algeria...', ....}
    return places_bag_vector

if __name__ == "__main__":
    sources = ["files/reut2-000.sgm", "files/reut2-001.sgm", "files/reut2-002.sgm", \
               "files/reut2-003.sgm", "files/reut2-004.sgm", "files/reut2-005.sgm", \
               "files/reut2-006.sgm", "files/reut2-007.sgm", "files/reut2-008.sgm", \
               "files/reut2-009.sgm", "files/reut2-010.sgm", "files/reut2-011.sgm", \
               "files/reut2-012.sgm", "files/reut2-013.sgm", "files/reut2-014.sgm", \
               "files/reut2-015.sgm", "files/reut2-016.sgm", "files/reut2-017.sgm", \
               "files/reut2-018.sgm", "files/reut2-019.sgm", "files/reut2-020.sgm", \
               "files/reut2-021.sgm"]
    total_blank_places = 0
    total_blank_topics = 0
    total_countries = []
    total_topics = []
    root = TrieNode('*')
    
    
    # Here, my algorithm for splitting the elements of the TOPICS and PLACES fields is my original work
    for source in sources:
        with open(source) as f: # Open the file and read line by line to a list array
            array = []
            for line in f:
                array.append(line)
        # Since PLACES were contained within one line of code according to the data I saw, I assumed 
        # that any line with the PLACES tag would contain all of the location info for that article
        places = []
        for index in array: # Look at lines containing the "PLACES" tag and read those into a separate list
            if "<PLACES>" in index:
                places.append(index)
        # Once I got the line, I split the string on the multiple "<D>" tags to extract the location
        # information within
        new_places = []
        for place in places:
            new_places.extend(multi_splitter(place, "<D>")) # Using the helpful method above, I split on one or more <D> tags
        new_places = [x for x in new_places if x not in ('', '/', '\n', 'PLACES', '/PLACES')]# I then removed instances of tag information or blank information from the overall list
        
        # One trick I learned in coding Python for work is that by casting a list as a set, 
        # you can remove duplicates in one line of code since sets do not contain duplicates
        distinct_countries = set(new_places)
        total_countries.extend(distinct_countries)
        
        # Next I moved onto TOPICS, using many of the same methods
        # that I used for PLACES to count and extract the information
        topics = []
        for index in array:
            if "<TOPICS>" in index:
                topics.append(index)
        
        # Once again I used the same string split method to extract the contents of each field
        tops = []
        for topic in topics:
            tops.extend(multi_splitter(topic, "<D>"))
        tops = [x for x in tops if x not in ('', '/', '\n', 'TOPICS', '/TOPICS')]
        
        # Counted distinct topics using the same cast to set 
        distinct_topics = set(tops)
        # You may notice the issue with simply extending the list of total topics
        # There may end up being duplicates between documents that are not addressed
        # I address this issue in the final step: printing the statistics after all loops are finished
        total_topics.extend(distinct_topics)
    
    # Here, we create all output vectors already sorted into training and test groups based on cross-validation where k = 21
    # These files are then fed into the classifier program 
    for i in range(3):
        training_sources = sources[:i] + sources[i+1:]
        test_sources = []
        test_sources.append(sources[i])
        # Here we begin to make our bag of words vectors
        # First we make the training groups
        
        # TEST SET FOR SPEED
        total_countries = ['afghanistan', 'uk', 'france', 'canada','turkey','usa','japan','pakistan']
        total_topics = ['acq', 'alum', 'lumber', 'jobs', 'interest', 'income','trade', 'wheat']
        # TEST
        
        
        bag_vector = {}
        for country in sorted(set(total_countries)):
            if "<PLACES>" not in country:
                get_text(country, training_sources, bag_vector, 'places')
        with open('place_bag_train' + str(i) + '.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["country", "text"])
            for key, value in bag_vector.items():
                writer.writerow([key, value])
        
        bag_vector = {}
        for topic in sorted(set(total_topics)):
            if "<TOPICS>" not in topic:
                get_text(topic, training_sources, bag_vector, 'topics')
        with open('topic_bag_train' + str(i) + '.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["topic", "text"])
            for key, value in bag_vector.items():
                writer.writerow([key, value])
        
        # These two will be the test groups
        bag_vector = {}
        for country in sorted(set(total_countries)):
            if "<PLACES>" not in country:
                get_text(country, test_sources, bag_vector, 'places')
        with open('place_bag_test' + str(i) + '.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["id", "text"])
            for key, value in bag_vector.items():
                writer.writerow([key, value])
        
        bag_vector = {}
        for topic in sorted(set(total_topics)):
            if "<TOPICS>" not in topic:
                get_text(topic, test_sources, bag_vector, 'topics')
        with open('topic_bag_test' + str(i) + '.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["id", "text"])
            for key, value in bag_vector.items():
                writer.writerow([key, value])
                
                
                
                
                
                
                