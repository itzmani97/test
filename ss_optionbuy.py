import requests 
import json
from datetime import datetime
stockName = "RELIANCE"
import time
#page1 = requests.get("https://www.nseindia.com/option-chain?symbolCode=-10006&symbol=NIFTY&symbol=NIFTY&instrument=-&date=-&segmentLink=17&symbolCount=2&segmentLink=17",headers=headers)



browser = requests.Session()
f = open("NIFTY50.txt").read().splitlines()
l = 0
for stockname in f:
	l = l + 1
	print(str(l)+"--->"+stockname)
	url = "https://www.nseindia.com/api/option-chain-equities?symbol="+stockname
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}
	time.sleep(5)
	page1 = browser.get("https://www.nseindia.com/option-chain", headers = headers )
	cookies = dict(page1.cookies)
	page = browser.get(url,headers=headers, cookies = cookies)
	#print(page.text)
	
	#print(page.text)
	try:
		options_data = json.loads(page.text)
		if('records' in options_data):
			current_price = options_data["records"]["underlyingValue"]
			timestamp =  options_data["records"]["timestamp"]
		else:
			print(page.text)
			raise Exception('No records in data')

		print("Stock Name: ", stockname)
		#strikeDifference = abs(options_data["filtered"]["data"][0]["strikePrice"] - options_data["filtered"]["data"][1]["strikePrice"])
		#LR = float(current_price) - float(strikeDifference)
		#print("strikeDifference: "+ str(strikeDifference))
		#CEOIChange = None
		#PEOIChange = None
		#closestStrikeDifference = current_price
		#closestStrike = None
		maxoiCE = 0 
		selectedCEStrike = None
		selectedCEChangeinOI = None

		maxoiPE = 0 
		selectedPEStrike = None
		selectedPEChangeinOI = None
		for i in options_data["filtered"]["data"]:
			if('CE' in i):
				if(i["CE"]["openInterest"] > maxoiCE):
					maxoiCE = i["CE"]["openInterest"]
					selectedCEStrike = i["strikePrice"]
					selectedCEChangeinOI = i["CE"]["changeinOpenInterest"]

				

			if('PE' in i):
				if(i["PE"]["openInterest"] > maxoiPE):
					maxoiPE = i["PE"]["openInterest"]
					selectedPEStrike = i["strikePrice"]
					selectedPEChangeinOI = i["PE"]["changeinOpenInterest"]


		f1 = open("StockWatch.txt","a+")
		
				
		writeCE = None
		writePE = None
		if(abs(current_price - selectedCEStrike)/current_price*100 <= 2.5):
			writeCE = "CE --- Strike Price: "+str(selectedCEStrike)+"  "+"OI: "+str(maxoiCE)+"  "+"Change in OI: "+str(selectedCEChangeinOI)
		if(abs(current_price - selectedPEStrike)/current_price*100 <= 2.5):
			writePE = "PE --- Strike Price: "+str(selectedPEStrike)+"  "+"OI: "+str(maxoiPE)+"  "+"Change in OI: "+str(selectedPEChangeinOI)

		if(writeCE != None or writePE != None):
			f1.write("Stock: "+ stockname+"\n")
			f1.write("Stock Price: "+ str(current_price)+"\n")
			if(writeCE != None):
				if(selectedCEChangeinOI < 0 and (abs(selectedCEChangeinOI) >= maxoiCE/2.5)):
					#ifttt link goes here
				if(selectedCEChangeinOI < 0 and (abs(selectedCEChangeinOI) >= maxoiCE/2)):
					f1.write(writeCE+"\n")
			if(writePE != None):
				if(selectedPEChangeinOI < 0 and (abs(selectedPEChangeinOI) >= maxoiPE/2.5)):
					#ifttt link goes here
				if(selectedCEChangeinOI < 0 and (abs(selectedCEChangeinOI) >= maxoiCE/2)):
					f1.write(writePE+"\n")
			f1.write("------------------------------------------------------"+"\n")
		
		f1.close()

		

	except Exception as e:
		print("E: "+str(e))
		print("In except")
		f1 = open("StockWatch.txt","a+")
		f1.write("Stock: "+ stockname+"\n")
		f1.write("Some Error: "+str(e)+"\n")
		f1.write("------------------------------------------------------"+"\n")
		f1.close()
