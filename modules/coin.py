import re

#list of supported cryptocoins
coin_names = [
"BTC",
"ETH",
"XMR"
]

class coin(object):
	def __init__(self, coin_name, new_data = None):
		if coin_name in coin_names and new_data:
			print "Created ", coin_name, " instance."
			self.coin_name = coin_name
			self.coin_properties = {}
			self.update(new_data)
		else:
			print "Error creating new coin, did you pass in new data?"
			return None
	
	
	def __getitem__(self, key):
		return self.coin_properties[key]
	"""allows you to get properties of a coin instance like a dictionary"""
	
	
	def update(self, new_data):
		""" get new data for this coin type, this is gonna have to be more robust to handle other types of data, but for now it'll do """
		numeric = re.compile(r'\-?[0-9]+\.?[0-9]*')				#set RE for 
		
		iter_data = new_data[self.coin_name].split(',')
		for i in range(len(iter_data)):
			key, value = iter_data[i].split(':')
			
			key = key.strip('"')
			value = value.strip('"')
			
			#if the property in question looks like a numeric value, cast it to a float
			is_numeric = re.search(numeric, value)
			if is_numeric:
				value = float(value)
				
			self.coin_properties[key] = value
			
	def summary(self):
		print "-----------", self.coin_name, " summary ------------"
		for key, value in self.coin_properties.iteritems():
			print key, ":", value
		print "----------------------------------"

	def inventory(self):
		pass
	""" return current amount we have of this coin (i kinda wanna pass in a csv of wallet addresses for each coin type or something) """
	
def main():
	bitcoin = coin("BTC")
	bitcoin.summary()
	
if __name__ == "__main__":main()