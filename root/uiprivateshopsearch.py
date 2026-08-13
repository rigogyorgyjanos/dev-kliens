import app
import ui
import item
import chat
import localeInfo
import uiCommon
import constInfo
import privateShopSearch
import offlineShop
import wndMgr
from _weakref import proxy

## Solaris2-reference asset folder (ui/search/*) - copied into this project's own
## ETC/ymir work/ui/search/ tree. The whole window below is rebuilt around the
## reference's flat-box layout (SearchBox/MenuBox/ResultBox/PaginationBox, see
## uiscript/offlineshop/privateshopsearchdialog.py) instead of the old private_*
## textured skin, matching what the reference client actually looks like.
IMG_DIR = "d:/ymir work/ui/search/"

## (label, searchType, searchSubType, iconName) - searchSubType -1 means "any subtype".
## Mapped onto THIS project's own GetItemCategory() numbering (server-src/server/game/
## src/offlineshop_search_manager.cpp), not the reference server's - sash/aura/pet/
## accessory/chest categories from the reference have no real backing category here
## (CheckFilter never classifies anything into them), so showing them would be a
## filter that silently matches nothing. Only real, working categories are listed.
CATEGORY_LIST = (
	("All", -1, -1, None),
	("Weapon", 1, -1, "sword"),
	("Armor", 2, -1, "helmet"),
	("Dragon Soul / Alchemy", 3, -1, "gem"),
	("Costumes", 4, -1, "shirt"),
	("Books", 7, -1, "scroll"),
	("Mount / Pets", 10, -1, "horse"),
)

## Subtype rows shown under a category once expanded - (subType, label) - taken
## directly from COfflineShopManager::GetItemCategory()'s actual return values for
## that searchType, not guessed.
CATEGORY_SUBTYPES = {
	1 : (  # weapon
		(0, "Sword"), (1, "Two-Handed"), (2, "Dagger"),
		(3, "Bow"), (4, "Bell"), (5, "Fan"),
	),
	2 : (  # armor
		(0, "Body"), (1, "Shield"), (2, "Ear"), (3, "Neck"),
		(4, "Wrist"), (5, "Feet"), (7, "Head"),
	),
	4 : (  # costume
		(0, "Body"), (1, "Hair"), (2, "Weapon: Sword"), (3, "Weapon: 2H"),
		(4, "Weapon: Fan"), (5, "Weapon: Bell"), (6, "Weapon: Dagger"), (7, "Weapon: Bow"),
	),
}

CHARACTER_ITEMS = {
	0 : "Any class",
	1 : "Warrior",
	2 : "Ninja",
	4 : "Sura",
	3 : "Shaman",
}
## race^warrior^ninja^sura^shaman$ wire order - the already-working race[] slot order
## used by the "race" command segment.
CHARACTER_TO_RACE_INDEX = { 1 : 0, 2 : 1, 4 : 2, 3 : 3 }

SEX_ITEMS = {
	0 : "Any sex",
	1 : "Male",
	2 : "Female",
}

ALCHEMY_ITEMS = {
	0 : "Any alchemy",
	1 : "Clear",
	2 : "Flawless",
	3 : "Brilliant",
	4 : "Excellent",
	5 : "Perfect",
}

## COfflineShopManager::CheckFilter's costumeList[4] = {COSTUME_BODY, COSTUME_WEAPON,
## COSTUME_HAIR, COSTUME_MOUNT}, indexed by filter.costumeType - 1 - this codebase's
## costume system has no accessory/pet/skin variants beyond these four.
COSTUME_TYPE_ITEMS = {
	0 : "Any costume",
	1 : "Body",
	2 : "Weapon",
	3 : "Hair",
	4 : "Mount",
}

## Verified APPLY_* numeric values (server-src/server/common/length.h) - a deliberately
## small, confirmed-correct subset rather than a guessed exhaustive list, since a wrong
## bType value would silently match nothing instead of erroring.
ATTR_TYPE_ITEMS = {
	0  : "Any bonus",
	1  : "Max HP",
	7  : "Attack speed",
	8  : "Move speed",
	15 : "Critical %",
	16 : "Penetrate %",
	69 : "Max HP %",
}
ATTR_TYPE_ORDER = (0, 1, 7, 8, 15, 16, 69)
ATTR_FILTER_ROW_COUNT = 3

SUGGEST_ROW_HEIGHT = 20
SUGGEST_MAX_ROWS = 8

## MenuBox/ResultBox/PaginationBox sizes, mirrored from the uiscript layout (kept in
## sync by hand - see BOARD_WIDTH/HEIGHT there).
MENU_WIDTH = 170
MENU_HEIGHT = 365
RESULT_WIDTH = 435
RESULT_HEIGHT = 445
RESULT_ICON_SIZE = 32
PAGINATION_HEIGHT = 30

## ResultBox is 445px tall on paper (uiscript: y=35, height=445 -> bottom at
## absolute y=480), but PaginationBox starts at absolute y=455 (uiscript:
## BOARD_HEIGHT-35-30) and renders after it - the two boxes deliberately overlap
## by 25px, with PaginationBox's own background painting over that band. Content
## has to stay within the non-overlapping part (455-35=420) or it visibly hangs
## into the Buy Selected bar.
RESULT_USABLE_HEIGHT = 420
## Same overlap, worse: MenuBox (uiscript: y=120, height=365 -> bottom at
## absolute y=485) overlaps PaginationBox (starts at 455) by 30px, not 25 -
## MenuBox sits one row taller than ResultBox but PaginationBox's top is fixed.
MENU_USABLE_HEIGHT = 335

MENU_ROW_HEIGHT = 27
SUBTYPE_ROW_HEIGHT = 22

COLOR_SELLER_ONLINE = 0xff40ff40
COLOR_SELLER_OFFLINE = 0xffaaaaaa
COLOR_DISABLED_TEXT = 0xAA999999


## ---- one row of the left-hand category tree: a menu1/2/3.png button + a small
## category icon, optionally with an expand arrow; subtype rows use submenu1/2/3.png
## and a tree_connect/tree_end connector graphic to their left - built directly in
## Python (not via a generic tree widget) since we need exact reference styling. ----
class CategoryRow(ui.ToggleButton):
	def __init__(self, parent, text, width, height, isSubType=False, isLast=False):
		ui.ToggleButton.__init__(self)
		self.SetParent(parent)
		## Size must be set before SetText()/icon placement below - both read back
		## self.GetWidth()/GetHeight(), which default to 0 until SetSize() runs.
		self.SetSize(width, height)
		if isSubType:
			self.SetUpVisual(IMG_DIR + "submenu1.png")
			self.SetOverVisual(IMG_DIR + "submenu2.png")
			self.SetDownVisual(IMG_DIR + "submenu3.png")
		else:
			self.SetUpVisual(IMG_DIR + "menu1.png")
			self.SetOverVisual(IMG_DIR + "menu2.png")
			self.SetDownVisual(IMG_DIR + "menu3.png")
		self.SetText(text)
		self.ButtonText.SetHorizontalAlignLeft()
		self.ButtonText.SetPosition(30 if not isSubType else 20, self.GetHeight() / 2 - self.ButtonText.GetHeight() / 2)
		self.Show()

		self.icon = None
		self.arrow = None
		self.connector = None
		if isSubType:
			self.connector = ui.ExpandedImageBox()
			self.connector.LoadImage(IMG_DIR + ("tree_end.png" if isLast else "tree_connect.png"))
			self.connector.SetParent(self)
			self.connector.AddFlag("not_pick")
			self.connector.SetPosition(-15, 0)
			self.connector.Show()

	def SetIcon(self, iconName):
		## Category icons were only copied over as .dds (sword.dds, helmet.dds, etc) -
		## there are no .png versions of these, unlike arrow/tree_connect/tree_end which
		## have both. Loading ".png" here silently fails and leaves the row iconless.
		self.icon = ui.ExpandedImageBox()
		self.icon.LoadImage(IMG_DIR + "%s.dds" % iconName)
		self.icon.SetParent(self)
		self.icon.AddFlag("not_pick")
		self.icon.SetPosition(8, self.GetHeight() / 2 - self.icon.GetHeight() / 2)
		self.icon.Show()

	def SetArrow(self):
		self.arrow = ui.ExpandedImageBox()
		self.arrow.LoadImage(IMG_DIR + "arrow.png")
		self.arrow.SetParent(self)
		self.arrow.AddFlag("not_pick")
		self.arrow.SetAlpha(0.65)
		self.arrow.SetPosition(self.GetWidth() - self.arrow.GetWidth() - 6, self.GetHeight() / 2 - self.arrow.GetHeight() / 2)
		self.arrow.Show()

	def Destroy(self):
		self.icon = None
		self.arrow = None
		self.connector = None
		self.Hide()


## One result row: item slot (icon w/ its own grade border) + name/price/seller +
## teleport/whisper/select controls, on a stretchable ToggleButton background so the
## reference's slot32/64/96.png assets (native 430px wide, 36/68/100px tall) actually
## fill the row instead of rendering at their raw texture size the way a plain
## ui.ImageBox would - this is what made icons/text look "messed up" before: the old
## ui.ImageBox background never matched the row's real bounds. Row height now follows
## item.GetItemSize() like the reference's ItemLine does, so 2-3 slot weapons/armor get
## a taller row instead of being squeezed into a fixed 46px slot.
class SearchResultRow(ui.ToggleButton):
	TELEPORT_COLUMN_WIDTH = 26

	def __init__(self, parent, rowWidth):
		ui.ToggleButton.__init__(self)
		self.SetParent(parent)
		self.rowWidth = rowWidth
		self.checkCallback = None

	def Build(self, vnum, count, name, seller, priceText, isOnline=False):
		item.SelectItem(vnum)
		(_, height) = item.GetItemSize()
		height = max(1, min(3, height))
		pixelHeight = RESULT_ICON_SIZE * height
		rowHeight = pixelHeight + 4

		self.SetSize(self.rowWidth, rowHeight)
		self.SetUpVisual(IMG_DIR + "slot%d.png" % pixelHeight)
		self.SetOverVisual(IMG_DIR + "slot%d_hover.png" % pixelHeight)
		self.SetDownVisual(IMG_DIR + "slot%d_hover.png" % pixelHeight)
		self.SetDisableVisual(IMG_DIR + "slot%d_sold.png" % pixelHeight)

		self.checkBox = ui.CheckBox()
		self.checkBox.SetParent(self)
		self.checkBox.SetPosition(6, rowHeight / 2 - 8)
		self.checkBox.Show()

		## The row itself is a ToggleButton, so clicking anywhere on it (outside the
		## checkbox's own small hit area) already toggles its Up/Down visual - that
		## used to be a silent no-op, which is exactly the reported bug: the
		## background visibly recolors on click, but the actual selection (the
		## checkbox glyph + selectedIndices) never changes unless the player hits the
		## checkbox pixel-perfectly. Mirror the row's own toggle into the checkbox so
		## the whole row is one consistent, correctly-sized click target.
		self.SetToggleDownEvent(ui.__mem_func__(self.__OnRowToggle), True)
		self.SetToggleUpEvent(ui.__mem_func__(self.__OnRowToggle), False)

		self.iconSlot = ui.GridSlotWindow()
		self.iconSlot.SetParent(self)
		self.iconSlot.ArrangeSlot(0, 1, height, RESULT_ICON_SIZE, RESULT_ICON_SIZE, 0, 0)
		self.iconSlot.SetPosition(28, 2)
		self.iconSlot.SetItemSlot(0, vnum, count if count > 1 else 0)
		self.iconSlot.EnableSlot(0)
		self.iconSlot.Show()

		## not_pick on the pure-display text so clicks over the name/price fall
		## through to the row's own ToggleButton instead of being swallowed by a
		## TextLine that has nothing bound to it.
		self.nameText = ui.TextLine()
		self.nameText.SetParent(self)
		self.nameText.AddFlag("not_pick")
		self.nameText.SetPosition(28 + RESULT_ICON_SIZE + 6, rowHeight / 2 - 12)
		self.nameText.SetHorizontalAlignLeft()
		self.nameText.SetText(name)
		self.nameText.Show()

		self.priceText = ui.TextLine()
		self.priceText.SetParent(self)
		self.priceText.AddFlag("not_pick")
		self.priceText.SetPosition(28 + RESULT_ICON_SIZE + 6, rowHeight / 2 + 1)
		self.priceText.SetHorizontalAlignLeft()
		self.priceText.SetText(priceText)
		self.priceText.Show()

		self.priceIcon = ui.ImageBox()
		self.priceIcon.SetParent(self)
		self.priceIcon.AddFlag("not_pick")
		self.priceIcon.LoadImage("d:/ymir work/ui/game/windows/money_icon.tga")
		(priceTextWidth, _) = self.priceText.GetTextSize()
		self.priceIcon.SetPosition(28 + RESULT_ICON_SIZE + 6 + priceTextWidth + 4, rowHeight / 2 - 1)
		self.priceIcon.Show()

		teleportX = self.rowWidth - 10 - self.TELEPORT_COLUMN_WIDTH
		self.teleportButton = ui.Button()
		self.teleportButton.SetParent(self)
		self.teleportButton.SetPosition(teleportX, rowHeight / 2 - 10)
		self.teleportButton.SetUpVisual("d:/ymir work/ui/offlineshop/teleport.dds")
		self.teleportButton.SetToolTipText("Teleport to seller")
		self.teleportButton.Show()

		self.sellerText = ui.TextLine()
		self.sellerText.SetParent(self)
		self.sellerText.AddFlag("not_pick")
		self.sellerText.SetPosition(teleportX - 8, rowHeight / 2 - 6)
		self.sellerText.SetHorizontalAlignRight()
		self.sellerText.SetPackedFontColor(COLOR_SELLER_ONLINE if isOnline else COLOR_SELLER_OFFLINE)
		self.sellerText.SetText(seller)
		self.sellerText.Show()

		(sellerTextWidth, _) = self.sellerText.GetTextSize()
		self.envelopeIcon = ui.ImageBox()
		self.envelopeIcon.SetParent(self)
		self.envelopeIcon.LoadImage(IMG_DIR + "envelope.png")
		self.envelopeIcon.SetPosition(teleportX - 8 - sellerTextWidth - 20, rowHeight / 2 - 6)
		if isOnline:
			self.envelopeIcon.Show()
		else:
			self.envelopeIcon.Hide()

	def __del__(self):
		ui.ToggleButton.__del__(self)

	def Destroy(self):
		self.checkBox = None
		self.iconSlot = None
		self.nameText = None
		self.sellerText = None
		self.priceIcon = None
		self.priceText = None
		self.teleportButton = None
		self.envelopeIcon = None
		self.checkCallback = None
		ui.ToggleButton.Destroy(self)

	def SetToolTip(self, tooltipItem, idx):
		if not tooltipItem:
			return
		self.iconSlot.SetOverInItemEvent(lambda slot, argTip=tooltipItem, argIdx=idx: argTip.SetPrivateShopSearchItem(argIdx))
		self.iconSlot.SetOverOutItemEvent(lambda argTip=tooltipItem: argTip.HideToolTip())

	def __OnRowToggle(self, isChecked):
		self.checkBox.SetCheckStatus(isChecked)
		if self.checkCallback:
			self.checkCallback("ON_CHECK" if isChecked else "ON_UNCKECK", isChecked)

	def SetEvents(self, onBuy, onTeleport, onWhisper, onCheckToggle):
		self.iconSlot.SetSelectItemSlotEvent(onBuy)
		self.teleportButton.SetEvent(onTeleport)
		self.envelopeIcon.OnMouseLeftButtonDown = onWhisper
		self.checkBox.SetEvent(onCheckToggle, "ON_CHECK", True)
		self.checkBox.SetEvent(onCheckToggle, "ON_UNCKECK", False)
		self.checkCallback = onCheckToggle

	def SetChecked(self, checked):
		self.checkBox.SetCheckStatus(checked)


class PrivateShopSearchWindow(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.isLoaded = False
		self.searchEdit = None
		self.resultRows = []
		self.resultScrollBar = None
		self.categoryRows = []
		self.categoryBasePos = 0
		self.categoryScrollBar = None
		self.categoryType = -1
		self.categorySubType = -1
		self.expandedCategory = None
		self.characterValue = 0
		self.sexValue = 0
		self.alchemyValue = 0
		self.costumeValue = 0
		self.attrChoices = [0] * ATTR_FILTER_ROW_COUNT
		self.attrValueEdits = []
		self.attrChooses = []
		self.characterChoose = None
		self.sexChoose = None
		self.alchemyChoose = None
		self.costumeChoose = None
		self.filterWidgets = []
		self.filterShown = False
		self.checkBoxes = {}
		self.pageButtons = []
		self.resultCountText = None
		self.suggestFrame = None
		self.suggestListBox = None
		self.buyQuestionDialog = None
		self.flags = { "seller" : False, "exact" : False, "timelimited" : False }
		self.selectedIndices = set()
		self.tooltipItem = None
		self.resultTotalHeight = 0

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def Destroy(self):
		self.searchEdit = None
		self.__ClearResultRows()
		self.__ClearCategoryRows()
		self.resultViewport = None
		self.resultScrollBar = None
		self.categoryScrollBar = None
		self.characterChoose = None
		self.sexChoose = None
		self.alchemyChoose = None
		self.costumeChoose = None
		self.attrChooses = []
		self.attrValueEdits = []
		self.checkBoxes = {}
		self.pageButtons = []
		self.suggestFrame = None
		self.suggestListBox = None

	def __LoadWindow(self):
		if self.isLoaded:
			return

		try:
			self.__BuildWindow()
			self.isLoaded = True
		except:
			import exception
			exception.Abort("PrivateShopSearchWindow.__LoadWindow")

	def __BuildWindow(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/offlineshop/privateshopsearchdialog.py")

		self.searchEdit = self.GetChild("InputName")
		self.searchBox = self.GetChild("SearchBox")
		self.menuBox = self.GetChild("MenuBox")
		self.resultBox = self.GetChild("ResultBox")
		self.paginationBox = self.GetChild("PaginationBox")

		## Plain "board" (Board class) has no built-in close button - only
		## BoardWithTitleBar does. Our uiscript uses a separate "titlebar" child
		## instead, which owns the actual close button (see TitleBar.SetCloseEvent).
		self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
		self.GetChild("SearchButton").SAFE_SetEvent(self.OnSearch)
		self.GetChild("FilterButton").SetToggleDownEvent(ui.__mem_func__(self.OnToggleFilter), True)
		self.GetChild("FilterButton").SetToggleUpEvent(ui.__mem_func__(self.OnToggleFilter), False)
		self.GetChild("ClearFilterButton").SAFE_SetEvent(self.OnClearFilters)
		self.GetChild("BuySelectedButton").SAFE_SetEvent(self.OnBuySelected)

		## Not declared in the uiscript as "checkbox2" - the script loader (ui.py
		## PythonScriptLoader) has no handler for that type, only a plain, non-loader-
		## registered ui.CheckBox exists - so these are always-visible Python-built
		## checkboxes parented straight onto SearchBox, matching the reference's
		## placement right under the name field.
		self.exactCheckBox = self.__MakeCheckBox(self.searchBox, 5, 30, "Exact", "exact")
		self.exactCheckBox.Show()
		self.sellerCheckBox = self.__MakeCheckBox(self.searchBox, 92, 30, "Seller name", "seller")
		self.sellerCheckBox.Show()

		self.searchEdit.SetReturnEvent(ui.__mem_func__(self.OnSearch))
		originalOnIMEUpdate = self.searchEdit.OnIMEUpdate
		def OnNameTextChanged(argSelf = proxy(self), original = originalOnIMEUpdate):
			original()
			argSelf.__RefreshSuggestions()
		self.searchEdit.OnIMEUpdate = OnNameTextChanged

		tooltipButton = self.GetChild("TooltipButton")
		tooltipButton.SetToolTipText(
			"Search offline shops across every channel.\n"
			"Type a name, or use the category tree / filter panel.\n"
			"Click the envelope to whisper an online seller.\n"
			"Tick rows and use Buy Selected for several at once."
		)

		self.resultScrollBar = ui.ScrollBarNew()
		self.resultScrollBar.SetParent(self.resultBox)
		self.resultScrollBar.SetScrollBarSize(RESULT_USABLE_HEIGHT)
		self.resultScrollBar.SetScrollEvent(ui.__mem_func__(self.__OnResultScroll))
		## Row width used to be RESULT_WIDTH - 10, which physically overlapped the
		## scrollbar's own column (it sits at RESULT_WIDTH - 12) - rows were newer
		## children than the scrollbar, so they rendered on top of it and ate its
		## clicks, making it undraggable. Measure the scrollbar's real width (from
		## its actual asset, not a guess) and size rows to stop a few px short of it.
		scrollbarWidth = self.resultScrollBar.GetWidth()
		self.resultScrollBar.SetPosition(RESULT_WIDTH - scrollbarWidth - 3, 5)
		self.resultScrollBar.Show()
		self.resultRowWidth = RESULT_WIDTH - scrollbarWidth - 3 - 5 - 3

		## Rows are parented to this dedicated viewport - NOT resultBox directly -
		## sized to RESULT_USABLE_HEIGHT, the exact same bound __UpdateRowVisibility
		## uses to decide what's on screen, so there's no mismatch between "what we
		## think is visible" and "what's actually cropped".
		##
		## Uses EnableScissorRect(), not SetClippingMaskWindow(): the latter has to
		## be individually patched into every widget type's own OnRender (image,
		## text, button, slot window, ...), and it turns out the row's own
		## ToggleButton background visual was never covered by that - it kept
		## rendering full-size regardless of the mask. EnableScissorRect is a real
		## D3D scissor test around this window's entire render + all its children's
		## render, so it clips literally everything inside it in one shot, and only
		## needs to be turned on once - not reapplied every time rows are rebuilt.
		##
		## Width stops exactly at the scrollbar's own column instead of spanning the
		## full ResultBox: even though individual rows are already narrower than
		## that, the viewport WINDOW ITSELF was still RESULT_WIDTH wide, and being a
		## newer sibling than the scrollbar (created after it, further down this
		## function) it won pick/render priority over the scrollbar's whole column -
		## an empty window still blocks clicks within its own bounds even where it
		## draws nothing, which is exactly why the scrollbar was only reachable in
		## the 3px gaps between rows.
		self.resultViewport = ui.Window()
		self.resultViewport.SetParent(self.resultBox)
		self.resultViewport.SetSize(RESULT_WIDTH - scrollbarWidth - 3, RESULT_USABLE_HEIGHT)
		self.resultViewport.SetPosition(0, 0)
		self.resultViewport.EnableScissorRect()
		self.resultViewport.Show()

		## Belt-and-suspenders: force the scrollbar to the front of resultBox's
		## sibling order so it always wins picking even if some future child ends up
		## overlapping its column again.
		self.resultScrollBar.SetTop()

		self.resultCountText = ui.TextLine()
		self.resultCountText.SetParent(self.paginationBox)
		self.resultCountText.SetPosition(5, PAGINATION_HEIGHT / 2)
		self.resultCountText.SetVerticalAlignCenter()
		self.resultCountText.SetHorizontalAlignRight()
		self.resultCountText.Show()

		self.categoryScrollBar = ui.ScrollBarNew()
		self.categoryScrollBar.SetParent(self.menuBox)
		self.categoryScrollBar.SetScrollBarSize(MENU_USABLE_HEIGHT)
		self.categoryScrollBar.SetScrollEvent(ui.__mem_func__(self.__OnCategoryScroll))
		categoryScrollbarWidth = self.categoryScrollBar.GetWidth()
		self.categoryScrollBar.SetPosition(MENU_WIDTH - categoryScrollbarWidth - 3, 5)
		self.categoryScrollBar.Show()

		## Same fixed-size scissor-rect viewport as resultViewport, stopping short of
		## the scrollbar's own column for the same reason (an empty window still
		## blocks clicks within its bounds, even where nothing is drawn there).
		self.categoryViewport = ui.Window()
		self.categoryViewport.SetParent(self.menuBox)
		self.categoryViewport.SetSize(MENU_WIDTH - categoryScrollbarWidth - 3, MENU_USABLE_HEIGHT)
		self.categoryViewport.SetPosition(0, 0)
		self.categoryViewport.EnableScissorRect()
		self.categoryViewport.Show()

		self.categoryScrollBar.SetTop()

		self.__BuildFilterPanel()
		self.__RebuildCategoryTree()
		self.__ShowCategoryTree()

	## ---- category tree: menu1/2/3.png rows w/ icons, expandable into submenu1/2/3.png
	## rows connected by tree_connect/tree_end graphics - exactly the reference's shape,
	## built/scrolled the same way our own result list already is (no engine-level
	## SetInsideRender/ModernScrollBar available here, so plain show/hide by index). ----
	def __ClearCategoryRows(self):
		for row in self.categoryRows:
			row.Hide()
			row.Destroy()
		self.categoryRows = []

	def __RebuildCategoryTree(self):
		self.__ClearCategoryRows()
		y = 5
		for (text, searchType, searchSubType, iconName) in CATEGORY_LIST:
			row = CategoryRow(self.categoryViewport, text, MENU_WIDTH - 20, MENU_ROW_HEIGHT)
			if iconName:
				row.SetIcon(iconName)
			hasSubTypes = searchType in CATEGORY_SUBTYPES
			if hasSubTypes:
				row.SetArrow()
			if searchType == self.expandedCategory:
				row.Down()
			row.SetToggleDownEvent(ui.__mem_func__(self.__OnClickCategory), searchType, searchSubType, hasSubTypes)
			row.SetToggleUpEvent(ui.__mem_func__(self.__OnClickCategory), searchType, searchSubType, hasSubTypes)
			row.treeX = 5
			row.treeY = y
			self.categoryRows.append(row)
			y += MENU_ROW_HEIGHT + 2

			if searchType == self.expandedCategory and hasSubTypes:
				subTypes = CATEGORY_SUBTYPES[searchType]
				for i, (subType, subLabel) in enumerate(subTypes):
					subRow = CategoryRow(self.categoryViewport, subLabel, MENU_WIDTH - 35, SUBTYPE_ROW_HEIGHT, isSubType=True, isLast=(i == len(subTypes) - 1))
					if searchType == self.categoryType and subType == self.categorySubType:
						subRow.Down()
					subRow.SetToggleDownEvent(ui.__mem_func__(self.__OnClickSubCategory), searchType, subType)
					subRow.SetToggleUpEvent(ui.__mem_func__(self.__OnClickSubCategory), searchType, subType)
					subRow.treeX = 20
					subRow.treeY = y
					self.categoryRows.append(subRow)
					y += SUBTYPE_ROW_HEIGHT + 2

		self.categoryTotalHeight = y
		self.categoryScrollBar.SetPos(0.0)
		## categoryViewport's scissor rect was already turned on once in __BuildWindow.
		self.__ApplyCategoryScroll()

	def __OnClickCategory(self, searchType, searchSubType, hasSubTypes):
		if hasSubTypes:
			self.expandedCategory = None if self.expandedCategory == searchType else searchType
			self.__RebuildCategoryTree()
			if self.expandedCategory != searchType:
				return
		self.categoryType = searchType
		self.categorySubType = searchSubType
		self.OnSearch()

	def __OnClickSubCategory(self, searchType, subType):
		self.categoryType = searchType
		self.categorySubType = subType
		self.__RebuildCategoryTree()
		self.OnSearch()

	def __OnCategoryScroll(self):
		self.__ApplyCategoryScroll()

	def __ApplyCategoryScroll(self):
		viewHeight = MENU_USABLE_HEIGHT
		scrollLen = max(0, self.categoryTotalHeight - viewHeight)
		offset = int(self.categoryScrollBar.GetPos() * scrollLen) if scrollLen > 0 else 0

		for row in self.categoryRows:
			posY = row.treeY - offset
			if -MENU_ROW_HEIGHT <= posY <= viewHeight:
				row.SetPosition(row.treeX, posY)
				row.Show()
			else:
				row.Hide()

		if scrollLen > 0:
			self.categoryScrollBar.SetMiddleBarSize(float(viewHeight) / self.categoryTotalHeight)
			self.categoryScrollBar.Show()
		else:
			self.categoryScrollBar.Hide()

	def __ShowCategoryTree(self):
		self.__ApplyCategoryScroll()
		self.categoryScrollBar.Show()
		for w in self.filterWidgets:
			w.Hide()

	def __ShowFilterPanel(self):
		for row in self.categoryRows:
			row.Hide()
		self.categoryScrollBar.Hide()
		for w in self.filterWidgets:
			w.Show()

	## ---- filter panel: our existing richer filter set (character/sex/alchemy/
	## costume/attr rows/min-max fields), reparented into MenuBox so it swaps with the
	## category tree in the same space, exactly like the reference's filterButton
	## toggling MenuBox between the type tree and the filter list. ----
	def __BuildFilterPanel(self):
		y = [5]
		def NextY(height):
			cur = y[0]
			y[0] += height + 6
			return cur

		## Exact/seller-name checkboxes live in SearchBox (always visible, built in
		## __BuildWindow) - not duplicated here, only filter-panel-exclusive toggles go
		## in this panel.
		self.checkBoxes = {}
		self.checkBoxes["timelimited"] = self.__MakeCheckBox(self.menuBox, 5, NextY(20), "Time-limited only", "timelimited")

		self.characterChoose = ui.ComboBoxImage(self.menuBox, "d:/ymir work/ui/game/privatesearch/class_image2.tga", 5, NextY(29), MENU_WIDTH - 25, 29)
		self.characterChoose.SetCurrentItem(CHARACTER_ITEMS[0])
		for index, text in CHARACTER_ITEMS.items():
			self.characterChoose.InsertItem(index, text)
		self.characterChoose.SetEvent(lambda idx, argSelf=proxy(self): argSelf.OnSelectCharacter(idx))
		self.characterChoose.SetOpenEvent(lambda argSelf=proxy(self): argSelf._PrivateShopSearchWindow__CloseOtherCombos("character"))

		self.sexChoose = ui.ComboBoxImage(self.menuBox, "d:/ymir work/ui/game/privatesearch/class_image2.tga", 5, NextY(29), MENU_WIDTH - 25, 29)
		self.sexChoose.SetCurrentItem(SEX_ITEMS[0])
		for index, text in SEX_ITEMS.items():
			self.sexChoose.InsertItem(index, text)
		self.sexChoose.SetEvent(lambda idx, argSelf=proxy(self): argSelf.OnSelectSex(idx))
		self.sexChoose.SetOpenEvent(lambda argSelf=proxy(self): argSelf._PrivateShopSearchWindow__CloseOtherCombos("sex"))

		self.alchemyChoose = ui.ComboBoxImage(self.menuBox, "d:/ymir work/ui/game/privatesearch/class_image2.tga", 5, NextY(29), MENU_WIDTH - 25, 29)
		self.alchemyChoose.SetCurrentItem(ALCHEMY_ITEMS[0])
		for index, text in ALCHEMY_ITEMS.items():
			self.alchemyChoose.InsertItem(index, text)
		self.alchemyChoose.SetEvent(lambda idx, argSelf=proxy(self): argSelf.OnSelectAlchemy(idx))
		self.alchemyChoose.SetOpenEvent(lambda argSelf=proxy(self): argSelf._PrivateShopSearchWindow__CloseOtherCombos("alchemy"))

		self.costumeChoose = ui.ComboBoxImage(self.menuBox, "d:/ymir work/ui/game/privatesearch/class_image2.tga", 5, NextY(29), MENU_WIDTH - 25, 29)
		self.costumeChoose.SetCurrentItem(COSTUME_TYPE_ITEMS[0])
		for index, text in COSTUME_TYPE_ITEMS.items():
			self.costumeChoose.InsertItem(index, text)
		self.costumeChoose.SetEvent(lambda idx, argSelf=proxy(self): argSelf.OnSelectCostume(idx))
		self.costumeChoose.SetOpenEvent(lambda argSelf=proxy(self): argSelf._PrivateShopSearchWindow__CloseOtherCombos("costume"))

		refineLabel = ui.TextLine()
		refineLabel.SetParent(self.menuBox)
		refineLabel.SetPosition(5, NextY(14))
		refineLabel.SetText("Refine min/max")
		refineLabel.Show()
		rowY = NextY(20)
		self.minRefineEdit = self.__MakeNumberEdit(5, rowY, 70)
		self.maxRefineEdit = self.__MakeNumberEdit(80, rowY, 70)

		levelLabel = ui.TextLine()
		levelLabel.SetParent(self.menuBox)
		levelLabel.SetPosition(5, NextY(14))
		levelLabel.SetText("Level min/max")
		levelLabel.Show()
		rowY = NextY(20)
		self.minLevelEdit = self.__MakeNumberEdit(5, rowY, 70)
		self.maxLevelEdit = self.__MakeNumberEdit(80, rowY, 70)

		countLabel = ui.TextLine()
		countLabel.SetParent(self.menuBox)
		countLabel.SetPosition(5, NextY(14))
		countLabel.SetText("Count min/max")
		countLabel.Show()
		rowY = NextY(20)
		self.minCountEdit = self.__MakeNumberEdit(5, rowY, 70)
		self.maxCountEdit = self.__MakeNumberEdit(80, rowY, 70)

		avgLabel = ui.TextLine()
		avgLabel.SetParent(self.menuBox)
		avgLabel.SetPosition(5, NextY(14))
		avgLabel.SetText("Min normal/skill dmg bonus %")
		avgLabel.Show()
		rowY = NextY(20)
		self.minAverageEdit = self.__MakeNumberEdit(5, rowY, 70)
		self.minSkillEdit = self.__MakeNumberEdit(80, rowY, 70)

		attrLabel = ui.TextLine()
		attrLabel.SetParent(self.menuBox)
		attrLabel.SetPosition(5, NextY(14))
		attrLabel.SetText("Bonus filters")
		attrLabel.Show()

		for row in xrange(ATTR_FILTER_ROW_COUNT):
			rowY = NextY(29)
			attrChoose = ui.ComboBoxImage(self.menuBox, "d:/ymir work/ui/game/privatesearch/class_image2.tga", 5, rowY, 100, 29)
			attrChoose.SetCurrentItem(ATTR_TYPE_ITEMS[0])
			for typeValue in ATTR_TYPE_ORDER:
				attrChoose.InsertItem(typeValue, ATTR_TYPE_ITEMS[typeValue])
			attrChoose.SetEvent(lambda idx, argSelf=proxy(self), argRow=row: argSelf.OnSelectAttrType(argRow, idx))
			attrChoose.SetOpenEvent(lambda argSelf=proxy(self), argRow=row: argSelf._PrivateShopSearchWindow__CloseOtherCombos("attr%d" % argRow))
			self.attrChooses.append(attrChoose)
			self.attrValueEdits.append(self.__MakeNumberEdit(110, rowY + 4, 50))

		applyButton = ui.Button()
		applyButton.SetParent(self.menuBox)
		applyButton.SetText("Search")
		applyButton.SetPosition(5, NextY(24))
		applyButton.SetUpVisual("d:/ymir work/ui/public/Middle_Button_01.sub")
		applyButton.SetOverVisual("d:/ymir work/ui/public/Middle_Button_02.sub")
		applyButton.SetDownVisual("d:/ymir work/ui/public/Middle_Button_03.sub")
		applyButton.SetEvent(ui.__mem_func__(self.OnSearch))
		applyButton.Show()

		self.filterWidgets = [
			self.checkBoxes["timelimited"],
			self.characterChoose, self.sexChoose, self.alchemyChoose, self.costumeChoose,
			refineLabel, self.minRefineEdit, self.maxRefineEdit,
			levelLabel, self.minLevelEdit, self.maxLevelEdit,
			countLabel, self.minCountEdit, self.maxCountEdit,
			avgLabel, self.minAverageEdit, self.minSkillEdit,
			attrLabel, applyButton,
		] + self.attrChooses + self.attrValueEdits
		for w in self.filterWidgets:
			w.Hide()

	def __MakeNumberEdit(self, x, y, width):
		edit = ui.EditLine()
		edit.SetParent(self.menuBox)
		edit.SetPosition(x, y)
		edit.SetSize(width, 20)
		edit.SetMax(6)
		edit.SetNumberMode()
		edit.SetText("")
		edit.Show()
		return edit

	def __MakeCheckBox(self, parent, x, y, text, flagKey):
		box = ui.CheckBox()
		box.SetParent(parent)
		box.SetPosition(x, y)
		box.SetTextInfo(text)
		box.SetEvent(ui.__mem_func__(self.OnCheckToggle), "ON_CHECK", flagKey, True)
		box.SetEvent(ui.__mem_func__(self.OnCheckToggle), "ON_UNCKECK", flagKey, False)
		return box

	def OnCheckToggle(self, state, flagKey, value):
		self.flags[flagKey] = value

	def __CloseOtherCombos(self, exceptName):
		if exceptName != "character":
			self.characterChoose.CloseListBox()
		if exceptName != "sex":
			self.sexChoose.CloseListBox()
		if exceptName != "alchemy":
			self.alchemyChoose.CloseListBox()
		if exceptName != "costume":
			self.costumeChoose.CloseListBox()
		for row, attrChoose in enumerate(self.attrChooses):
			if exceptName != "attr%d" % row:
				attrChoose.CloseListBox()

	if app.__BL_MOUSE_WHEEL_TOP_WINDOW__:
		def OnMouseWheelButtonUp(self):
			if self.resultScrollBar and self.resultScrollBar.IsShow():
				self.resultScrollBar.OnUp()
				return True
			return False

		def OnMouseWheelButtonDown(self):
			if self.resultScrollBar and self.resultScrollBar.IsShow():
				self.resultScrollBar.OnDown()
				return True
			return False
	
	def Open(self):
		self.__LoadWindow()
		self.SetCenterPosition()
		if app.__BL_MOUSE_WHEEL_TOP_WINDOW__:
			wndMgr.SetWheelTopWindow(self.hWnd)
		## Without this the window never becomes the topmost pick target, so mouse
		## input (scrollbar drags, row clicks) can be swallowed by whatever else is
		## on top instead of reaching this window's children - every other dialog in
		## this codebase does this in Open() (see uicommon.py's PopupDialog.Open).
		self.SetTop()
		self.Show()
		## Match the reference client: opening the window runs an immediate
		## "search everything" (categoryType/-Sub default to -1, which the server's
		## CheckFilter treats as "no category filter") instead of showing an empty
		## list until the player manually searches.
		self.OnSearch()

	def Close(self):
		if self.isLoaded:
			self.characterChoose.CloseListBox()
			self.sexChoose.CloseListBox()
			self.alchemyChoose.CloseListBox()
			self.costumeChoose.CloseListBox()
			for attrChoose in self.attrChooses:
				attrChoose.CloseListBox()
			self.__HideSuggestions()
		if self.buyQuestionDialog:
			self.buyQuestionDialog.Close()
			self.buyQuestionDialog = None
		self.Hide()

	def OnToggleFilter(self, isDown):
		self.filterShown = isDown
		if self.filterShown:
			self.__ShowFilterPanel()
		else:
			self.__ShowCategoryTree()

	def OnClearFilters(self):
		self.flags = { "seller" : False, "exact" : False, "timelimited" : False }
		for box in self.checkBoxes.values():
			box.SetCheckStatus(False)
		self.exactCheckBox.SetCheckStatus(False)
		self.sellerCheckBox.SetCheckStatus(False)
		self.characterValue = 0
		self.characterChoose.SetCurrentItem(CHARACTER_ITEMS[0])
		self.sexValue = 0
		self.sexChoose.SetCurrentItem(SEX_ITEMS[0])
		self.alchemyValue = 0
		self.alchemyChoose.SetCurrentItem(ALCHEMY_ITEMS[0])
		self.costumeValue = 0
		self.costumeChoose.SetCurrentItem(COSTUME_TYPE_ITEMS[0])
		for row in xrange(ATTR_FILTER_ROW_COUNT):
			self.attrChoices[row] = 0
			self.attrChooses[row].SetCurrentItem(ATTR_TYPE_ITEMS[0])
			self.attrValueEdits[row].SetText("")
		for edit in (self.minRefineEdit, self.maxRefineEdit, self.minLevelEdit, self.maxLevelEdit,
					self.minCountEdit, self.maxCountEdit, self.minAverageEdit, self.minSkillEdit):
			edit.SetText("")

	def OnClearText(self):
		self.searchEdit.SetText("")
		self.__HideSuggestions()

	def OnSelectCharacter(self, index):
		self.characterValue = index
		self.characterChoose.SetCurrentItem(CHARACTER_ITEMS[index])
		self.characterChoose.CloseListBox()

	def OnSelectSex(self, index):
		self.sexValue = index
		self.sexChoose.SetCurrentItem(SEX_ITEMS[index])
		self.sexChoose.CloseListBox()

	def OnSelectAlchemy(self, index):
		self.alchemyValue = index
		self.alchemyChoose.SetCurrentItem(ALCHEMY_ITEMS[index])
		self.alchemyChoose.CloseListBox()

	def OnSelectCostume(self, index):
		self.costumeValue = index
		self.costumeChoose.SetCurrentItem(COSTUME_TYPE_ITEMS[index])
		self.costumeChoose.CloseListBox()

	def OnSelectAttrType(self, row, index):
		self.attrChoices[row] = index
		self.attrChooses[row].SetCurrentItem(ATTR_TYPE_ITEMS[index])
		self.attrChooses[row].CloseListBox()

	## ---- item-name autocomplete: a small bordered dropdown, not a stack of buttons ----
	def __HideSuggestions(self):
		if self.suggestListBox:
			self.suggestListBox.Hide()
			self.suggestListBox.Destroy()
			self.suggestListBox = None
		if self.suggestFrame:
			self.suggestFrame.Hide()
			self.suggestFrame.Destroy()
			self.suggestFrame = None

	def __RefreshSuggestions(self):
		text = self.searchEdit.GetText()
		if not text or len(text) < 2:
			self.__HideSuggestions()
			return

		try:
			matches = item.GetItemsByName(text)
		except:
			matches = []

		self.__HideSuggestions()
		if not matches:
			return

		self.suggestMatches = matches[:SUGGEST_MAX_ROWS]
		frameHeight = len(self.suggestMatches) * SUGGEST_ROW_HEIGHT + 6

		frame = ui.ThinBoard()
		frame.SetParent(self)
		frame.SetPosition(15, 120)
		frame.SetSize(170, frameHeight)
		frame.Show()
		self.suggestFrame = frame

		listBox = ui.ListBox()
		listBox.SetParent(frame)
		listBox.SetPosition(3, 3)
		listBox.SetTextCenterAlign(False)
		listBox.SetWidth(164)
		for idx, (vnum, name) in enumerate(self.suggestMatches):
			listBox.InsertItem(idx, name)
		listBox.ArrangeItem()
		listBox.SetEvent(ui.__mem_func__(self.__OnSelectSuggestion))
		listBox.Show()
		self.suggestListBox = listBox

	def __OnSelectSuggestion(self, idx, name):
		self.searchEdit.SetText(name)
		self.__HideSuggestions()
		self.OnSearch()

	def __GetIntOrZero(self, editline):
		text = editline.GetText()
		if not text or not text.isdigit():
			return 0
		return int(text)

	def __BuildCommand(self, page = 1):
		text = self.searchEdit.GetText()
		if not text:
			text = ""

		playerSearch = 1 if self.flags["seller"] else 0
		timeType = 2 if self.flags["timelimited"] else 0

		race = [0, 0, 0, 0]
		if self.characterValue in CHARACTER_TO_RACE_INDEX:
			race[CHARACTER_TO_RACE_INDEX[self.characterValue]] = 1

		sexMale = 1 if self.sexValue == 1 else 0
		sexFemale = 1 if self.sexValue == 2 else 0

		minRefine = self.__GetIntOrZero(self.minRefineEdit)
		maxRefine = self.__GetIntOrZero(self.maxRefineEdit)
		minLevel = self.__GetIntOrZero(self.minLevelEdit)
		maxLevel = self.__GetIntOrZero(self.maxLevelEdit)
		minCount = self.__GetIntOrZero(self.minCountEdit)
		maxCount = self.__GetIntOrZero(self.maxCountEdit)
		minAverage = self.__GetIntOrZero(self.minAverageEdit)
		minSkill = self.__GetIntOrZero(self.minSkillEdit)

		## Up to ATTR_FILTER_ROW_COUNT real (type, value) pairs, padded with zeros to
		## fill CompareFilter's fixed 5-slot "attr" segment (vec.size() must be >= 11).
		attrPairs = []
		for row in xrange(ATTR_FILTER_ROW_COUNT):
			attrType = self.attrChoices[row]
			attrValue = self.__GetIntOrZero(self.attrValueEdits[row])
			if attrType > 0 and attrValue > 0:
				attrPairs.append((attrType, attrValue))
		while len(attrPairs) < 5:
			attrPairs.append((0, 0))
		attrArgs = []
		for attrType, attrValue in attrPairs:
			attrArgs.append(attrType)
			attrArgs.append(attrValue)

		command = "input^%s$" % text
		command += "checkbox^%d^%d$" % (1 if self.flags["exact"] else 0, playerSearch)
		command += "type^%d^%d$" % (self.categoryType, self.categorySubType)
		command += "combo^%d^%d^%d^0^%d^0^0^%d$" % (minRefine, maxRefine, self.alchemyValue, self.costumeValue, timeType)
		command += "race^%d^%d^%d^%d$" % (race[0], race[1], race[2], race[3])
		command += "sex^%d^%d$" % (sexMale, sexFemale)
		command += "editline^%d^%d^%d^%d^0^0^%d^%d$" % (minCount, maxCount, minAverage, minSkill, minLevel, maxLevel)
		command += "attr^%d^%d^%d^%d^%d^%d^%d^%d^%d^%d$" % tuple(attrArgs)
		command += "page^%d$" % page
		return command

	def OnSearch(self):
		self.__HideSuggestions()
		privateShopSearch.Search(self.__BuildCommand(1))

	def __GoToPage(self, page):
		if page < 1:
			return
		privateShopSearch.Search(self.__BuildCommand(page))

	## ---- pagination: sliding 5-button window + first/prev/next/last, same shape as
	## the reference's CreatePagination, using pagination_btn1-4.png (up/over/down/
	## disabled) instead of the old private_* pagenumber skin. ----
	def __ClearPageButtons(self):
		for btn in self.pageButtons:
			btn.Hide()
			btn.Destroy()
		self.pageButtons = []

	def __MakePageButton(self, x, text, page, enabled):
		btn = ui.Button()
		btn.SetParent(self.paginationBox)
		btn.SetText(text)
		btn.SetPosition(x, 3)
		btn.SetUpVisual(IMG_DIR + "pagination_btn1.png")
		btn.SetOverVisual(IMG_DIR + "pagination_btn2.png")
		btn.SetDownVisual(IMG_DIR + "pagination_btn3.png")
		btn.SetDisableVisual(IMG_DIR + "pagination_btn4.png")
		if enabled:
			btn.SetEvent(ui.__mem_func__(self.__GoToPage), page)
		else:
			btn.Disable()
		btn.Show()
		self.pageButtons.append(btn)
		return btn

	## Pagination buttons are laid out right-to-left from the pagination box's own
	## right edge (matching the reference's CreatePagination), and only rendered at
	## all when there's more than one page - with a single page, "<<"/"<"/">"/">>"
	## are useless clutter (this is what looked like squished, overlapping icons
	## next to the result count before). resultCountText is then right-anchored to
	## end just left of whatever buttons were actually placed, so it can never
	## collide with them or with BuySelectedButton on the far left.
	def __RefreshPageButtons(self):
		self.__ClearPageButtons()

		curPage = privateShopSearch.GetPageIdx()
		totalPage = max(1, privateShopSearch.GetTotalPageCount())
		curIndex = curPage - 1
		itemCount = privateShopSearch.GetItemCount()

		boxWidth = self.paginationBox.GetWidth()
		x = boxWidth - 5 - 20

		if totalPage > 1:
			show = min(5, totalPage)
			center = show / 2
			start = curIndex - center
			if start + show >= totalPage:
				start = totalPage - show
			if start < 0:
				start = 0
			end = start + show

			self.__MakePageButton(x, ">>", totalPage, curIndex < totalPage - 1)
			x -= 24
			self.__MakePageButton(x, ">", curPage + 1, curIndex < totalPage - 1)
			x -= 24
			for pageIndex in xrange(end - 1, start - 1, -1):
				btn = self.__MakePageButton(x, str(pageIndex + 1), pageIndex + 1, pageIndex != curIndex)
				if pageIndex == curIndex:
					btn.Down()
				x -= 24
			self.__MakePageButton(x, "<", curPage - 1, curIndex > 0)
			x -= 24
			self.__MakePageButton(x, "<<", 1, curIndex > 0)
			x -= 24

		self.resultCountText.SetPosition(x + 4, PAGINATION_HEIGHT / 2)
		self.resultCountText.SetText("%d results - page %d / %d" % (itemCount, curPage, totalPage))

	def __ClearResultRows(self):
		for rowWidget in self.resultRows:
			rowWidget.Hide()
			rowWidget.Destroy()
		self.resultRows = []

	def __OnResultScroll(self):
		self.__UpdateRowVisibility()

	## Rows are variable height now (1-3 item-slot cells), so visibility can't be
	## computed from a row index * fixed height - each row remembers its own
	## cumulative pixel Y (rowWidget.rowY, set in RefreshMe) and this just slides
	## that by a pixel offset from the scrollbar, same pattern as the already-working
	## category tree scroller (__ApplyCategoryScroll). resultBox now has a real
	## GPU-level clip mask (SetClippingMaskWindow, applied in RefreshMe), so a row
	## only needs to be shown if it overlaps the viewport AT ALL - the mask crops
	## whatever sticks out past the top/bottom edge, instead of us hiding the whole
	## row until it fits entirely (which is what made partially-visible rows vanish).
	def __UpdateRowVisibility(self):
		viewHeight = RESULT_USABLE_HEIGHT
		scrollLen = max(0, self.resultTotalHeight - viewHeight)
		offset = int(self.resultScrollBar.GetPos() * scrollLen) if scrollLen > 0 else 0

		for rowWidget in self.resultRows:
			posY = rowWidget.rowY - offset
			if posY + rowWidget.GetHeight() > 0 and posY < viewHeight:
				rowWidget.SetPosition(5, posY)
				rowWidget.Show()
			else:
				rowWidget.Hide()

		if scrollLen > 0:
			self.resultScrollBar.SetMiddleBarSize(float(viewHeight) / self.resultTotalHeight)
			self.resultScrollBar.Show()
		else:
			self.resultScrollBar.Hide()

	def RefreshMe(self):
		if not self.isLoaded:
			return

		self.__ClearResultRows()
		self.selectedIndices = set()
		itemCount = privateShopSearch.GetItemCount()
		rowWidth = self.resultRowWidth
		cumulativeY = 0

		for idx in xrange(itemCount):
			vnum = privateShopSearch.GetItemVnum(idx)
			count = privateShopSearch.GetItemCountAt(idx)
			price = privateShopSearch.GetItemPrice(idx)
			seller = privateShopSearch.GetItemSeller(idx)
			isOnline = privateShopSearch.GetItemOwnerStatus(idx) != 0
			try:
				# GetItemName() takes no vnum argument - it reads whatever item
				# SelectItem() last pointed at. Passing vnum straight to GetItemName()
				# silently ignores it and returns the name of whatever item happened to
				# be selected elsewhere in the game (inventory hover, tooltips, etc.) -
				# this is what was actually causing "wrong item name in search results".
				item.SelectItem(vnum)
				name = item.GetItemName()
			except:
				name = "item#%d" % vnum
			try:
				priceText = localeInfo.NumberToMoneyString(price)
			except:
				priceText = str(price)

			rowWidget = SearchResultRow(self.resultViewport, rowWidth)
			rowWidget.Build(vnum, count, name, seller, priceText, isOnline)
			rowWidget.SetToolTip(self.tooltipItem, idx)
			rowWidget.SetEvents(
				lambda pos, argSelf=proxy(self), argIdx=idx: argSelf.OnBuyRow(argIdx),
				lambda argSelf=proxy(self), argIdx=idx: argSelf.OnTeleportRow(argIdx),
				lambda argSelf=proxy(self), argIdx=idx: argSelf.OnWhisperRow(argIdx),
				lambda state, checked, argSelf=proxy(self), argIdx=idx: argSelf.OnToggleSelect(argIdx, checked),
			)
			rowWidget.rowY = cumulativeY
			rowWidget.Show()
			cumulativeY += rowWidget.GetHeight() + 3
			self.resultRows.append(rowWidget)

		self.resultTotalHeight = cumulativeY
		self.resultScrollBar.SetPos(0.0)
		## resultViewport's scissor rect was already turned on once in __BuildWindow -
		## it clips every row rebuilt here automatically, nothing to reapply.
		self.__UpdateRowVisibility()
		self.__RefreshPageButtons()

	def OnToggleSelect(self, idx, checked):
		if checked:
			self.selectedIndices.add(idx)
		else:
			self.selectedIndices.discard(idx)

	## ---- Buy Selected: one up-front confirmation (count + total), then fire every
	## SendBuy in a tight loop - each is an independent one-shot request keyed by its
	## own (owner_id, pos, itemID), so there's no need to wait for per-item acks
	## before sending the next one. ----
	def OnBuySelected(self):
		if not self.selectedIndices:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "No items selected.")
			return

		totalPrice = 0
		for idx in self.selectedIndices:
			totalPrice += privateShopSearch.GetItemPrice(idx)
		try:
			priceText = localeInfo.NumberToMoneyString(totalPrice)
		except:
			priceText = str(totalPrice)

		dlg = uiCommon.QuestionDialog2()
		dlg.SetText1("Buy %d selected items?" % len(self.selectedIndices))
		dlg.SetText2("Total: %s yang" % priceText)
		## OnBuySelected is itself invoked via SAFE_SetEvent (ui.__mem_func__), which
		## already calls it with a weakref-proxied self, not the real instance -
		## wrapping it in proxy() again is a proxy-of-a-proxy, which weakref rejects
		## outright ("cannot create weak reference to 'weakproxy' object"). Just
		## reuse the self we were already given.
		dlg.SetAcceptEvent(lambda argSelf=self: argSelf._PrivateShopSearchWindow__AnswerBuySelected(True))
		dlg.SetCancelEvent(lambda argSelf=self: argSelf._PrivateShopSearchWindow__AnswerBuySelected(False))
		dlg.Open()
		self.buyQuestionDialog = dlg

	def __AnswerBuySelected(self, accepted):
		if accepted:
			for idx in self.selectedIndices:
				vid = privateShopSearch.GetItemShopVID(idx)
				pos = privateShopSearch.GetItemPos(idx)
				itemID = privateShopSearch.GetItemID(idx)
				offlineShop.SendBuy(vid, pos, itemID)
			self.selectedIndices = set()
		if self.buyQuestionDialog:
			self.buyQuestionDialog.Close()
			self.buyQuestionDialog = None
		return True

	def OnBuyRow(self, idx):
		vnum = privateShopSearch.GetItemVnum(idx)
		count = privateShopSearch.GetItemCountAt(idx)
		price = privateShopSearch.GetItemPrice(idx)
		try:
			item.SelectItem(vnum)
			name = item.GetItemName()
		except:
			name = "item#%d" % vnum
		try:
			priceText = localeInfo.NumberToMoneyString(price)
		except:
			priceText = str(price)

		dlg = uiCommon.QuestionDialog2()
		dlg.SetText1("%s x%d" % (name, count))
		dlg.SetText2("%s yang?" % priceText)
		dlg.SetAcceptEvent(lambda argIdx=idx, argSelf=proxy(self): argSelf._PrivateShopSearchWindow__AnswerBuyRow(argIdx, True))
		dlg.SetCancelEvent(lambda argIdx=idx, argSelf=proxy(self): argSelf._PrivateShopSearchWindow__AnswerBuyRow(argIdx, False))
		dlg.Open()
		self.buyQuestionDialog = dlg

	def __AnswerBuyRow(self, idx, accepted):
		if accepted:
			vid = privateShopSearch.GetItemShopVID(idx)
			pos = privateShopSearch.GetItemPos(idx)
			itemID = privateShopSearch.GetItemID(idx)
			offlineShop.SendBuy(vid, pos, itemID)
		if self.buyQuestionDialog:
			self.buyQuestionDialog.Close()
			self.buyQuestionDialog = None
		return True

	def OnTeleportRow(self, idx):
		seller = privateShopSearch.GetItemSeller(idx)
		if not seller:
			return
		offlineShop.SendTeleport(seller)

	def OnWhisperRow(self, idx):
		seller = privateShopSearch.GetItemSeller(idx)
		if not seller:
			return
		interfaceInstance = constInfo.GetInterfaceInstance()
		if interfaceInstance:
			interfaceInstance.OpenWhisperDialog(seller)
