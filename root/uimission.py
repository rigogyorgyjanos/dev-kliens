import ui, _weakref, app, item, localeInfo, nonplayer, constInfo, uiCommon, net, chat, player, wndMgr

IMG_DIR = "d:/ymir work/ui/game/mission/"

def calculateRect(curValue, maxValue):
	try:
		return -1.0 + float(curValue) / float(maxValue)
	except:
		return 0.0

class MissionWindow(ui.ScriptWindow):
	class MissionItem(ui.ScriptWindow):
		def __del__(self):
			ui.ScriptWindow.__del__(self)
		def Destroy(self):
			self.ClearDictionary()
			self.parent = None
			self.__missionData = {}
			self.missionDataItem = None

		def __init__(self, parent, missionData):
			ui.ScriptWindow.__init__(self)
			self.Destroy()
			self.parent = parent
			self.__missionData = missionData
			self.missionDataItem = None
			self.SetParent(parent)
			self.__LoadItem()
		def __LoadItem(self):
			try:
				pyScrLoader = ui.PythonScriptLoader()
				pyScrLoader.LoadScriptFile(self, "uiscript/mission/item.py")
			except:
				import exception
				exception.Abort("MissionItem.__LoadItem.LoadObject")
			self.Refresh(False, True)
			self.Show()
		def Refresh(self, onlyUpdateValue = False, isLoading = False):
			missionData = self.__missionData
			GetChild = self.GetChild
			GetChild("status_text").SetText(localeInfo.MISSION_STATUS_COUNT % (missionData["value"], missionData["maxvalue"]))
			if onlyUpdateValue:
				return
			GetChild("reward_btn").SAFE_SetEvent(self.__ClickButton, True)
			GetChild("delete_btn").SAFE_SetEvent(self.__ClickButton, False)
			GetChild("icon").SAFE_SetStringEvent("MOUSE_OVER_IN",self.OverInItem, missionData["item"])
			GetChild("icon").SAFE_SetStringEvent("MOUSE_OVER_OUT",self.OverOutItem)
			item.SelectItem(missionData["item"])
											   
			GetChild("icon").LoadImage(item.GetIconImageFileName())
			GetChild("icon").SetScale(0.8, 0.8)

																																																		   
   
			if missionData["subtype"] == 0:
				# All type
				if missionData["type"] == 0:#Mob
					GetChild("type_text").SetText((localeInfo.MISSION_TYPE_NAME % localeInfo.MISSION_TYPE_ALL_MONSTER) + (localeInfo.MISSION_TYPE_LEVELRANGE % missionData["levelrange"]))
				elif missionData["type"] == 1:#Metin
					GetChild("type_text").SetText((localeInfo.MISSION_TYPE_NAME % localeInfo.MISSION_TYPE_ALL_METIN) + (localeInfo.MISSION_TYPE_LEVELRANGE % missionData["levelrange"]))
				elif missionData["type"] == 2:#Boss
					GetChild("type_text").SetText((localeInfo.MISSION_TYPE_NAME % localeInfo.MISSION_TYPE_ALL_BOSS) + (localeInfo.MISSION_TYPE_LEVELRANGE % missionData["levelrange"]))
			else:
				if missionData["type"] >= 0 and missionData["type"] <= 2:
					GetChild("type_text").SetText(localeInfo.MISSION_TYPE_SPECIAL % nonplayer.GetMonsterName(missionData["subtype"]))

			missionData["needUpdate"] = 0
			itemImage = IMG_DIR+"mission_0.png"
			leftTime = missionData["lefttime"]-app.GetGlobalTimeStamp() if missionData.has_key("lefttime") else 0
			if leftTime <= 0:
				GetChild("time_text").SetText(localeInfo.MISSION_LEFTTIME % "0s")
				missionData["lefttime"] = -99
				itemImage = IMG_DIR+"mission_2.png"
			if missionData["value"] == missionData["maxvalue"]:
				if missionData["reward_get"]:
					GetChild("reward_btn").Disable()
				GetChild("time_text").SetText(localeInfo.MISSION_END_TIME % self.__missionData["endTime"])
				missionData["lefttime"] = -99
				itemImage = IMG_DIR+"mission_1.png"
			board = self.GetChild("board")
			board.LoadImage(itemImage)
			if not isLoading:
				return
			i = 0
			gridCalculater = Grid(3, 2)
			for itemData in missionData["items"]:
				if self.ElementDictionary.has_key("itemIcon{}".format(i)):
					self.ElementDictionary["itemIcon{}".format(i)].Hide()
					self.ElementDictionary["itemIcon{}".format(i)]=None
				if self.ElementDictionary.has_key("itemCount{}".format(i)):
					self.ElementDictionary["itemCount{}".format(i)].Hide()
					self.ElementDictionary["itemCount{}".format(i)]=None
				if not itemData[0]:
					i += 1
					continue
				item.SelectItem(itemData[0])
				emptyCell = gridCalculater.find_blank(*item.GetItemSize())
				if emptyCell != -1:
					gridCalculater.put(emptyCell, *item.GetItemSize())
					_x = emptyCell
					_y = 0
					if emptyCell > 2:
						_y+=32
						_x-=3
					#if item.GetItemSize()[1] > 1:
					#	_y += ((item.GetItemSize()[1]+1) * 32)
					itemIcon = ui.ExpandedImageBox()
					itemIcon.SetParent(board)
					itemIcon.SetPosition(371+67+(_x * 32), 11-5+_y)
					itemIcon.LoadImage(item.GetIconImageFileName())
					itemIcon.SAFE_SetStringEvent("MOUSE_OVER_IN",self.OverInItem, itemData[0])
					itemIcon.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.OverOutItem)
					itemIcon.Show()
					self.ElementDictionary["itemIcon{}".format(i)] = itemIcon

					itemCount = ui.NumberLine()
					itemCount.SetParent(itemIcon)
					itemCount.AddFlag("not_pick")
					itemCount.SetWindowHorizontalAlignRight()
					itemCount.SetNumber(str(itemData[1]))
					#itemCount.SetPosition(21 - ( itemData[1] * 0.045 ), 22 + ((item.GetItemSize()[1]-1) * 32))
					itemCount.SetPosition(5+(len(str(itemData[1]))*5), 22)
					itemCount.Show()
					self.ElementDictionary["itemCount{}".format(i)] = itemCount
				i += 1
		def OverOutItem(self):
			interface = constInfo.GetInterfaceInstance()
			if interface:
				if interface.tooltipItem:
					interface.tooltipItem.HideToolTip()

		def OverInItem(self, itemVnum):
			interface = constInfo.GetInterfaceInstance()
			if interface:
				if interface.tooltipItem:
					interface.tooltipItem.SetItemToolTip(itemVnum)

		def OverOutImage(self):
			interface = constInfo.GetInterfaceInstance()
			if interface:
				if interface.tooltipText:
					interface.tooltipText.HideToolTip()

		def OverInImage(self, string):
			import grp
			TITLE_COLOR = grp.GenerateColor(0.9490, 0.9058, 0.7568, 1.0)
			interface = constInfo.GetInterfaceInstance()
			if interface:
				if interface.tooltipText:
					interface.tooltipText.AppendTextLine(string, TITLE_COLOR)

		def __ClickButton(self, btnType = False):
			questionDialog = self.GetChild("questionDialog") if self.IsChild("questionDialog") else None
			if not questionDialog:
				questionDialog = uiCommon.QuestionDialog()
				questionDialog.SetCancelEvent(lambda arg = False , type = btnType: self.ResultQuestionDialog(arg, type))
			questionDialog.SetText(localeInfo.MISSION_REWARD_TEXT if btnType else localeInfo.MISSION_DELETE_TEXT)
			questionDialog.SetAcceptEvent(lambda arg = True, type = btnType: self.ResultQuestionDialog(arg, type))
			questionDialog.Open()
			self.ElementDictionary["questionDialog"] = questionDialog

		def ResultQuestionDialog(self, result, btnType):
			missionData = self.__missionData
			leftTime = self.__missionData["lefttime"]-app.GetGlobalTimeStamp() if self.__missionData.has_key("lefttime") else 0
			questionDialog = self.GetChild("questionDialog") if self.IsChild("questionDialog") else None

			if missionData["item"] == 50317 and leftTime > 0 :
				chat.AppendChat(chat.CHAT_TYPE_INFO, "This is a mandatory mission, can be deleted only if the mission has been completed.")
				if questionDialog:
					questionDialog.Close()
				return

			if missionData["item"] == 50317:
				if not btnType: ## adica fals
					if missionData["reward_get"]:
						net.SendChatPacket("/mission {} {}".format("delete", self.__missionData["id"]))
					else:
						chat.AppendChat(chat.CHAT_TYPE_INFO, "This is a mandatory mission, can be deleted only if the mission has been redeemed.")
				else:
					net.SendChatPacket("/mission {} {}".format("reward", self.__missionData["id"]))
			else:
				if result:
					net.SendChatPacket("/mission {} {}".format("reward" if btnType else "delete", self.__missionData["id"]))
					net.SendChatPacket("mission {} {}".format("reward" if btnType else "delete", self.__missionData["id"]))

			if questionDialog:
				questionDialog.Close()

		def GetData(self):
			return self.__missionData
		def __CheckLeftTime(self):
			needUpdate = self.__missionData["needUpdate"] if self.__missionData.has_key("needUpdate") else 0
			if needUpdate:
				self.Refresh(True if needUpdate == 2 else False)
			leftTime = self.__missionData["lefttime"]-app.GetGlobalTimeStamp() if self.__missionData.has_key("lefttime") else 0
			if leftTime <= 0:
				if leftTime != -99:
					self.__missionData["needUpdate"] = 1
				return
			m, s = divmod(leftTime, 60)
			h, m = divmod(m, 60)
			d, h = divmod(h, 24)
			timeText = ""
			if d > 0:
				timeText+="{}d".format(d)
			if h > 0:
				timeText+="{}{}h".format(" " if len(timeText) > 0 else "", h)
			if m > 0:
				timeText+="{}{}m".format(" " if len(timeText) > 0 else "", m)
			if s > 0:
				timeText+="{}{}s".format(" " if len(timeText) > 0 else "", s)

			if leftTime >= 31556926:
				self.GetChild("time_text").SetText(localeInfo.MISSION_LEFTTIME % "Unlimited")
			else:
				self.GetChild("time_text").SetText(localeInfo.MISSION_LEFTTIME % timeText)
		def OnRender(self):
			self.__CheckLeftTime()
			_wy = self.parent.GetGlobalPosition()[1]
			_height = self.parent.GetHeight()
			for chilname, childItem in self.ElementDictionary.items():
				if isinstance(childItem, ui.TextLine) or isinstance(childItem, ui.NumberLine):
					(_x,_y) = childItem.GetGlobalPosition()
					childHeight = childItem.GetHeight()
					if _y < _wy:
						if childItem.IsShow():
							childItem.Hide()
						continue
					if _y+childHeight > (_wy+_height-20):
						if childItem.IsShow():
							childItem.Hide()
						continue
					if not childItem.IsShow():
						childItem.Show()
				if isinstance(childItem, ui.Button) or isinstance(childItem, ui.ExpandedImageBox):
					topRender = 0
					bottomRender = 0
					itsRendered = False
					(_x,_y) = childItem.GetGlobalPosition()
					childHeight = childItem.GetHeight()
					if _y < _wy:
						topRender = _y-_wy
						itsRendered = True
					if _y+childHeight > (_wy+_height-2):
						bottomRender = (_wy+_height-2)-(_y+childHeight)
						itsRendered = True
					if itsRendered:
						childItem.SetRenderingRect(0,calculateRect(childHeight-abs(topRender), childHeight),0,calculateRect(childHeight-abs(bottomRender),childHeight))
					else:
						childItem.SetRenderingRect(0,0,0,0)
					if not childItem.IsShow():
						childItem.Show()
	def __del__(self):
		ui.ScriptWindow.__del__(self)

	if app.ENABLE_SAVE_LAST_WINDOW_POSITION:
		def SetLastPosition(self):
			try:
				file = open("data/user_data/wnd/" + player.GetName() + "/"+ "missions" + ".pos", 'r')
				line = file.read().split(",")
				pos_x, pos_y = int(line[0]), int(line[1])
				file.close()
				if pos_x > wndMgr.GetScreenWidth() or pos_y > wndMgr.GetScreenHeight():
					return
				if pos_x < 0:
					pos_x = 0
				if pos_y < 0:
					pos_y = 0
				self.SetPosition(pos_x, pos_y)
			except:
				pass
		
		def SaveLastPosition(self):
			pos_x, pos_y = self.GetGlobalPosition()
			file = open("data/user_data/wnd/" + player.GetName() + "/"+ "missions" + ".pos","w")
			file.write(str(pos_x)+","+str(pos_y))
			file.close()

	def Destroy(self):
		if self.IsShow():
			self.SaveLastPosition()
		self.ClearDictionary()
		self.__missionData=[]
		self.__packetSended = False

	def Close(self):
		if self.IsShow():
			self.SaveLastPosition()
		self.Hide()

		if app.__BL_MOUSE_WHEEL_TOP_WINDOW__:
			wndMgr.ClearWheelTopWindow()

	def Open(self):
		self.Show()
		self.SetTop()
		self.SetLastPosition()

		if app.__BL_MOUSE_WHEEL_TOP_WINDOW__:
			wndMgr.SetWheelTopWindow(self.hWnd)

		if not self.__packetSended:
			self.__packetSended = True
			net.SendChatPacket("/mission_books load")

	if app.__BL_MOUSE_WHEEL_TOP_WINDOW__:
		def OnMouseWheelButtonUp(self):
			scrollBar = self.ElementDictionary.get("scrollBar")
			if scrollBar and scrollBar.IsShow():
				scrollBar.OnUp()
				return True
			return False

		def OnMouseWheelButtonDown(self):
			scrollBar = self.ElementDictionary.get("scrollBar")
			if scrollBar and scrollBar.IsShow():
				scrollBar.OnDown()
				return True
			return False
	def OnPressEscapeKey(self):
		self.Close()
		return True
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.Destroy()
		self.__LoadWindow()
	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/mission/window.py")
		except:
			import exception
			exception.Abort("MissionItem.__LoadItem.LoadObject")
		self.GetChild("board").SetCloseEvent(self.Close)
		self.SetCenterPosition()
		listBox = self.GetChild("listbox")
		scrollBar = ScrollBarNew()
		scrollBar.SetParent(self.GetChild("bg"))
		scrollBar.SetPosition(3+listBox.GetWidth(), 3)
		scrollBar.SetScrollBarSize(listBox.GetHeight())
		
		scrollBar.SetMiddleBarSize(1.0)
		scrollBar.Show()
		listBox.SetScrollBar(_weakref.proxy(scrollBar))
		self.ElementDictionary["scrollBar"] = scrollBar
	def Clear(self):
		self.__missionData = []
		self.Refresh()
	def Refresh(self):
		listBox = self.GetChild("listbox")
		listBox.RemoveAllItems()
		for mission in self.__missionData:
			missionWnd = self.MissionItem(_weakref.proxy(listBox), mission)
			missionWnd.SetPosition(0, len(listBox.itemList) * missionWnd.GetHeight(), True)
			missionWnd.Show()
			listBox.AppendItem(missionWnd)
		listBox.RefreshAll()
		
	def UpdateMissionInfo(self, cmd):
		cmdList = cmd.split("#")
		missionData = {
			"id": int(cmdList[0]),
			"item": int(cmdList[1]),
			"type": int(cmdList[2]),
			"subtype": int(cmdList[3]),
			"levelrange": int(cmdList[4]),
			"value": int(cmdList[5]),
			"maxvalue": int(cmdList[6]),
			"lefttime": app.GetGlobalTimeStamp()+int(cmdList[7]),
			"maxtime": int(cmdList[8]),
			"endTime": cmdList[9],
			"gold": [int(cmdList[10]), int(cmdList[11])],
			"exp": [int(cmdList[12]), int(cmdList[13])],
			"reward_get": int(cmdList[14]),
			"items": [ [int(cmdList[16+(j*2)]), int(cmdList[17+(j*2)])] for j in xrange(int(cmdList[15])) ],
			"needUpdate": 0,
		}
		for j in xrange(len(self.__missionData)):
			if self.__missionData[j]["id"] == missionData["id"]:
				self.__missionData[j] = missionData
				self.Refresh()
				return
		self.__missionData.append(missionData)
		self.Refresh()
	def UpdateMissionEndTime(self, missionID, endTime):
		for mission in self.__missionData:
			if mission["id"] == missionID:
				mission["endTime"] = endTime
	def UpdateMissionValue(self, missionID, value):
		for mission in self.__missionData:
			if mission["id"] == missionID:
				mission["value"] = value
				mission["needUpdate"] = 1 if mission["value"] == mission["value"] else 2
	def RemoveMissionData(self, missionID):
		for j in xrange(len(self.__missionData)):
			if self.__missionData[j]["id"] == missionID:
				del self.__missionData[j]
				break
		self.Refresh()
	def RewardMissionData(self, missionID, rewardStatus):
		for mission in self.__missionData:
			if mission["id"] == missionID:
				mission["reward_get"] = rewardStatus
				mission["needUpdate"] = 1
		self.Refresh()
class ScrollBarNew(ui.Window):
	SCROLLBAR_WIDTH = 10
	SCROLL_BTN_XDIST = 2
	SCROLL_BTN_YDIST = 2
	class MiddleBar(ui.DragButton):
		def __init__(self):
			ui.DragButton.__init__(self)
			self.AddFlag("movable")
			self.SetWindowName("scrollbar_middlebar")
		def MakeImage(self):
			top = ui.ExpandedImageBox()
			top.SetParent(self)
			top.LoadImage(IMG_DIR+"scrollbar_ex/scrollbar_top.tga")
			top.AddFlag("not_pick")
			top.Show()
			topScale = ui.ExpandedImageBox()
			topScale.SetParent(self)
			topScale.SetPosition(0, top.GetHeight())
			topScale.LoadImage(IMG_DIR+"scrollbar_ex/scrollbar_scale.tga")
			topScale.AddFlag("not_pick")
			topScale.Show()
			bottom = ui.ExpandedImageBox()
			bottom.SetParent(self)
			bottom.LoadImage(IMG_DIR+"scrollbar_ex/scrollbar_bottom.tga")
			bottom.AddFlag("not_pick")
			bottom.Show()
			bottomScale = ui.ExpandedImageBox()
			bottomScale.SetParent(self)
			bottomScale.LoadImage(IMG_DIR+"scrollbar_ex/scrollbar_scale.tga")
			bottomScale.AddFlag("not_pick")
			bottomScale.Show()
			middle = ui.ExpandedImageBox()
			middle.SetParent(self)
			middle.LoadImage(IMG_DIR+"scrollbar_ex/scrollbar_mid.tga")
			middle.AddFlag("not_pick")
			middle.Show()
			self.top = top
			self.topScale = topScale
			self.bottom = bottom
			self.bottomScale = bottomScale
			self.middle = middle
		def SetSize(self, height):
			minHeight = self.top.GetHeight() + self.bottom.GetHeight() + self.middle.GetHeight()
			height = max(minHeight, height)
			ui.DragButton.SetSize(self, 10, height)
			scale = (height - minHeight) / 2 
			extraScale = 0
			if (height - minHeight) % 2 == 1:
				extraScale = 1
			self.topScale.SetRenderingRect(0, 0, 0, scale - 1)
			self.middle.SetPosition(0, self.top.GetHeight() + scale)
			self.bottomScale.SetPosition(0, self.middle.GetBottom())
			self.bottomScale.SetRenderingRect(0, 0, 0, scale - 1 + extraScale)
			self.bottom.SetPosition(0, height - self.bottom.GetHeight())
	def __init__(self):
		ui.Window.__init__(self)
		self.pageSize = 1
		self.curPos = 0.0
		self.eventScroll = None
		self.eventArgs = None
		self.lockFlag = False
		self.CreateScrollBar()
		self.SetScrollBarSize(0)
		self.scrollStep = 0.2
		self.SetWindowName("NONAME_ScrollBar")
	def __del__(self):
		ui.Window.__del__(self)
	def CreateScrollBar(self):
		topImage = ui.ExpandedImageBox()
		topImage.SetParent(self)
		topImage.AddFlag("not_pick")
		topImage.LoadImage(IMG_DIR+"scrollbar_ex/scroll_top.tga")
		topImage.Show()
		bottomImage = ui.ExpandedImageBox()
		bottomImage.SetParent(self)
		bottomImage.AddFlag("not_pick")
		bottomImage.LoadImage(IMG_DIR+"scrollbar_ex/scroll_bottom.tga")
		bottomImage.Show()
		middleImage = ui.ExpandedImageBox()
		middleImage.SetParent(self)
		middleImage.AddFlag("not_pick")
		middleImage.SetPosition(0, topImage.GetHeight())
		middleImage.LoadImage(IMG_DIR+"scrollbar_ex/scroll_mid.tga")
		middleImage.Show()
		self.topImage = topImage
		self.bottomImage = bottomImage
		self.middleImage = middleImage
		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(ui.__mem_func__(self.OnMove))
		middleBar.Show()
		middleBar.MakeImage()
		middleBar.SetSize(12)
		self.middleBar = middleBar
	def Destroy(self):
		self.eventScroll = None
		self.eventArgs = None
	def SetScrollEvent(self, event, *args):
		self.eventScroll = event
		self.eventArgs = args
	def SetMiddleBarSize(self, pageScale):
		self.middleBar.SetSize(int(pageScale * float(self.GetHeight() - (self.SCROLL_BTN_YDIST*2))))
		realHeight = self.GetHeight() - (self.SCROLL_BTN_YDIST*2) - self.middleBar.GetHeight()
		self.pageSize = realHeight

	def SetScrollBarSize(self, height):
		self.SetSize(self.SCROLLBAR_WIDTH, height)
		self.pageSize = height - self.SCROLL_BTN_YDIST*2 - self.middleBar.GetHeight() - 45
		middleImageScale = float((height - self.SCROLL_BTN_YDIST*2) - self.middleImage.GetHeight()) / float(self.middleImage.GetHeight() - 45)
		self.middleImage.SetRenderingRect(0, 0, 0, middleImageScale)
		self.bottomImage.SetPosition(0, height - self.bottomImage.GetHeight())
		self.middleBar.SetRestrictMovementArea(self.SCROLL_BTN_XDIST, self.SCROLL_BTN_YDIST, \
			self.middleBar.GetWidth(), (height) - self.SCROLL_BTN_YDIST * 2)
		self.middleBar.SetPosition(self.SCROLL_BTN_XDIST, self.SCROLL_BTN_YDIST)
	def SetScrollStep(self, step):
		self.scrollStep = step
	def OnUp(self):
		self.SetPos(self.curPos-self.scrollStep)
	def OnDown(self):
		self.SetPos(self.curPos+self.scrollStep)
	def GetScrollStep(self):
		return self.scrollStep
	def GetPos(self):
		return self.curPos
	def OnUp(self):
		self.SetPos(self.curPos-self.scrollStep)
	def OnDown(self):
		self.SetPos(self.curPos+self.scrollStep)
	def SetPos(self, pos, moveEvent = True):
		pos = max(0.0, pos)
		pos = min(1.0, pos)
		newPos = float(self.pageSize) * pos
		self.middleBar.SetPosition(self.SCROLL_BTN_XDIST, int(newPos) + self.SCROLL_BTN_YDIST)
		if moveEvent == True:
			self.OnMove()
	def OnMove(self):
		if self.lockFlag:
			return
		if 0 == self.pageSize:
			return
		(xLocal, yLocal) = self.middleBar.GetLocalPosition()
		self.curPos = float(yLocal - self.SCROLL_BTN_YDIST) / float(self.pageSize)
		if self.eventScroll:
			apply(self.eventScroll, self.eventArgs)
	def OnMouseLeftButtonDown(self):
		(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()
		newPos = float(yMouseLocalPosition) / float(self.GetHeight())
		self.SetPos(newPos)
	def LockScroll(self):
		self.lockFlag = True
	def UnlockScroll(self):
		self.lockFlag = False

class Grid: # from KeN
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.reset()
	def find_blank(self, width, height):
		if width > self.width or height > self.height:
			return -1

		for row in range(self.height):
			for col in range(self.width):
				index = row * self.width + col
				if self.is_empty(index, width, height):
					return index
		return -1
	def put(self, pos, width, height):
		if not self.is_empty(pos, width, height):
			return False
		for row in range(height):
			start = pos + (row * self.width)
			self.grid[start] = True
			col = 1
			while col < width:
				self.grid[start + col] = True
				col += 1
		return True
	def clear(self, pos, width, height):
		if pos < 0 or pos >= (self.width * self.height):
			return
		for row in range(height):
			start = pos + (row * self.width)
			self.grid[start] = True
			col = 1
			while col < width:
				self.grid[start + col] = False
				col += 1
	def is_empty(self, pos, width, height):
		if pos < 0:
			return False
		row = pos // self.width
		if (row + height) > self.height:
			return False
		if (pos + width) > ((row * self.width) + self.width):
			return False
		for row in range(height):
			start = pos + (row * self.width)
			if self.grid[start]:
				return False
			col = 1
			while col < width:
				if self.grid[start + col]:
					return False
				col += 1
		return True
	def get_size(self):
		return self.width * self.height
	def reset(self):
		self.grid = [False] * (self.width * self.height)
		#self.put(self.width,1,1) # fix from dracaryS

class ValueOperator(object):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return str(self.value)
	def __neg__(self):
		self.value-=1
		return self.value
	def __pos__(self):
		self.value+=1
		return self.value
