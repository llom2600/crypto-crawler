import os
import sys
import hashlib
import urllib2
import re

# add paths to search space, to make importing modules and data sets easier
sys.path.append('./modules')
sys.path.append('./data-sets')

from session import sesh
import util
import parse_chain as pc


#global constants
source_file = "sources.lst"


#global objects, if we need later


# load in a list of web pages with data that we want
def load_sources():
	source_list = []
	
	with open(source_file, 'r') as f:
		for line in f:
			if not line:
				break
			line = parse_source_line(line)
			if line is not None:
				source_list.append(line)
		return source_list

	
#split the line up into components and 
def parse_source_line(line):
	h = hashlib.sha1()
	
	if line[0] == "#":
		return None
	
	line = line.strip('\n') #strip newlines from each source line
	
	#generate hash key for the URL we are currently scraping
	h.update(line)
	h= h.hexdigest()
	
	temp = line.split(',')

	source_dict = { 
	temp[0]: temp[1],			#host, e.g. coinwarz.com
	temp[2]: temp[3],			#port, 
	temp[4]: temp[5],			#actual page with the data we want, e.g. /cryptocurrency
	"hash":h						#hash key
							}
	return source_dict



#entry point
def main():
	source = load_sources()			#load an external list with the urls we want to crawl
	
	#get_source(source_list[0])
	test_chain = pc.load_chain(source[1]["hash"])
	
	market_cap_search = test_chain[0].split(":",1)
	search_keys = market_cap_search[0].split(',')
	
	search_in_key = search_keys[0].strip()
	result_to_key = search_keys[1].strip()
	
	search_string = market_cap_search[1]
	
	test_result = {}
	url = "http://" + source[1]["host"] + source[1]["page"]
	
	req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
	response = urllib2.urlopen( req )
	test_result["response"] = response.read()
	
	search = re.compile(search_string)
	test_result[result_to_key] = re.findall(search_string, test_result[search_in_key])
	
	print test_result[result_to_key]
	
if __name__ == "__main__": main()