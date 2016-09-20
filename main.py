import os, sys, re
import sched, time
from threading import Thread
import urllib2
import numpy as np
import pyqtgraph as pg

# add paths to search space, to make importing modules and data sets easier
sys.path.append('./modules')
sys.path.append('./visual')
sys.path.append('./trends')
sys.path.append('./wallets')
sys.path.append('./data-sets')

from util import *
from coin import *
from shapeshift import *
from plot import *

#global constants
source_file = "sources.lst"
run_limit = 1800.0					#time to pull data in seconds

#global objects
sources = None
coinList = None
exc = None

#this runs forever, and continuously updates data sources and stuff
def main_event_loop(params):
	global coinList, sources, exc
	
	updateCoinList(coinList,sources)			#grab first batch of data before entering event loop
	
	EXIT_FLAG = False
	init_time = time.time()
	timeVector = np.array([], dtype=float)
	yVector = np.array([], dtype=float)
	
	#temporary plotting object to visualize data
	#pw = simplePlot()
	
	while not EXIT_FLAG:
		iteration_begin = time.time()
		thread_updateData = Thread(target = updateCoinList,  args = (coinList, sources))
		
		thread_updateData.start()
		thread_updateData.join()				#ensures that the main event loop is blocked from continuing
		
		#loop frequency must be greater than or equal to the longest thread frequency
		#print "Current time:", time.time()
		
		#coinList["btc"].summary()
		#print coinList["xmr"]["price"]
		
		total_elapsed = time.time() - init_time
		iteration_elapsed = time.time() - iteration_begin
		
		if params["record_data"]:
			for key,value in coinList.iteritems():
				log_coin_data(coinList[key], params["watch_list"])
		
		#temporary mechanism to update data
		#pw.plot(timeVector, yVector, clear=True)
		#pg.QtGui.QApplication.processEvents()
		
		#exc["rate", "btc_eth"]
		
		if iteration_elapsed < params["loop_frequency"]:
			remaining_sleep = params["loop_frequency"] - iteration_elapsed
			print "Remaining sleep:", remaining_sleep
			time.sleep(remaining_sleep)
			
		if  total_elapsed >= run_limit:
			print "Exiting after ", total_elapsed, " seconds."
			EXIT_FLAG = True
			#pg.QtGui.QApplication.closeAllWindows()
#entry point
def main():
	global sources, exc, coinList
	
	event_loop_parameters = {
	"update_frequency":1,
	"loop_frequency":1.000,
	"watch_list":["time","difficulty", "difficulty24", "mktcap", "block_reward", "exchange_rate",  "exchange_rate24",  "volume", "price"],
	"record_data":True
	}
	
	sources = load_sources(source_file)		 #load an external list with the urls we want to crawl
	#print sources
	
	# subset specifies the indices of sources that each coin type will pull new data from
	# it sucks, i know. i'm working on a better system
	
	btc = coin("BTC", subset = [0,1])						#upon creation, pass in current coin data from running parse chain
	eth = coin("ETH", subset = [0,2])						
	xmr = coin("XMR", subset = [0,3])		
	
	coinList = {"btc":btc, "eth":eth, "xmr":xmr}			#create list to store all coins we are working with
	exc = exchange()					#class wrapper for shapeshift api
	
	main_event_loop(event_loop_parameters)
	
	#to make an api call, specify the path of api call (see below), followed by the pair of coins
	#sample shapeshift api calls
	'''
	exc["rate", "btc_ltc"]
	exc["limit", "btc_ltc"]
	exc["marketinfo", "btc_ltc"]
	'''
	#if no pair is specified, it gets all pair info
	#exc["rate"]

if __name__ == "__main__": main()