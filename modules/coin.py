#list of supported cryptocoins
coin_names = [
"BTC",
"ETH",
"XMR"
]

class coin(object):
	def __init__(self, coin_name, new_data):
		if coin_name in coin_names:
			print "Created ", coin_name, " instance."
			self.coin_name = coin_name
			self.coin_properties = {}
			self.update(new_data)
		else:
			print "Coin type does not exist."
			return None
	
	def __getitem__(self, key):
		return self.coin_properties[key]
	
	def update(self, new_data):
		""" get new data for this coin type, this is gonna have to be more robust to handle other types of data, but for now it'll do """
		self.coin_properties = {}
		iter_data = new_data[self.coin_name].split(',')
		for i in range(len(iter_data)):
			key, value = iter_data[i].split(':')
			self.coin_properties[key.strip('"')] = value.strip('"')
		#print self.coin_properties
	
	def summary(self):
		print "-----------", self.coin_name, " summary ------------"
		for key, value in self.coin_properties.iteritems():
			print key, ":", value
		print "----------------------------------"

	def inventory(self):
		pass
	""" return current amount we have of this coin """
	
def main():
	bitcoin = coin("BTC")
	bitcoin.summary()
	
if __name__ == "__main__":main()