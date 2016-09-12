import os
import sys
import hashlib
import urllib2
import re
import time

# add paths to search space, to make importing modules and data sets easier
sys.path.append('./modules')
sys.path.append('./data-sets')

from util import *
import parse_chain as pc
from coin import *
from shapeshift import *


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
	response = get_raw_data(source["host"] + ":" + source["port"], source["page"])									#get raw data from source
	new_data["source"] = source
	new_data["response"] = response									#set new data key to initial response data
	
	#print new_data["response"]
	
	for i in range(len(current_chain)):									#go through list of search strings and find the data we want, then store it in new_data dictionary
		parsed_link = current_chain[i].split(':', 1)			
		key_from, key_to = parsed_link[0].split(',')
		search_string = parsed_link[1].strip()
		
		key_to = key_to.strip()
		key_from = key_from.strip()
		
		current_re = re.compile(search_string)
		
		if type(new_data[key_from]) == str:
			current_result = re.findall(current_re, new_data[key_from])
		elif type(new_data[key_from]) == list:
			for i in range(len(new_data[key_from])):
				current_result = re.search(current_re, new_data[key_from][i])
				if current_result:
					break
					
		if current_result:
			if type(current_result) ==  list:
				new_data[key_to] = current_result
			else:
				new_data[key_to] = current_result.group(0)
			found_data = True
			
	if found_data:
		return new_data
	else: 
		return None

	
#entry point
def main():
	source = load_sources()								   #load an external list with the urls we want to crawl
	new_data = run_parse_chain(source[1])		#this is how easy it will be to get data from a source!!!! run it!
	
	btc = coin("BTC", new_data)						#upon creation, pass in current coin data from running parse chain
	eth = coin("ETH", new_data)						
	xmr = coin("XMR", new_data)		
	exc = exchange()										#class wrapper for shapeshift api
	
	new_data = run_parse_chain(source[1])		#get some new data from a source
	btc.update(new_data)								    #update data
	
	#to make an api call, specify the path of api call (see below), followed by the pair of coins
	exc["rate", "btc_ltc"]
	exc["limit", "btc_ltc"]
	exc["marketinfo", "btc_ltc"]
	
	#if no pair is specified, it gets all pair info
	#exc["rate"]

	
if __name__ == "__main__": main()