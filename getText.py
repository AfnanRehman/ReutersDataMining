from bs4 import BeautifulSoup #make sure BeautifulSoup is installed on your device beffore running it

'''
This is the function takes PLACES as argument and takes body text from file for each body where PLACES happens. It output whole body text to a file based on its <place>.txt name where place 
is the name of the place
'''
def get_text(place):
	#all the source files
	sources = ["files/reut2-000.sgm", "files/reut2-001.sgm", "files/reut2-002.sgm", \
               "files/reut2-003.sgm", "files/reut2-004.sgm", "files/reut2-005.sgm", \
               "files/reut2-006.sgm", "files/reut2-007.sgm", "files/reut2-008.sgm", \
               "files/reut2-009.sgm", "files/reut2-010.sgm", "files/reut2-011.sgm", \
               "files/reut2-012.sgm", "files/reut2-013.sgm", "files/reut2-014.sgm", \
               "files/reut2-015.sgm", "files/reut2-016.sgm", "files/reut2-017.sgm", \
               "files/reut2-018.sgm", "files/reut2-019.sgm", "files/reut2-020.sgm", \
               "files/reut2-021.sgm"]
	for source in sources:
		with open(source) as f:
			data = f.read()
			soup = BeautifulSoup(data, 'html.parser')
			reuters_tags = soup.find_all('reuters')
			individualplace_list =[]
			for reuter_tag in reuters_tags:
				places_tag = reuter_tag.places
				d_tags = places_tag.find_all('d')
				for d_tag in d_tags:
					for child in d_tag.children:
						individualplace_list.append(child)        	
				for place_name in individualplace_list:
					#print(individualplace_list)
					if(place == place_name):
						#print(reuter_tag.body.get_text())
						file= open(place+'.txt', "a")
						file.write(reuter_tag.body.get_text())
						file.close();

if __name__ == "__main__":
	get_text("nepal")

