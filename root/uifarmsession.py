import ui
import app
import net
import chat
import os
import time
import _weakref
import uiScriptLocale

try:
	import json
except ImportError:
	json = None

SAVE_DIR = "UserData/FarmSessions/"

def FormatElapsedTime(elapsedSec):
	elapsedSec = int(elapsedSec)
	h = elapsedSec / 3600
	m = (elapsedSec % 3600) / 60
	s = elapsedSec % 60
	return "%02d:%02d:%02d" % (h, m, s)

class FarmSessionListItem(ui.ScriptWindow):
	def __init__(self, parent, text, clickHandler = None, clickArg = None):
		ui.ScriptWindow.__init__(self)
		self.SetParent(parent)
		self.__LoadWindow()
		self.GetChild("name_btn").SetText(text)
		if clickHandler:
			self.GetChild("name_btn").SAFE_SetEvent(clickHandler, clickArg)
		self.Show()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/farmsession/listitem.py")
		except:
			import exception
			exception.Abort("FarmSessionListItem.__LoadWindow")

class FarmSessionWindow(ui.ScriptWindow):
	LIST_MODE_BREAKDOWN = 0
	LIST_MODE_HISTORY = 1

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.isActive = False
		self.elapsedSec = 0
		self.killTotal = 0
		self.itemTotal = 0
		self.yangGained = 0
		self.yangSpent = 0
		self.killsByType = {}
		self.itemsByType = {}
		self.hasReport = False

		self.displayOverride = None

		self.listMode = self.LIST_MODE_BREAKDOWN
		self.lastTickTime = 0

		self.__LoadWindow()
		self.Hide()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/farmsession/window.py")
		except:
			import exception
			exception.Abort("FarmSessionWindow.__LoadWindow")

		self.GetChild("board").SetCloseEvent(self.Hide)
		self.GetChild("startstop_btn").SAFE_SetEvent(self.OnClickStartStop)
		self.GetChild("save_btn").SAFE_SetEvent(self.OnClickSave)
		self.GetChild("history_btn").SAFE_SetEvent(self.OnClickHistory)

		self.__RefreshTexts()
		self.__RefreshList()

	## Public

	def Open(self):
		self.SetCenterPosition()
		self.Show()
		self.SetTop()

	## Network callbacks (called from C++ via PyCallClassMemberFunc)

	def OnFarmSessionState(self, isActive, elapsedSec, killTotal, itemTotal, yangGained, yangSpent):
		self.isActive = isActive and True or False
		self.elapsedSec = elapsedSec
		self.killTotal = killTotal
		self.itemTotal = itemTotal
		self.yangGained = yangGained
		self.yangSpent = yangSpent

		if not self.isActive:
			self.killsByType = {}
			self.itemsByType = {}
			self.hasReport = False

		self.displayOverride = None
		if self.listMode != self.LIST_MODE_BREAKDOWN:
			self.listMode = self.LIST_MODE_BREAKDOWN

		self.__RefreshTexts()
		self.__RefreshList()

	def OnFarmSessionKillEntry(self, mobVnum, count):
		self.killsByType[mobVnum] = count

	def OnFarmSessionItemEntry(self, itemVnum, count):
		self.itemsByType[itemVnum] = count

	def OnFarmSessionReportEnd(self):
		self.hasReport = True
		self.__RefreshList()

	## Button handlers

	def OnClickStartStop(self):
		self.displayOverride = None
		if self.isActive:
			net.SendFarmSessionControlPacket(0)
		else:
			net.SendFarmSessionControlPacket(1)

	def OnClickSave(self):
		if not self.hasReport:
			chat.AppendChat(chat.CHAT_TYPE_INFO, uiScriptLocale.FARM_SESSION_SAVE_NO_DATA)
			return

		self.__SaveToFile()

	def OnClickHistory(self):
		self.displayOverride = None
		self.listMode = self.LIST_MODE_HISTORY
		self.__RefreshTexts()
		self.__RefreshList()

	def OnClickHistoryItem(self, fileName):
		data = self.__LoadFromFile(fileName)
		if data == None:
			return

		self.displayOverride = data
		self.listMode = self.LIST_MODE_BREAKDOWN
		self.__RefreshTexts()
		self.__RefreshList()

	## Internal

	def __CurrentValues(self):
		if self.displayOverride:
			d = self.displayOverride
			return (d.get("elapsedSec", 0), d.get("killTotal", 0), d.get("itemTotal", 0), d.get("yangGained", 0), d.get("yangSpent", 0), d.get("killsByType", {}), d.get("itemsByType", {}))

		return (self.elapsedSec, self.killTotal, self.itemTotal, self.yangGained, self.yangSpent, self.killsByType, self.itemsByType)

	def __RefreshTexts(self):
		elapsedSec, killTotal, itemTotal, yangGained, yangSpent, killsByType, itemsByType = self.__CurrentValues()

		GetChild = self.GetChild
		GetChild("time_text").SetText(uiScriptLocale.FARM_SESSION_TIME_FORMAT % FormatElapsedTime(elapsedSec))
		GetChild("kill_text").SetText(uiScriptLocale.FARM_SESSION_KILLS_FORMAT % killTotal)
		GetChild("item_text").SetText(uiScriptLocale.FARM_SESSION_ITEMS_FORMAT % itemTotal)
		GetChild("yang_gained_text").SetText(uiScriptLocale.FARM_SESSION_YANG_GAINED_FORMAT % yangGained)
		GetChild("yang_spent_text").SetText(uiScriptLocale.FARM_SESSION_YANG_SPENT_FORMAT % yangSpent)
		GetChild("yang_net_text").SetText(uiScriptLocale.FARM_SESSION_YANG_NET_FORMAT % (yangGained - yangSpent))

		if self.listMode == self.LIST_MODE_HISTORY:
			GetChild("list_title_text").SetText(uiScriptLocale.FARM_SESSION_HISTORY_TITLE)
		else:
			GetChild("list_title_text").SetText(uiScriptLocale.FARM_SESSION_BREAKDOWN_TITLE)

		if self.isActive:
			GetChild("startstop_btn").SetText(uiScriptLocale.FARM_SESSION_STOP)
		else:
			GetChild("startstop_btn").SetText(uiScriptLocale.FARM_SESSION_START)

	def __RefreshList(self):
		listBox = self.GetChild("listbox")
		listBox.RemoveAllItems()
		listBoxRef = _weakref.proxy(listBox)

		if self.listMode == self.LIST_MODE_HISTORY:
			for fileName in self.__GetHistoryFileList():
				label = fileName
				if label.endswith(".json"):
					label = label[:-5]
				rowWnd = FarmSessionListItem(listBoxRef, label, self.OnClickHistoryItem, fileName)
				rowWnd.SetPosition(0, len(listBox.itemList) * rowWnd.GetHeight(), True)
				listBox.AppendItem(rowWnd)
		else:
			elapsedSec, killTotal, itemTotal, yangGained, yangSpent, killsByType, itemsByType = self.__CurrentValues()

			for vnum, count in killsByType.items():
				text = uiScriptLocale.FARM_SESSION_MOB_ROW_FORMAT % (vnum, count)
				rowWnd = FarmSessionListItem(listBoxRef, text)
				rowWnd.SetPosition(0, len(listBox.itemList) * rowWnd.GetHeight(), True)
				listBox.AppendItem(rowWnd)

			for vnum, count in itemsByType.items():
				text = uiScriptLocale.FARM_SESSION_ITEM_ROW_FORMAT % (vnum, count)
				rowWnd = FarmSessionListItem(listBoxRef, text)
				rowWnd.SetPosition(0, len(listBox.itemList) * rowWnd.GetHeight(), True)
				listBox.AppendItem(rowWnd)

		listBox.RefreshAll()

	def __GetHistoryFileList(self):
		if not os.path.exists(SAVE_DIR):
			return []

		fileList = [name for name in os.listdir(SAVE_DIR) if name.endswith(".json")]
		fileList.sort()
		fileList.reverse()
		return fileList

	def __SaveToFile(self):
		if json == None:
			chat.AppendChat(chat.CHAT_TYPE_INFO, uiScriptLocale.FARM_SESSION_SAVE_FAILED)
			return

		if not os.path.exists(SAVE_DIR):
			os.makedirs(SAVE_DIR)

		data = {
			"elapsedSec" : self.elapsedSec,
			"killTotal" : self.killTotal,
			"itemTotal" : self.itemTotal,
			"yangGained" : self.yangGained,
			"yangSpent" : self.yangSpent,
			"killsByType" : self.killsByType,
			"itemsByType" : self.itemsByType,
			"savedAt" : int(time.time()),
		}

		fileName = "%sfarm_session_%d.json" % (SAVE_DIR, int(time.time()))

		try:
			f = open(fileName, "w")
			f.write(json.dumps(data))
			f.close()
			chat.AppendChat(chat.CHAT_TYPE_INFO, uiScriptLocale.FARM_SESSION_SAVE_DONE)
		except:
			chat.AppendChat(chat.CHAT_TYPE_INFO, uiScriptLocale.FARM_SESSION_SAVE_FAILED)

	def __LoadFromFile(self, fileName):
		if json == None:
			return None

		try:
			f = open(SAVE_DIR + fileName, "r")
			raw = f.read()
			f.close()
			data = json.loads(raw)
		except:
			return None

		## JSON always decodes dict keys as strings/unicode - convert kill/item
		## vnum keys back to int so they format correctly (%d) in the row text.
		for key in ("killsByType", "itemsByType"):
			byType = {}
			for vnumStr, count in data.get(key, {}).items():
				try:
					byType[int(vnumStr)] = count
				except:
					pass
			data[key] = byType

		return data

	def OnUpdate(self):
		if not self.isActive or self.displayOverride:
			return

		now = app.GetGlobalTime()
		if now - self.lastTickTime < 1000:
			return

		self.lastTickTime = now
		self.elapsedSec += 1
		self.GetChild("time_text").SetText(uiScriptLocale.FARM_SESSION_TIME_FORMAT % FormatElapsedTime(self.elapsedSec))
