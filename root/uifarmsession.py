import ui
import app
import net
import chat
import dbg
import item
import nonplayer
import os
import re
import time
import traceback
import uiScriptLocale

SAVE_DIR = "UserData/FarmSessions/"

LIST_AREA_X = 15
LIST_AREA_Y = 148
LIST_ROW_HEIGHT = 22
LIST_MAX_ROWS = 6

COLOR_YANG_POSITIVE = 0xff40ff40
COLOR_YANG_NEGATIVE = 0xffff4040

## Hand-rolled JSON encode/decode for this feature's simple, known data shape
## (a flat dict of ints plus two int-keyed dicts of ints) - the embedded
## Python here may not ship a working "json" module, so this avoids depending
## on it entirely. The output is still valid JSON, readable by any real
## parser; the decoder below just doesn't need to BE a general one.
def _FormatIntDict(d):
	items = ['"%d": %d' % (int(k), int(v)) for k, v in d.items()]
	return "{" + ", ".join(items) + "}"

def _FormatJson(data):
	return (
		"{\n"
		'\t"elapsedSec": %d,\n'
		'\t"killTotal": %d,\n'
		'\t"stoneKillTotal": %d,\n'
		'\t"bossKillTotal": %d,\n'
		'\t"normalKillTotal": %d,\n'
		'\t"itemTotal": %d,\n'
		'\t"yangGained": %d,\n'
		'\t"yangSpent": %d,\n'
		'\t"savedAt": %d,\n'
		'\t"killsByType": %s,\n'
		'\t"itemsByType": %s\n'
		"}"
	) % (
		data["elapsedSec"], data["killTotal"], data["stoneKillTotal"], data["bossKillTotal"], data["normalKillTotal"],
		data["itemTotal"], data["yangGained"], data["yangSpent"], data["savedAt"],
		_FormatIntDict(data["killsByType"]), _FormatIntDict(data["itemsByType"]),
	)

_JSON_KV_RE = re.compile(r'"(\w+)"\s*:\s*(-?\d+)')
_JSON_DICT_RE = re.compile(r'"(\w+)"\s*:\s*\{([^}]*)\}')
_JSON_PAIR_RE = re.compile(r'"(-?\d+)"\s*:\s*(-?\d+)')

def _ParseJson(raw):
	data = {}
	for m in _JSON_KV_RE.finditer(raw):
		data[m.group(1)] = int(m.group(2))
	for m in _JSON_DICT_RE.finditer(raw):
		subDict = {}
		for pm in _JSON_PAIR_RE.finditer(m.group(2)):
			subDict[int(pm.group(1))] = int(pm.group(2))
		data[m.group(1)] = subDict
	return data

def FormatElapsedTime(elapsedSec):
	elapsedSec = int(elapsedSec)
	h = elapsedSec / 3600
	m = (elapsedSec % 3600) / 60
	s = elapsedSec % 60
	return "%02d:%02d:%02d" % (h, m, s)

def _SortedByCountDesc(d):
	return sorted(d.items(), key = lambda pair: pair[1], reverse = True)

def _GetMobName(raceNum):
	try:
		name = nonplayer.GetMonsterName(raceNum)
		if name:
			return name
	except:
		pass
	return "#%d" % raceNum

def _GetItemName(vnum):
	try:
		item.SelectItem(vnum)
		name = item.GetItemName()
		if name:
			return name
	except:
		pass
	return "#%d" % vnum

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
	LIST_MODE_KILLS = 0
	LIST_MODE_ITEMS = 1
	LIST_MODE_HISTORY = 2

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.isActive = False
		self.elapsedSec = 0
		self.killTotal = 0
		self.stoneKillTotal = 0
		self.bossKillTotal = 0
		self.normalKillTotal = 0
		self.itemTotal = 0
		self.yangGained = 0
		self.yangSpent = 0
		self.killsByType = {}
		self.itemsByType = {}
		self.hasReport = False

		self.displayOverride = None

		self.listMode = self.LIST_MODE_KILLS
		self.lastTickTime = 0
		self.rowWndList = []

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
		self.GetChild("toggle_btn").SAFE_SetEvent(self.OnClickToggleList)
		self.GetChild("history_btn").SAFE_SetEvent(self.OnClickHistory)

		self.__RefreshTexts()
		self.__RefreshList()

	## Public

	def Open(self):
		self.SetCenterPosition()
		self.Show()
		self.SetTop()

	## Network callbacks (called from C++ via PyCallClassMemberFunc)

	def OnFarmSessionState(self, isActive, elapsedSec, killTotal, stoneKillTotal, bossKillTotal, normalKillTotal, itemTotal, yangGained, yangSpent):
		self.isActive = isActive and True or False
		self.elapsedSec = elapsedSec
		self.killTotal = killTotal
		self.stoneKillTotal = stoneKillTotal
		self.bossKillTotal = bossKillTotal
		self.normalKillTotal = normalKillTotal
		self.itemTotal = itemTotal
		self.yangGained = yangGained
		self.yangSpent = yangSpent

		## A brand new session always reports every total as 0 in its very
		## first state push - use that to detect "this is a fresh Start" and
		## drop the previous session's per-type breakdown, which otherwise
		## stuck around (harmless no-op the rest of the time, since these
		## totals being 0 mean the breakdown dicts are already empty anyway).
		isFreshOrStopped = (not self.isActive) or (stoneKillTotal == 0 and bossKillTotal == 0 and normalKillTotal == 0 and itemTotal == 0)
		if isFreshOrStopped:
			self.killsByType = {}
			self.itemsByType = {}
			self.hasReport = False

		self.displayOverride = None
		if self.listMode == self.LIST_MODE_HISTORY:
			self.listMode = self.LIST_MODE_KILLS

		self.__RefreshTexts()
		self.__RefreshList()

	def OnFarmSessionKillEntry(self, mobVnum, count):
		self.killsByType[mobVnum] = count
		self.__RefreshListIfShowingLive(self.LIST_MODE_KILLS)

	def OnFarmSessionItemEntry(self, itemVnum, count):
		self.itemsByType[itemVnum] = count
		self.__RefreshListIfShowingLive(self.LIST_MODE_ITEMS)

	def OnFarmSessionReportEnd(self):
		self.hasReport = True
		self.__RefreshListIfShowingLive(self.listMode)

	def __RefreshListIfShowingLive(self, relevantMode):
		## Don't clobber the list if the player is currently browsing the
		## history list, looking at a loaded historical session, or looking
		## at the OTHER live list (kills vs items) than the one that changed.
		if self.listMode == relevantMode and not self.displayOverride:
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

	def OnClickToggleList(self):
		if self.listMode == self.LIST_MODE_KILLS:
			self.listMode = self.LIST_MODE_ITEMS
		else:
			self.listMode = self.LIST_MODE_KILLS

		self.__RefreshTexts()
		self.__RefreshList()

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
		self.listMode = self.LIST_MODE_KILLS
		self.__RefreshTexts()
		self.__RefreshList()

	## Internal

	def __CurrentValues(self):
		if self.displayOverride:
			d = self.displayOverride
			return (
				d.get("elapsedSec", 0), d.get("killTotal", 0),
				d.get("stoneKillTotal", 0), d.get("bossKillTotal", 0), d.get("normalKillTotal", 0),
				d.get("itemTotal", 0), d.get("yangGained", 0), d.get("yangSpent", 0),
				d.get("killsByType", {}), d.get("itemsByType", {}),
			)

		return (
			self.elapsedSec, self.killTotal,
			self.stoneKillTotal, self.bossKillTotal, self.normalKillTotal,
			self.itemTotal, self.yangGained, self.yangSpent,
			self.killsByType, self.itemsByType,
		)

	def __RefreshTexts(self):
		elapsedSec, killTotal, stoneKillTotal, bossKillTotal, normalKillTotal, itemTotal, yangGained, yangSpent, killsByType, itemsByType = self.__CurrentValues()

		GetChild = self.GetChild
		GetChild("time_text").SetText(uiScriptLocale.FARM_SESSION_TIME_FORMAT % FormatElapsedTime(elapsedSec))

		netYang = yangGained - yangSpent
		netText = ("+%d" % netYang) if netYang >= 0 else ("%d" % netYang)
		yangWnd = GetChild("yang_net_text")
		yangWnd.SetText(uiScriptLocale.FARM_SESSION_YANG_NET_FORMAT % netText)
		yangWnd.SetPackedFontColor(COLOR_YANG_POSITIVE if netYang >= 0 else COLOR_YANG_NEGATIVE)

		GetChild("stone_text").SetText(uiScriptLocale.FARM_SESSION_STONE_FORMAT % stoneKillTotal)
		GetChild("boss_text").SetText(uiScriptLocale.FARM_SESSION_BOSS_FORMAT % bossKillTotal)
		GetChild("normal_text").SetText(uiScriptLocale.FARM_SESSION_NORMAL_FORMAT % normalKillTotal)

		if self.listMode == self.LIST_MODE_HISTORY:
			GetChild("list_title_text").SetText(uiScriptLocale.FARM_SESSION_HISTORY_TITLE)
		elif self.listMode == self.LIST_MODE_ITEMS:
			GetChild("list_title_text").SetText(uiScriptLocale.FARM_SESSION_ITEMS_LIST_TITLE)
		else:
			GetChild("list_title_text").SetText(uiScriptLocale.FARM_SESSION_KILLS_LIST_TITLE)

		if self.isActive:
			GetChild("startstop_btn").SetText(uiScriptLocale.FARM_SESSION_STOP)
		else:
			GetChild("startstop_btn").SetText(uiScriptLocale.FARM_SESSION_START)

	def __AddRow(self, parent, text, clickHandler = None, clickArg = None):
		if len(self.rowWndList) >= LIST_MAX_ROWS:
			return

		rowWnd = FarmSessionListItem(parent, text, clickHandler, clickArg)
		rowWnd.SetPosition(LIST_AREA_X, LIST_AREA_Y + len(self.rowWndList) * LIST_ROW_HEIGHT)
		self.rowWndList.append(rowWnd)

	def __RefreshList(self):
		## No listbox_new/scrollbar widget is used here (that combination
		## requires a scrollbar object to be attached or RefreshAll() crashes,
		## and the working example of that in this codebase depends on custom
		## art assets this feature doesn't have) - rows are plain child windows
		## manually positioned under "board", capped at LIST_MAX_ROWS with no
		## scrolling.
		self.rowWndList = []

		parent = self.GetChild("board")

		if self.listMode == self.LIST_MODE_HISTORY:
			for fileName in self.__GetHistoryFileList():
				label = fileName
				if label.endswith(".json"):
					label = label[:-5]
				self.__AddRow(parent, label, self.OnClickHistoryItem, fileName)
		elif self.listMode == self.LIST_MODE_ITEMS:
			elapsedSec, killTotal, stoneKillTotal, bossKillTotal, normalKillTotal, itemTotal, yangGained, yangSpent, killsByType, itemsByType = self.__CurrentValues()
			for vnum, count in _SortedByCountDesc(itemsByType):
				self.__AddRow(parent, uiScriptLocale.FARM_SESSION_ITEM_ROW_FORMAT % (_GetItemName(vnum), count))
		else:
			elapsedSec, killTotal, stoneKillTotal, bossKillTotal, normalKillTotal, itemTotal, yangGained, yangSpent, killsByType, itemsByType = self.__CurrentValues()
			for vnum, count in _SortedByCountDesc(killsByType):
				self.__AddRow(parent, uiScriptLocale.FARM_SESSION_MOB_ROW_FORMAT % (_GetMobName(vnum), count))

	def __GetHistoryFileList(self):
		if not os.path.exists(SAVE_DIR):
			return []

		fileList = [name for name in os.listdir(SAVE_DIR) if name.endswith(".json")]
		fileList.sort()
		fileList.reverse()
		return fileList

	def __SaveToFile(self):
		data = {
			"elapsedSec" : self.elapsedSec,
			"killTotal" : self.killTotal,
			"stoneKillTotal" : self.stoneKillTotal,
			"bossKillTotal" : self.bossKillTotal,
			"normalKillTotal" : self.normalKillTotal,
			"itemTotal" : self.itemTotal,
			"yangGained" : self.yangGained,
			"yangSpent" : self.yangSpent,
			"killsByType" : self.killsByType,
			"itemsByType" : self.itemsByType,
			"savedAt" : int(time.time()),
		}

		fileName = "%sfarm_session_%d.json" % (SAVE_DIR, int(time.time()))

		try:
			if not os.path.exists(SAVE_DIR):
				os.makedirs(SAVE_DIR)

			f = open(fileName, "w")
			f.write(_FormatJson(data))
			f.close()
			chat.AppendChat(chat.CHAT_TYPE_INFO, uiScriptLocale.FARM_SESSION_SAVE_DONE)
		except:
			dbg.TraceError("FarmSessionWindow.__SaveToFile(%s):\n%s" % (fileName, traceback.format_exc()))
			chat.AppendChat(chat.CHAT_TYPE_INFO, uiScriptLocale.FARM_SESSION_SAVE_FAILED)

	def __LoadFromFile(self, fileName):
		try:
			f = open(SAVE_DIR + fileName, "r")
			raw = f.read()
			f.close()
			data = _ParseJson(raw)
		except:
			dbg.TraceError("FarmSessionWindow.__LoadFromFile(%s):\n%s" % (fileName, traceback.format_exc()))
			return None

		return data

	def OnUpdate(self):
		try:
			if not self.isActive or self.displayOverride or not self.IsShow():
				return

			now = app.GetGlobalTime()
			if now - self.lastTickTime < 1000:
				return

			self.lastTickTime = now
			self.elapsedSec += 1
			self.GetChild("time_text").SetText(uiScriptLocale.FARM_SESSION_TIME_FORMAT % FormatElapsedTime(self.elapsedSec))
		except:
			## OnUpdate runs every frame - never let an exception here repeat
			## indefinitely (observed to visibly stall the client during a
			## portal/map transition before this guard was added).
			dbg.TraceError("FarmSessionWindow.OnUpdate:\n%s" % traceback.format_exc())
			self.lastTickTime = app.GetGlobalTime()
