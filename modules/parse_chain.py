import re
import numpy

PARSE_CHAIN_FILE = "parsing_rules.lst"

def load_chain(key = None):
	hash_key = re.compile(r'^[a-f0-9]{40}')
	open_block = re.compile(r'^[\{][\n]')
	close_block = re.compile(r'^[\}][\n]?')
	comment = re.compile(r'^#')

	with open(PARSE_CHAIN_FILE, 'r') as f:
		search_dict = {}
		currentLine = f.readline()
		isOpenBlock = False
		search_dict["comments"] = []
		
		while currentLine:
			search_key = re.search(hash_key, currentLine)					   #looks for a hash key
			search_open_block = re.search(open_block, currentLine)		#looks for the start of a parse chain bracket '{'
			search_close_block = re.search(close_block, currentLine)	 #looks for the end of parse chain bracket '}'
			search_comment = re.search(comment, currentLine)			 #looks for a comment line
			
			if search_key and isOpenBlock == False:
				currentHashKey = search_key.group(0)
				search_dict[currentHashKey] = []
			elif search_open_block and isOpenBlock == False:
				isOpenBlock = True				
			elif search_close_block and isOpenBlock == True:
				isOpenBlock = False
			elif search_comment:
				currentLine = currentLine.strip('\n')
				search_dict["comments"].append(currentLine)
			else:
				currentLine = currentLine.strip('\n')
				if currentLine:
					search_dict[currentHashKey].append(currentLine)
				
			currentLine = f.readline()
			
		if key is None:
			return search_dict
		else:
			try:
				return search_dict[key]
			except KeyError:
				return None
			

def main():
	coin_io = load_chain("fe0a6bcc2560fe02501682705d2226427bc7fc93")
	
	if coin_io is not None:
		print "Loaded parsing chain by hash key: ", coin_io 
	else:
		print "chain undefined"

if __name__ == "__main__":main()