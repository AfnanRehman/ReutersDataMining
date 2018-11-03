# -*- coding: utf-8 -*-
"""
@author: Kumar, Afnan
"""

from bs4 import BeautifulSoup # Make sure BeautifulSoup is installed on your device before running it

'''
This is the function takes PLACES as argument and takes body text from file for each body where PLACES happens. 
It output whole body text to a file based on its <place>.txt name where place is the name of the country.
This method example could be placed in another script such as countTags.py to create vectors for PLACES and TOPICS separaately.
It counts only one country at a time, so if 'usa' is in an article along with 'uk', then the body of that article would
fall into both the USA key of the dictionary vector as well as the UK key of the vector.
'''
def get_text(place, sources, places_bag_vector):
    # This portion involving reading the body text in from the file mostly done by Kumar
    total_text = ""
    for source in sources:
        with open(source) as f:
            data = f.read()
            soup = BeautifulSoup(data, 'html.parser') # parse using HTML parser, close to structure of these files
            reuters_tags = soup.find_all('reuters')
            for reuter_tag in reuters_tags: # get information stored within each reuters tag
                places_tag = reuter_tag.places
                d_tags = places_tag.find_all('d') # find all places/topics mentioned
                for d_tag in d_tags:
                    for child in d_tag.children: # find relevant tags to current call and add text to a master string
                        if(place == child):
                            total_text += reuter_tag.body.get_text()
                            
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
        word += " "
        new_array.append(word)
        
    cleaned_text = ""
    for newword in new_array: # now removing some final pesky words as well as any numbers we don't want in our analysis
        if "reuter" not in newword.lower() and "\x03" not in newword and newword.isdigit() == False:
            cleaned_text += newword
    # Optionally, add the finished bag of words to a output file    
    file= open(place+'.txt', "a")
    try:
        file.write(cleaned_text)
    except:
        file.write("")
    file.close();            
    # Create vector and return to calling function            
    places_bag_vector[place] = cleaned_text
    return places_bag_vector
    # output looks like: {'afghanistan' : 'Pakistan complained to the United Nations today that...', 'algeria' : 'Liquefied natural gas imports from Algeria...', ....}
                                        
if __name__ == "__main__":
    sources = ["files/reut2-000.sgm", "files/reut2-001.sgm", "files/reut2-002.sgm", \
               "files/reut2-003.sgm", "files/reut2-004.sgm", "files/reut2-005.sgm", \
               "files/reut2-006.sgm", "files/reut2-007.sgm", "files/reut2-008.sgm", \
               "files/reut2-009.sgm", "files/reut2-010.sgm", "files/reut2-011.sgm", \
               "files/reut2-012.sgm", "files/reut2-013.sgm", "files/reut2-014.sgm", \
               "files/reut2-015.sgm", "files/reut2-016.sgm", "files/reut2-017.sgm", \
               "files/reut2-018.sgm", "files/reut2-019.sgm", "files/reut2-020.sgm", \
               "files/reut2-021.sgm"]
    vector = {}
    vector = get_text("nepal", sources, vector) # call method
    print(vector)
