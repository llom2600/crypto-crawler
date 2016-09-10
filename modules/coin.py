#list of supported cryptocoins
coin_names = [
"BTC",
"ETC",
"CTA"
]

class coin(object):
	def __init__(self, coin_name):
		if coin_name in coin_names:
			print "Created ", coin_name, " instance."
			self.coin_name = coin_name
			self.coin_properties = {}
			self.update_values()
		else:
			print "Coin type does not exist."
			return None
	
	def update_values(self):
		self.coin_properties = {}
	""" get new data for this coin type """
	
	def summary(self):
		print "-----------Summary ------------"
		print self.coin_name
		for key, value in self.coin_properties:
			print key, ":", value
		print "----------------------------------"

	def inventory(self):
		pass
	""" return current amount we have of this coin """
	
def main():
	bitcoin = coin("BTC")
	bitcoin.summary()
	
if __name__ == "__main__":main()