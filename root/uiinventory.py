import ui
import player
import mouseModule
import net
import app
import snd
import item
import player
import chat
import grp
import uiScriptLocale
import uiRefine
import uiAttachMetin
import uiPickMoney
import uiCommon
import uiPrivateShopBuilder # ���λ��� ������ ItemMove ����
import localeInfo
import constInfo
import ime
import wndMgr
if app.ENABLE_SORT_INVEN:
	import uiToolTip

ITEM_MALL_BUTTON_ENABLE = True

ITEM_FLAG_APPLICABLE = 1 << 14

class CostumeWindow(ui.ScriptWindow):

	if app.ENABLE_SAVE_LAST_WINDOW_POSITION:

		def SetLastPosition(self):
			try:
				file = open("data/user_data/wnd/" + player.GetName() + "/"+ "inventory" + ".pos", 'r')
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
			file = open("data/user_data/wnd/" + player.GetName() + "/"+ "inventory" + ".pos","w")
			file.write(str(pos_x)+","+str(pos_y))
			file.close()
   
	def __init__(self, wndInventory):
		import exception
		
		if not app.ENABLE_COSTUME_SYSTEM:			
			exception.Abort("What do you do?")
			return

		if not wndInventory:
			exception.Abort("wndInventory parameter must be set to InventoryWindow")
			return						
			 	 
		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0
		self.wndInventory = wndInventory;

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()
		if app.ENABLE_SAVE_LAST_WINDOW_POSITION:
			self.SetLastPosition()
		self.RefreshCostumeSlot()

		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/CostumeWindow.py")
		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.LoadObject")

		try:
			wndEquip = self.GetChild("CostumeSlot")
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			
		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.BindObject")

		## Equipment
		wndEquip.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItem))
		wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))
		wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndEquip.SetUseSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))						
		wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.wndInventory.SelectEmptySlot))
		wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.wndInventory.SelectItemSlot))

		self.wndEquip = wndEquip

	def RefreshCostumeSlot(self):
		getItemVNum=player.GetItemIndex
		
		for i in xrange(item.COSTUME_SLOT_COUNT):
			slotNumber = item.COSTUME_SLOT_START + i
			self.wndEquip.SetItemSlot(slotNumber, getItemVNum(slotNumber), 0)
			print("RefreshCostumeSlot: slotnum: %d, vnum %d" % (slotNumber, getItemVNum(slotNumber)) )
			
		self.wndEquip.RefreshSlot()
		
class BeltInventoryWindow(ui.ScriptWindow):

	def __init__(self, wndInventory):
		import exception
		
		if not app.ENABLE_NEW_EQUIPMENT_SYSTEM:			
			exception.Abort("What do you do?")
			return

		if not wndInventory:
			exception.Abort("wndInventory parameter must be set to InventoryWindow")
			return						
			 	 
		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0
		self.wndInventory = wndInventory;
		
		self.wndBeltInventoryLayer = None
		self.wndBeltInventorySlot = None
		self.expandBtn = None
		self.minBtn = None

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self, openBeltSlot = FALSE):
		self.__LoadWindow()
		self.RefreshSlot()

		ui.ScriptWindow.Show(self)
		
		if openBeltSlot:
			self.OpenInventory()
		else:
			self.CloseInventory()

	def Close(self):
		self.Hide()

	def IsOpeningInventory(self):
		return self.wndBeltInventoryLayer.IsShow()
		
	def OpenInventory(self):
		self.wndBeltInventoryLayer.Show()
		self.expandBtn.Hide()

		if localeInfo.IsARABIC() == 0:
			self.AdjustPositionAndSize()
				
	def CloseInventory(self):
		self.wndBeltInventoryLayer.Hide()
		self.expandBtn.Show()
		
		if localeInfo.IsARABIC() == 0:
			self.AdjustPositionAndSize()

	def GetBasePosition(self):
		x, y = self.wndInventory.GetGlobalPosition()
		return x - 148, y + 241
		
	def AdjustPositionAndSize(self):
		bx, by = self.GetBasePosition()
		
		if self.IsOpeningInventory():			
			self.SetPosition(bx, by)
			self.SetSize(self.ORIGINAL_WIDTH, self.GetHeight())
			
		else:
			self.SetPosition(bx + 138, by);
			self.SetSize(10, self.GetHeight())

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/BeltInventoryWindow.py")
		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.LoadObject")

		try:
			self.ORIGINAL_WIDTH = self.GetWidth()
			wndBeltInventorySlot = self.GetChild("BeltInventorySlot")
			self.wndBeltInventoryLayer = self.GetChild("BeltInventoryLayer")
			self.expandBtn = self.GetChild("ExpandBtn")
			self.minBtn = self.GetChild("MinimizeBtn")
			
			self.expandBtn.SetEvent(ui.__mem_func__(self.OpenInventory))
			self.minBtn.SetEvent(ui.__mem_func__(self.CloseInventory))
			
			if localeInfo.IsARABIC() :
				self.expandBtn.SetPosition(self.expandBtn.GetWidth() - 2, 15)
				self.wndBeltInventoryLayer.SetPosition(self.wndBeltInventoryLayer.GetWidth() - 5, 0)
				self.minBtn.SetPosition(self.minBtn.GetWidth() + 3, 15)			
	
			for i in xrange(item.BELT_INVENTORY_SLOT_COUNT):
				slotNumber = item.BELT_INVENTORY_SLOT_START + i							
				wndBeltInventorySlot.SetCoverButton(slotNumber,	"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/belt_inventory/slot_disabled.tga", FALSE, FALSE)									
			
		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.BindObject")

		## Equipment
		wndBeltInventorySlot.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItem))
		wndBeltInventorySlot.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))
		wndBeltInventorySlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndBeltInventorySlot.SetUseSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))						
		wndBeltInventorySlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.wndInventory.SelectEmptySlot))
		wndBeltInventorySlot.SetSelectItemSlotEvent(ui.__mem_func__(self.wndInventory.SelectItemSlot))

		self.wndBeltInventorySlot = wndBeltInventorySlot

	def RefreshSlot(self):
		getItemVNum=player.GetItemIndex
		
		for i in xrange(item.BELT_INVENTORY_SLOT_COUNT):
			slotNumber = item.BELT_INVENTORY_SLOT_START + i
			self.wndBeltInventorySlot.SetItemSlot(slotNumber, getItemVNum(slotNumber), player.GetItemCount(slotNumber))
			self.wndBeltInventorySlot.SetAlwaysRenderCoverButton(slotNumber, TRUE)
			
			avail = "0"
			
			if player.IsAvailableBeltInventoryCell(slotNumber):
				self.wndBeltInventorySlot.EnableCoverButton(slotNumber)				
			else:
				self.wndBeltInventorySlot.DisableCoverButton(slotNumber)				

		self.wndBeltInventorySlot.RefreshSlot()

		
class InventoryWindow(ui.ScriptWindow):
	USE_TYPE_TUPLE = ("USE_CLEAN_SOCKET", "USE_CHANGE_ATTRIBUTE", "USE_ADD_ATTRIBUTE", "USE_ADD_ATTRIBUTE2", "USE_ADD_ACCESSORY_SOCKET", "USE_PUT_INTO_ACCESSORY_SOCKET", "USE_PUT_INTO_BELT_SOCKET", "USE_PUT_INTO_RING_SOCKET")

	questionDialog = None
	tooltipItem = None
	wndCostume = None
	wndBelt = None
	dlgPickMoney = None
	interface = None
	
	sellingSlotNumber = -1
	isLoaded = 0
	isOpenedCostumeWindowWhenClosingInventory = 0		# �κ��丮 ���� �� �ڽ����� �����־����� ����-_-; ���̹� ����
	isOpenedBeltWindowWhenClosingInventory = 0		# �κ��丮 ���� �� ��Ʈ �κ��丮�� �����־����� ����-_-; ���̹� ����

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.isOpenedBeltWindowWhenClosingInventory = 0		# �κ��丮 ���� �� ��Ʈ �κ��丮�� �����־����� ����-_-; ���̹� ����

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()

		ui.ScriptWindow.Show(self)

		if self.isOpenedCostumeWindowWhenClosingInventory and self.wndCostume:
			self.wndCostume.Show() 

		if self.wndBelt:
			self.wndBelt.Show(self.isOpenedBeltWindowWhenClosingInventory)

	def BindInterfaceClass(self, interface):
		self.interface = interface
		
	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()

			if ITEM_MALL_BUTTON_ENABLE:
				pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "InventoryWindow.py")
			else:
				pyScrLoader.LoadScriptFile(self, "UIScript/InventoryWindow.py")
		except:
			import exception
			exception.Abort("InventoryWindow.LoadWindow.LoadObject")

		try:
			wndItem = self.GetChild("ItemSlot")
			wndEquip = self.GetChild("EquipmentSlot")
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			self.wndMoney = self.GetChild("Money")
			self.wndMoneySlot = self.GetChild("Money_Slot")
			self.mallButton = self.GetChild2("MallButton")
			self.DSSButton = self.GetChild2("DSSButton")
			self.costumeButton = self.GetChild2("CostumeButton")
			
			self.inventoryTab = []
			self.inventoryTab.append(self.GetChild("Inventory_Tab_01"))
			self.inventoryTab.append(self.GetChild("Inventory_Tab_02"))
			self.inventoryTab.append(self.GetChild("Inventory_Tab_03"))
			self.inventoryTab.append(self.GetChild("Inventory_Tab_04"))

			self.equipmentTab = []
			self.equipmentTab.append(self.GetChild("Equipment_Tab_01"))
			self.equipmentTab.append(self.GetChild("Equipment_Tab_02"))

			if app.BL_ENABLE_PICKUP_ITEM_EFFECT:
				self.listHighlightedSlot = []


			if app.ENABLE_SORT_INVEN:
				self.yenilebutton = self.GetChild2("YenileButton")
				self.yenilebutton.SetEvent(ui.__mem_func__(self.ClickYenileButton))
				self.tooltipI = uiToolTip.ToolTip()
				self.tooltipI.Hide()
				self.tooltipInfo = [self.tooltipI]*4
				self.InformationText = [localeInfo.YENILE_BUTTON_TITLE,
										localeInfo.YENILE_BUTTON,
										localeInfo.YENILE_BUTTON2,
										localeInfo.YENILE_BUTTON3
				]
				for i in xrange(len(self.tooltipInfo)):
					self.tooltipInfo[i].SetFollow(True)
					self.tooltipInfo[i].AlignHorizonalCenter()
					if i == 0:
						self.tooltipInfo[i].AppendTextLine(self.InformationText[i], 0xffffff00)
					else:
						self.tooltipInfo[i].AppendTextLine(self.InformationText[i])
					self.tooltipInfo[i].Hide()
					
			if self.costumeButton and not app.ENABLE_COSTUME_SYSTEM:
				self.costumeButton.Hide()
				self.costumeButton.Destroy()
				self.costumeButton = 0

			# Belt Inventory Window
			self.wndBelt = None
			
			if app.ENABLE_NEW_EQUIPMENT_SYSTEM:
				self.wndBelt = BeltInventoryWindow(self)
			
		except:
			import exception
			exception.Abort("InventoryWindow.LoadWindow.BindObject")

		## Item
		wndItem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndItem.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndItem.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		## Equipment
		wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndEquip.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndEquip.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		## PickMoneyDialog
		dlgPickMoney = uiPickMoney.PickMoneyDialog()
		dlgPickMoney.LoadDialog()
		dlgPickMoney.Hide()

		## RefineDialog
		self.refineDialog = uiRefine.RefineDialogNew()
		self.refineDialog.Hide()

		## AttachMetinDialog
		self.attachMetinDialog = uiAttachMetin.AttachMetinDialog()
		self.attachMetinDialog.Hide()

		## MoneySlot
		self.wndMoneySlot.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog))

		self.inventoryTab[0].SetEvent(lambda arg=0: self.SetInventoryPage(arg))
		self.inventoryTab[1].SetEvent(lambda arg=1: self.SetInventoryPage(arg))
		self.inventoryTab[2].SetEvent(lambda arg=2: self.SetInventoryPage(arg))
		self.inventoryTab[3].SetEvent(lambda arg=3: self.SetInventoryPage(arg))
		self.inventoryTab[0].Down()
		self.inventoryPageIndex = 0

		self.equipmentTab[0].SetEvent(lambda arg=0: self.SetEquipmentPage(arg))
		self.equipmentTab[1].SetEvent(lambda arg=1: self.SetEquipmentPage(arg))
		self.equipmentTab[0].Down()
		self.equipmentTab[0].Hide()
		self.equipmentTab[1].Hide()

		self.wndItem = wndItem
		self.wndEquip = wndEquip
		self.dlgPickMoney = dlgPickMoney

		# MallButton
		if self.mallButton:
			self.mallButton.SetEvent(ui.__mem_func__(self.ClickMallButton))

		if self.DSSButton:
			self.DSSButton.SetEvent(ui.__mem_func__(self.ClickDSSButton)) 
		
		# Costume Button
		if self.costumeButton:
			self.costumeButton.SetEvent(ui.__mem_func__(self.ClickCostumeButton))

		self.wndCostume = None
		
 		#####

		## Refresh
		self.SetInventoryPage(0)
		self.SetEquipmentPage(0)
		self.RefreshItemSlot()
		self.RefreshStatus()

	def Destroy(self):
		if app.ENABLE_SAVE_LAST_WINDOW_POSITION:
			if self.IsShow():
				self.SaveLastPosition()
		self.ClearDictionary()

		self.dlgPickMoney.Destroy()
		self.dlgPickMoney = 0

		self.refineDialog.Destroy()
		self.refineDialog = 0

		self.attachMetinDialog.Destroy()
		self.attachMetinDialog = 0

		self.tooltipItem = None
		self.wndItem = 0
		self.wndEquip = 0
		self.dlgPickMoney = 0
		self.wndMoney = 0
		self.wndMoneySlot = 0
		self.questionDialog = None
		self.mallButton = None
		self.DSSButton = None
		self.interface = None

		if self.wndCostume:
			self.wndCostume.Destroy()
			self.wndCostume = 0
			
		if self.wndBelt:
			self.wndBelt.Destroy()
			self.wndBelt = None
			
		self.inventoryTab = []
		self.equipmentTab = []

	def Hide(self):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			self.OnCloseQuestionDialog()
			return
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

		if self.wndCostume:
			self.isOpenedCostumeWindowWhenClosingInventory = self.wndCostume.IsShow()			# �κ��丮 â�� ���� �� �ڽ����� ���� �־��°�?
			self.wndCostume.Close()
 
		if self.wndBelt:
			self.isOpenedBeltWindowWhenClosingInventory = self.wndBelt.IsOpeningInventory()		# �κ��丮 â�� ���� �� ��Ʈ �κ��丮�� ���� �־��°�?
			self.wndBelt.Close()
  
		if self.dlgPickMoney:
			self.dlgPickMoney.Close()
			
		if app.ENABLE_SAVE_LAST_WINDOW_POSITION:
			if self.IsShow():
				self.SaveLastPosition()
		
		wndMgr.Hide(self.hWnd)
		
	
	def Close(self):
		self.Hide()
	
	if app.ENABLE_SORT_INVEN:
		def ClickYenileButton(self):
			if app.IsPressed(app.DIK_LALT):
				net.SortInven(2)
			elif app.IsPressed(app.DIK_LCONTROL):
				net.SortInven(3)
			else:
				net.SortInven(1)
				
	def SetInventoryPage(self, page):
		self.inventoryTab[self.inventoryPageIndex].SetUp()
		self.inventoryPageIndex = page
		self.inventoryTab[self.inventoryPageIndex].Down()
		self.RefreshBagSlotWindow()

	def SetEquipmentPage(self, page):
		self.equipmentPageIndex = page
		self.equipmentTab[1-page].SetUp()
		self.RefreshEquipSlotWindow()

	def ClickMallButton(self):
		net.SendChatPacket("/click_mall")

	# DSSButton
	def ClickDSSButton(self):
		self.interface.ToggleDragonSoulWindow()

	def ClickCostumeButton(self):
		if self.wndCostume:
			if self.wndCostume.IsShow(): 
				self.wndCostume.Hide()
			else:
				self.wndCostume.Show()
		else:
			self.wndCostume = CostumeWindow(self)
			self.wndCostume.Show()

	def OpenPickMoneyDialog(self):
		if mouseModule.mouseController.isAttached():

			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			if player.SLOT_TYPE_SAFEBOX == mouseModule.mouseController.GetAttachedType():

				if player.ITEM_MONEY == mouseModule.mouseController.GetAttachedItemIndex():
					net.SendSafeboxWithdrawMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())
					snd.PlaySound("sound/ui/money.wav")

			mouseModule.mouseController.DeattachObject()

		else:
			curMoney = player.GetElk()

			if curMoney <= 0:
				return

			self.dlgPickMoney.SetTitleName(localeInfo.PICK_MONEY_TITLE)
			self.dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickMoney))
			self.dlgPickMoney.Open(curMoney)
			self.dlgPickMoney.SetMax(7) 

	def OnPickMoney(self, money):
		mouseModule.mouseController.AttachMoney(self, player.SLOT_TYPE_INVENTORY, money)

	def OnPickItem(self, count):
		itemSlotIndex = self.dlgPickMoney.itemGlobalSlotIndex
		selectedItemVNum = player.GetItemIndex(itemSlotIndex)
		mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, count)

	def __InventoryLocalSlotPosToGlobalSlotPos(self, local):
		if player.IsEquipmentSlot(local) or player.IsCostumeSlot(local) or (app.ENABLE_NEW_EQUIPMENT_SYSTEM and player.IsBeltInventorySlot(local)):
			return local

		return self.inventoryPageIndex*player.INVENTORY_PAGE_SIZE + local

	def RefreshBagSlotWindow(self):
		getItemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		setItemVNum=self.wndItem.SetItemSlot

		if app.BL_ENABLE_PICKUP_ITEM_EFFECT:
			for i in xrange(self.wndItem.GetSlotCount()):
				self.wndItem.DeactivateSlot(i)

		for i in xrange(player.INVENTORY_PAGE_SIZE):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
			
			itemCount = getItemCount(slotNumber)
			if 0 == itemCount:
				self.wndItem.ClearSlot(i)
				continue
			elif 1 == itemCount:
				itemCount = 0
				
			itemVnum = getItemVNum(slotNumber)
			setItemVNum(i, itemVnum, itemCount)
			
			if constInfo.IS_AUTO_POTION(itemVnum):
				metinSocket = [player.GetItemMetinSocket(slotNumber, j) for j in xrange(player.METIN_SOCKET_MAX_NUM)]	
				
				if slotNumber >= player.INVENTORY_PAGE_SIZE*self.inventoryPageIndex:
					slotNumber -= player.INVENTORY_PAGE_SIZE*self.inventoryPageIndex
					
				isActivated = 0 != metinSocket[0]
				
				if isActivated:
					self.wndItem.ActivateSlot(slotNumber)
					potionType = 0;
					if constInfo.IS_AUTO_POTION_HP(itemVnum):
						potionType = player.AUTO_POTION_TYPE_HP
					elif constInfo.IS_AUTO_POTION_SP(itemVnum):
						potionType = player.AUTO_POTION_TYPE_SP						
					
					usedAmount = int(metinSocket[1])
					totalAmount = int(metinSocket[2])					
					player.SetAutoPotionInfo(potionType, isActivated, (totalAmount - usedAmount), totalAmount, self.__InventoryLocalSlotPosToGlobalSlotPos(i))
					
				else:
					self.wndItem.DeactivateSlot(slotNumber)


		if app.BL_ENABLE_PICKUP_ITEM_EFFECT:
			self.__HighlightSlot_Refresh()

		self.wndItem.RefreshSlot()

		if self.wndBelt:
			self.wndBelt.RefreshSlot()
		
		if self.interface:
				if self.interface.dlgRefineNew.IsShow():
					self.interface.dlgRefineNew.RecalcMaterials()
		
		if self.tooltipItem and self.tooltipItem.IsShow():
				self.tooltipItem.RefreshNeededItemCounts()
	
	if app.ENABLE_SAVE_LAST_WINDOW_POSITION:
		def SetLastPosition(self):
			try:
				file = open("data/user_data/wnd/" + player.GetName() + "/"+ "inventory" + ".pos", 'r')
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
			file = open("data/user_data/wnd/" + player.GetName() + "/"+ "inventory" + ".pos","w")
			file.write(str(pos_x)+","+str(pos_y))
			file.close()
			
	def OnUpdate(self):
		if app.ENABLE_SORT_INVEN and self.tooltipInfo:
			for i in xrange(len(self.tooltipInfo)):
				if self.yenilebutton.IsIn():
					self.tooltipInfo[i].Show()
				else:
					self.tooltipInfo[i].Hide()
					
		self.GetChild("Money").OnUpdateCool()
					
	def RefreshEquipSlotWindow(self):
		getItemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		setItemVNum=self.wndEquip.SetItemSlot
		for i in xrange(player.EQUIPMENT_PAGE_COUNT):
			slotNumber = player.EQUIPMENT_SLOT_START + i
			itemCount = getItemCount(slotNumber)
			if itemCount <= 1:
				itemCount = 0
			setItemVNum(slotNumber, getItemVNum(slotNumber), itemCount)

		# if app.ENABLE_NEW_EQUIPMENT_SYSTEM:
			# for i in xrange(player.NEW_EQUIPMENT_SLOT_COUNT):
				# slotNumber = player.NEW_EQUIPMENT_SLOT_START + i
				# itemCount = getItemCount(slotNumber)
				# if itemCount <= 1:
					# itemCount = 0
				# setItemVNum(slotNumber, getItemVNum(slotNumber), itemCount)
				# print "ENABLE_NEW_EQUIPMENT_SYSTEM", slotNumber, itemCount, getItemVNum(slotNumber)
		setItemVNum(item.EQUIPMENT_RING1, getItemVNum(item.EQUIPMENT_RING1), 0)
		setItemVNum(item.EQUIPMENT_RING2, getItemVNum(item.EQUIPMENT_RING2), 0)
		setItemVNum(item.EQUIPMENT_BELT, getItemVNum(item.EQUIPMENT_BELT), 0)


		self.wndEquip.RefreshSlot()
		
		if self.wndCostume:
			self.wndCostume.RefreshCostumeSlot()

	def RefreshItemSlot(self):
		self.RefreshBagSlotWindow()
		self.RefreshEquipSlotWindow()

	def RefreshStatus(self):
		money = player.GetElk()
		self.GetChild("Money").SetText(player.GetElk())

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def SellItem(self):
		if self.sellingSlotitemIndex == player.GetItemIndex(self.sellingSlotNumber):
			if self.sellingSlotitemCount == player.GetItemCount(self.sellingSlotNumber):
				net.SendShopSellPacketNew(self.sellingSlotNumber, self.questionDialog.count, player.INVENTORY)
				snd.PlaySound("sound/ui/money.wav")
		self.OnCloseQuestionDialog()

	def OnDetachMetinFromItem(self):
		if None == self.questionDialog:
			return
			
		#net.SendItemUseToItemPacket(self.questionDialog.sourcePos, self.questionDialog.targetPos)		
		self.__SendUseItemToItemPacket(self.questionDialog.sourcePos, self.questionDialog.targetPos)
		self.OnCloseQuestionDialog()

	def OnCloseQuestionDialog(self):
		if not self.questionDialog:
			return
		
		self.questionDialog.Close()
		self.questionDialog = None
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	## Slot Event
	def SelectEmptySlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		selectedSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(selectedSlotPos)

		if mouseModule.mouseController.isAttached():

			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()

			if player.SLOT_TYPE_INVENTORY == attachedSlotType or\
				player.SLOT_TYPE_SKILL_BOOK_INVENTORY == attachedSlotType or\
				player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY == attachedSlotType or\
				player.SLOT_TYPE_STONE_INVENTORY == attachedSlotType or\
				player.SLOT_TYPE_SANDIK_INVENTORY == attachedSlotType:
				itemCount = player.GetItemCount(attachedSlotPos)
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				self.__SendMoveItemPacket(attachedSlotPos, selectedSlotPos, attachedCount)

				if item.IsRefineScroll(attachedItemIndex):
					self.wndItem.SetUseMode(False)

			elif player.SLOT_TYPE_PRIVATE_SHOP == attachedSlotType:
				mouseModule.mouseController.RunCallBack("INVENTORY")

			elif player.SLOT_TYPE_SHOP == attachedSlotType:
				net.SendShopBuyPacket(attachedSlotPos)

			elif player.SLOT_TYPE_SAFEBOX == attachedSlotType:

				if player.ITEM_MONEY == attachedItemIndex:
					net.SendSafeboxWithdrawMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())
					snd.PlaySound("sound/ui/money.wav")

				else:
					net.SendSafeboxCheckoutPacket(attachedSlotPos, selectedSlotPos)

			elif player.SLOT_TYPE_MALL == attachedSlotType:
				net.SendMallCheckoutPacket(attachedSlotPos, selectedSlotPos)

			mouseModule.mouseController.DeattachObject()

	def SelectItemSlot(self, itemSlotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		itemSlotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(itemSlotIndex)

		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemVID = mouseModule.mouseController.GetAttachedItemIndex()

			if player.SLOT_TYPE_INVENTORY == attachedSlotType or\
				player.SLOT_TYPE_SKILL_BOOK_INVENTORY == attachedSlotType or\
				player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY == attachedSlotType or\
				player.SLOT_TYPE_STONE_INVENTORY == attachedSlotType or\
				player.SLOT_TYPE_SANDIK_INVENTORY == attachedSlotType:
				self.__DropSrcItemToDestItemInInventory(attachedItemVID, attachedSlotPos, itemSlotIndex)

			mouseModule.mouseController.DeattachObject()

		else:

			curCursorNum = app.GetCursor()
			if app.SELL == curCursorNum:
				self.__SellItem(itemSlotIndex)
				
			elif app.BUY == curCursorNum:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)

			elif app.IsPressed(app.DIK_LALT):
				link = player.GetItemLink(itemSlotIndex)
				ime.PasteString(link)

			elif app.IsPressed(app.DIK_LSHIFT):
				itemCount = player.GetItemCount(itemSlotIndex)
				
				if itemCount > 1:
					self.dlgPickMoney.SetTitleName(localeInfo.PICK_ITEM_TITLE)
					self.dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickItem))
					self.dlgPickMoney.Open(itemCount)
					self.dlgPickMoney.itemGlobalSlotIndex = itemSlotIndex
				#else:
					#selectedItemVNum = player.GetItemIndex(itemSlotIndex)
					#mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum)

			elif app.IsPressed(app.DIK_LCONTROL):
				itemIndex = player.GetItemIndex(itemSlotIndex)

				if True == item.CanAddToQuickSlotItem(itemIndex):
					player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_INVENTORY, itemSlotIndex)
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.QUICKSLOT_REGISTER_DISABLE_ITEM)

			else:
				selectedItemVNum = player.GetItemIndex(itemSlotIndex)
				itemCount = player.GetItemCount(itemSlotIndex)
				mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, itemCount)
				
				if self.__IsUsableItemToItem(selectedItemVNum, itemSlotIndex):				
					self.wndItem.SetUseMode(True)
				else:					
					self.wndItem.SetUseMode(False)

				snd.PlaySound("sound/ui/pick.wav")

	def __DropSrcItemToDestItemInInventory(self, srcItemVID, srcItemSlotPos, dstItemSlotPos):
		if srcItemSlotPos == dstItemSlotPos:
			return
	         	
		elif item.IsRefineScroll(srcItemVID):
			self.RefineItem(srcItemSlotPos, dstItemSlotPos)
			self.wndItem.SetUseMode(False)

		elif item.IsMetin(srcItemVID):
			self.AttachMetinToItem(srcItemSlotPos, dstItemSlotPos)

		elif item.IsDetachScroll(srcItemVID):
			self.DetachMetinFromItem(srcItemSlotPos, dstItemSlotPos)

		elif item.IsKey(srcItemVID):
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)			

		elif (player.GetItemFlags(srcItemSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		elif item.GetUseType(srcItemVID) in self.USE_TYPE_TUPLE:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)			

		else:
			#snd.PlaySound("sound/ui/drop.wav")

			## �̵���Ų ���� ���� ������ ��� �������� ����ؼ� ���� ��Ų�� - [levites]
			if player.IsEquipmentSlot(dstItemSlotPos):

				## ��� �ִ� �������� ����϶���
				if item.IsEquipmentVID(srcItemVID):
					self.__UseItem(srcItemSlotPos)

			else:
				self.__SendMoveItemPacket(srcItemSlotPos, dstItemSlotPos, 0)
				#net.SendItemMovePacket(srcItemSlotPos, dstItemSlotPos, 0)

	def __SellItem(self, itemSlotPos):
		if not player.IsEquipmentSlot(itemSlotPos):
			self.sellingSlotNumber = itemSlotPos
			itemIndex = player.GetItemIndex(itemSlotPos)
			itemCount = player.GetItemCount(itemSlotPos)
			
			
			self.sellingSlotitemIndex = itemIndex
			self.sellingSlotitemCount = itemCount

			item.SelectItem(itemIndex)
			## ��Ƽ �÷��� �˻� ������ �߰�
			## 20140220
			if item.IsAntiFlag(item.ANTIFLAG_SELL):
				popup = uiCommon.PopupDialog()
				popup.SetText(localeInfo.SHOP_CANNOT_SELL_ITEM)
				popup.SetAcceptEvent(self.__OnClosePopupDialog)
				popup.Open()
				self.popup = popup
				return

			itemPrice = item.GetISellItemPrice()

			if item.Is1GoldItem():
				itemPrice = itemCount / itemPrice
			else:
				itemPrice = itemPrice * itemCount

			item.GetItemName(itemIndex)
			itemName = item.GetItemName()

			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.DO_YOU_SELL_ITEM(itemName, itemCount, itemPrice))
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.SellItem))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
			self.questionDialog.count = itemCount
		
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

	def __OnClosePopupDialog(self):
		self.pop = None

	def RefineItem(self, scrollSlotPos, targetSlotPos):

		scrollIndex = player.GetItemIndex(scrollSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)

		if player.REFINE_OK != player.CanRefine(scrollIndex, targetSlotPos):
			return
		
		if app.ENABLE_REFINE_RENEWAL:
			constInfo.AUTO_REFINE_TYPE = 1
			constInfo.AUTO_REFINE_DATA["ITEM"][0] = scrollSlotPos
			constInfo.AUTO_REFINE_DATA["ITEM"][1] = targetSlotPos
			
		###########################################################
		self.__SendUseItemToItemPacket(scrollSlotPos, targetSlotPos)
		#net.SendItemUseToItemPacket(scrollSlotPos, targetSlotPos)
		return
		###########################################################

		###########################################################
		#net.SendRequestRefineInfoPacket(targetSlotPos)
		#return
		###########################################################

		result = player.CanRefine(scrollIndex, targetSlotPos)

		if player.REFINE_ALREADY_MAX_SOCKET_COUNT == result:
			#snd.PlaySound("sound/ui/jaeryun_fail.wav")
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_MORE_SOCKET)

		elif player.REFINE_NEED_MORE_GOOD_SCROLL == result:
			#snd.PlaySound("sound/ui/jaeryun_fail.wav")
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NEED_BETTER_SCROLL)

		elif player.REFINE_CANT_MAKE_SOCKET_ITEM == result:
			#snd.PlaySound("sound/ui/jaeryun_fail.wav")
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_SOCKET_DISABLE_ITEM)

		elif player.REFINE_NOT_NEXT_GRADE_ITEM == result:
			#snd.PlaySound("sound/ui/jaeryun_fail.wav")
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_UPGRADE_DISABLE_ITEM)

		elif player.REFINE_CANT_REFINE_METIN_TO_EQUIPMENT == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_EQUIP_ITEM)

		if player.REFINE_OK != result:
			return

		self.refineDialog.Open(scrollSlotPos, targetSlotPos)

	def DetachMetinFromItem(self, scrollSlotPos, targetSlotPos):
		scrollIndex = player.GetItemIndex(scrollSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)

		if not player.CanDetach(scrollIndex, targetSlotPos):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_METIN_INSEPARABLE_ITEM)
			return

		self.questionDialog = uiCommon.QuestionDialog()
		self.questionDialog.SetText(localeInfo.REFINE_DO_YOU_SEPARATE_METIN)
		self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnDetachMetinFromItem))
		self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
		self.questionDialog.Open()
		self.questionDialog.sourcePos = scrollSlotPos
		self.questionDialog.targetPos = targetSlotPos

	def AttachMetinToItem(self, metinSlotPos, targetSlotPos):
		metinIndex = player.GetItemIndex(metinSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)

		item.SelectItem(metinIndex)
		itemName = item.GetItemName()

		result = player.CanAttachMetin(metinIndex, targetSlotPos)

		if player.ATTACH_METIN_NOT_MATCHABLE_ITEM == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_CAN_NOT_ATTACH(itemName))

		if player.ATTACH_METIN_NO_MATCHABLE_SOCKET == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_SOCKET(itemName))

		elif player.ATTACH_METIN_NOT_EXIST_GOLD_SOCKET == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_GOLD_SOCKET(itemName))

		elif player.ATTACH_METIN_CANT_ATTACH_TO_EQUIPMENT == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_EQUIP_ITEM)

		if player.ATTACH_METIN_OK != result:
			return

		self.attachMetinDialog.Open(metinSlotPos, targetSlotPos)


		
	def OverOutItem(self):
		self.wndItem.SetUsableItem(False)
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OverInItem(self, overSlotPos):
		overSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(overSlotPos)
		self.wndItem.SetUsableItem(False)

		if app.BL_ENABLE_PICKUP_ITEM_EFFECT:
			self.DelHighlightSlot(overSlotPos)

		if mouseModule.mouseController.isAttached():
			attachedItemType = mouseModule.mouseController.GetAttachedType()
			if player.SLOT_TYPE_INVENTORY == attachedItemType:

				attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
				attachedItemVNum = mouseModule.mouseController.GetAttachedItemIndex()
				
				if self.__CanUseSrcItemToDstItem(attachedItemVNum, attachedSlotPos, overSlotPos):
					self.wndItem.SetUsableItem(True)
					self.ShowToolTip(overSlotPos)
					return
				
		self.ShowToolTip(overSlotPos)


	def __IsUsableItemToItem(self, srcItemVNum, srcSlotPos):
		"�ٸ� �����ۿ� ����� �� �ִ� �������ΰ�?"

		if item.IsRefineScroll(srcItemVNum):
			return True
		elif item.IsMetin(srcItemVNum):
			return True
		elif item.IsDetachScroll(srcItemVNum):
			return True
		elif item.IsKey(srcItemVNum):
			return True
		elif (player.GetItemFlags(srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			return True
		else:
			if item.GetUseType(srcItemVNum) in self.USE_TYPE_TUPLE:
				return True
			
		return False

	def __CanUseSrcItemToDstItem(self, srcItemVNum, srcSlotPos, dstSlotPos):
		"��� �����ۿ� ����� �� �ִ°�?"

		if srcSlotPos == dstSlotPos:
			return False

		if item.IsRefineScroll(srcItemVNum):
			if player.REFINE_OK == player.CanRefine(srcItemVNum, dstSlotPos):
				return True
		elif item.IsMetin(srcItemVNum):
			if player.ATTACH_METIN_OK == player.CanAttachMetin(srcItemVNum, dstSlotPos):
				return True
		elif item.IsDetachScroll(srcItemVNum):
			if player.DETACH_METIN_OK == player.CanDetach(srcItemVNum, dstSlotPos):
				return True
		elif item.IsKey(srcItemVNum):
			if player.CanUnlock(srcItemVNum, dstSlotPos):
				return True

		elif (player.GetItemFlags(srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			return True

		else:
			useType=item.GetUseType(srcItemVNum)

			if "USE_CLEAN_SOCKET" == useType:
				if self.__CanCleanBrokenMetinStone(dstSlotPos):
					return True
			elif "USE_CHANGE_ATTRIBUTE" == useType:
				if self.__CanChangeItemAttrList(dstSlotPos):
					return True
			elif "USE_ADD_ATTRIBUTE" == useType:
				if self.__CanAddItemAttr(dstSlotPos):
					return True
			elif "USE_ADD_ATTRIBUTE2" == useType:
				if self.__CanAddItemAttr(dstSlotPos):
					return True
			elif "USE_ADD_ACCESSORY_SOCKET" == useType:
				if self.__CanAddAccessorySocket(dstSlotPos):
					return True
			elif "USE_PUT_INTO_ACCESSORY_SOCKET" == useType:								
				if self.__CanPutAccessorySocket(dstSlotPos, srcItemVNum):
					return TRUE;
			elif "USE_PUT_INTO_BELT_SOCKET" == useType:								
				dstItemVNum = player.GetItemIndex(dstSlotPos)
				print "USE_PUT_INTO_BELT_SOCKET", srcItemVNum, dstItemVNum

				item.SelectItem(dstItemVNum)
		
				if item.ITEM_TYPE_BELT == item.GetItemType():
					return True

		return False

	def __CanCleanBrokenMetinStone(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)
		
		if item.ITEM_TYPE_WEAPON != item.GetItemType():
			return False

		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemMetinSocket(dstSlotPos, i) == constInfo.ERROR_METIN_STONE:
				return True

		return False

	def __CanChangeItemAttrList(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)
		
		if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):	 
			return False

		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemAttribute(dstSlotPos, i) != 0:
				return True

		return False

	def __CanPutAccessorySocket(self, dstSlotPos, mtrlVnum):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() != item.ITEM_TYPE_ARMOR:
			return False

		if not item.GetItemSubType() in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
			return False

		curCount = player.GetItemMetinSocket(dstSlotPos, 0)
		maxCount = player.GetItemMetinSocket(dstSlotPos, 1)

		if mtrlVnum != constInfo.GET_ACCESSORY_MATERIAL_VNUM(dstItemVNum, item.GetItemSubType()):
			return False
		
		if curCount>=maxCount:
			return False

		return True

	def __CanAddAccessorySocket(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() != item.ITEM_TYPE_ARMOR:
			return False

		if not item.GetItemSubType() in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
			return False

		curCount = player.GetItemMetinSocket(dstSlotPos, 0)
		maxCount = player.GetItemMetinSocket(dstSlotPos, 1)
		
		ACCESSORY_SOCKET_MAX_SIZE = 3
		if maxCount >= ACCESSORY_SOCKET_MAX_SIZE:
			return False

		return True

	def __CanAddItemAttr(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)
		
		if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):	 
			return False
			
		attrCount = 0
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemAttribute(dstSlotPos, i) != 0:
				attrCount += 1

		if attrCount<4:
			return True
								
		return False

	def ShowToolTip(self, slotIndex):
		if None != self.tooltipItem:
			self.tooltipItem.SetInventoryItem(slotIndex)

	def OnTop(self):
		if None != self.tooltipItem:
			self.tooltipItem.SetTop()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def UseItemSlot(self, slotIndex):
		curCursorNum = app.GetCursor()
		if app.SELL == curCursorNum:
			return

		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			return

		slotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(slotIndex)

		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			if self.wndDragonSoulRefine.IsShow():
				self.wndDragonSoulRefine.AutoSetItem((player.INVENTORY, slotIndex), 1)
				return

		self.__UseItem(slotIndex)
		mouseModule.mouseController.DeattachObject()
		self.OverOutItem()

	def __UseItem(self, slotIndex):
		ItemVNum = player.GetItemIndex(slotIndex)
		item.SelectItem(ItemVNum)
		if item.IsFlag(item.ITEM_FLAG_CONFIRM_WHEN_USE):
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.INVENTORY_REALLY_USE_ITEM)
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnAccept))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnCancel))
			self.questionDialog.Open()
			self.questionDialog.slotIndex = slotIndex
		
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

		else:
			self.__SendUseItemPacket(slotIndex)
			#net.SendItemUsePacket(slotIndex)	

	def __UseItemQuestionDialog_OnCancel(self):
		self.OnCloseQuestionDialog()

	def __UseItemQuestionDialog_OnAccept(self):
		self.__SendUseItemPacket(self.questionDialog.slotIndex)
		self.OnCloseQuestionDialog()		

	def __SendUseItemToItemPacket(self, srcSlotPos, dstSlotPos):
		# ���λ��� ���� �ִ� ���� ������ ��� ����
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		net.SendItemUseToItemPacket(srcSlotPos, dstSlotPos)

	def __SendUseItemPacket(self, slotPos):
		# ���λ��� ���� �ִ� ���� ������ ��� ����
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		net.SendItemUsePacket(slotPos)
	
	def __SendMoveItemPacket(self, srcSlotPos, dstSlotPos, srcItemCount):
		# ���λ��� ���� �ִ� ���� ������ ��� ����
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		net.SendItemMovePacket(srcSlotPos, dstSlotPos, srcItemCount)
	
	def SetDragonSoulRefineWindow(self, wndDragonSoulRefine):
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoulRefine = wndDragonSoulRefine
			
	def OnMoveWindow(self, x, y):
#		print "Inventory Global Pos : ", self.GetGlobalPosition()
		if self.wndBelt:
#			print "Belt Global Pos : ", self.wndBelt.GetGlobalPosition()
			self.wndBelt.AdjustPositionAndSize()

	if app.BL_ENABLE_PICKUP_ITEM_EFFECT:
		# Pickup-glow highlight (freshly picked-up items) - sticky until hovered, tracked by
		# global slot number so it survives inventory page switches like uiDragonSoul's version.
		def __HighlightSlot_Refresh(self):
			for i in xrange(self.wndItem.GetSlotCount()):
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
				if slotNumber in self.listHighlightedSlot:
					self.wndItem.ActivateSlot(i)

		def __HighlightSlot_Clear(self):
			for i in xrange(self.wndItem.GetSlotCount()):
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
				if slotNumber in self.listHighlightedSlot:
					self.wndItem.DeactivateSlot(i)
					self.listHighlightedSlot.remove(slotNumber)

		def HighlightSlot(self, slot):
			if slot >= player.INVENTORY_PAGE_SIZE * player.INVENTORY_PAGE_COUNT:
				return

			if not slot in self.listHighlightedSlot:
				self.listHighlightedSlot.append(slot)

		def DelHighlightSlot(self, inventorylocalslot):
			if inventorylocalslot in self.listHighlightedSlot:
				if inventorylocalslot >= player.INVENTORY_PAGE_SIZE:
					self.wndItem.DeactivateSlot(inventorylocalslot - (self.inventoryPageIndex * player.INVENTORY_PAGE_SIZE))
				else:
					self.wndItem.DeactivateSlot(inventorylocalslot)

				self.listHighlightedSlot.remove(inventorylocalslot)

# WJ_SPLIT_INVENTORY_SYSTEM
class ExtendedInventoryWindow(ui.ScriptWindow):
	tooltipItem = None
	interface = None
	dlgPickMoney = None
	dlgPickItem = None
	sellingSlotNumber = -1
	isLoaded = 0

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.inventoryPageIndex = 0
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)

	def BindInterfaceClass(self, interface):
		self.interface = interface

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/ExtendedInventoryWindow.py")
		except:
			import exception
			exception.Abort("ExtendedInventoryWindow.LoadWindow.LoadObject")

		try:
			wndItem = self.GetChild("ItemSlot")
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			self.titleName = self.GetChild("TitleName")
			self.SkillBookButton = self.GetChild("SkillBookButton")
			self.UpgradeItemsButton = self.GetChild("UpgradeItemsButton")
			self.stoneButton = self.GetChild("StoneButton")
			self.sandikButton = self.GetChild("SandikButton")
			self.inventoryTab = []
			self.inventoryTab.append(self.GetChild("Inventory_Tab_01"))
			self.inventoryTab.append(self.GetChild("Inventory_Tab_02"))
			self.inventoryTab.append(self.GetChild("Inventory_Tab_03"))

			if app.BL_ENABLE_PICKUP_ITEM_EFFECT:
				self.listHighlightedSlot = []

			if app.ENABLE_SORT_INVEN:
				self.yenilebutton = self.GetChild2("YenileButton")
				self.yenilebutton.SetEvent(ui.__mem_func__(self.ClickYenileButton))
				self.tooltipI = uiToolTip.ToolTip()
				self.tooltipI.Hide()
				self.tooltipInfo = [self.tooltipI]*4
				self.InformationText = [localeInfo.YENILE_BUTTON_TITLE,
										localeInfo.YENILE_BUTTON,
										localeInfo.YENILE_BUTTON2,
										localeInfo.YENILE_BUTTON3
				]
				for i in xrange(len(self.tooltipInfo)):
					self.tooltipInfo[i].SetFollow(True)
					self.tooltipInfo[i].AlignHorizonalCenter()
					if i == 0:
						self.tooltipInfo[i].AppendTextLine(self.InformationText[i], 0xffffff00)
					else:
						self.tooltipInfo[i].AppendTextLine(self.InformationText[i])
					self.tooltipInfo[i].Hide()
		except:
			import exception
			exception.Abort("ExtendedInventoryWindow.LoadWindow.BindObject")

		## Item
		wndItem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndItem.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndItem.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		self.SkillBookButton.SetEvent(lambda arg=0: self.SetInventoryType(arg))
		self.UpgradeItemsButton.SetEvent(lambda arg=1: self.SetInventoryType(arg))
		self.stoneButton.SetEvent(lambda arg=2: self.SetInventoryType(arg))
		self.sandikButton.SetEvent(lambda arg=3: self.SetInventoryType(arg))
		self.SkillBookButton.Down()

		self.inventoryTab[0].SetEvent(lambda arg=0: self.SetInventoryPage(arg))
		self.inventoryTab[1].SetEvent(lambda arg=1: self.SetInventoryPage(arg))
		self.inventoryTab[2].SetEvent(lambda arg=2: self.SetInventoryPage(arg))
		self.inventoryTab[0].Down()

		## PickMoneyDialog
		dlgPickMoney = uiPickMoney.PickMoneyDialog()
		dlgPickMoney.LoadDialog()
		dlgPickMoney.Hide()

		self.dlgPickMoney = dlgPickMoney

		self.wndItem = wndItem
		self.SetInventoryType(0)
		self.SetInventoryPage(0)

	def Destroy(self):
		self.ClearDictionary()
		self.dlgPickMoney.Destroy()
		self.dlgPickMoney = 0
		self.tooltipItem = None
		self.wndItem = 0
		self.interface = None
		self.inventoryTab = []

	def Hide(self):
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()
		wndMgr.Hide(self.hWnd)

	def Close(self):
		self.Hide()

	def SetInventoryType(self, type):
		self.inventoryType = type
		if type == 0:
			self.SkillBookButton.Down()
			self.UpgradeItemsButton.SetUp()
			self.stoneButton.SetUp()
			self.sandikButton.SetUp()
			self.titleName.SetText(localeInfo.INVENTORY_SKILL_BOOK_TOOLTIP)
		elif type == 2:
			self.stoneButton.Down()
			self.sandikButton.SetUp()
			self.UpgradeItemsButton.SetUp()
			self.SkillBookButton.SetUp()
			self.titleName.SetText(localeInfo.INVENTORY_STONE_TOOLTIP)
		elif type == 3:
			self.sandikButton.Down()
			self.stoneButton.SetUp()
			self.UpgradeItemsButton.SetUp()
			self.SkillBookButton.SetUp()
			self.titleName.SetText(localeInfo.INVENTORY_SANDIK_TOOLTIP)
		else:
			self.UpgradeItemsButton.Down()
			self.SkillBookButton.SetUp()
			self.stoneButton.SetUp()
			self.sandikButton.SetUp()
			self.titleName.SetText(localeInfo.INVENTORY_UPGRADE_ITEM_TOOLTIP)
		self.RefreshBagSlotWindow()

	def SetInventoryPage(self, page):
		self.inventoryPageIndex = page
		for i in range(0,len(self.inventoryTab)):
			self.inventoryTab[i].SetUp()
		self.inventoryTab[page].Down()
		self.RefreshBagSlotWindow()

	def OnPickItem(self, count):
		itemSlotIndex = self.dlgPickMoney.itemGlobalSlotIndex
		selectedItemVNum = player.GetItemIndex(itemSlotIndex)
		if self.inventoryType == 0:
			mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_SKILL_BOOK_INVENTORY, itemSlotIndex, selectedItemVNum, count)
		elif self.inventoryType == 2:
			mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_STONE_INVENTORY, itemSlotIndex, selectedItemVNum, count)
		elif self.inventoryType == 3:
			mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_SANDIK_INVENTORY, itemSlotIndex, selectedItemVNum, count)
		else:
			mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY, itemSlotIndex, selectedItemVNum, count)

	def GetInventoryPageIndex(self):
		return self.inventoryPageIndex

	def __GetSortCategory(self):
		# WJ_SPLIT_INVENTORY_SYSTEM: maps the currently open tab to the server's
		# SortInven category id (0=base bag, 1=skillbook, 2=upgrade, 3=stone, 4=sandik).
		if self.inventoryType == 0:
			return 1
		elif self.inventoryType == 2:
			return 3
		elif self.inventoryType == 3:
			return 4
		else:
			return 2

	if app.ENABLE_SORT_INVEN:
		def ClickYenileButton(self):
			category = self.__GetSortCategory()
			if app.IsPressed(app.DIK_LALT):
				net.SortInven(2, category)
			elif app.IsPressed(app.DIK_LCONTROL):
				net.SortInven(3, category)
			else:
				net.SortInven(1, category)

	def OnUpdate(self):
		if app.ENABLE_SORT_INVEN and self.tooltipInfo:
			for i in xrange(len(self.tooltipInfo)):
				if self.yenilebutton.IsIn():
					self.tooltipInfo[i].Show()
				else:
					self.tooltipInfo[i].Hide()

	def RefreshBagSlotWindow(self):
		getItemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		setItemVNum=self.wndItem.SetItemSlot

		if app.BL_ENABLE_PICKUP_ITEM_EFFECT:
			for i in xrange(self.wndItem.GetSlotCount()):
				self.wndItem.DeactivateSlot(i)

		if self.inventoryType == 0:
			slotStart = item.SKILL_BOOK_INVENTORY_SLOT_START
			slotCount = player.SKILL_BOOK_INVENTORY_SLOT_COUNT
		elif self.inventoryType == 2:
			slotStart = item.STONE_INVENTORY_SLOT_START
			slotCount = player.STONE_INVENTORY_SLOT_COUNT
		elif self.inventoryType == 3:
			slotStart = item.SANDIK_INVENTORY_SLOT_START
			slotCount = player.SANDIK_INVENTORY_SLOT_COUNT
		else:
			slotStart = item.UPGRADE_ITEMS_INVENTORY_SLOT_START
			slotCount = player.UPGRADE_ITEMS_INVENTORY_SLOT_COUNT

		for i in xrange(slotCount):
			slotNumber = slotStart + i
			if self.GetInventoryPageIndex() == 1:
				slotNumber += 45
			elif self.GetInventoryPageIndex() == 2:
				slotNumber += 90
			itemCount = getItemCount(slotNumber)
			if 0 == itemCount:
				self.wndItem.ClearSlot(i)
				continue
			elif 1 == itemCount:
				itemCount = 0
			itemVnum = getItemVNum(slotNumber)
			setItemVNum(i, itemVnum, itemCount)
		self.wndItem.RefreshSlot()

		if app.BL_ENABLE_PICKUP_ITEM_EFFECT:
			self.__HighlightSlot_Refresh()

	if app.BL_ENABLE_PICKUP_ITEM_EFFECT:
		# Pickup-glow highlight (freshly picked-up items) - sticky until hovered, tracked by
		# global slot number so it survives category/page switches, mirroring the base
		# InventoryWindow's implementation.
		def __HighlightSlot_Refresh(self):
			for i in xrange(self.wndItem.GetSlotCount()):
				slotNumber = self.__LocalSlotToGlobalSlot(i)
				if slotNumber in self.listHighlightedSlot:
					self.wndItem.ActivateSlot(i)

		def HighlightSlot(self, slot):
			if slot < item.SKILL_BOOK_INVENTORY_SLOT_START or slot >= item.SANDIK_INVENTORY_SLOT_START + player.SANDIK_INVENTORY_SLOT_COUNT:
				return

			if not slot in self.listHighlightedSlot:
				self.listHighlightedSlot.append(slot)

		def DelHighlightSlot(self, globalSlot, localSlot):
			if globalSlot in self.listHighlightedSlot:
				self.wndItem.DeactivateSlot(localSlot)
				self.listHighlightedSlot.remove(globalSlot)

	def RefreshItemSlot(self):
		self.RefreshBagSlotWindow()

	def RefreshStatus(self):
		pass

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def __LocalSlotToGlobalSlot(self, localSlot):
		if self.inventoryType == 0:
			slotIndex = localSlot + item.SKILL_BOOK_INVENTORY_SLOT_START
		elif self.inventoryType == 2:
			slotIndex = localSlot + item.STONE_INVENTORY_SLOT_START
		elif self.inventoryType == 3:
			slotIndex = localSlot + item.SANDIK_INVENTORY_SLOT_START
		else:
			slotIndex = localSlot + item.UPGRADE_ITEMS_INVENTORY_SLOT_START

		if self.GetInventoryPageIndex() == 1:
			slotIndex += 45
		elif self.GetInventoryPageIndex() == 2:
			slotIndex += 90
		return slotIndex

	def SelectEmptySlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		selectedSlotPos = self.__LocalSlotToGlobalSlot(selectedSlotPos)

		if mouseModule.mouseController.isAttached():

			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()

			if player.SLOT_TYPE_INVENTORY == attachedSlotType or player.SLOT_TYPE_SKILL_BOOK_INVENTORY == attachedSlotType or player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY == attachedSlotType or player.SLOT_TYPE_STONE_INVENTORY == attachedSlotType or player.SLOT_TYPE_SANDIK_INVENTORY == attachedSlotType:
				itemCount = player.GetItemCount(attachedSlotPos)
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				self.__SendMoveItemPacket(attachedSlotPos, selectedSlotPos, attachedCount)

				if item.IsRefineScroll(attachedItemIndex):
					self.wndItem.SetUseMode(False)

			elif player.SLOT_TYPE_PRIVATE_SHOP == attachedSlotType:
				mouseModule.mouseController.RunCallBack("INVENTORY")

			elif player.SLOT_TYPE_SHOP == attachedSlotType:
				net.SendShopBuyPacket(attachedSlotPos)

			elif player.SLOT_TYPE_SAFEBOX == attachedSlotType:

				if player.ITEM_MONEY == attachedItemIndex:
					net.SendSafeboxWithdrawMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())
					snd.PlaySound("sound/ui/money.wav")

				else:
					net.SendSafeboxCheckoutPacket(attachedSlotPos, selectedSlotPos)

			elif player.SLOT_TYPE_MALL == attachedSlotType:
				net.SendMallCheckoutPacket(attachedSlotPos, selectedSlotPos)

			mouseModule.mouseController.DeattachObject()

	def SelectItemSlot(self, itemSlotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		itemSlotIndex = self.__LocalSlotToGlobalSlot(itemSlotIndex)

		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemVID = mouseModule.mouseController.GetAttachedItemIndex()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()

			if player.GetItemCount(itemSlotIndex) > attachedItemCount:
				return

			curCursorNum = app.GetCursor()
			if app.SELL == curCursorNum:
				self.__SellItem(itemSlotIndex)

			if player.SLOT_TYPE_INVENTORY == attachedSlotType or player.SLOT_TYPE_SKILL_BOOK_INVENTORY == attachedSlotType or player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY == attachedSlotType or player.SLOT_TYPE_STONE_INVENTORY == attachedSlotType or player.SLOT_TYPE_SANDIK_INVENTORY == attachedSlotType:
				self.__SendMoveItemPacket(attachedSlotPos, itemSlotIndex, attachedItemCount)

			mouseModule.mouseController.DeattachObject()
		else:

			curCursorNum = app.GetCursor()
			if app.SELL == curCursorNum:
				self.__SellItem(itemSlotIndex)

			elif app.BUY == curCursorNum:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)

			elif app.IsPressed(app.DIK_LALT):
				link = player.GetItemLink(itemSlotIndex)
				ime.PasteString(link)

			elif app.IsPressed(app.DIK_LSHIFT):
				itemCount = player.GetItemCount(itemSlotIndex)

				if itemCount > 1:
					self.dlgPickMoney.SetTitleName(localeInfo.PICK_ITEM_TITLE)
					self.dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickItem))
					self.dlgPickMoney.Open(itemCount)
					self.dlgPickMoney.itemGlobalSlotIndex = itemSlotIndex

			elif app.IsPressed(app.DIK_LCONTROL):
				itemIndex = player.GetItemIndex(itemSlotIndex)

				if True == item.CanAddToQuickSlotItem(itemIndex):
					if self.inventoryType == 0:
						player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_SKILL_BOOK_INVENTORY, itemSlotIndex)
					elif self.inventoryType == 2:
						player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_STONE_INVENTORY, itemSlotIndex)
					elif self.inventoryType == 3:
						player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_SANDIK_INVENTORY, itemSlotIndex)
					else:
						player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY, itemSlotIndex)
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.QUICKSLOT_REGISTER_DISABLE_ITEM)

			else:
				selectedItemVNum = player.GetItemIndex(itemSlotIndex)
				itemCount = player.GetItemCount(itemSlotIndex)
				if self.inventoryType == 0:
					mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_SKILL_BOOK_INVENTORY, itemSlotIndex, selectedItemVNum, itemCount)
				elif self.inventoryType == 2:
					mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_STONE_INVENTORY, itemSlotIndex, selectedItemVNum, itemCount)
				elif self.inventoryType == 3:
					mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_SANDIK_INVENTORY, itemSlotIndex, selectedItemVNum, itemCount)
				else:
					mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY, itemSlotIndex, selectedItemVNum, itemCount)

				self.wndItem.SetUseMode(True)

				snd.PlaySound("sound/ui/pick.wav")

	def __SellItem(self, itemSlotPos):
		if not player.IsEquipmentSlot(itemSlotPos):
			self.sellingSlotNumber = itemSlotPos
			itemIndex = player.GetItemIndex(itemSlotPos)
			itemCount = player.GetItemCount(itemSlotPos)

			self.sellingSlotitemIndex = itemIndex
			self.sellingSlotitemCount = itemCount

			item.SelectItem(itemIndex)
			if item.IsAntiFlag(item.ANTIFLAG_SELL):
				popup = uiCommon.PopupDialog()
				popup.SetText(localeInfo.SHOP_CANNOT_SELL_ITEM)
				popup.SetAcceptEvent(self.__OnClosePopupDialog)
				popup.Open()
				self.popup = popup
				return
			itemPrice = player.GetISellItemPrice(itemSlotPos)

			item.GetItemName(itemIndex)
			itemName = item.GetItemName()

			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.DO_YOU_SELL_ITEM(itemName, itemCount, itemPrice))
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.SellItem))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
			self.questionDialog.count = itemCount

			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

	def SellItem(self):
		if self.sellingSlotitemIndex == player.GetItemIndex(self.sellingSlotNumber):
			if self.sellingSlotitemCount == player.GetItemCount(self.sellingSlotNumber):
				net.SendShopSellPacketNew(self.sellingSlotNumber, self.questionDialog.count)
				snd.PlaySound("sound/ui/money.wav")
		self.OnCloseQuestionDialog()

	def OnCloseQuestionDialog(self):
		if not self.questionDialog:
			return

		self.questionDialog.Close()
		self.questionDialog = None
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def __OnClosePopupDialog(self):
		self.pop = None

	def OverOutItem(self):
		self.wndItem.SetUsableItem(False)
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OverInItem(self, overSlotPos):
		globalSlotPos = self.__LocalSlotToGlobalSlot(overSlotPos)
		self.wndItem.SetUsableItem(False)

		if app.BL_ENABLE_PICKUP_ITEM_EFFECT:
			self.DelHighlightSlot(globalSlotPos, overSlotPos)

		self.ShowToolTip(globalSlotPos)

	def ShowToolTip(self, slotIndex):
		if None != self.tooltipItem:
			self.tooltipItem.SetInventoryItem(slotIndex)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def UseItemSlot(self, slotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			return

		slotIndex = self.__LocalSlotToGlobalSlot(slotIndex)
		self.__UseItem(slotIndex)
		mouseModule.mouseController.DeattachObject()
		self.OverOutItem()

	def __UseItem(self, slotIndex):
		ItemVNum = player.GetItemIndex(slotIndex)
		item.SelectItem(ItemVNum)
		if item.IsFlag(item.ITEM_FLAG_CONFIRM_WHEN_USE):
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.INVENTORY_REALLY_USE_ITEM)
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnAccept))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnCancel))
			self.questionDialog.Open()
			self.questionDialog.slotIndex = slotIndex

			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

		else:
			self.__SendUseItemPacket(slotIndex)

	def __UseItemQuestionDialog_OnCancel(self):
		self.OnCloseQuestionDialog()

	def __UseItemQuestionDialog_OnAccept(self):
		self.__SendUseItemPacket(self.questionDialog.slotIndex)
		self.OnCloseQuestionDialog()

	def __SendUseItemPacket(self, slotPos):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		net.SendItemUsePacket(slotPos)

	def __SendMoveItemPacket(self, srcSlotPos, dstSlotPos, srcItemCount):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		net.SendItemMovePacket(srcSlotPos, dstSlotPos, srcItemCount)

