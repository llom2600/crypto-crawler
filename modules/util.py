import re
#useful functions
import urllib
import urllib2

def get_raw_data(foreign_host, link_path, proxy=False, method="GET", data = {}, headers = {}):
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
			print "Problem opening source: ", foreign_host
			return None
		
	elif method == "POST":
		try:
			data = urllib.urlencode(data)
			h = httplib.HTTPConnection(foreign_host)
			h.request('POST', link_path, data, headers)
			response = h.getresponse().read()
			h.close()
		except Exception as e:
			print "Problem opening source: ", foreign_host
			return None
		
	return response