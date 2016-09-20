import re, time
#useful functions
import urllib, urllib2
import hashlib
import threading

import parse_chain as pc

ATTEMPT_FREQUENCY = 1.5

def get_raw_data(foreign_host, link_path, proxy=False, method="GET", data = {}, headers = {}, attempts = 0):
	attempts = attempts
	attempt_limit = 3
	
	domain, port = foreign_host.split(':')

	if not headers:
		headers = {
		'User-Agent' : "Magic Browser"
		}
	
	if port == "443":
		request_url = "https://" + domain + link_path
	elif port == "80":
		request_url = "http://" + domain + link_path

	if proxy:
		proxy = urllib2.ProxyHandler({'http': '127.0.0.1'})
		opener = urllib2.build_opener(proxy)
		urllib2.install_opener(opener)
	
	if method == "GET":
		req = urllib2.Request(request_url, headers=headers) 
		try:
			req_handle = urllib2.urlopen( req )
			response = req_handle.read()
		except Exception as e:
			#print "Problem opening source: ", foreign_host
			attempts += 1
			if attempts <= attempt_limit:
				print "Attempt:", attempts
				return attempts
			else:
				return None
		
	elif method == "POST":
		try:
			data = urllib.urlencode(data)
			h = httplib.HTTPConnection(foreign_host)
			h.request('POST', link_path, data, headers)
			response = h.getresponse().read()
			h.close()
		except Exception as e:
			#print "Problem opening source: ", foreign_host
			return None
		
	return response

def updateCoinData(coin, sources, subset=[]):
	if subset == []:
		for i in range(0, len(sources)):
			print sources[i]
			new_data = run_parse_chain(sources[i])
			coin.update(new_data)
	else:
		for i in (coin["subset"]):
			new_data = run_parse_chain(sources[i])
			coin.update(new_data)
		
	
def updateCoinList (coinList, sources):
	print "Updating coin data..."
	
	for key,value in coinList.iteritems():
		print "\t--- updating", coinList[key]["coin_name"], "data..."
		updateCoinData(coinList[key], sources, coinList[key]["subset"])
	
		
# load in a list of web pages with data that we want
def load_sources(source_file):
	source_list = []
	with open(source_file, 'r') as f:
		for line in f:
			if not line:
				break
			line = parse_source_line(line)
			if line is not None:
				source_list.append(line)
		return source_list

	
	
	#split the line up into components
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
	response = get_raw_data(source["host"] + ":" + source["port"], source["page"])						#get raw data from source
	
	if response == None:
		return None
	elif type(response) == int:
		while(type(response) == int):
			time.sleep(ATTEMPT_FREQUENCY)			#wait a second before retrying
			response = get_raw_data(source["host"] + ":" + source["port"], source["page"], attempts=response)						#get raw data from source
			if response == None:
				return None
	
	new_data["source"] = source
	new_data["response"] = response									#set new data key to initial response data
	
	
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