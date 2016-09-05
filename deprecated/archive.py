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
	
	
	