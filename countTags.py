# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 01:30:28 2018

@author: Afnan
"""
# This method works like str.split, but splits for as many times as a delimiter shows up in the doc
# It is also original work based on prior knowledge of how string splits work in Python.
def multi_splitter(input_string, delimiter): 
    out_strings = []
    new_sub = str(input_string).split(delimiter)
    for str_element in new_sub:
        sub = str_element.split("</D>")
        out_strings.append(sub[0])
    return out_strings

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
    
    
    # Here, my algorithm for splitting the elements of the TOPICS and PLACES fields is my original work
    for source in sources:
        print(source)
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
        
        # Here I refer back to the original list of lines with the PLACES tag to locate blanks
        # Since blank PLACES fields all had the same structure, counting them was a simple string comparison.
        count_blanks = 0
        for place in places:
            if place == "<PLACES></PLACES>\n":
                count_blanks += 1
        total_blank_places += count_blanks
        
        
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
        
        # Counted distinct topics using th esame cast to set 
        distinct_topics = set(tops)
        # You may notice the issue with simply extending the list of total topics
        # There may end up being duplicates between documents that are not addressed
        # I address this issue in the final step: printing the statistics after all loops are finished
        total_topics.extend(distinct_topics)
        
        count_blanks = 0
        for topic in topics:
            if topic == "<TOPICS></TOPICS>\n":
                count_blanks += 1
        total_blank_topics += count_blanks
        
    # At the end here I printed some statistics that I could use in the report document.
    print("Total countries: " + str(len(set(total_countries))-2))
    print(sorted(set(total_countries))) # Final list is alphabetized for ease of reading
    print("Total topics: " + str(len(set(total_topics))-2))
    print(sorted(set(total_topics))) # Final list is alphabetized for ease of reading
    print("Total blank places: " + str(total_blank_places))
    print("Total blank topics: " + str(total_blank_topics))
        