import app
import ui
import offlineShop
import item
import chat
import player
import localeInfo
import uiCommon
import mouseModule
import snd
import offlineShopItemPrice

ROOT_OFFLINESHOP = "d:/ymir work/ui/offlineshop/"

## Bit 63 of offlineShop.GetSlotFlag() - mirrors server-src/server/common/length.h's
## SHOP_LOCKED_FLAG. Only bits 0-39 are ever used for the 40 extra-slot unlocks, so
## this rides the same already-synced field instead of needing a new one.
SHOP_LOCKED_FLAG = 1 << 63

## The owner sees the full chrome (title/watcher/expire/gold boxes + icon row) above
## and below the grid, so the grid sits lower and the window is taller. A guest sees
## only the item grid - matching the reference exactly - so the grid moves up into
## the space the title box would occupy and the window shrinks to fit just the grid.
OWNER_GRID_Y = 56
GUEST_GRID_Y = 32
OWNER_BOARD_HEIGHT = 431
GUEST_BOARD_HEIGHT = GUEST_GRID_Y + 8 * 32 + 13

## Ctrl+right-click QOL (uiinventory.UseItemSlot calls this): re-stocking a vnum
## that's already listed in the currently-open owner shop should skip the price
## dialog entirely and reuse that listing's per-unit price. Slot placement itself
## is NOT decided here - offlineShop.SendAddItemShortcut() hands the item to the
## server (COfflineShopManager::AddItemShortcut) which finds the target slot
## itself using the same bSize-aware CGrid occupancy check the rest of the shop
## grid uses, so a 2-3 row tall weapon/armor icon can never get placed under (or
## have something placed under) a neighboring item's footprint, and rapid clicks
## can't race each other onto the same slot the way a client-side guess could.
## Returns the existing listing's per-unit price, or 0 if there's no live owner
## shop or no matching vnum currently on sale.
def FindQuickAddUnitPrice(itemVNum):
	if not offlineShop.IsOpen() or not offlineShop.IsOwner():
		return 0

	for pos in xrange(offlineShop.HOST_ITEM_MAX_NUM):
		if offlineShop.GetItemVnum(pos) == itemVNum:
			existingCount = offlineShop.GetItemCount(pos)
			if existingCount <= 0:
				existingCount = 1
			return offlineShop.GetItemPrice(pos) / existingCount

	return 0

## Ctrl+right-click QOL, no-existing-listing case: FindQuickAddUnitPrice() found
## nothing to copy a price from, so the caller needs a free slot to open the
## normal price dialog against instead (same target-picking a manual drag-and-
## drop onto an empty slot would land on, just found automatically). Returns
## None if the shop is full/fully locked.
def FindEmptyUnlockedSlot():
	slotFlag = offlineShop.GetSlotFlag()
	for pos in xrange(offlineShop.HOST_ITEM_MAX_NUM):
		if offlineShop.GetItemVnum(pos) != 0:
			continue
		if pos >= 40 and not (slotFlag & (1 << (pos - 40))):
			continue
		return pos
	return None

class OfflineShopDecorationWindow(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.isLoaded = False

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		if self.isLoaded:
			return

		## isLoaded must only flip to True once the whole body below has actually
		## succeeded - setting it early (as this used to) means a single failed build
		## permanently bricks the window: every later Open() would see isLoaded==True
		## and skip straight past __BuildWindow, forever, with no retry and no visible
		## error (the failure only ever showed up once, the very first time).
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/offlineshop/offlineshopdecoration.py")

			self.GetChild("board").SetCloseEvent(ui.__mem_func__(self.Close))
			for i in xrange(16):
				self.GetChild("deco_%d" % i).SAFE_SetEvent(self.OnSelect, i)

			self.isLoaded = True
		except:
			import exception
			exception.Abort("OfflineShopDecorationWindow.__LoadWindow")

	def Open(self):
		self.__LoadWindow()
		self.SetCenterPosition()
		self.Show()

	def Close(self):
		self.Hide()

	def OnSelect(self, vnum):
		sign = offlineShop.GetTitle()
		offlineShop.SendChangeDecoration(vnum, 0, sign)
		self.Close()


## One sale-log row, styled after the Solaris2 reference's HistoryWindow.Item: a
## line.png divider background with item name+count on the left, price centered,
## date right-aligned - no buyer name, matching the reference exactly.
LOG_ROW_HEIGHT = 21

class HistoryLogItem(ui.Window):
	def __init__(self, parent):
		ui.Window.__init__(self)
		self.SetParent(parent)
		self.SetSize(300, LOG_ROW_HEIGHT)

		self.lineImage = ui.ExpandedImageBox()
		self.lineImage.SetParent(self)
		self.lineImage.AddFlag("not_pick")
		self.lineImage.SetPosition(0, 0)
		self.lineImage.LoadImage(ROOT_OFFLINESHOP + "line.png")
		self.lineImage.Show()

		self.nameText = ui.TextLine()
		self.nameText.SetParent(self)
		self.nameText.SetPosition(4, LOG_ROW_HEIGHT / 2)
		self.nameText.SetVerticalAlignCenter()
		self.nameText.Show()

		self.priceText = ui.TextLine()
		self.priceText.SetParent(self)
		self.priceText.SetPosition(165, LOG_ROW_HEIGHT / 2)
		self.priceText.SetVerticalAlignCenter()
		self.priceText.SetHorizontalAlignCenter()
		self.priceText.Show()

		self.dateText = ui.TextLine()
		self.dateText.SetParent(self)
		self.dateText.SetPosition(255, LOG_ROW_HEIGHT / 2)
		self.dateText.SetVerticalAlignCenter()
		self.dateText.SetHorizontalAlignCenter()
		self.dateText.Show()

		self.Show()

	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		self.lineImage = None
		self.nameText = None
		self.priceText = None
		self.dateText = None
		self.Hide()

	def SetData(self, vnum, count, price, date, priceText):
		try:
			item.SelectItem(vnum)
			name = item.GetItemName()
		except:
			name = "item#%d" % vnum
		text = ("%d x %s" % (count, name)) if count > 1 else name
		if len(text) > 22:
			text = text[:22] + ".."
		self.nameText.SetText(text)
		self.priceText.SetText(priceText)
		self.dateText.SetText(date.split(" ")[0] if date else "")


class OfflineShopWindow(ui.ScriptWindow):

	USE_SHOP_LIMIT_RANGE = 1500

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.isLoaded = False
		self.itemSlot = None
		self.lockOverlays = {}
		self.nameLine = None
		self.moneyText = None
		self.logsWindow = None
		self.tooltipItem = None
		self.decorationWindow = None
		self.questionDialog = None
		self.itemBuyQuestionDialog = None
		self.priceInputBoard = None
		self.logShown = False
		self.logRows = []
		self.logScrollBar = None
		self.logBasePos = 0
		self.xShopStart = 0
		self.yShopStart = 0
		self.lastUpdateTime = 0
		self.ownerChrome = []
		self.titleBox = None
		self.titleBar = None
		self.titleEdit = None
		self.titleEditBtn = None
		self.expireBox = None
		self.expireBar = None
		self.expireText = None
		self.goldBox = None
		self.goldBar = None
		self.goldText = None
		self.goldIcon = None
		self.valueBox = None
		self.valueBar = None
		self.valueText = None
		self.locationBox = None
		self.locationBar = None
		self.locationText = None
		self.lockButton = None
		self.lockButtonIcon = None
		self.plus1DayButton = None
		self.plus1DayButtonIcon = None
		self.teleportButton = None
		self.teleportButtonIcon = None
		self.designButton = None
		self.designButtonIcon = None
		self.historyButton = None
		self.historyButtonIcon = None
		self.destroyButton = None
		self.destroyButtonIcon = None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.itemSlot = None
		self.lockOverlays = {}
		self.decorationWindow = None
		self.__ClearLogRows()
		self.logScrollBar = None

	def __LoadWindow(self):
		if self.isLoaded:
			return

		## isLoaded must only flip to True once the whole body below has actually
		## succeeded - see the identical note in OfflineShopDecorationWindow above.
		## A failed build used to permanently brick this window: every later F7/Open()
		## would see isLoaded==True and return immediately, forever, with the failure
		## itself never shown to the user (RefreshMe() then crashes silently on the
		## half-built chrome, e.g. a None lockButtonIcon, with no dialog at all).
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/offlineshop/offlineshopwindow.py")

			self.logsWindow = self.GetChild("LogsWindow")
			self.itemSlot = self.GetChild("ItemSlot")
			self.__BuildLockOverlays()

			self.GetChild("board").SetCloseEvent(ui.__mem_func__(self.CloseReal))
			self.GetChild("close_log_button").SAFE_SetEvent(self.OnToggleLogs)

			self.logScrollBar = ui.ScrollBarNew()
			self.logScrollBar.SetParent(self.logsWindow)
			self.logScrollBar.SetPosition(300, 0)
			self.logScrollBar.SetScrollBarSize(256)
			self.logScrollBar.SetScrollEvent(ui.__mem_func__(self.__OnLogScroll))
			self.logScrollBar.Show()

			self.__BuildSolarisChrome()

			self.itemSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.OnSelectItemSlot))
			self.itemSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.OnSelectEmptySlot))
			self.itemSlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.OnUnselectItemSlot))
			self.itemSlot.SetUnselectEmptySlotEvent(ui.__mem_func__(self.OnUnselectEmptySlot))
			self.itemSlot.SetOverInItemEvent(ui.__mem_func__(self.OnOverInItem))
			self.itemSlot.SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutItem))

			self.decorationWindow = OfflineShopDecorationWindow()
			self.logsWindow.Hide()

			self.isLoaded = True
		except:
			import exception
			exception.Abort("OfflineShopWindow.__LoadWindow")

	## ---- Solaris2-reference-style chrome, positions taken directly from the real
	## reference (uishop.py ShopDialog.LoadDialog/Open): a dark title box sitting right
	## above the item grid, a row of 2 dark info boxes (expire/gold) right below it, a
	## full-width "shop value" box below that, and a row of small square icon buttons
	## (lock/+1day/teleport/design/history/destroy) below that - all flat Box/Bar/
	## ImageBox widgets built in Python, exactly like the reference builds its own
	## shopTitleBox/shopExpireBox/shopGoldBox/shopLockButton etc, since this isn't
	## expressible as a uiscript layout. Everything here is owner-only - a guest sees
	## only the item grid, see __ApplyLayoutForRole. ----
	def __BuildSolarisChrome(self):
		DARK_COLOR = 0xFF44423d
		GRID_BOTTOM = 56 + 8 * 32   # ItemSlot y (56) + 8 rows * 32px

		self.titleBox = ui.Box()
		self.titleBox.SetParent(self)
		self.titleBox.SetSize(self.GetWidth() - 44, 19)
		self.titleBox.SetPosition(12, 32)
		self.titleBox.SetColor(DARK_COLOR)
		self.titleBox.Show()

		self.titleBar = ui.Bar()
		self.titleBar.SetParent(self.titleBox)
		self.titleBar.SetSize(self.titleBox.GetWidth() - 1, self.titleBox.GetHeight() - 2)
		self.titleBar.SetPosition(1, 1)
		self.titleBar.AddFlag("not_pick")
		self.titleBar.AddFlag("attach")
		self.titleBar.Show()

		self.titleEdit = ui.EditLine()
		self.titleEdit.SetParent(self.titleBox)
		self.titleEdit.SetPosition(5, 2)
		self.titleEdit.SetSize(self.titleBox.GetWidth() - 10, 16)
		self.titleEdit.SetMax(32)
		self.titleEdit.SetText("")
		self.titleEdit.Show()
		self.nameLine = self.titleEdit

		self.titleEditBtn = ui.Button()
		self.titleEditBtn.SetParent(self)
		self.titleEditBtn.SetPosition(12 + self.titleBox.GetWidth(), 32)
		self.titleEditBtn.SetUpVisual(ROOT_OFFLINESHOP + "edit_btn1.png")
		self.titleEditBtn.SetOverVisual(ROOT_OFFLINESHOP + "edit_btn2.png")
		self.titleEditBtn.SetDownVisual(ROOT_OFFLINESHOP + "edit_btn3.png")
		self.titleEditBtn.SetToolTipText("Apply sign")
		self.titleEditBtn.SetEvent(ui.__mem_func__(self.OnApplyTitle))
		self.titleEditBtn.Show()

		## Time-left / shop revenue (2 equal boxes), then a full-width "shop value"
		## box right below it (sum of every currently-listed item's price) - the
		## watcher count ("1/3") this used to also show wasn't wanted here.
		infoY = GRID_BOTTOM + 5
		infoWidth = (self.GetWidth() - 24 - 4) / 2

		def MakeInfoBox(x, width, initialText, clickEvent = None):
			box = ui.Box()
			box.SetParent(self)
			box.SetSize(width, 19)
			box.SetPosition(x, infoY)
			box.SetColor(DARK_COLOR)
			if clickEvent:
				box.OnMouseLeftButtonDown = clickEvent
			box.Show()

			bar = ui.Bar()
			bar.SetParent(box)
			bar.SetSize(box.GetWidth() - 1, box.GetHeight() - 2)
			bar.SetPosition(1, 1)
			bar.AddFlag("not_pick")
			bar.AddFlag("attach")
			bar.Show()

			text = ui.TextLine()
			text.SetParent(box)
			text.SetPosition(5, box.GetHeight() / 2)
			text.SetVerticalAlignCenter()
			text.AddFlag("not_pick")
			text.SetText(initialText)
			text.Show()
			return box, bar, text

		## bar/box refs kept as self.* attributes for the same reason the icons below
		## are - see the note on MakeIconButton.
		self.expireBox, self.expireBar, self.expireText = MakeInfoBox(12, infoWidth, "-")
		self.goldBox, self.goldBar, self.goldText = MakeInfoBox(12 + infoWidth + 4, infoWidth, "0", ui.__mem_func__(self.OnWithdraw))
		self.moneyText = self.goldText

		self.goldIcon = ui.ImageBox()
		self.goldIcon.SetParent(self.goldBox)
		self.goldIcon.SetPosition(self.goldBox.GetWidth() - 17, 2)
		self.goldIcon.LoadImage("d:/ymir work/ui/game/windows/money_icon.tga")
		self.goldIcon.AddFlag("not_pick")
		self.goldIcon.AddFlag("attach")
		self.goldIcon.Show()

		valueY = infoY + 19 + 5
		self.valueBox, self.valueBar, self.valueText = MakeInfoBox(12, self.GetWidth() - 24, "Shop value: 0 Yang")
		self.valueBox.SetPosition(12, valueY)

		## Where the shop actually is - channel + map + coordinates. There's no
		## map-index -> human place name lookup anywhere in this codebase (server or
		## client), so this shows the raw map index rather than a resolved area name.
		locationY = valueY + 19 + 5
		self.locationBox, self.locationBar, self.locationText = MakeInfoBox(12, self.GetWidth() - 24, "-")
		self.locationBox.SetPosition(12, locationY)

		## Icon-button row: lock / +1 day / teleport-to-my-shop / design / history / destroy.
		BTN_SIZE = 28
		BTN_GAP = 5
		buttonsY = locationY + 19 + 5
		buttonsX = self.GetWidth() - (BTN_SIZE + BTN_GAP) * 6 - 12

		def MakeIconButton(index, iconFile, toolTip, event):
			btn = ui.Button()
			btn.SetParent(self)
			btn.SetPosition(buttonsX + (BTN_SIZE + BTN_GAP) * index, buttonsY)
			btn.SetUpVisual(ROOT_OFFLINESHOP + "offline_btn1.png")
			btn.SetOverVisual(ROOT_OFFLINESHOP + "offline_btn2.png")
			btn.SetDownVisual(ROOT_OFFLINESHOP + "offline_btn3.png")
			btn.SetToolTipText(toolTip)
			btn.SetEvent(event)
			btn.Show()

			icon = ui.ImageBox()
			icon.SetParent(btn)
			icon.SetPosition(6, 6)
			icon.LoadImage(ROOT_OFFLINESHOP + iconFile)
			icon.AddFlag("not_pick")
			icon.AddFlag("attach")
			icon.Show()
			return btn, icon

		## Every returned icon MUST be kept alive via a self.* attribute - ui.Window's
		## __del__ calls wndMgr.Destroy(self.hWnd), so a Python-side icon reference
		## that only lived in a throwaway local (previously "_") gets garbage-collected
		## and destroys the native image the moment this function returns. That is
		## exactly what made 5 of the 6 button icons vanish (only lockButtonIcon, which
		## was already stored on self, survived).
		self.lockButton, self.lockButtonIcon = MakeIconButton(0, "lock.dds", "Lock/unlock sales", ui.__mem_func__(self.OnToggleLock))
		self.plus1DayButton, self.plus1DayButtonIcon = MakeIconButton(1, "plus1.dds", "Extend +1 day", ui.__mem_func__(self.OnAddTime))
		self.teleportButton, self.teleportButtonIcon = MakeIconButton(2, "teleport.dds", "Teleport to my shop", ui.__mem_func__(self.OnTeleportSelf))
		self.designButton, self.designButtonIcon = MakeIconButton(3, "design.dds", "Change decoration", ui.__mem_func__(self.OnOpenDecoration))
		self.historyButton, self.historyButtonIcon = MakeIconButton(4, "history.dds", "Sale log", ui.__mem_func__(self.OnToggleLogs))
		self.destroyButton, self.destroyButtonIcon = MakeIconButton(5, "close.dds", "Destroy shop", ui.__mem_func__(self.OnDestroyShop))

		## Every one of these is owner-only, matching the reference exactly - a guest
		## browsing someone else's shop sees nothing but the item grid (no title, no
		## gold/watcher/expire info, no icon row). Previously the info boxes were shown
		## to guests too as a "helpful" addition, but that wasn't what the reference
		## does and the user explicitly wants it hidden for guests.
		self.ownerChrome = [
			self.titleBox, self.titleEditBtn,
			self.expireBox, self.goldBox, self.valueBox, self.locationBox,
			self.lockButton, self.plus1DayButton, self.teleportButton,
			self.designButton, self.historyButton, self.destroyButton,
		]

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def Open(self):
		self.__LoadWindow()
		(self.xShopStart, self.yShopStart, z) = player.GetMainCharacterPosition()
		self.logShown = False
		self.itemSlot.Show()
		self.logsWindow.Hide()
		self.__ApplyLayoutForRole()
		self.RefreshMe()
		self.SetCenterPosition()
		self.Show()

	## Locked-slot lock icons (pos 40-79) are drawn as plain ImageBox overlays,
	## NOT via ItemSlot's SetCoverButton/EnableCoverButton mechanism - that cover
	## button object is created once and never destroyed, and CSlotWindow::SetSlot
	## unconditionally re-Show()s it on every later SetItemSlot() call regardless
	## of enable state (PythonSlotWindow.cpp), so a slot that was locked and then
	## permanently unlocked would show its last cover-button visual (the generic
	## translucent "disabled" texture) faded on top of whatever item is placed
	## there afterwards. A separate overlay window sidesteps that entirely and is
	## also what belt-inventory's disabled-cell overlay relies on the SAME buggy
	## re-Show() behavior for, so fixing the shared C++ isn't a safe option here.
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

	def __ApplyLayoutForRole(self):
		## Ownership doesn't change while a shop dialog is open, so this only needs to
		## run once per Open() - not on every RefreshMe() (which fires on every item/
		## price/watcher update and would otherwise re-center a window the player just
		## dragged).
		isOwner = offlineShop.IsOwner()
		width = self.GetWidth()
		if isOwner:
			self.itemSlot.SetPosition(12, OWNER_GRID_Y)
			newHeight = OWNER_BOARD_HEIGHT
		else:
			self.itemSlot.SetPosition(12, GUEST_GRID_Y)
			newHeight = GUEST_BOARD_HEIGHT
		self.SetSize(width, newHeight)
		self.GetChild("board").SetSize(width, newHeight)

	def CloseReal(self):
		self.Close()

	def Close(self):
		# Server-side StopShopping() correctly handles both the owner and the guest
		# case (it clears CHARACTER::m_pkOfflineShop either way) - if the owner's
		# client never sends this, the server still thinks they're "inside" their
		# shop and silently refuses AddGuest() on the next F7 press.
		if offlineShop.IsOpen():
			offlineShop.SendStopShopping()
		if self.decorationWindow:
			self.decorationWindow.Close()
		self.OnCloseQuestionDialog()
		self.Hide()

	def OnCloseQuestionDialog(self):
		if self.questionDialog:
			self.questionDialog.Close()
			self.questionDialog = None
		if self.itemBuyQuestionDialog:
			self.itemBuyQuestionDialog.Close()
			self.itemBuyQuestionDialog = None
		if self.priceInputBoard:
			self.priceInputBoard.Close()
			self.priceInputBoard = None

	def RefreshMe(self):
		if not self.isLoaded or not self.IsShow():
			return

		isOwner = offlineShop.IsOwner()

		for widget in self.ownerChrome:
			widget.Show() if isOwner else widget.Hide()

		if isOwner:
			isLocked = (offlineShop.GetSlotFlag() & SHOP_LOCKED_FLAG) != 0
			self.lockButtonIcon.LoadImage(ROOT_OFFLINESHOP + ("lock.dds" if isLocked else "unlock.dds"))
			self.lockButton.SetToolTipText("Unlock sales" if isLocked else "Lock sales")

		totalValue = 0
		for pos in xrange(offlineShop.HOST_ITEM_MAX_NUM):
			vnum = offlineShop.GetItemVnum(pos)

			if vnum != 0:
				totalValue += offlineShop.GetItemPrice(pos)

			if vnum == 0:
				if pos >= 40 and not (offlineShop.GetSlotFlag() & (1 << (pos - 40))):
					self.itemSlot.ClearSlot(pos)
					self.lockOverlays[pos].Show()
				else:
					self.itemSlot.ClearSlot(pos)
					if pos in self.lockOverlays:
						self.lockOverlays[pos].Hide()
				continue

			if pos in self.lockOverlays:
				self.lockOverlays[pos].Hide()
			count = offlineShop.GetItemCount(pos)
			if count <= 1:
				count = 0
			self.itemSlot.SetItemSlot(pos, vnum, count)

		self.itemSlot.RefreshSlot()

		try:
			valueText = localeInfo.NumberToMoneyString(totalValue)
		except:
			valueText = str(totalValue)
		self.valueText.SetText("Shop value: %s Yang" % valueText)

		if isOwner:
			## Static for the shop's lifetime - cheap enough to just re-set every
			## refresh rather than tracking whether it's already been shown once.
			(shopX, shopY) = offlineShop.GetPosition()
			self.locationText.SetText("CH %d, Map #%d (%d, %d)" % (offlineShop.GetChannel(), offlineShop.GetMapIndex(), shopX, shopY))

		if not self.nameLine.IsFocus():
			title = offlineShop.GetTitle()
			self.nameLine.SetText(title[1:] if len(title) > 0 else title)
		try:
			self.moneyText.SetText(localeInfo.NumberToMoneyString(offlineShop.GetPrice()))
		except:
			self.moneyText.SetText(str(offlineShop.GetPrice()))

		if isOwner:
			self.__RefreshLogs()

	def OnUpdate(self):
		if offlineShop.IsOpen() and not offlineShop.IsOwner():
			(x, y, z) = player.GetMainCharacterPosition()
			if abs(x - self.xShopStart) > self.USE_SHOP_LIMIT_RANGE or abs(y - self.yShopStart) > self.USE_SHOP_LIMIT_RANGE:
				self.CloseReal()
				return

		if offlineShop.IsOpen() and app.GetGlobalTime() - self.lastUpdateTime > 1000:
			self.lastUpdateTime = app.GetGlobalTime()
			self.expireText.SetText(localeInfo.SecondToDHM(offlineShop.GetTime() - app.GetGlobalTimeStamp()))

	## ---- guest: click item to buy | owner: click item to pick it up and move it ----
	def OnSelectItemSlot(self, pos):
		if offlineShop.IsOwner():
			if mouseModule.mouseController.isAttached():
				snd.PlaySound("sound/ui/loginfail.wav")
				mouseModule.mouseController.DeattachObject()
				return

			itemID = offlineShop.GetItemID(pos)
			if itemID == 0:
				return
			if offlineShop.GetItemStatus(pos) != 0:
				return

			vnum = offlineShop.GetItemVnum(pos)
			count = offlineShop.GetItemCount(pos)
			mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_OFFLINE_SHOP_ITEM, pos, vnum, count)
			snd.PlaySound("sound/ui/pick.wav")
			return

		itemID = offlineShop.GetItemID(pos)
		if itemID == 0:
			return
		if offlineShop.GetItemStatus(pos) != 0:
			return

		vnum = offlineShop.GetItemVnum(pos)
		count = offlineShop.GetItemCount(pos)
		price = offlineShop.GetItemPrice(pos)
		item.SelectItem(vnum)

		dlg = uiCommon.QuestionDialog2()
		dlg.SetText1(localeInfo.DO_YOU_BUY_ITEM(item.GetItemName(), count, price) if hasattr(localeInfo, "DO_YOU_BUY_ITEM") else "%s x%d - %d yang?" % (item.GetItemName(), count, price))
		dlg.SetText2("")
		dlg.SetAcceptEvent(lambda arg=True: self.AnswerBuyItem(arg))
		dlg.SetCancelEvent(lambda arg=False: self.AnswerBuyItem(arg))
		dlg.Open()
		dlg.pos = pos
		self.itemBuyQuestionDialog = dlg

	def AnswerBuyItem(self, flag):
		if not self.itemBuyQuestionDialog:
			return True
		pos = self.itemBuyQuestionDialog.pos
		if flag:
			itemID = offlineShop.GetItemID(pos)
			if itemID != 0:
				# Buy() server-side keys off the owner's player ID, not the shop NPC's
				# VID - GetOwnerVID() here silently failed every purchase.
				offlineShop.SendBuy(offlineShop.GetOwnerID(), pos, itemID)
		self.itemBuyQuestionDialog.Close()
		self.itemBuyQuestionDialog = None
		return True

	## ---- owner: drop an inventory item onto an empty slot to restock the shop ----
	## (the shop is already open/live at this point, so this goes straight to the
	## server - AddItem() there broadcasts the new slot to every nearby watcher,
	## same as any other shop update.)
	def OnSelectEmptySlot(self, pos):
		if not offlineShop.IsOwner():
			return

		if not mouseModule.mouseController.isAttached():
			return

		if pos >= 40 and not (offlineShop.GetSlotFlag() & (1 << (pos - 40))):
			snd.PlaySound("sound/ui/loginfail.wav")
			mouseModule.mouseController.DeattachObject()
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OFFLINE_SHOP_CANT_SLOT_OPEN if hasattr(localeInfo, "OFFLINE_SHOP_CANT_SLOT_OPEN") else "This slot is locked.")
			return

		attachedSlotType = mouseModule.mouseController.GetAttachedType()
		attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
		mouseModule.mouseController.DeattachObject()

		## Reordering an item already in this shop (picked up via OnSelectItemSlot),
		## as opposed to restocking from inventory below - MoveItem() server-side
		## does the same bSize-aware occupancy check AddItem() does, so this can't
		## overlap a multi-row item's footprint either.
		if app.ENABLE_OFFLINESHOP_SYSTEM and attachedSlotType == player.SLOT_TYPE_OFFLINE_SHOP_ITEM:
			if attachedSlotPos != pos:
				offlineShop.SendMoveItem(attachedSlotPos, pos)
				snd.PlaySound("sound/ui/drop.wav")
			return

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
		priceInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptAddItemPrice))
		priceInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelAddItemPrice))
		priceInputBoard.Open()

		# If this same item is already on sale in this shop, offer its current
		# per-unit price first; otherwise fall back to whatever per-unit price this
		# vnum last sold for anywhere (remembered in UserData/shop/item_prices.txt).
		# Both sources are per-unit, so scale by how many of this item are actually
		# being stocked right now (a stack of 10 at 1000/each suggests 10000).
		newItemCount = player.GetItemCount(attachedInvenType, attachedSlotPos)
		if newItemCount <= 0:
			newItemCount = 1

		suggestedUnitPrice = self.__FindPriceOfItemInShop(itemVNum)
		if suggestedUnitPrice <= 0:
			suggestedUnitPrice = offlineShopItemPrice.GetPrice(itemVNum)
		if suggestedUnitPrice > 0:
			priceInputBoard.SetValue(suggestedUnitPrice * newItemCount)

		# Live server-wide market average (see COfflineShopManager::CheckAveragePrice) -
		# shown via the dialog's own built-in SetAveragePrice (matches the Solaris2
		# reference: grows the board and adds the line in-place) once the reply
		# arrives - see OfflineShopWindow.SetAveragePrice below.

		self.priceInputBoard = priceInputBoard
		self.priceInputBoard.itemVNum = itemVNum
		self.priceInputBoard.sourceWindowType = attachedInvenType
		self.priceInputBoard.sourceSlotPos = attachedSlotPos
		self.priceInputBoard.targetSlotPos = pos
		offlineShop.SendGetAveragePrice(itemVNum)

	# Returns the PER-UNIT price of an already-listed matching stack, not its total.
	def __FindPriceOfItemInShop(self, itemVNum):
		for pos in xrange(offlineShop.HOST_ITEM_MAX_NUM):
			if offlineShop.GetItemVnum(pos) == itemVNum:
				existingCount = offlineShop.GetItemCount(pos)
				if existingCount <= 0:
					existingCount = 1
				return offlineShop.GetItemPrice(pos) / existingCount
		return 0

	def AcceptAddItemPrice(self):
		if not self.priceInputBoard:
			return True

		text = self.priceInputBoard.GetText()
		if text and text.isdigit() and int(text) > 0:
			price = int(text)
			offlineShop.SendAddItem(self.priceInputBoard.targetSlotPos, self.priceInputBoard.sourceWindowType, self.priceInputBoard.sourceSlotPos, price)

			# Remember this as a PER-UNIT price so a differently-sized stack next
			# time still gets a correctly scaled suggestion.
			stockedCount = player.GetItemCount(self.priceInputBoard.sourceWindowType, self.priceInputBoard.sourceSlotPos)
			if stockedCount <= 0:
				stockedCount = 1
			offlineShopItemPrice.SetPrice(self.priceInputBoard.itemVNum, price / stockedCount)

		self.priceInputBoard.Close()
		self.priceInputBoard = None
		return True

	def CancelAddItemPrice(self):
		if self.priceInputBoard:
			self.priceInputBoard.Close()
			self.priceInputBoard = None
		return True

	def SetAveragePrice(self, vnum, price):
		if not self.priceInputBoard or getattr(self.priceInputBoard, "itemVNum", None) != vnum:
			return
		if price > 0:
			self.priceInputBoard.SetAveragePrice(price)

	## ---- owner: right-click filled slot to remove, right-click locked empty slot to unlock ----
	def OnUnselectItemSlot(self, pos):
		if not offlineShop.IsOwner():
			return
		itemID = offlineShop.GetItemID(pos)
		if itemID == 0:
			return

		vnum = offlineShop.GetItemVnum(pos)
		item.SelectItem(vnum)

		dlg = uiCommon.QuestionDialog()
		dlg.SetText("Get back %s?" % item.GetItemName())
		dlg.SetAcceptEvent(ui.__mem_func__(self.AcceptRemoveItem))
		dlg.SetCancelEvent(ui.__mem_func__(self.CancelDialog))
		dlg.Open()
		dlg.pos = pos
		self.questionDialog = dlg

	def OnUnselectEmptySlot(self, pos):
		if not offlineShop.IsOwner() or pos < 40:
			return
		cell = pos - 40
		if offlineShop.GetSlotFlag() & (1 << cell):
			return

		# Shift held = pay gold instead of the usual 2x item 72319 (ExpandSlot vs
		# OpenSlot both just unlock the same slot bit - only the payment differs).
		payWithGold = app.IsPressed(app.DIK_LSHIFT)

		dlg = uiCommon.QuestionDialog()
		if payWithGold:
			try:
				priceText = localeInfo.NumberToMoneyString(offlineShop.SHOP_EXPAND_SLOT_PRICE)
			except:
				priceText = str(offlineShop.SHOP_EXPAND_SLOT_PRICE)
			dlg.SetText("Unlock this slot for %s yang?" % priceText)
		else:
			dlg.SetText("Unlock this slot? (72319 x2, hold Shift to pay gold instead)")
		dlg.SetAcceptEvent(ui.__mem_func__(self.AcceptOpenSlot))
		dlg.SetCancelEvent(ui.__mem_func__(self.CancelDialog))
		dlg.Open()
		dlg.pos = cell
		dlg.payWithGold = payWithGold
		self.questionDialog = dlg

	def AcceptOpenSlot(self):
		if self.questionDialog:
			if getattr(self.questionDialog, "payWithGold", False):
				offlineShop.SendExpandSlot(self.questionDialog.pos)
			else:
				offlineShop.SendOpenSlot(self.questionDialog.pos)
		self.CancelDialog()
		return True

	def AcceptRemoveItem(self):
		if self.questionDialog:
			itemID = offlineShop.GetItemID(self.questionDialog.pos)
			if itemID != 0:
				offlineShop.SendRemoveItem(self.questionDialog.pos, itemID, 0)
		self.CancelDialog()
		return True

	def CancelDialog(self):
		if self.questionDialog:
			self.questionDialog.Close()
			self.questionDialog = None
		return True

	## ---- owner panel buttons ----
	def OnOpenDecoration(self):
		if not offlineShop.IsOwner():
			return
		if self.decorationWindow:
			self.decorationWindow.Open()

	def OnApplyTitle(self):
		if not offlineShop.IsOwner():
			return
		sign = self.nameLine.GetText()
		if not sign or len(sign) == 0:
			return
		offlineShop.SendChangeTitle(sign)

	def OnWithdraw(self):
		if offlineShop.IsOwner() and offlineShop.GetPrice() > 0:
			offlineShop.SendWithdrawMoney()

	def OnAddTime(self):
		offlineShop.SendAddTime()

	def OnToggleLock(self):
		offlineShop.SendToggleLock()

	def OnTeleportSelf(self):
		offlineShop.SendTeleport(player.GetMainCharacterName())

	def OnDestroyShop(self):
		dlg = uiCommon.QuestionDialog()
		dlg.SetText("Destroy this shop?")
		dlg.SetAcceptEvent(lambda arg=True: self.AnswerDestroyShop(arg))
		dlg.SetCancelEvent(lambda arg=False: self.AnswerDestroyShop(arg))
		dlg.Open()
		self.questionDialog = dlg

	def AnswerDestroyShop(self, flag):
		self.CancelDialog()
		if flag:
			offlineShop.SendDestroy()

	def OnToggleLogs(self):
		self.logShown = not self.logShown
		if self.logShown:
			self.itemSlot.Hide()
			self.logsWindow.Show()
			self.__RefreshLogs()
		else:
			self.itemSlot.Show()
			self.logsWindow.Hide()

	def __ClearLogRows(self):
		for row in self.logRows:
			row.Hide()
			row.Destroy()
		self.logRows = []

	def __RefreshLogs(self):
		if not self.logShown:
			return

		self.__ClearLogRows()
		self.logBasePos = 0

		for i in xrange(offlineShop.GetLogCount()):
			buyerName, date, itemVnum, itemCount, price = offlineShop.GetLog(i)
			try:
				priceText = localeInfo.NumberToMoneyString(price)
			except:
				priceText = str(price)

			row = HistoryLogItem(self.logsWindow)
			row.SetData(itemVnum, itemCount, price, date, priceText)
			self.logRows.append(row)

		self.logScrollBar.SetPos(0.0)
		self.__UpdateLogRowVisibility()

	def __OnLogScroll(self):
		viewCount = max(1, 256 / LOG_ROW_HEIGHT)
		rowCount = len(self.logRows)
		scrollLen = max(0, rowCount - viewCount)
		self.logBasePos = int(self.logScrollBar.GetPos() * scrollLen)
		self.__UpdateLogRowVisibility()

	def __UpdateLogRowVisibility(self):
		viewCount = max(1, 256 / LOG_ROW_HEIGHT)
		rowCount = len(self.logRows)

		for i, row in enumerate(self.logRows):
			if self.logBasePos <= i < self.logBasePos + viewCount:
				row.SetPosition(0, (i - self.logBasePos) * LOG_ROW_HEIGHT)
				row.Show()
			else:
				row.Hide()

		if viewCount < rowCount:
			self.logScrollBar.SetMiddleBarSize(float(viewCount) / rowCount)
			self.logScrollBar.Show()
		else:
			self.logScrollBar.Hide()

	def OnOverInItem(self, slotIndex):
		if self.tooltipItem:
			self.tooltipItem.SetOfflineShopItem(slotIndex)

	def OnOverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OnOfflineShopReturn(self, subheader):
		chat.AppendChat(chat.CHAT_TYPE_INFO, "OfflineShop: return code %d" % subheader)

	def OnPressEscapeKey(self):
		self.CloseReal()
		return True
