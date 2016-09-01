import re
#useful functions

def decodeResponse(response_body):
	chunk = re.compile(r'\r\n[0-9A-Fa-f]+\r\n', flags = re.MULTILINE)
	m = re.findall(chunk, response_body)
	response_body = re.sub(chunk, "", response_body)
	return response_body