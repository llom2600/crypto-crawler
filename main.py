import os
import sys

# add paths to search space, to make importing modules and data sets easier
sys.path.append('./modules')
sys.path.append('./data-set')

from session import sesh
import util

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
	if line[0] == "#":
		return None
	
	temp = line.split(',')
	
	source_dict = { 
	temp[0]: temp[1],			#host, e.g. coinwarz.com
	temp[2]: temp[3],			#port, 
	temp[4]: temp[5]			#actual page with the data we want, e.g. /cryptocurrency
							}
	return source_dict



#entry point
def main():
	source_list = load_sources()			#load an external list with the urls we want to crawl
	
	#the following is just a sample request of a page to make sure everything is working ok.
	print "Pages to crawl:\n\n", source_list
	
	sessionParameters = {
	'host': source_list[0]["host"],
	'port': source_list[0]["port"]
	}
	
	request_session = sesh(sessionParameters)	
	status = request_session.open()
	
	if request_session.is_connected:
		print "Successfully connected to: ", source_list[0]["host"]
	
	request_session.get(source_list[0]["page"])	
	
	if request_session.response_body != None:
		response_body = util.decodeResponse(request_session.response_body)
	
	print request_session.response_body
	
	request_session.close()
	
	
	
	
if __name__ == "__main__": main()