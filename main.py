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

def run_parse_chain(source):
	new_data = {}
	found_data = False
	
	current_chain = pc.load_chain(source["hash"])			#load the current parse chain for the target source
	response = get_raw_data(source)									#get raw data from source
	new_data["response"] = response									#set new data key to initial response data
	
	for i in range(len(current_chain)):									#go through list of search strings and find the data we want, then store it in new_data dictionary
		
		parsed_link = current_chain[i].split(':', 1)			
		key_from, key_to = parsed_link[0].split(',')
		search_string = parsed_link[1].strip()
		
		key_to = key_to.strip()
		key_from = key_from.strip()
		
		current_re = re.compile(search_string)
		current_result = re.findall(current_re, new_data[key_from])
		if current_result:
			new_data[key_to] = current_result
			print new_data[key_to]
			found_data = True
			
	if found_data:
		return new_data
	else: 
		return None


def get_raw_data(source):
	request_url = "http://" + source["host"] + source["page"]
	req = urllib2.Request(request_url, headers={'User-Agent' : "Magic Browser"}) 
	try:
		req_handle = urllib2.urlopen( req )
		response = req_handle.read()
	except Exception as e:
		print "Problem opening source ", source["host"]
	return response
	
#entry point
def main():
	source = load_sources()			#load an external list with the urls we want to crawl
	run_parse_chain(source[1])		#this is how easy it will be to get data from a source!!!! run it!
	
if __name__ == "__main__": main()