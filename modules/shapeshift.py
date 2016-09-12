#little api wrapper class for shapeshift.io 

from util import *

shapeshift_host = "shapeshift.io"
shapeshift_port = 443

supported_get_requests = [
					["rate",1],
					["limit",1],
					["marketinfo",1],
					["recenttx",1],
					["txStat",1],
					["timeremaining",1],
					["getcoins",1],
					["txbyapikey",1],
					["txbyaddress",2],
					["validateAddress", 2]
										]


supported_post_requests = [
				   ["shift",6],
				   ["email",2],
				   ["sendamount", 7],
				   ["cancelpending", 1]
											]


class exchange(object):
	def __init__(self):
		self.foreign_host = shapeshift_host + ":" + str(shapeshift_port)
	
	def __getitem__(self, key):
		if type(key) == tuple:
			request_page = key[0]
			request_value = key[1]
		else:
			request_page = key
			request_value = None
			
		for i in range(len(supported_get_requests)):
			if 	request_page == supported_get_requests[i][0]:
				self._apiGetRequest(request_page, request_value)
				return True

		for i in range(len(supported_post_requests)):
			if 	request_page == supported_post_requests[i][0]:
				self._apiPostRequest(request_page, request_value)
				return True
		
		#self._apiCall(request_page, request_value)
		
	def _apiGetRequest(self,request_page, request_value = None):
		if request_value:
			response = get_raw_data(self.foreign_host, "/" + request_page + "/" + request_value, method="GET")
		else:
			response = get_raw_data(self.foreign_host, "/" + request_page + "/", method="GET")
		
		print response
		
		
		