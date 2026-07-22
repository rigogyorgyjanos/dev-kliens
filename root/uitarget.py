import app
import ui
import player
import net
import wndMgr
import messenger
import guild
import chr
import nonplayer
import localeInfo
import constInfo
import uiToolTip
import item
import uiToolTip
import math


if app.ENABLE_VIEW_ELEMENT:
	ELEMENT_IMAGE_DIC = {1: "elect", 2: "fire", 3: "ice", 4: "wind", 5: "earth", 6 : "dark"}
	
if app.ENABLE_SEND_TARGET_INFO:
	def HAS_FLAG(value, flag):
		return (value & flag) == flag

BASIC_SKILL_BOOKS = [50401, 50402, 50403, 50404, 50405, 50406, 50416, 50417, 50418, 50419, 50420, 50421, 50431, 50432, 50433, 50434, 50435, 50436, 50446, 50447, 50448, 50449, 50450, 50451, 50461, 50462, 50463, 50464, 50465, 50466, 50476, 50477, 50478, 50479, 50480, 50481, 50491, 50492, 50493, 50494, 50495, 50496, 50506, 50507, 50508, 50509, 50510, 50511]


class TargetBoard(ui.ThinBoard):
	if app.ENABLE_SEND_TARGET_INFO:
		class InfoBoard(ui.ThinBoard):
			class ItemListBoxItem(ui.ListBoxExNew.Item):
				def __init__(self, width):
					ui.ListBoxExNew.Item.__init__(self)

					image = ui.ExpandedImageBox()
					image.SetParent(self)
					image.Show()
					self.image = image

					nameLine = ui.TextLine()
					nameLine.SetParent(self)
					nameLine.SetPosition(32 + 5, 0)
					nameLine.Show()
					self.nameLine = nameLine
					self.itemScrollBarB = None

					self.SetSize(width, 32 + 5)
					
				def LoadImage(self, image, name = None):
					self.image.LoadImage(image)
					self.SetSize(self.GetWidth(), self.image.GetHeight() + 5 * (self.image.GetHeight() / 32))
					self.nameLine.SetPosition(32 + 5, self.GetHeight() / 2 - 10)
					if name != None:
						self.SetText(name)

				def SetText(self, text):
					self.nameLine.SetText(text)

				def RefreshHeight(self):
					ui.ListBoxExNew.Item.RefreshHeight(self)
					self.image.SetRenderingRect(0.0, 0.0 - float(self.removeTop) / float(self.GetHeight()), 0.0, 0.0 - float(self.removeBottom) / float(self.GetHeight()))
					self.image.SetPosition(0, - self.removeTop)
					self.nameLine.SetPosition(32 + 5, self.GetHeight() / 2 - 10 - self.removeTop)

			MAX_ITEM_COUNT = 5

			EXP_BASE_LVDELTA = [
				1,  #  -15 0
				5,  #  -14 1
				10, #  -13 2
				20, #  -12 3
				30, #  -11 4
				50, #  -10 5
				70, #  -9  6
				80, #  -8  7
				85, #  -7  8
				90, #  -6  9
				92, #  -5  10
				94, #  -4  11
				96, #  -3  12
				98, #  -2  13
				100,	#  -1  14
				100,	#  0   15
				105,	#  1   16
				110,	#  2   17
				115,	#  3   18
				120,	#  4   19
				125,	#  5   20
				130,	#  6   21
				135,	#  7   22
				140,	#  8   23
				145,	#  9   24
				150,	#  10  25
				155,	#  11  26
				160,	#  12  27
				165,	#  13  28
				170,	#  14  29
				180,	#  15  30
			]

			RACE_FLAG_TO_NAME = {
				1 << 0  : localeInfo.TARGET_INFO_RACE_ANIMAL,
				1 << 1 	: localeInfo.TARGET_INFO_RACE_UNDEAD,
				1 << 2  : localeInfo.TARGET_INFO_RACE_DEVIL,
				1 << 3  : localeInfo.TARGET_INFO_RACE_HUMAN,
				1 << 4  : localeInfo.TARGET_INFO_RACE_ORC,
				1 << 5  : localeInfo.TARGET_INFO_RACE_MILGYO,
			}

			SUB_RACE_FLAG_TO_NAME = {
				1 << 11 : localeInfo.TARGET_INFO_RACE_ELEC,
				1 << 12 : localeInfo.TARGET_INFO_RACE_FIRE,
				1 << 13 : localeInfo.TARGET_INFO_RACE_ICE,
				1 << 14 : localeInfo.TARGET_INFO_RACE_WIND,
				1 << 15 : localeInfo.TARGET_INFO_RACE_EARTH,
				1 << 16 : localeInfo.TARGET_INFO_RACE_DARK,
			}

			STONE_START_VNUM = 28030
			STONE_LAST_VNUM = 28042

			BOARD_WIDTH = 250

			def __init__(self):
				ui.ThinBoard.__init__(self)

				self.HideCorners(self.LT)
				self.HideCorners(self.RT)
				self.HideLine(self.T)

				self.race = 0
				self.hasItems = False

				self.itemTooltip = uiToolTip.ItemToolTip()
				self.itemTooltip.HideToolTip()

				self.stoneImg = None
				self.stoneVnum = None
				self.lastStoneVnum = 0
				self.nextStoneIconChange = 0
				self.itemScrollBarB = None
				self.itemSlotS = None
				self.itemslotInfos = []
				self.extraSlots = [0, 0]
				self.LastSlot = -1
				
				self.SetSize(self.BOARD_WIDTH, 0)


			def __del__(self):
				ui.ThinBoard.__del__(self)

			def __UpdatePosition(self, targetBoard):
				self.SetPosition(targetBoard.GetLeft() + (targetBoard.GetWidth() - self.GetWidth()) / 2, targetBoard.GetBottom() - 17)

			def Open(self, targetBoard, race):
				self.__LoadInformation(race)

				self.SetSize(self.BOARD_WIDTH, self.yPos + 10)
				self.__UpdatePosition(targetBoard)

				self.Show()

				if app.__BL_MOUSE_WHEEL_TOP_WINDOW__:
					wndMgr.SetWheelTopWindow(self.hWnd)

			def Refresh(self):
				self.__LoadInformation(self.race)
				self.SetSize(self.BOARD_WIDTH, self.yPos + 10)

			def Close(self):
				if self.itemScrollBarB:
					self.itemScrollBarB.Hide()
				self.itemScrollBarB = None
				if self.itemSlotS:
					self.itemSlotS.Hide()
				self.itemSlotS = None
				self.itemTooltip.HideToolTip()
				self.itemslotInfos = []
				self.extraSlots = [0, 0]
				self.Hide()

				if app.__BL_MOUSE_WHEEL_TOP_WINDOW__:
					wndMgr.ClearWheelTopWindow()

			if app.__BL_MOUSE_WHEEL_TOP_WINDOW__:
				def OnMouseWheelButtonUp(self):
					if self.itemScrollBarB and self.itemScrollBarB.IsShow():
						self.itemScrollBarB.OnUp()
						return True
					return False

				def OnMouseWheelButtonDown(self):
					if self.itemScrollBarB and self.itemScrollBarB.IsShow():
						self.itemScrollBarB.OnDown()
						return True
					return False

			def __LoadInformation(self, race):
				self.yPos = 7
				self.children = []
				self.race = race
				self.stoneImg = None
				self.stoneVnum = None
				self.nextStoneIconChange = 0
				self.itemslotInfos = []
				self.extraSlots = [0, 0]
				self.LastSlot = -1


				self.__LoadInformation_Default(race)
				self.__LoadInformation_Race(race)
				self.__LoadInformation_Drops(race)

			def __LoadInformation_Default_GetHitRate(self, race):
				attacker_dx = nonplayer.GetMonsterDX(race)
				attacker_level = nonplayer.GetMonsterLevel(race)

				self_dx = player.GetStatus(player.DX)
				self_level = player.GetStatus(player.LEVEL)

				iARSrc = min(90, (attacker_dx * 4 + attacker_level * 2) / 6)
				iERSrc = min(90, (self_dx * 4 + self_level * 2) / 6)

				fAR = (float(iARSrc) + 210.0) / 300.0
				fER = (float(iERSrc) * 2 + 5) / (float(iERSrc) + 95) * 3.0 / 10.0

				return fAR - fER

			def __LoadInformation_Default(self, race):
				self.AppendSeperator()
				self.AppendTextLine(localeInfo.TARGET_INFO_MAX_HP % str(nonplayer.GetMonsterMaxHP(race)))

				# calc att damage
				monsterLevel = nonplayer.GetMonsterLevel(race)
				fHitRate = self.__LoadInformation_Default_GetHitRate(race)
				iDamMin, iDamMax = nonplayer.GetMonsterDamage(race)
				iDamMin = int((iDamMin + nonplayer.GetMonsterST(race)) * 2 * fHitRate) + monsterLevel * 2
				iDamMax = int((iDamMax + nonplayer.GetMonsterST(race)) * 2 * fHitRate) + monsterLevel * 2
				iDef = player.GetStatus(player.DEF_GRADE) * (100 + player.GetStatus(player.DEF_BONUS)) / 100
				fDamMulti = nonplayer.GetMonsterDamageMultiply(race)
				iDamMin = int(max(0, iDamMin - iDef) * fDamMulti)
				iDamMax = int(max(0, iDamMax - iDef) * fDamMulti)
				if iDamMin < 1:
					iDamMin = 1
				if iDamMax < 5:
					iDamMax = 5
				self.AppendTextLine(localeInfo.TARGET_INFO_DAMAGE % (str(iDamMin), str(iDamMax)))

				idx = min(len(self.EXP_BASE_LVDELTA) - 1, max(0, (monsterLevel + 15) - player.GetStatus(player.LEVEL)))
				iExp = nonplayer.GetMonsterExp(race) * self.EXP_BASE_LVDELTA[idx] / 100
				self.AppendTextLine(localeInfo.TARGET_INFO_EXP % str(iExp))

			def __LoadInformation_Race(self, race):
				dwRaceFlag = nonplayer.GetMonsterRaceFlag(race)
				self.AppendSeperator()

				mainrace = ""
				subrace = ""
				for i in xrange(17):
					curFlag = 1 << i
					if HAS_FLAG(dwRaceFlag, curFlag):
						if self.RACE_FLAG_TO_NAME.has_key(curFlag):
							mainrace += self.RACE_FLAG_TO_NAME[curFlag] + ", "
						elif self.SUB_RACE_FLAG_TO_NAME.has_key(curFlag):
							subrace += self.SUB_RACE_FLAG_TO_NAME[curFlag] + ", "
				if nonplayer.IsMonsterStone(race):
					mainrace += localeInfo.TARGET_INFO_RACE_METIN + ", "
				if mainrace == "":
					mainrace = localeInfo.TARGET_INFO_NO_RACE
				else:
					mainrace = mainrace[:-2]
				if subrace == "":
					subrace = localeInfo.TARGET_INFO_NO_RACE
				else:
					subrace = subrace[:-2]

				self.AppendTextLine(localeInfo.TARGET_INFO_MAINRACE % mainrace)
				self.AppendTextLine(localeInfo.TARGET_INFO_SUBRACE % subrace)
			
			def __ItemSortFunc(self, elem):
				vnum = 0
				if type(elem["vnum"]) == int:
					vnum = elem["vnum"]
				else:
					vnum = elem["vnum"][0]
				if elem["type"] == 1: # Fegyver
					if elem["itemheight"] == 1:
						vnum += 400000
					elif elem["itemheight"] == 2:
						vnum += 300000
					elif elem["itemheight"] == 3:
						vnum += 150000
				elif elem["type"] == 2: # Vért
					vnum += 300000
				elif elem["type"] == 3: # Accesory
					vnum += 400000
				return vnum

			def __LoadInformation_Drops(self, race):
				self.AppendSeperator()
				
				if race in constInfo.MONSTER_INFO_DATA:
					if len(constInfo.MONSTER_INFO_DATA[race]["items"]) == 0:
						if self.itemScrollBarB:
							self.itemScrollBarB.Hide()
							self.itemScrollBarB = None
						self.AppendTextLine(localeInfo.TARGET_INFO_NO_ITEM_TEXT)
					else:

						itemNeed = {}
						addedItemID = []
						seperationNeed = False
						for curItem in constInfo.MONSTER_INFO_DATA[race]["items"]:
							if not seperationNeed and curItem["itemheight"] > 1:
								seperationNeed = True
							if curItem.__contains__("vnum_list"):
								curItem["vnum"] = curItem["vnum_list"]
								curItem["countmin"] = curItem["count"]
								curItem["countmax"] = curItem["count"]
								itemNeed[curItem["vnum"][0]] = curItem
								#height += self.AppendItem(itemListBox, curItem["vnum_list"], curItem["count"])
							else:
								if curItem["vnum"] in BASIC_SKILL_BOOKS:
									curItem["vnum"] = 50300
								if curItem["vnum"] not in addedItemID:
									curItem["countmin"] = curItem["count"]
									curItem["countmax"] = curItem["count"]
									itemNeed[curItem["vnum"]] = curItem
									addedItemID.append(curItem["vnum"])
								else:
									if (curItem["count"] < itemNeed[curItem["vnum"]]["countmin"]):
										itemNeed[curItem["vnum"]]["countmin"] = curItem["count"]
									if (curItem["count"] > itemNeed[curItem["vnum"]]["countmax"]):
										itemNeed[curItem["vnum"]]["countmax"] = curItem["count"]

						sortable = []
						for x in itemNeed:
							sortable.append(itemNeed[x])
						sortable.sort(key = self.__ItemSortFunc)

						forbiddenSlots = []
						slotNumber = 0
						for curItem in sortable:
							if curItem.__contains__("vnum") and type(curItem["vnum"]) == int:
								itemVnum = curItem["vnum"]
							elif curItem.__contains__("vnum_list"):
								itemVnum = curItem["vnum_list"][0]

							while slotNumber in forbiddenSlots:
								slotNumber += 1

							if curItem["itemheight"] > 1:
								if curItem["itemheight"] > 2:
									forbiddenSlots.append(slotNumber+7)
									forbiddenSlots.append(slotNumber+14)
								else:
									forbiddenSlots.append(slotNumber+7)
							curItem["appendSlot"] = slotNumber
							slotNumber += 1

						self.itemSlotS = ui.GridSlotWindow()
						self.itemSlotS.SetParent(self)
						heightSlots	= math.ceil(float((float(max(forbiddenSlots)+1 if len(forbiddenSlots) > 0 else slotNumber) / float(7))))
						if len(forbiddenSlots) > 0:
							if slotNumber < max(forbiddenSlots):
								slotNumber =  max(forbiddenSlots)
								heightSlots	= math.ceil(float((float(max(forbiddenSlots)+1) / float(7))))

						self.itemSlotS.ArrangeSlot(0, 7, heightSlots, 32, 32, 0, 0)
						self.itemSlotS.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
						self.itemSlotS.SetWindowHorizontalAlignCenter()
						self.itemSlotS.SetPosition(0, 82)
						self.itemSlotS.SetOverInItemEvent(self.OnShowItemTooltip)
						self.itemSlotS.SetOverOutItemEvent(self.OnHideItemTooltip)
						self.yPos += (heightSlots*32)
						self.itemSlotS.Show()

						self.SetSize(self.BOARD_WIDTH, self.yPos + 10)

						for curItem in sortable:
							if curItem.__contains__("vnum") and type(curItem["vnum"]) == int:
								itemVnum = curItem["vnum"]
							elif curItem.__contains__("vnum_list"):
								itemVnum = curItem["vnum_list"][0]
								if curItem["type"] == 4:
									self.extraSlots[1] = curItem["appendSlot"]
									self.lastStoneVnum = self.STONE_LAST_VNUM + int(curItem["vnum_list"][len(curItem["vnum_list"]) - 1] % 1000 // 100 * 100)

							if itemVnum == 50300:
								self.extraSlots[0] = curItem["appendSlot"]

							# self.itemSlotS.ActivateSlot(5)
							self.itemslotInfos.append({"slot":curItem["appendSlot"], "itemVnum":itemVnum, "countmax":curItem["countmax"], "countmin":curItem["countmin"]})
							self.itemSlotS.SetItemSlot(curItem["appendSlot"], itemVnum, 0 if curItem["countmax"] <= 1 else curItem["countmax"])

				else:
					self.AppendTextLine(localeInfo.TARGET_INFO_NO_ITEM_TEXT)

			def AppendTextLine(self, text):
				textLine = ui.TextLine()
				textLine.SetParent(self)
				textLine.SetWindowHorizontalAlignCenter()
				textLine.SetHorizontalAlignCenter()
				textLine.SetText(text)
				textLine.SetPosition(0, self.yPos)
				textLine.Show()

				self.children.append(textLine)
				self.yPos += 17

			def AppendSeperator(self):
				img = ui.ImageBox()
				img.LoadImage("d:/ymir work/ui/seperator.tga")
				self.AppendWindow(img)
				img.SetPosition(img.GetLeft(), img.GetTop() - 15)
				self.yPos -= 15

			def AppendItem(self, listBox, vnums, count):
				if type(vnums) == int:
					vnum = vnums
				else:
					vnum = vnums[0]

				item.SelectItem(vnum)
				itemName = item.GetItemName()
				if type(vnums) != int and len(vnums) > 1:
					vnums = sorted(vnums)
					realName = itemName[:itemName.find("+")]
					if item.GetItemType() == item.ITEM_TYPE_METIN:
						realName = localeInfo.TARGET_INFO_STONE_NAME
						itemName = realName + "+0 - +4"
					else:
						itemName = realName + "+" + str(vnums[0] % 10) + " - +" + str(vnums[len(vnums) - 1] % 10)
					vnum = vnums[len(vnums) - 1]

				myItem = self.ItemListBoxItem(listBox.GetWidth())
				myItem.LoadImage(item.GetIconImageFileName())
				if count <= 1:
					myItem.SetText(itemName)
				else:
					myItem.SetText("%dx %s" % (count, itemName))
				myItem.SAFE_SetOverInEvent(self.OnShowItemTooltip, vnum)
				myItem.SAFE_SetOverOutEvent(self.OnHideItemTooltip)
				listBox.AppendItem(myItem)

				if item.GetItemType() == item.ITEM_TYPE_METIN:
					self.stoneImg = myItem
					self.stoneVnum = vnums
					self.lastStoneVnum = self.STONE_LAST_VNUM + vnums[len(vnums) - 1] % 1000 / 100 * 100

				return myItem.GetHeight()
			

			def OnShowItemTooltip(self, slot, replace = False, newID = 0, refresh = True):
				if refresh:
					self.LastSlot = slot
				vnum = 0
				chosenItem = -1
				for items in self.itemslotInfos:
					if items["slot"] == slot:
						if replace and newID != 0:
							items["itemVnum"] = newID
						vnum = items["itemVnum"]
						chosenItem = items
				if vnum != 0 and refresh:
					if chosenItem != -1:
						# self.itemTooltip.SetItemToolTip(vnum, iLink = True, countmins = chosenItem["countmin"], countmaxs = chosenItem["countmax"])
						self.itemTooltip.SetItemToolTip(vnum)
					else:
						# self.itemTooltip.SetItemToolTip(vnum, iLink = True)
						self.itemTooltip.SetItemToolTip(vnum)

			def OnHideItemTooltip(self):
				self.itemTooltip.HideToolTip()

			def AppendWindow(self, wnd, x = 0, width = 0, height = 0):
				if width == 0:
					width = wnd.GetWidth()
				if height == 0:
					height = wnd.GetHeight()

				wnd.SetParent(self)
				if x == 0:
					wnd.SetPosition((self.GetWidth() - width) / 2, self.yPos)
				else:
					wnd.SetPosition(x, self.yPos)
				wnd.Show()

				self.children.append(wnd)
				self.yPos += height + 5

			def OnUpdate(self):
				if self.IsShow() and app.GetTime() >= self.nextStoneIconChange:
					if self.extraSlots[1] != 0:
						nextImg = self.lastStoneVnum + 1
						if nextImg % 100 > self.STONE_LAST_VNUM % 100:
							nextImg -= (self.STONE_LAST_VNUM - self.STONE_START_VNUM) + 1
						self.lastStoneVnum = nextImg
						
						self.OnShowItemTooltip(self.extraSlots[1], replace = True, newID = nextImg, refresh = self.LastSlot == self.extraSlots[1])
						
						if self.itemSlotS:
							self.itemSlotS.ClearSlot(self.extraSlots[1])
							self.itemSlotS.SetItemSlot(self.extraSlots[1], nextImg, 0)
					self.nextStoneIconChange = app.GetTime() + 2.5

					# item.SelectItem(nextImg)
					# itemName = item.GetItemName()
					# realName = itemName[:itemName.find("+")]
					# realName = realName + "+0 - +4"
					# self.stoneImg.LoadImage(item.GetIconImageFileName(), realName)

					# if self.itemTooltip.IsShow() and self.itemTooltip.isStone:
						# self.itemTooltip.SetItemToolTip(nextImg)
						
	BUTTON_NAME_LIST = ( 
		localeInfo.TARGET_BUTTON_WHISPER, 
		localeInfo.TARGET_BUTTON_EXCHANGE, 
		localeInfo.TARGET_BUTTON_FIGHT, 
		localeInfo.TARGET_BUTTON_ACCEPT_FIGHT, 
		localeInfo.TARGET_BUTTON_AVENGE, 
		localeInfo.TARGET_BUTTON_FRIEND, 
		localeInfo.TARGET_BUTTON_INVITE_PARTY, 
		localeInfo.TARGET_BUTTON_LEAVE_PARTY, 
		localeInfo.TARGET_BUTTON_EXCLUDE, 
		localeInfo.TARGET_BUTTON_INVITE_GUILD,
		localeInfo.TARGET_BUTTON_DISMOUNT,
		localeInfo.TARGET_BUTTON_EXIT_OBSERVER,
		localeInfo.TARGET_BUTTON_VIEW_EQUIPMENT,
		localeInfo.TARGET_BUTTON_REQUEST_ENTER_PARTY,
		localeInfo.TARGET_BUTTON_BUILDING_DESTROY,
		localeInfo.TARGET_BUTTON_EMOTION_ALLOW,
		"VOTE_BLOCK_CHAT",
	)

	GRADE_NAME =	{
						nonplayer.PAWN : localeInfo.TARGET_LEVEL_PAWN,
						nonplayer.S_PAWN : localeInfo.TARGET_LEVEL_S_PAWN,
						nonplayer.KNIGHT : localeInfo.TARGET_LEVEL_KNIGHT,
						nonplayer.S_KNIGHT : localeInfo.TARGET_LEVEL_S_KNIGHT,
						nonplayer.BOSS : localeInfo.TARGET_LEVEL_BOSS,
						nonplayer.KING : localeInfo.TARGET_LEVEL_KING,
					}
	EXCHANGE_LIMIT_RANGE = 3000

	def __init__(self):
		ui.ThinBoard.__init__(self)

		name = ui.TextLine()
		name.SetParent(self)
		name.SetDefaultFontName()
		name.SetOutline()
		name.Show()

		if app.__AUTO_QUQUE_ATTACK__:
			autoFarmText = ui.TextLine()
			autoFarmText.SetParent(self)
			autoFarmText.SetOutline()
			autoFarmText.SetHorizontalAlignCenter()
			autoFarmText.SetText("|Eemoji/key_shift|e + |Eemoji/key_rclick|e Metinkő kijelölés")
			autoFarmText.Hide()
			self.autoFarmText = autoFarmText

			autoFarmBtn = ui.Button()
			autoFarmBtn.SetParent(self)
			autoFarmBtn.SetUpVisual("d:/ymir work/ui/pattern/q_mark_01.tga")
			autoFarmBtn.SetOverVisual("d:/ymir work/ui/pattern/q_mark_02.tga")
			autoFarmBtn.SetDownVisual("d:/ymir work/ui/pattern/q_mark_01.tga")
			autoFarmBtn.SetEvent(ui.__mem_func__(self.__AutoFarmInfo))
			autoFarmBtn.Hide()
			self.autoFarmBtn = autoFarmBtn

			self.autoFarmInfo = None

		hpGauge = ui.Gauge()
		hpGauge.SetParent(self)
		hpGauge.MakeGauge(130, "red")
		hpGauge.Hide()

		closeButton = ui.Button()
		closeButton.SetParent(self)
		closeButton.SetUpVisual("d:/ymir work/ui/public/close_button_01.sub")
		closeButton.SetOverVisual("d:/ymir work/ui/public/close_button_02.sub")
		closeButton.SetDownVisual("d:/ymir work/ui/public/close_button_03.sub")
		closeButton.SetPosition(30, 13)

		if localeInfo.IsARABIC():
			hpGauge.SetPosition(55, 17)
			hpGauge.SetWindowHorizontalAlignLeft()
			closeButton.SetWindowHorizontalAlignLeft()
		else:
			hpGauge.SetPosition(175, 17)
			hpGauge.SetWindowHorizontalAlignRight()
			closeButton.SetWindowHorizontalAlignRight()
		
		if app.ENABLE_SEND_TARGET_INFO:
			infoButton = ui.Button()
			infoButton.SetParent(self)
			infoButton.SetUpVisual("d:/ymir work/ui/pattern/q_mark_01.tga")
			infoButton.SetOverVisual("d:/ymir work/ui/pattern/q_mark_02.tga")
			infoButton.SetDownVisual("d:/ymir work/ui/pattern/q_mark_01.tga")
			infoButton.SetEvent(ui.__mem_func__(self.OnPressedInfoButton))
			infoButton.Hide()

			infoBoard = self.InfoBoard()
			infoBoard.Hide()
			infoButton.showWnd = infoBoard

		closeButton.SetEvent(ui.__mem_func__(self.OnPressedCloseButton))
		closeButton.Show()

		self.buttonDict = {}
		self.showingButtonList = []
		for buttonName in self.BUTTON_NAME_LIST:
			button = ui.Button()
			button.SetParent(self)
		
			if localeInfo.IsARABIC():
				button.SetUpVisual("d:/ymir work/ui/public/Small_Button_01.sub")
				button.SetOverVisual("d:/ymir work/ui/public/Small_Button_02.sub")
				button.SetDownVisual("d:/ymir work/ui/public/Small_Button_03.sub")
			else:
				button.SetUpVisual("d:/ymir work/ui/public/small_thin_button_01.sub")
				button.SetOverVisual("d:/ymir work/ui/public/small_thin_button_02.sub")
				button.SetDownVisual("d:/ymir work/ui/public/small_thin_button_03.sub")
			
			button.SetWindowHorizontalAlignCenter()
			button.SetText(buttonName)
			button.Hide()
			self.buttonDict[buttonName] = button
			self.showingButtonList.append(button)

		self.buttonDict[localeInfo.TARGET_BUTTON_WHISPER].SetEvent(ui.__mem_func__(self.OnWhisper))
		self.buttonDict[localeInfo.TARGET_BUTTON_EXCHANGE].SetEvent(ui.__mem_func__(self.OnExchange))
		self.buttonDict[localeInfo.TARGET_BUTTON_FIGHT].SetEvent(ui.__mem_func__(self.OnPVP))
		self.buttonDict[localeInfo.TARGET_BUTTON_ACCEPT_FIGHT].SetEvent(ui.__mem_func__(self.OnPVP))
		self.buttonDict[localeInfo.TARGET_BUTTON_AVENGE].SetEvent(ui.__mem_func__(self.OnPVP))
		self.buttonDict[localeInfo.TARGET_BUTTON_FRIEND].SetEvent(ui.__mem_func__(self.OnAppendToMessenger))
		self.buttonDict[localeInfo.TARGET_BUTTON_FRIEND].SetEvent(ui.__mem_func__(self.OnAppendToMessenger))
		self.buttonDict[localeInfo.TARGET_BUTTON_INVITE_PARTY].SetEvent(ui.__mem_func__(self.OnPartyInvite))
		self.buttonDict[localeInfo.TARGET_BUTTON_LEAVE_PARTY].SetEvent(ui.__mem_func__(self.OnPartyExit))
		self.buttonDict[localeInfo.TARGET_BUTTON_EXCLUDE].SetEvent(ui.__mem_func__(self.OnPartyRemove))

		self.buttonDict[localeInfo.TARGET_BUTTON_INVITE_GUILD].SAFE_SetEvent(self.__OnGuildAddMember)
		self.buttonDict[localeInfo.TARGET_BUTTON_DISMOUNT].SAFE_SetEvent(self.__OnDismount)
		self.buttonDict[localeInfo.TARGET_BUTTON_EXIT_OBSERVER].SAFE_SetEvent(self.__OnExitObserver)
		self.buttonDict[localeInfo.TARGET_BUTTON_VIEW_EQUIPMENT].SAFE_SetEvent(self.__OnViewEquipment)
		self.buttonDict[localeInfo.TARGET_BUTTON_REQUEST_ENTER_PARTY].SAFE_SetEvent(self.__OnRequestParty)
		self.buttonDict[localeInfo.TARGET_BUTTON_BUILDING_DESTROY].SAFE_SetEvent(self.__OnDestroyBuilding)
		self.buttonDict[localeInfo.TARGET_BUTTON_EMOTION_ALLOW].SAFE_SetEvent(self.__OnEmotionAllow)
		
		self.buttonDict["VOTE_BLOCK_CHAT"].SetEvent(ui.__mem_func__(self.__OnVoteBlockChat))

		self.name = name
		self.hpGauge = hpGauge
		if app.ENABLE_VIEW_TARGET_DECIMAL_HP:
			hpDecimal = ui.TextLine()
			hpDecimal.SetParent(hpGauge)
			hpDecimal.SetDefaultFontName()
			hpDecimal.SetPosition(5, 5)
			hpDecimal.SetOutline()
			hpDecimal.Hide()
			self.hpDecimal = hpDecimal
		if app.ENABLE_SEND_TARGET_INFO:
			self.infoButton = infoButton
		if app.ENABLE_SEND_TARGET_INFO:
			self.vnum = 0
		self.closeButton = closeButton
		self.nameString = 0
		self.nameLength = 0
		self.vid = 0
		self.eventWhisper = None
		self.isShowButton = False
		if app.ENABLE_VIEW_ELEMENT:
			self.elementImage = None
			self.elementId = None
			self.elementImageToolTip = None
		self.__Initialize()
		self.ResetTargetBoard()

	def __del__(self):
		ui.ThinBoard.__del__(self)

		print "===================================================== DESTROYED TARGET BOARD"

	def __Initialize(self):
		self.nameString = ""
		self.nameLength = 0
		self.vid = 0
		if app.ENABLE_SEND_TARGET_INFO:
			self.vnum = 0
		self.isShowButton = False

	def Destroy(self):
		self.eventWhisper = None
		if app.ENABLE_SEND_TARGET_INFO:
			self.infoButton = None
		self.closeButton = None
		self.showingButtonList = None
		self.buttonDict = None
		self.name = None
		self.hpGauge = None
		if app.ENABLE_VIEW_ELEMENT:
			self.elementImage = None
			self.elementId = None
			self.elementImageToolTip = None
		if app.ENABLE_VIEW_TARGET_DECIMAL_HP:
			self.hpDecimal = None
		self.__Initialize()
	
	if app.ENABLE_SEND_TARGET_INFO:
		def RefreshMonsterInfoBoard(self):
			if not self.infoButton.showWnd.IsShow():
				return

			self.infoButton.showWnd.Refresh()

		def OnPressedInfoButton(self):
			net.SendTargetInfoLoad(player.GetTargetVID())
			if self.infoButton.showWnd.IsShow():
				self.infoButton.showWnd.Close()
			elif self.vnum != 0:
				self.infoButton.showWnd.Open(self, self.vnum)

	def OnPressedCloseButton(self):
		player.ClearTarget()
		self.Close()

	def Close(self):
		self.__Initialize()
		self.Hide()
		if app.__AUTO_QUQUE_ATTACK__:
			if self.autoFarmInfo:
				self.autoFarmInfo.Close()
				self.autoFarmInfo = None
		if app.ENABLE_SEND_TARGET_INFO:
			self.infoButton.showWnd.Close()
		if app.ENABLE_VIEW_ELEMENT and self.elementImage:
			self.elementImage.Hide()

	def Open(self, vid, name):
		if vid:
			if not constInfo.GET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD():
				if not player.IsSameEmpire(vid):
					self.Hide()
					return

			if vid != self.GetTargetVID():
				self.ResetTargetBoard()
				self.SetTargetVID(vid)
				self.SetTargetName(name)

			if player.IsMainCharacterIndex(vid):
				self.__ShowMainCharacterMenu()		
			elif chr.INSTANCE_TYPE_BUILDING == chr.GetInstanceType(self.vid):
				self.Hide()
			else:
				self.RefreshButton()
				self.Show()
		else:
			self.HideAllButton()
			self.__ShowButton(localeInfo.TARGET_BUTTON_WHISPER)
			self.__ShowButton("VOTE_BLOCK_CHAT")
			self.__ArrangeButtonPosition()
			self.SetTargetName(name)
			self.Show()
			
	def Refresh(self):
		if self.IsShow():
			if self.IsShowButton():			
				self.RefreshButton()		

	def RefreshByVID(self, vid):
		if vid == self.GetTargetVID():			
			self.Refresh()
			
	def RefreshByName(self, name):
		if name == self.GetTargetName():
			self.Refresh()

	def __ShowMainCharacterMenu(self):
		canShow=0

		self.HideAllButton()

		if player.IsMountingHorse():
			self.__ShowButton(localeInfo.TARGET_BUTTON_DISMOUNT)
			canShow=1

		if player.IsObserverMode():
			self.__ShowButton(localeInfo.TARGET_BUTTON_EXIT_OBSERVER)
			canShow=1

		if canShow:
			self.__ArrangeButtonPosition()
			self.Show()
		else:
			self.Hide()
			
	def __ShowNameOnlyMenu(self):
		self.HideAllButton()

	def SetWhisperEvent(self, event):
		self.eventWhisper = event

	def UpdatePosition(self):
		self.SetPosition(wndMgr.GetScreenWidth()/2 - self.GetWidth()/2, 10)
		if app.__AUTO_QUQUE_ATTACK__:
			if chr.GetInstanceType(self.vid) == chr.INSTANCE_TYPE_STONE:
				self.SetSize(self.GetWidth(), self.GetHeight() + 20)

				self.autoFarmText.SetPosition(self.GetWidth() / 2, 30)
				self.autoFarmText.Show()

				self.autoFarmBtn.SetPosition((self.GetWidth() / 2) + (self.autoFarmText.GetTextSize()[1]/2) + 85, 30)
				self.autoFarmBtn.Show()
			else:
				self.autoFarmText.Hide()
				self.autoFarmBtn.Hide()
				if self.autoFarmInfo:
					self.autoFarmInfo.Close()

	def ResetTargetBoard(self):
		for btn in self.buttonDict.values():
			btn.Hide()

		self.__Initialize()

		self.name.SetPosition(0, 13)
		self.name.SetHorizontalAlignCenter()
		self.name.SetWindowHorizontalAlignCenter()
		self.hpGauge.Hide()
		if app.ENABLE_VIEW_TARGET_DECIMAL_HP:
			self.hpDecimal.Hide()
		if app.ENABLE_VIEW_ELEMENT and self.elementImage:
			self.elementImage = None
			self.elementId = None
			if self.elementImageToolTip:
				self.elementImageToolTip.Hide()
				
		if app.ENABLE_SEND_TARGET_INFO:
			self.infoButton.Hide()
			self.infoButton.showWnd.Close()
		self.SetSize(250, 40)

	def SetTargetVID(self, vid):
		self.vid = vid
		if app.ENABLE_SEND_TARGET_INFO:
			self.vnum = 0

	def SetEnemyVID(self, vid):
		self.SetTargetVID(vid)

		name = chr.GetNameByVID(vid)
		if app.ENABLE_SEND_TARGET_INFO:
			vnum = nonplayer.GetRaceNumByVID(vid)
		level = nonplayer.GetLevelByVID(vid)
		grade = nonplayer.GetGradeByVID(vid)

		nameFront = ""
		if -1 != level:
			nameFront += "Lv." + str(level) + " "
		if self.GRADE_NAME.has_key(grade):
			nameFront += "(" + self.GRADE_NAME[grade] + ") "

		self.SetTargetName(nameFront + name)
		if app.ENABLE_SEND_TARGET_INFO:
			(textWidth, textHeight) = self.name.GetTextSize()

			self.infoButton.SetPosition(textWidth + 25, 12)
			self.infoButton.SetWindowHorizontalAlignLeft()

			self.vnum = vnum
			self.infoButton.Show()

	def GetTargetVID(self):
		return self.vid

	def GetTargetName(self):
		return self.nameString

	def SetTargetName(self, name):
		self.nameString = name
		self.nameLength = len(name)
		self.name.SetText(name)
	
	def SetElementImage(self, elementId):
		try:
			if elementId > 0 and elementId in ELEMENT_IMAGE_DIC.keys():
				self.elementId = elementId
				self.elementImage = ui.ImageBox()
				self.elementImage.SAFE_SetStringEvent("MOUSE_OVER_IN", self.OnElementImageOverIn)
				self.elementImage.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.OnElementImageOverOut)
				self.elementImage.SetPosition(self.GetLeft() - 40, self.GetTop())
				self.elementImage.LoadImage(
					"d:/ymir work/ui/game/12zi/element/%s.sub" % (ELEMENT_IMAGE_DIC[elementId]))
				self.elementImage.Show()
		except:
			pass
			
	def OnElementImageOverIn(self):
		if not self.elementImageToolTip:
			self.elementImageToolTip = uiToolTip.ToolTip()
		self.elementImageToolTip.ClearToolTip()
		self.elementImageToolTip.AppendTextLine(ELEMENT_IMAGE_DIC[self.elementId] + " element")
		self.elementImageToolTip.SetToolTipPosition(self.GetLeft() - 40, self.GetTop() + 70)
		self.elementImageToolTip.Show()

	def OnElementImageOverOut(self):
		if self.elementImageToolTip:
			self.elementImageToolTip.Hide()
				
	def SetHP(self, hpPercentage, iMinHP, iMaxHP):
		if not self.hpGauge.IsShow():
			showingButtonCount = len(self.showingButtonList)
			if showingButtonCount < len(self.BUTTON_NAME_LIST):
				if chr.GetInstanceType(self.vid) == chr.INSTANCE_TYPE_PLAYER:
					self.SetSize(max(150 + 75 * 3, showingButtonCount * 75), self.GetHeight())
				else:
					self.SetSize(200 + 7 * self.nameLength, self.GetHeight())
			else:
				self.SetSize(200 + 7 * self.nameLength, self.GetHeight())

			if localeInfo.IsARABIC():
				self.name.SetPosition( self.GetWidth()-23, 13)
			else:
				self.name.SetPosition(23, 13)

			self.name.SetWindowHorizontalAlignLeft()
			self.name.SetHorizontalAlignLeft()
			self.hpGauge.Show()
			self.UpdatePosition()
			
		if app.ENABLE_VIEW_TARGET_DECIMAL_HP:
			iMinHPText = '.'.join([i - 3 < 0 and str(iMinHP)[:i] or str(iMinHP)[i-3:i] for i in range(len(str(iMinHP)) % 3, len(str(iMinHP))+1, 3) if i])
			iMaxHPText = '.'.join([i - 3 < 0 and str(iMaxHP)[:i] or str(iMaxHP)[i-3:i] for i in range(len(str(iMaxHP)) % 3, len(str(iMaxHP))+1, 3) if i])
			self.hpDecimal.SetText(str(iMinHPText) + "/" + str(iMaxHPText))
			(textWidth, textHeight) = self.hpDecimal.GetTextSize()
			self.hpDecimal.SetPosition(130 / 2 - textWidth / 2, -15)
			self.hpDecimal.Show()

		self.hpGauge.SetPercentage(hpPercentage, 100)

	def ShowDefaultButton(self):

		self.isShowButton = True
		self.showingButtonList.append(self.buttonDict[localeInfo.TARGET_BUTTON_WHISPER])
		self.showingButtonList.append(self.buttonDict[localeInfo.TARGET_BUTTON_EXCHANGE])
		self.showingButtonList.append(self.buttonDict[localeInfo.TARGET_BUTTON_FIGHT])
		self.showingButtonList.append(self.buttonDict[localeInfo.TARGET_BUTTON_EMOTION_ALLOW])
		for button in self.showingButtonList:
			button.Show()

	def HideAllButton(self):
		self.isShowButton = False
		for button in self.showingButtonList:
			button.Hide()
		self.showingButtonList = []

	def __ShowButton(self, name):

		if not self.buttonDict.has_key(name):
			return

		self.buttonDict[name].Show()
		self.showingButtonList.append(self.buttonDict[name])

	def __HideButton(self, name):

		if not self.buttonDict.has_key(name):
			return

		button = self.buttonDict[name]
		button.Hide()

		for btnInList in self.showingButtonList:
			if btnInList == button:
				self.showingButtonList.remove(button)
				break

	def OnWhisper(self):
		if None != self.eventWhisper:
			self.eventWhisper(self.nameString)

	def OnExchange(self):
		net.SendExchangeStartPacket(self.vid)

	def OnPVP(self):
		net.SendChatPacket("/pvp %d" % (self.vid))

	def OnAppendToMessenger(self):
		net.SendMessengerAddByVIDPacket(self.vid)

	def OnPartyInvite(self):
		net.SendPartyInvitePacket(self.vid)

	def OnPartyExit(self):
		net.SendPartyExitPacket()

	def OnPartyRemove(self):
		net.SendPartyRemovePacket(self.vid)

	def __OnGuildAddMember(self):
		net.SendGuildAddMemberPacket(self.vid)

	def __OnDismount(self):
		net.SendChatPacket("/unmount")

	def __OnExitObserver(self):
		net.SendChatPacket("/observer_exit")

	def __OnViewEquipment(self):
		net.SendChatPacket("/view_equip " + str(self.vid))

	def __OnRequestParty(self):
		net.SendChatPacket("/party_request " + str(self.vid))

	def __OnDestroyBuilding(self):
		net.SendChatPacket("/build d %d" % (self.vid))

	def __OnEmotionAllow(self):
		net.SendChatPacket("/emotion_allow %d" % (self.vid))
		
	def __OnVoteBlockChat(self):
		cmd = "/vote_block_chat %s" % (self.nameString)
		net.SendChatPacket(cmd)

	def OnPressEscapeKey(self):
		self.OnPressedCloseButton()
		return True

	def IsShowButton(self):
		return self.isShowButton

	def RefreshButton(self):

		self.HideAllButton()

		if chr.INSTANCE_TYPE_BUILDING == chr.GetInstanceType(self.vid):
			#self.__ShowButton(localeInfo.TARGET_BUTTON_BUILDING_DESTROY)
			#self.__ArrangeButtonPosition()
			return
		
		if player.IsPVPInstance(self.vid) or player.IsObserverMode():
			# PVP_INFO_SIZE_BUG_FIX
			self.SetSize(200 + 7*self.nameLength, 40)
			self.UpdatePosition()
			# END_OF_PVP_INFO_SIZE_BUG_FIX			
			return	

		self.ShowDefaultButton()

		if guild.MainPlayerHasAuthority(guild.AUTH_ADD_MEMBER):
			if not guild.IsMemberByName(self.nameString):
				if 0 == chr.GetGuildID(self.vid):
					self.__ShowButton(localeInfo.TARGET_BUTTON_INVITE_GUILD)

		if not messenger.IsFriendByName(self.nameString):
			self.__ShowButton(localeInfo.TARGET_BUTTON_FRIEND)

		if player.IsPartyMember(self.vid):

			self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)

			if player.IsPartyLeader(self.vid):
				self.__ShowButton(localeInfo.TARGET_BUTTON_LEAVE_PARTY)
			elif player.IsPartyLeader(player.GetMainCharacterIndex()):
				self.__ShowButton(localeInfo.TARGET_BUTTON_EXCLUDE)

		else:
			if player.IsPartyMember(player.GetMainCharacterIndex()):
				if player.IsPartyLeader(player.GetMainCharacterIndex()):
					self.__ShowButton(localeInfo.TARGET_BUTTON_INVITE_PARTY)
			else:
				if chr.IsPartyMember(self.vid):
					self.__ShowButton(localeInfo.TARGET_BUTTON_REQUEST_ENTER_PARTY)
				else:
					self.__ShowButton(localeInfo.TARGET_BUTTON_INVITE_PARTY)

			if player.IsRevengeInstance(self.vid):
				self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)
				self.__ShowButton(localeInfo.TARGET_BUTTON_AVENGE)
			elif player.IsChallengeInstance(self.vid):
				self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)
				self.__ShowButton(localeInfo.TARGET_BUTTON_ACCEPT_FIGHT)
			elif player.IsCantFightInstance(self.vid):
				self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)

			if not player.IsSameEmpire(self.vid):
				self.__HideButton(localeInfo.TARGET_BUTTON_INVITE_PARTY)
				self.__HideButton(localeInfo.TARGET_BUTTON_FRIEND)
				self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)

		distance = player.GetCharacterDistance(self.vid)
		if distance > self.EXCHANGE_LIMIT_RANGE:
			self.__HideButton(localeInfo.TARGET_BUTTON_EXCHANGE)
			self.__ArrangeButtonPosition()

		self.__ArrangeButtonPosition()

	def __ArrangeButtonPosition(self):
		showingButtonCount = len(self.showingButtonList)

		pos = -(showingButtonCount / 2) * 68
		if 0 == showingButtonCount % 2:
			pos += 34

		for button in self.showingButtonList:
			button.SetPosition(pos, 33)
			pos += 68

		if app.ENABLE_VIEW_TARGET_PLAYER_HP:
			if showingButtonCount <= 2:
				self.SetSize(max(150 + 125, showingButtonCount * 75), 65)
			else:
				self.SetSize(max(150, showingButtonCount * 75), 65)
		else:
			self.SetSize(max(150, showingButtonCount * 75), 65)
			
		self.UpdatePosition()

	def OnUpdate(self):
		if self.isShowButton:

			exchangeButton = self.buttonDict[localeInfo.TARGET_BUTTON_EXCHANGE]
			distance = player.GetCharacterDistance(self.vid)

			if distance < 0:
				return

			if exchangeButton.IsShow():
				if distance > self.EXCHANGE_LIMIT_RANGE:
					self.RefreshButton()

			else:
				if distance < self.EXCHANGE_LIMIT_RANGE:
					self.RefreshButton()

	if app.__AUTO_QUQUE_ATTACK__:
		def __AutoFarmInfo(self):
			if not self.autoFarmInfo:
				self.autoFarmInfo = AutoFarmInfoWindow()
			if self.autoFarmInfo.IsShow():
				self.autoFarmInfo.Close()
			else:
				self.autoFarmInfo.Open()
				(x, y) = self.autoFarmBtn.GetGlobalPosition()
				self.autoFarmInfo.SetPosition(x + 10, y + 30)

if app.__AUTO_QUQUE_ATTACK__:
	class AutoFarmInfoWindow(ui.ThinBoard):
		def __init__(self):
			ui.ThinBoard.__init__(self)
			self.__LoadWindow()

		def __LoadWindow(self):
			self.SetSize(356, 166)
			self.AddFlag("float")
			self.AddFlag("not_pick")

			title = ui.TextLine()
			title.SetParent(self)
			title.AddFlag("not_pick")
			title.SetHorizontalAlignCenter()
			title.SetPackedFontColor(0xFFFBC401)
			title.SetOutline()
			title.SetText("Metinkő kijelölés")
			title.SetPosition(self.GetWidth() / 2, 15)
			title.Show()
			self.title = title
			
			firstText = "Ha |cFF74FF20Shift + jobb kattintással|r kattintasz egy Metinkőre, a karaktered#"\
			"kijelöli azt, és miután elpusztítottad, automatikusan a |cFF74FF20következőre|r vált."

			firstDescription = ui.MultiTextLine()
			firstDescription.SetParent(self)
			firstDescription.AddFlag("not_pick")
			firstDescription.SetTextRange(13)
			firstDescription.SetTextType("horizontal#center")
			firstDescription.SetPosition(self.GetWidth() / 2, 37)
			firstDescription.SetOutline(1)
			firstDescription.SetText(firstText)
			firstDescription.Show()
			self.firstDescription = firstDescription

			secondText = "Max. 3 Metinkő jelölhető ki (Metinkő kijelölés hatás nélkül)#"\
			"Max. 5 Metinkő jelölhető ki (Metinkő kijelölés hatással)"

			secondDescription = ui.MultiTextLine()
			secondDescription.SetParent(self)
			secondDescription.AddFlag("not_pick")
			secondDescription.SetTextRange(13)
			secondDescription.SetTextType("horizontal#center")
			secondDescription.SetPosition(self.GetWidth() / 2, 73)
			secondDescription.SetOutline(1)
			secondDescription.SetPackedFontColor(0xFFFFD071)
			secondDescription.SetText(secondText)
			secondDescription.Show()
			self.secondDescription = secondDescription


			item.SelectItem(61400)
			itemIcon = ui.ImageBox()
			itemIcon.SetParent(self)
			itemIcon.AddFlag("not_pick")
			itemIcon.LoadImage(item.GetIconImageFileName())
			itemIcon.SetPosition((self.GetWidth() / 2) - 16, 105)
			itemIcon.Show()
			self.itemIcon = itemIcon

			itemName = ui.TextLine()
			itemName.SetParent(self)
			itemName.AddFlag("not_pick")
			itemName.SetHorizontalAlignCenter()
			itemName.SetPackedFontColor(0xFFFBC401)
			itemName.SetOutline()
			itemName.SetText("Metinkő kijelölés")
			itemName.SetPosition(self.GetWidth() / 2, 105 + 32 + 5)
			itemName.Show()
			self.itemName = itemName

			self.SetCenterPosition()

		def Open(self):
			self.Show()
			self.SetTop()
		def Close(self):
			self.Hide()
		def OnPressEscapeKey(self):
			self.Close()
			return True
