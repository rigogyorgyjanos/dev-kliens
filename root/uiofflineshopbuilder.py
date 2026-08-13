import ui
import snd
import offlineShop
import mouseModule
import player
import item
import chat
import localeInfo
import uiCommon
import offlineShopItemPrice

class OfflineShopBuilderWindow(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.isLoaded = False
		self.nameLine = None
		self.moneyText = None
		self.itemSlot = None
		self.lockOverlays = {}
		self.itemStock = {}
		self.tooltipItem = None
		self.priceInputBoard = None
		self.title = ""
		self.totalMoney = 0
		self.slotFlag = 0

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.itemStock = {}
		self.nameLine = None
		self.moneyText = None
		self.itemSlot = None
		self.lockOverlays = {}
		self.priceInputBoard = None

	def __LoadWindow(self):
		if self.isLoaded:
			return

		## isLoaded must only flip to True once the whole body below has actually
		## succeeded - see the identical note in uiofflineshop.py's OfflineShopWindow.
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/offlineshop/offlineshopbuilderwindow.py")

			self.nameLine = self.GetChild("NameLine")
			self.moneyText = self.GetChild("Money")
			self.itemSlot = self.GetChild("ItemSlot")
			self.__BuildLockOverlays()

			self.GetChild("board").SetCloseEvent(ui.__mem_func__(self.CloseReal))
			self.GetChild("FirstButton").SetEvent(ui.__mem_func__(self.OnOk))
			self.GetChild("SecondButton").SetEvent(ui.__mem_func__(self.CloseReal))

			self.itemSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.OnSelectEmptySlot))
			self.itemSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.OnSelectItemSlot))
			self.itemSlot.SetOverInItemEvent(ui.__mem_func__(self.OnOverInItem))
			self.itemSlot.SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutItem))

			self.isLoaded = True
		except:
			import exception
			exception.Abort("OfflineShopBuilderWindow.__LoadWindow")

	## Plain ImageBox overlays instead of ItemSlot's cover-button mechanism - see
	## the identical note in uiofflineshop.py's OfflineShopWindow.__BuildLockOverlays
	## for why (a slot that was locked and then unlocked would otherwise show a
	## faded leftover cover-button visual on top of any item placed there after).
	def __BuildLockOverlays(self):
		for pos in xrange(40, offlineShop.HOST_ITEM_MAX_NUM):
			overlay = ui.ImageBox()
			overlay.SetParent(self.itemSlot)
			## Purely decorative - without this it sits on top of the grid and
			## swallows the right-click that's supposed to reach ItemSlot's own
			## UnselectEmptySlotEvent (the unlock dialog), making locked slots
			## un-unlockable.
			overlay.AddFlag("not_pick")
			overlay.LoadImage("d:/ymir work/ui/game/offlineshop/lock_0.tga")
			col = pos % 10
			row = pos // 10
			overlay.SetPosition(col * 32, row * 32)
			overlay.Hide()
			self.lockOverlays[pos] = overlay

	def Open(self, title, slotFlag = 0):
		self.__LoadWindow()

		self.title = title
		self.itemStock = {}
		self.totalMoney = 0
		self.slotFlag = long(slotFlag)
		offlineShop.ClearBuilderStock()
		self.nameLine.SetText(title)
		self.__SetMoneyText()
		self.SetCenterPosition()
		self.Refresh()
		self.Show()

	def SetSlotFlag(self, slotFlag):
		self.slotFlag = long(slotFlag)
		self.Refresh()

	def CloseReal(self):
		self.Close()

	def Close(self):
		# Tells the server we're done with the pre-creation panel flow, whether we
		# actually created a shop or cancelled out - server no-ops if there's nothing
		# to clear, but skipping this send is what left OfflineShopPanel stuck server-side.
		offlineShop.SendStopShopping()
		self.title = ""
		self.itemStock = {}
		self.totalMoney = 0
		offlineShop.ClearBuilderStock()
		self.Hide()

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def __SetMoneyText(self):
		try:
			text = localeInfo.NumberToMoneyString(self.totalMoney)
		except:
			text = str(self.totalMoney)
		self.moneyText.SetText(text)

	def Refresh(self):
		getItemVNum = player.GetItemIndex
		getItemCount = player.GetItemCount

		for i in xrange(offlineShop.HOST_ITEM_MAX_NUM):
			if not self.itemStock.has_key(i):
				if i >= 40 and not (self.slotFlag & (1 << (i - 40))):
					self.itemSlot.ClearSlot(i)
					self.lockOverlays[i].Show()
				else:
					self.itemSlot.ClearSlot(i)
					if i in self.lockOverlays:
						self.lockOverlays[i].Hide()
				continue

			if i in self.lockOverlays:
				self.lockOverlays[i].Hide()
			invenType, invenPos, price = self.itemStock[i]
			itemCount = getItemCount(invenType, invenPos)
			if itemCount <= 1:
				itemCount = 0
			self.itemSlot.SetItemSlot(i, getItemVNum(invenType, invenPos), itemCount)

		self.itemSlot.RefreshSlot()

	def OnSelectEmptySlot(self, selectedSlotPos):
		isAttached = mouseModule.mouseController.isAttached()
		if not isAttached:
			return

		if selectedSlotPos >= 40 and not (self.slotFlag & (1 << (selectedSlotPos - 40))):
			snd.PlaySound("sound/ui/loginfail.wav")
			mouseModule.mouseController.DeattachObject()
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OFFLINE_SHOP_CANT_SLOT_OPEN if hasattr(localeInfo, "OFFLINE_SHOP_CANT_SLOT_OPEN") else "This slot is locked.")
			return

		attachedSlotType = mouseModule.mouseController.GetAttachedType()
		attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
		mouseModule.mouseController.DeattachObject()

		if player.SLOT_TYPE_INVENTORY != attachedSlotType and player.SLOT_TYPE_DRAGON_SOUL_INVENTORY != attachedSlotType and \
			player.SLOT_TYPE_SKILL_BOOK_INVENTORY != attachedSlotType and \
			player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY != attachedSlotType and \
			player.SLOT_TYPE_STONE_INVENTORY != attachedSlotType and \
			player.SLOT_TYPE_SANDIK_INVENTORY != attachedSlotType:
			return

		attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
		itemVNum = player.GetItemIndex(attachedInvenType, attachedSlotPos)
		if itemVNum == 0:
			return

		item.SelectItem(itemVNum)
		if item.IsAntiFlag(item.ANTIFLAG_GIVE) or item.IsAntiFlag(item.ANTIFLAG_MYSHOP):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.PRIVATE_SHOP_CANNOT_SELL_ITEM)
			return

		priceInputBoard = uiCommon.MoneyInputDialog()
		priceInputBoard.SetTitle(localeInfo.PRIVATE_SHOP_INPUT_PRICE_DIALOG_TITLE)
		priceInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptInputPrice))
		priceInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelInputPrice))
		priceInputBoard.Open()

		# Suggest whatever PER-UNIT price this item vnum last sold for, remembered
		# across shops/sessions (UserData/shop/item_prices.txt), scaled by how many
		# of this item are actually being stocked right now (a stack of 10 at
		# 1000/each suggests 10000, not 1000).
		newItemCount = player.GetItemCount(attachedInvenType, attachedSlotPos)
		if newItemCount <= 0:
			newItemCount = 1

		rememberedUnitPrice = offlineShopItemPrice.GetPrice(itemVNum)
		if rememberedUnitPrice > 0:
			priceInputBoard.SetValue(rememberedUnitPrice * newItemCount)

		# Live server-wide market average (see COfflineShopManager::CheckAveragePrice) -
		# shown via the dialog's own built-in SetAveragePrice (matches the Solaris2
		# reference: grows the board and adds the line in-place) once the reply
		# arrives - see SetAveragePrice below.

		self.priceInputBoard = priceInputBoard
		self.priceInputBoard.itemVNum = itemVNum
		self.priceInputBoard.sourceWindowType = attachedInvenType
		self.priceInputBoard.sourceSlotPos = attachedSlotPos
		self.priceInputBoard.targetSlotPos = selectedSlotPos
		offlineShop.SendGetAveragePrice(itemVNum)

	def OnSelectItemSlot(self, selectedSlotPos):
		isAttached = mouseModule.mouseController.isAttached()
		if isAttached:
			snd.PlaySound("sound/ui/loginfail.wav")
			mouseModule.mouseController.DeattachObject()
			return

		if not selectedSlotPos in self.itemStock:
			return

		invenType, invenPos, price = self.itemStock[selectedSlotPos]
		self.totalMoney -= price
		self.__SetMoneyText()

		offlineShop.RemoveBuilderItem(selectedSlotPos)
		del self.itemStock[selectedSlotPos]
		snd.PlaySound("sound/ui/drop.wav")
		self.Refresh()

	def AcceptInputPrice(self):
		if not self.priceInputBoard:
			return True

		text = self.priceInputBoard.GetText()
		if not text or not text.isdigit() or int(text) <= 0:
			return True

		attachedInvenType = self.priceInputBoard.sourceWindowType
		sourceSlotPos = self.priceInputBoard.sourceSlotPos
		targetSlotPos = self.priceInputBoard.targetSlotPos
		price = int(text)

		for stockPos, (itemWindowType, itemSlotIndex, itemPrice) in self.itemStock.items():
			if itemWindowType == attachedInvenType and itemSlotIndex == sourceSlotPos:
				self.totalMoney -= itemPrice
				del self.itemStock[stockPos]

		self.itemStock[targetSlotPos] = (attachedInvenType, sourceSlotPos, price)
		self.totalMoney += price
		self.__SetMoneyText()
		offlineShop.AddBuilderItem(attachedInvenType, sourceSlotPos, targetSlotPos, price)

		itemVNum = player.GetItemIndex(attachedInvenType, sourceSlotPos)
		if itemVNum != 0:
			# Remember this as a PER-UNIT price so a differently-sized stack next
			# time still gets a correctly scaled suggestion.
			stockedCount = player.GetItemCount(attachedInvenType, sourceSlotPos)
			if stockedCount <= 0:
				stockedCount = 1
			offlineShopItemPrice.SetPrice(itemVNum, price / stockedCount)
		snd.PlaySound("sound/ui/drop.wav")

		self.Refresh()
		self.priceInputBoard = None
		return True

	def CancelInputPrice(self):
		self.priceInputBoard = None
		return True

	def SetAveragePrice(self, vnum, price):
		if not self.priceInputBoard or getattr(self.priceInputBoard, "itemVNum", None) != vnum:
			return
		if price > 0:
			self.priceInputBoard.SetAveragePrice(price)

	def OnOk(self):
		if not self.title:
			return
		if 0 == len(self.itemStock):
			return

		# Server forces this back to 30000 unless AFFECT_DECORATION is active anyway;
		# real decoration choice happens post-creation from the owner panel (ChangeDecoration).
		offlineShop.SendMyOfflineShop(self.title, 0, 30000)

	def OnPressEscapeKey(self):
		self.CloseReal()
		return True

	def OnOverInItem(self, slotIndex):
		if self.tooltipItem and self.itemStock.has_key(slotIndex):
			invenType, invenPos, price = self.itemStock[slotIndex]
			self.tooltipItem.SetOfflineShopBuilderItem(invenType, invenPos, price)

	def OnOverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OnCheckResult(self, hasShop):
		# HasOfflineShop() on the server fires unconditionally on EVERY F7 press, not just
		# during creation - it also runs when an OWNER reopens their existing shop. If this
		# builder was never opened this session, self.IsShow() is False, so this must skip:
		# calling Close() here would send SendStopShopping(), which the server processes as
		# "this player wants to stop shopping" - removing the owner as guest of the shop
		# they just (re)entered a moment earlier via AddGuest(), closing it again instantly.
		if hasShop and self.IsShow():
			self.Close()
