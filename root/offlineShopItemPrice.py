import os
import dbg
import traceback

PRICE_DIR = "UserData/shop/"
PRICE_FILE = PRICE_DIR + "item_prices.txt"

_priceDict = None

def __Load():
	global _priceDict
	if _priceDict is not None:
		return

	_priceDict = {}
	try:
		if os.path.exists(PRICE_FILE):
			f = open(PRICE_FILE, "r")
			for line in f.readlines():
				line = line.strip()
				if not line or line.startswith("#") or "=" not in line:
					continue
				vnumStr, priceStr = line.split("=", 1)
				try:
					_priceDict[int(vnumStr)] = long(priceStr)
				except ValueError:
					continue
			f.close()
	except:
		dbg.TraceError("offlineShopItemPrice.__Load:\n%s" % traceback.format_exc())

def GetPrice(itemVNum):
	__Load()
	return _priceDict.get(int(itemVNum), 0)

def SetPrice(itemVNum, price):
	__Load()
	_priceDict[int(itemVNum)] = long(price)

	try:
		if not os.path.exists(PRICE_DIR):
			os.makedirs(PRICE_DIR)

		f = open(PRICE_FILE, "w")
		for vnum, savedPrice in _priceDict.items():
			f.write("%d=%d\n" % (vnum, savedPrice))
		f.close()
	except:
		dbg.TraceError("offlineShopItemPrice.SetPrice:\n%s" % traceback.format_exc())
