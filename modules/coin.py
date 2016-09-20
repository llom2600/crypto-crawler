import re
import ast

#list of supported cryptocoins
coin_names = [
"BTC",
"ETH",
"XMR"
]

#used for proper eval
true = True
false = False

class coin(object):
	def __init__(self, coin_name, new_data = None, subset = []):
		if coin_name in coin_names:
			print "Created ", coin_name, " instance."
			self.coin_name = coin_name
			self.coin_properties = {}
			
			self.coin_properties["coin_name"] = self.coin_name
			self.coin_properties["subset"] = subset
			self._loadwallets()				#load csv with current wallet addresses for this coin type and update inventory
			
			if new_data != None:
				self.update(new_data)
		else:
			print "Error creating new coin, did you pass in new data?"
			return None
	
	
	def __getitem__(self, key):
		return self.coin_properties[key]
	"""allows you to get properties of a coin instance like a dictionary"""
	
	
	def update(self, new_data):
		if new_data == None:
			print "Couldn't update data that time around."
			return None
		
		""" get new data for this coin type, this is gonna have to be more robust to handle other types of data, but for now it'll do """
		#print "Updating data from: ", new_data["source"]
		numeric = re.compile(r'^\-?[0-9]+\.?[0-9]*')
		
		try:
			iter_data = new_data[self.coin_name]
		except KeyError as e:
			return None
		
		#temporary fix to eval bug i've been having with AST literal_eval
		if type(iter_data) == list:
			iter_data = iter_data[0]

		#clean up formatting
		iter_data = iter_data.strip('{')
		iter_data = iter_data.rstrip('}')
		iter_data = iter_data.split(',"')
			
		for i in range(len(iter_data)):
			key, value = iter_data[i].split(':')						
			key = key.strip('"')
			key = key.rstrip('"')
			value = value.strip('"')
			value = value.rstrip('"')

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
		
	def _loadwallets(self):
		self.wallet_list = {}
		with open("./wallets/" +self.coin_name + "_stock.lst", 'r+') as f:
			for line in f:
				if not line:
					break
				if line is not None:
					address, amount = line.rstrip('\n').split(':')
					self.wallet_list[address] = float(amount)
	
def main():
	bitcoin = coin("BTC")
	bitcoin.summary()
	
if __name__ == "__main__":main()