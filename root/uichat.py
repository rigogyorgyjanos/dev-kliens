import ui
import grp
import chat
import wndMgr
import net
import app
import ime
import chr
import localeInfo
import colorInfo
import constInfo
import systemSetting
from resizeexpr import Expr

if app.ENABLE_CHATTING_WINDOW_RENEWAL:
	import os
	import uiCommon
	import uiScriptLocale
	import cPickle
	import player

ENABLE_CHAT_COMMAND = True
ENABLE_LAST_SENTENCE_STACK = True
ENABLE_INSULT_CHECK = True

if localeInfo.IsHONGKONG():
	ENABLE_LAST_SENTENCE_STACK = True

if localeInfo.IsEUROPE():
	ENABLE_CHAT_COMMAND = False

if localeInfo.IsCANADA():
	ENABLE_LAST_SENTENCE_STACK = False

chatInputSetList = []
def InsertChatInputSetWindow(wnd):
	global chatInputSetList
	chatInputSetList.append(wnd)
def RefreshChatMode():
	global chatInputSetList
	map(lambda wnd:wnd.OnRefreshChatMode(), chatInputSetList)
def DestroyChatInputSetWindow():
	global chatInputSetList
	chatInputSetList = []

## ChatModeButton
class ChatModeButton(ui.Window):

	OUTLINE_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 1.0)
	OVER_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 0.3)
	BUTTON_STATE_UP = 0
	BUTTON_STATE_OVER = 1
	BUTTON_STATE_DOWN = 2

	def __init__(self):
		ui.Window.__init__(self)
		self.state = None
		self.buttonText = None
		self.event = None
		self.SetWindowName("ChatModeButton")

		net.EnableChatInsultFilter(ENABLE_INSULT_CHECK)

	def __del__(self):
		ui.Window.__del__(self)

	def SAFE_SetEvent(self, event):
		self.event=ui.__mem_func__(event)

	def SetText(self, text):
		if None == self.buttonText:
			textLine = ui.TextLine()
			textLine.SetParent(self)
			textLine.SetWindowHorizontalAlignCenter()
			textLine.SetWindowVerticalAlignCenter()
			textLine.SetVerticalAlignCenter()
			textLine.SetHorizontalAlignCenter()
			textLine.SetPackedFontColor(self.OUTLINE_COLOR)
			textLine.Show()
			self.buttonText = textLine

		self.buttonText.SetText(text)

	def SetSize(self, width, height):
		self.width = width
		self.height = height
		ui.Window.SetSize(self, width, height)

	def OnMouseOverIn(self):
		self.state = self.BUTTON_STATE_OVER

	def OnMouseOverOut(self):
		self.state = self.BUTTON_STATE_UP

	def OnMouseLeftButtonDown(self):
		self.state = self.BUTTON_STATE_DOWN

	def OnMouseLeftButtonUp(self):
		self.state = self.BUTTON_STATE_UP
		if self.IsIn():
			self.state = self.BUTTON_STATE_OVER

		if None != self.event:
			self.event()

	def OnRender(self):

		(x, y) = self.GetGlobalPosition()

		grp.SetColor(self.OUTLINE_COLOR)
		grp.RenderRoundBox(x, y, self.width, self.height)

		if self.state >= self.BUTTON_STATE_OVER:
			grp.RenderRoundBox(x+1, y, self.width-2, self.height)
			grp.RenderRoundBox(x, y+1, self.width, self.height-2)

			if self.BUTTON_STATE_DOWN == self.state:
				grp.SetColor(self.OVER_COLOR)
				grp.RenderBar(x+1, y+1, self.width-2, self.height-2)

## ChatLine
class ChatLine(ui.EditLine):

	CHAT_MODE_NAME = {	chat.CHAT_TYPE_TALKING : localeInfo.CHAT_NORMAL,
						chat.CHAT_TYPE_PARTY : localeInfo.CHAT_PARTY,
						chat.CHAT_TYPE_GUILD : localeInfo.CHAT_GUILD,
						chat.CHAT_TYPE_SHOUT : localeInfo.CHAT_SHOUT, }

	def __init__(self):
		ui.EditLine.__init__(self)
		self.SetWindowName("Chat Line")
		self.lastShoutTime = 0
		self.eventEscape = lambda *arg: None
		self.eventReturn = lambda *arg: None
		self.eventTab = None
		self.chatMode = chat.CHAT_TYPE_TALKING
		self.bCodePage = True

		self.overTextLine = ui.TextLine()
		self.overTextLine.SetParent(self)
		self.overTextLine.SetPosition(-1, 0)
		self.overTextLine.SetFontColor(1.0, 1.0, 0.0)
		self.overTextLine.SetOutline()
		self.overTextLine.Hide()

		self.lastSentenceStack = []
		self.lastSentencePos = 0

	def SetChatMode(self, mode):
		self.chatMode = mode

	def GetChatMode(self):
		return self.chatMode

	def ChangeChatMode(self):
		if chat.CHAT_TYPE_TALKING == self.GetChatMode():
			self.SetChatMode(chat.CHAT_TYPE_PARTY)
			self.SetText("#")
			self.SetEndPosition()

		elif chat.CHAT_TYPE_PARTY == self.GetChatMode():
			self.SetChatMode(chat.CHAT_TYPE_GUILD)
			self.SetText("%")
			self.SetEndPosition()

		elif chat.CHAT_TYPE_GUILD == self.GetChatMode():
			self.SetChatMode(chat.CHAT_TYPE_SHOUT)
			self.SetText("!")
			self.SetEndPosition()

		elif chat.CHAT_TYPE_SHOUT == self.GetChatMode():
			self.SetChatMode(chat.CHAT_TYPE_TALKING)
			self.SetText("")

		self.__CheckChatMark()

	
	def GetLink(self, text):
		link = ""
		start = text.find("http://")
		if start == -1:
			start = text.find("https://")
		if start == -1:
			return ""

		return text[start:len(text)].split(" ")[0]
			
	def GetCurrentChatModeName(self):
		try:
			return self.CHAT_MODE_NAME[self.chatMode]
		except:
			import exception
			exception.Abort("ChatLine.GetCurrentChatModeName")

	def SAFE_SetEscapeEvent(self, event):
		self.eventReturn = ui.__mem_func__(event)

	def SAFE_SetReturnEvent(self, event):
		self.eventEscape = ui.__mem_func__(event)

	def SAFE_SetTabEvent(self, event):
		self.eventTab = ui.__mem_func__(event)

	def SetTabEvent(self, event):
		self.eventTab = event

	def OpenChat(self):
		self.SetFocus()
		self.__ResetChat()

	def __ClearChat(self):
		self.SetText("")
		self.lastSentencePos = 0

	def __ResetChat(self):
		if chat.CHAT_TYPE_PARTY == self.GetChatMode():
			self.SetText("#")
			self.SetEndPosition()
		elif chat.CHAT_TYPE_GUILD == self.GetChatMode():
			self.SetText("%")
			self.SetEndPosition()
		elif chat.CHAT_TYPE_SHOUT == self.GetChatMode():
			self.SetText("!")
			self.SetEndPosition()
		else:
			self.__ClearChat()

		self.__CheckChatMark()
		

	def __SendChatPacket(self, text, type):
		if net.IsChatInsultIn(text):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CHAT_INSULT_STRING)
		else:
			link = self.GetLink(text)
			if link != "":
				text = text.replace(link, "|cFF00C0FC|h|Hsysweb:" + link.replace("://", "XxX") + "|h" + link + "|h|r")
				
					
			net.SendChatPacket(text, type)
		
	def __SendPartyChatPacket(self, text):

		if 1 == len(text):
			self.RunCloseEvent()
			return

		self.__SendChatPacket(text[1:], chat.CHAT_TYPE_PARTY)
		self.__ResetChat()

	def __SendGuildChatPacket(self, text):

		if 1 == len(text):
			self.RunCloseEvent()
			return

		self.__SendChatPacket(text[1:], chat.CHAT_TYPE_GUILD)
		self.__ResetChat()

	def __SendShoutChatPacket(self, text):

		if 1 == len(text):
			self.RunCloseEvent()
			return

		if app.GetTime() < self.lastShoutTime + 15:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CHAT_SHOUT_LIMIT)
			self.__ResetChat()
			return

		self.__SendChatPacket(text[1:], chat.CHAT_TYPE_SHOUT)
		self.__ResetChat()

		self.lastShoutTime = app.GetTime()

	def __SendTalkingChatPacket(self, text):
		self.__SendChatPacket(text, chat.CHAT_TYPE_TALKING)
		self.__ResetChat()

	def OnIMETab(self):
		#if None != self.eventTab:
		#	self.eventTab()
		#return True
		return False

	def OnIMEUpdate(self):
		ui.EditLine.OnIMEUpdate(self)
		self.__CheckChatMark()

	def __CheckChatMark(self):

		self.overTextLine.Hide()

		text = self.GetText()
		if len(text) > 0:
			if '#' == text[0]:
				self.overTextLine.SetText("#")
				self.overTextLine.Show()
			elif '%' == text[0]:
				self.overTextLine.SetText("%")
				self.overTextLine.Show()
			elif '!' == text[0]:
				self.overTextLine.SetText("!")
				self.overTextLine.Show()

	def OnIMEKeyDown(self, key):
		# LAST_SENTENCE_STACK
		if app.VK_UP == key:
			self.__PrevLastSentenceStack()
			return True

		if app.VK_DOWN == key:
			self.__NextLastSentenceStack()				
			return True			
		# END_OF_LAST_SENTENCE_STACK

		ui.EditLine.OnIMEKeyDown(self, key)

	# LAST_SENTENCE_STACK
	def __PrevLastSentenceStack(self):
		global ENABLE_LAST_SENTENCE_STACK
		if not ENABLE_LAST_SENTENCE_STACK:
			return

		if self.lastSentenceStack and self.lastSentencePos < len(self.lastSentenceStack):
			self.lastSentencePos += 1
			lastSentence = self.lastSentenceStack[-self.lastSentencePos]
			self.SetText(lastSentence)				
			self.SetEndPosition()			

	def __NextLastSentenceStack(self):
		global ENABLE_LAST_SENTENCE_STACK
		if not ENABLE_LAST_SENTENCE_STACK:
			return

		if self.lastSentenceStack and self.lastSentencePos > 1:
			self.lastSentencePos -= 1
			lastSentence = self.lastSentenceStack[-self.lastSentencePos]
			self.SetText(lastSentence)				
			self.SetEndPosition()			

	def __PushLastSentenceStack(self, text):		
		global ENABLE_LAST_SENTENCE_STACK
		if not ENABLE_LAST_SENTENCE_STACK:
			return

		if len(text) <= 0:
			return
			
		LAST_SENTENCE_STACK_SIZE = 32
		if len(self.lastSentenceStack) > LAST_SENTENCE_STACK_SIZE:
			self.lastSentenceStack.pop(0)

		self.lastSentenceStack.append(text)
	# END_OF_LAST_SENTENCE_STACK

	def OnIMEReturn(self):
		text = self.GetText()
		textLen=len(text)

		# LAST_SENTENCE_STACK
		self.__PushLastSentenceStack(text)
		# END_OF_LAST_SENTENCE_STACK
				
		textSpaceCount=text.count(' ')

		if (textLen > 0) and (textLen != textSpaceCount):
			if '#' == text[0]:
				self.__SendPartyChatPacket(text)
			elif '%' == text[0]:
				self.__SendGuildChatPacket(text)
			elif '!' == text[0]:
				self.__SendShoutChatPacket(text)
			else:
				self.__SendTalkingChatPacket(text)
		else:
			self.__ClearChat()
			self.eventReturn()

		return True

	def OnPressEscapeKey(self):
		self.__ClearChat()
		self.eventEscape()
		return True

	def RunCloseEvent(self):
		self.eventEscape()

	def BindInterface(self, interface):
		self.interface = interface

	def OnMouseLeftButtonDown(self):
		hyperlink = ui.GetHyperlink()
		if hyperlink:
			if app.IsPressed(app.DIK_LALT):
				link = chat.GetLinkFromHyperlink(hyperlink)
				ime.PasteString(link)
			else:
				self.interface.MakeHyperlinkTooltip(hyperlink)
		else:
			ui.EditLine.OnMouseLeftButtonDown(self)

class ChatInputSet(ui.Window):

	CHAT_OUTLINE_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 1.0)

	def __init__(self):
		ui.Window.__init__(self)
		self.SetWindowName("ChatInputSet")

		InsertChatInputSetWindow(self)
		self.__Create()

	def __del__(self):
		ui.Window.__del__(self)

	def __Create(self):
		chatModeButton = ChatModeButton()
		chatModeButton.SetParent(self)
		chatModeButton.SetSize(40, 17)
		chatModeButton.SetText(localeInfo.CHAT_NORMAL)
		chatModeButton.SetPosition(7, 2)
		chatModeButton.SAFE_SetEvent(self.OnChangeChatMode)
		self.chatModeButton = chatModeButton

		chatLine = ChatLine()
		chatLine.SetParent(self)
		chatLine.SetMax(512)
		chatLine.SetUserMax(76)
		chatLine.SetText("")
		chatLine.SetMultiLine()
		# Clips wrapped text to this box's own (small, unchanged - see RefreshPosition) footprint
		# instead of letting it render past the box into the taskbar below. Only the current line
		# is guaranteed visible while composing a longer message; the rest still sends correctly,
		# it's just clipped from view (see RefreshPosition for why the box wasn't made taller).
		chatLine.EnableScissorRect()
		chatLine.SAFE_SetTabEvent(self.OnChangeChatMode)
		chatLine.x = 0
		chatLine.y = 0
		chatLine.width = 0
		chatLine.height = 0
		self.chatLine = chatLine

		btnSend = ui.Button()
		btnSend.SetParent(self)
		btnSend.SetUpVisual("d:/ymir work/ui/game/taskbar/Send_Chat_Button_01.sub")
		btnSend.SetOverVisual("d:/ymir work/ui/game/taskbar/Send_Chat_Button_02.sub")
		btnSend.SetDownVisual("d:/ymir work/ui/game/taskbar/Send_Chat_Button_03.sub")
		btnSend.SetToolTipText(localeInfo.CHAT_SEND_CHAT)
		btnSend.SAFE_SetEvent(self.chatLine.OnIMEReturn)
		self.btnSend = btnSend

	def Destroy(self):
		self.chatModeButton = None
		self.chatLine = None
		self.btnSend = None

	def Open(self):
		self.chatLine.Show()
		self.chatLine.SetPosition(57, 5)
		self.chatLine.SetFocus()
		self.chatLine.OpenChat()

		self.chatModeButton.SetPosition(7, 2)
		self.chatModeButton.Show()

		self.btnSend.Show()
		self.Show()

		self.RefreshPosition()
		return True

	def Close(self):
		self.chatLine.KillFocus()
		self.chatLine.Hide()
		self.chatModeButton.Hide()
		self.btnSend.Hide()
		self.Hide()
		return True

	def SetEscapeEvent(self, event):
		self.chatLine.SetEscapeEvent(event)

	def SetReturnEvent(self, event):
		self.chatLine.SetReturnEvent(event)

	def OnChangeChatMode(self):
		RefreshChatMode()

	def OnRefreshChatMode(self):
		self.chatLine.ChangeChatMode()
		self.chatModeButton.SetText(self.chatLine.GetCurrentChatModeName())

	def SetChatFocus(self):
		self.chatLine.SetFocus()

	def KillChatFocus(self):
		self.chatLine.KillFocus()

	def SetChatMax(self, max):
		self.chatLine.SetUserMax(max)

	def RefreshPosition(self):
		lineWidth = self.GetWidth() - 93

		# Footprint kept at its original size on purpose: the taskbar sits directly below this
		# row with very little verified clearance (ChatWindow's own position formula reserves
		# only ~37px below it in __MakeChatWindow, and uitaskbar.py positions at least one of its
		# own elements just a few px into that same margin), so growing this box risks visually
		# overlapping the taskbar in a way that can't be confirmed without a live client. Wrap is
		# still enabled below, so long text no longer overflows sideways past the box - it wraps
		# and clips within this same footprint instead (EnableScissorRect(), set in __Create()).
		if localeInfo.IsARABIC():
			self.chatLine.SetSize(lineWidth, 18)
		else:
			self.chatLine.SetSize(lineWidth, 13)
		self.chatLine.SetLimitWidth(lineWidth)

		self.btnSend.SetPosition(self.GetWidth() - 25, 2)

		(self.chatLine.x, self.chatLine.y, self.chatLine.width, self.chatLine.height) = self.chatLine.GetRect()

	def BindInterface(self, interface):
		self.chatLine.BindInterface(interface)

	def OnRender(self):
		(x, y, width, height) = self.chatLine.GetRect()
		ui.RenderRoundBox(x-4, y-3, width+7, height+4, self.CHAT_OUTLINE_COLOR)

## ChatWindow
class ChatWindow(ui.Window):

	BOARD_START_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.0)
	BOARD_END_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.8)
	BOARD_MIDDLE_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.5)
	CHAT_OUTLINE_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 1.0)

	EDIT_LINE_HEIGHT = 25
	CHAT_WINDOW_WIDTH = 600

	if app.ENABLE_CHATTING_WINDOW_RENEWAL:
		EDIT_LINE_HIDE_HEIGHT = 20
		MAX_TAB_NUMBER = 9

	class ChatBackBoard(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)
		def __del__(self):
			ui.Window.__del__(self)

	class ChatButton(ui.DragButton):

		def __init__(self):
			ui.DragButton.__init__(self)
			self.AddFlag("float")
			self.AddFlag("movable")
			self.AddFlag("restrict_x")
			self.topFlag = False
			self.SetWindowName("ChatWindow:ChatButton")
		

		def __del__(self):
			ui.DragButton.__del__(self)

		def SetOwner(self, owner):
			self.owner = owner

		def OnMouseOverIn(self):
			app.SetCursor(app.VSIZE)

		def OnMouseOverOut(self):
			app.SetCursor(app.NORMAL)

		def OnTop(self):
			if True == self.topFlag:
				return

			self.topFlag = True
			self.owner.SetTop()
			self.topFlag = False

	def __init__(self):
		ui.Window.__init__(self)
		self.AddFlag("float")

		self.SetWindowName("ChatWindow")
		self.__RegisterChatColorDict()

		self.boardState = chat.BOARD_STATE_VIEW
		self.chatID = chat.CreateChatSet(chat.CHAT_SET_CHAT_WINDOW)
		chat.SetBoardState(self.chatID, chat.BOARD_STATE_VIEW)

		# Wrap width is global (shared by every chat line, see PythonChat.cpp), so size it once
		# against the main chat window rather than per chat set.
		chat.SetLimitWidth(self.CHAT_WINDOW_WIDTH - 40)

		self.xBar = 0
		self.yBar = 0
		self.widthBar = 0
		self.heightBar = 0
		self.curHeightBar = 0
		self.visibleLineCount = 0
		self.scrollBarPos = 1.0
		self.scrollLock = False
		self.interface = 0

		chatInputSet = ChatInputSet()
		chatInputSet.SetParent(self)
		chatInputSet.SetEscapeEvent(ui.__mem_func__(self.CloseChat))
		chatInputSet.SetReturnEvent(ui.__mem_func__(self.CloseChat))
		chatInputSet.SetSize(550, 25)
		self.chatInputSet = chatInputSet

		btnSendWhisper = ui.Button()
		btnSendWhisper.SetParent(self)
		btnSendWhisper.SetUpVisual("d:/ymir work/ui/game/taskbar/Send_Whisper_Button_01.sub")
		btnSendWhisper.SetOverVisual("d:/ymir work/ui/game/taskbar/Send_Whisper_Button_02.sub")
		btnSendWhisper.SetDownVisual("d:/ymir work/ui/game/taskbar/Send_Whisper_Button_03.sub")
		btnSendWhisper.SetToolTipText(localeInfo.CHAT_SEND_MEMO)
		btnSendWhisper.Hide()
		self.btnSendWhisper = btnSendWhisper

		btnChatLog = ui.Button()
		btnChatLog.SetParent(self)
		btnChatLog.SetUpVisual("d:/ymir work/ui/game/taskbar/Open_Chat_Log_Button_01.sub")
		btnChatLog.SetOverVisual("d:/ymir work/ui/game/taskbar/Open_Chat_Log_Button_02.sub")
		btnChatLog.SetDownVisual("d:/ymir work/ui/game/taskbar/Open_Chat_Log_Button_03.sub")
		btnChatLog.SetToolTipText(localeInfo.CHAT_LOG)
		btnChatLog.Hide()
		self.btnChatLog = btnChatLog

		btnChatSizing = self.ChatButton()
		btnChatSizing.SetOwner(self)
		btnChatSizing.SetMoveEvent(ui.__mem_func__(self.Refresh))
		btnChatSizing.Hide()
		self.btnChatSizing = btnChatSizing

		if app.ENABLE_CHATTING_WINDOW_RENEWAL:
			self.userDefinedTabs = {}
			self.userDefinedTabLogs = {}
			self.selectedTab = -1

			imgChatBarLeft = ui.ImageBox()
			imgChatBarLeft.SetParent(self.btnChatSizing)
			imgChatBarLeft.AddFlag("not_pick")
			imgChatBarLeft.LoadImage("d:/ymir work/ui/chat/chat_linebar_left.tga")
			imgChatBarLeft.Show()
			self.imgChatBarLeft = imgChatBarLeft

			imgChatBarRight = ui.ImageBox()
			imgChatBarRight.SetParent(self.btnChatSizing)
			imgChatBarRight.AddFlag("not_pick")
			imgChatBarRight.LoadImage("d:/ymir work/ui/chat/chat_linebar_right.tga")
			imgChatBarRight.Show()
			self.imgChatBarRight = imgChatBarRight

			imgChatBarMiddle = ui.ExpandedImageBox()
			imgChatBarMiddle.SetParent(self.btnChatSizing)
			imgChatBarMiddle.AddFlag("not_pick")
			imgChatBarMiddle.LoadImage("d:/ymir work/ui/chat/chatmenutab_line.tga")
			imgChatBarMiddle.Show()
			self.imgChatBarMiddle = imgChatBarMiddle

			btnChatTab = self.CreateTab(uiScriptLocale.CHATTING_SETTING_TALKING)
			btnChatTab.Down()
			self.btnChatTab = btnChatTab

			btnChatSettingOption = ui.Button()
			btnChatSettingOption.SetParent(self.btnChatSizing)
			btnChatSettingOption.SetUpVisual("d:/ymir work/ui/chat/btn_option01_default.tga")
			btnChatSettingOption.SetOverVisual("d:/ymir work/ui/chat/btn_option01_over.tga")
			btnChatSettingOption.SetDownVisual("d:/ymir work/ui/chat/btn_option01_down.tga")
			btnChatSettingOption.SetToolTipText(localeInfo.CHATTING_SETTING_SETTING, 0, -23)
			btnChatSettingOption.SetEvent(ui.__mem_func__(self.__SettingOptionWndOpen))
			btnChatSettingOption.Show()
			self.btnChatSettingOption = btnChatSettingOption

			self.wndChatSettingOption = ChatSettingWindow(self)
			self.wndChatSettingOption.LoadGlobalFile()
			self.__SelectTab(self.wndChatSettingOption.GetSelectedChat(), True)

			btnChatAddTab = ui.Button()
			btnChatAddTab.SetParent(self.btnChatSizing)
			btnChatAddTab.SetUpVisual("d:/ymir work/ui/chat/btn_addtab01_default.tga")
			btnChatAddTab.SetOverVisual("d:/ymir work/ui/chat/btn_addtab01_over.tga")
			btnChatAddTab.SetDownVisual("d:/ymir work/ui/chat/btn_addtab01_down.tga")
			btnChatAddTab.SetToolTipText(localeInfo.CHATTING_SETTING_ADD, 0, -23)
			btnChatAddTab.SetEvent(ui.__mem_func__(self.__AddNewTab))
			btnChatAddTab.Show()
			self.btnChatAddTab = btnChatAddTab
		else:
			imgChatBarLeft = ui.ImageBox()
			imgChatBarLeft.SetParent(self.btnChatSizing)
			imgChatBarLeft.AddFlag("not_pick")
			imgChatBarLeft.LoadImage("d:/ymir work/ui/pattern/chat_bar_left.tga")
			imgChatBarLeft.Show()
			self.imgChatBarLeft = imgChatBarLeft
			imgChatBarRight = ui.ImageBox()
			imgChatBarRight.SetParent(self.btnChatSizing)
			imgChatBarRight.AddFlag("not_pick")
			imgChatBarRight.LoadImage("d:/ymir work/ui/pattern/chat_bar_right.tga")
			imgChatBarRight.Show()
			self.imgChatBarRight = imgChatBarRight
			imgChatBarMiddle = ui.ExpandedImageBox()
			imgChatBarMiddle.SetParent(self.btnChatSizing)
			imgChatBarMiddle.AddFlag("not_pick")
			imgChatBarMiddle.LoadImage("d:/ymir work/ui/pattern/chat_bar_middle.tga")
			imgChatBarMiddle.Show()
			self.imgChatBarMiddle = imgChatBarMiddle

		scrollBar = ui.ScrollBar()
		scrollBar.AddFlag("float")
		scrollBar.SetScrollEvent(ui.__mem_func__(self.OnScroll))
		self.scrollBar = scrollBar

		self.Refresh()
		if app.ENABLE_CHATTING_WINDOW_RENEWAL:
			self.RefreshChatWindow()
		self.chatInputSet.RefreshPosition() # RTL �� ��ġ�� ����� �������� ��ġ ������ �ʿ��ϴ�
	
	def __del__(self):
		ui.Window.__del__(self)

	def __RegisterChatColorDict(self):
		CHAT_COLOR_DICT = {
			chat.CHAT_TYPE_TALKING : colorInfo.CHAT_RGB_TALK,
			chat.CHAT_TYPE_INFO : colorInfo.CHAT_RGB_INFO,
			chat.CHAT_TYPE_NOTICE : colorInfo.CHAT_RGB_NOTICE,
			chat.CHAT_TYPE_PARTY : colorInfo.CHAT_RGB_PARTY,
			chat.CHAT_TYPE_GUILD : colorInfo.CHAT_RGB_GUILD,
			chat.CHAT_TYPE_COMMAND : colorInfo.CHAT_RGB_COMMAND,
			chat.CHAT_TYPE_SHOUT : colorInfo.CHAT_RGB_SHOUT,
			chat.CHAT_TYPE_WHISPER : colorInfo.CHAT_RGB_WHISPER,
		}

		if app.ENABLE_CHATTING_WINDOW_RENEWAL:
			CHAT_COLOR_DICT.update({
				chat.CHAT_TYPE_EXP_INFO : colorInfo.CHAT_RGB_INFO,
				chat.CHAT_TYPE_ITEM_INFO : colorInfo.CHAT_RGB_INFO,
				chat.CHAT_TYPE_MONEY_INFO : colorInfo.CHAT_RGB_INFO,
			})

		for colorItem in CHAT_COLOR_DICT.items():
			type=colorItem[0]
			rgb=colorItem[1]
			chat.SetChatColor(type, rgb[0], rgb[1], rgb[2])

	def Destroy(self):
		self.chatInputSet.Destroy()
		self.chatInputSet = None

		self.btnSendWhisper = 0
		self.btnChatLog = 0
		self.btnChatSizing = 0

		if app.ENABLE_CHATTING_WINDOW_RENEWAL:
			for i in range(self.MAX_TAB_NUMBER):
				if i in self.userDefinedTabs:
					del self.userDefinedTabs[i]
				if i in self.userDefinedTabLogs:
					del self.userDefinedTabLogs[i]

			self.userDefinedTabs = {}
			self.userDefinedTabLogs = {}

			self.btnChatTab = None
			self.btnChatSettingOption = None
			self.btnChatAddTab = None

			if self.wndChatSettingOption:
				self.wndChatSettingOption.Close()
				self.wndChatSettingOption = None

	################
	## Open & Close
	def OpenChat(self):
		self.SetSize(self.CHAT_WINDOW_WIDTH, self.EDIT_LINE_HEIGHT)
		chat.SetBoardState(self.chatID, chat.BOARD_STATE_EDIT)
		self.boardState = chat.BOARD_STATE_EDIT

		(x, y, width, height) = self.GetRect()
		(btnX, btnY) = self.btnChatSizing.GetGlobalPosition()

		if localeInfo.IsARABIC():
			chat.SetPosition(self.chatID, x + width - 10, y)
		else:
			chat.SetPosition(self.chatID, x + 10, y)

		chat.SetHeight(self.chatID, y - btnY - self.EDIT_LINE_HEIGHT + 100)

		if self.IsShow():
			self.btnChatSizing.Show()

		self.Refresh()
		if app.ENABLE_CHATTING_WINDOW_RENEWAL:
			self.__SelectTab(self.selectedTab, True)

		self.btnSendWhisper.SetPosition(self.GetWidth() - 50, 2)
		self.btnSendWhisper.Show()

		self.btnChatLog.SetPosition(self.GetWidth() - 25, 2)
		self.btnChatLog.Show()

		self.chatInputSet.Open()
		self.chatInputSet.SetTop()
		self.SetTop()

	def CloseChat(self):
		chat.SetBoardState(self.chatID, chat.BOARD_STATE_VIEW)
		self.boardState = chat.BOARD_STATE_VIEW

		(x, y, width, height) = self.GetRect()

		if localeInfo.IsARABIC():
			chat.SetPosition(self.chatID, x + width - 10, y + self.EDIT_LINE_HEIGHT)
		else:
			chat.SetPosition(self.chatID, x + 10, y + self.EDIT_LINE_HEIGHT)

		self.SetSize(self.CHAT_WINDOW_WIDTH, 0)

		self.chatInputSet.Close()
		self.btnSendWhisper.Hide()
		self.btnChatLog.Hide()
		self.btnChatSizing.Hide()

		self.Refresh()
		if app.ENABLE_CHATTING_WINDOW_RENEWAL:
			self.RefreshChatWindow()

	def SetSendWhisperEvent(self, event):
		self.btnSendWhisper.SetEvent(event)

	def SetOpenChatLogEvent(self, event):
		self.btnChatLog.SetEvent(event)

	def IsEditMode(self):
		if chat.BOARD_STATE_EDIT == self.boardState:
			return True

		return False

	def __RefreshSizingBar(self):
		(x, y, width, height) = self.GetRect()
		gxChat, gyChat = self.btnChatSizing.GetGlobalPosition()
		self.btnChatSizing.SetPosition(x, gyChat)
		self.btnChatSizing.SetSize(width, 22)
		if app.ENABLE_CHATTING_WINDOW_RENEWAL:
			self.imgChatBarLeft.SetPosition(0, 17)
			self.imgChatBarRight.SetPosition(width - 57, 0)

			self.btnChatTab.SetPosition(4, 0)

			index = 1
			for i in range(self.MAX_TAB_NUMBER):
				if i in self.userDefinedTabs:
					tabBtn = self.userDefinedTabs[i]
					if tabBtn.IsShow():
						tabBtn.SetPosition(4 + 54 * index, 0)
						index = index + 1

			plusWidth = 54 * (index - 1)

			self.imgChatBarMiddle.SetPosition(57.0 + plusWidth, 0)
			self.imgChatBarMiddle.SetRenderingRect(0.0, 0.0, float(width - 57.0 * 2 - plusWidth) / 57.0 - 1.0, 0.0)

			self.btnChatSettingOption.SetPosition(width - 27, 3)
			self.btnChatAddTab.SetPosition(width - 27 - 22, 3)
		else:
			self.imgChatBarLeft.SetPosition(0, 0)
			self.imgChatBarRight.SetPosition(width - 64, 0)
			self.imgChatBarMiddle.SetPosition(64, 0)
			self.imgChatBarMiddle.SetRenderingRect(0.0, 0.0, float(width - 128) / 64.0 - 1.0, 0.0)

	def SetPosition(self, x, y):
		ui.Window.SetPosition(self, x, y)
		self.__RefreshSizingBar()

	def SetSize(self, width, height):
		ui.Window.SetSize(self, width, height)
		self.__RefreshSizingBar()

	def SetHeight(self, height):
		gxChat, gyChat = self.btnChatSizing.GetGlobalPosition()
		self.btnChatSizing.SetPosition(gxChat, wndMgr.GetScreenHeight() - height)
		self.btnChatSizing.SetResizeDic({"position" : (Expr("SCREEN_WIDTH")/2 - self.CHAT_WINDOW_WIDTH/2, Expr("SCREEN_HEIGHT") - height)})


	###########
	## Refresh
	def Refresh(self):
		if self.boardState == chat.BOARD_STATE_EDIT:
			self.RefreshBoardEditState()
		elif self.boardState == chat.BOARD_STATE_VIEW:
			self.RefreshBoardViewState()
		self.btnChatSizing.SetRestrictMovementArea(0, 0, Expr("SCREEN_WIDTH")*5, Expr("SCREEN_HEIGHT")*5)

	def RefreshBoardEditState(self):

		(x, y, width, height) = self.GetRect()
		(btnX, btnY) = self.btnChatSizing.GetGlobalPosition()

		self.xBar = x
		self.yBar = btnY
		self.widthBar = width
		self.heightBar = y - btnY + self.EDIT_LINE_HEIGHT
		self.curHeightBar = self.heightBar

		if localeInfo.IsARABIC():
			chat.SetPosition(self.chatID, x + width - 10, y)
		else:
			chat.SetPosition(self.chatID, x + 10, y)

		chat.SetHeight(self.chatID, y - btnY - self.EDIT_LINE_HEIGHT)
		chat.ArrangeShowingChat(self.chatID)

		if btnY > y:
			self.btnChatSizing.SetPosition(btnX, y)
			self.heightBar = self.EDIT_LINE_HEIGHT

	def RefreshBoardViewState(self):
		(x, y, width, height) = self.GetRect()
		(btnX, btnY) = self.btnChatSizing.GetGlobalPosition()
		# GetTotalLineCount (not visibleLineCount) so wrapped multi-line messages get a
		# background bar tall enough to actually cover every rendered line.
		textAreaHeight = chat.GetTotalLineCount(self.chatID) * chat.GetLineStep(self.chatID)

		if localeInfo.IsARABIC():
			chat.SetPosition(self.chatID, x + width - 10, y + self.EDIT_LINE_HEIGHT)
		else:
			chat.SetPosition(self.chatID, x + 10, y + self.EDIT_LINE_HEIGHT)

		chat.SetHeight(self.chatID, y - btnY - self.EDIT_LINE_HEIGHT + 100)

		if self.boardState == chat.BOARD_STATE_EDIT:
			textAreaHeight += 45
		elif self.visibleLineCount != 0:
			textAreaHeight += 10 + 10
		
		self.xBar = x
		self.yBar = y + self.EDIT_LINE_HEIGHT - textAreaHeight
		self.widthBar = width
		self.heightBar = textAreaHeight

		self.scrollBar.Hide()

	##########
	## Render
	def OnUpdate(self):
		if self.boardState == chat.BOARD_STATE_EDIT:
			chat.Update(self.chatID)
		elif self.boardState == chat.BOARD_STATE_VIEW:
			if systemSetting.IsViewChat():
				chat.Update(self.chatID)

	def OnRender(self):
		if chat.GetVisibleLineCount(self.chatID) != self.visibleLineCount:
			self.visibleLineCount = chat.GetVisibleLineCount(self.chatID)
			self.Refresh()

		if self.curHeightBar != self.heightBar:
			self.curHeightBar += (self.heightBar - self.curHeightBar) / 10

		if self.boardState == chat.BOARD_STATE_EDIT:
			grp.SetColor(self.BOARD_MIDDLE_COLOR)
			if app.ENABLE_CHATTING_WINDOW_RENEWAL:
				grp.RenderBar(self.xBar, self.yBar + (self.heightBar - self.curHeightBar) + self.EDIT_LINE_HIDE_HEIGHT, self.widthBar, self.curHeightBar)
			else:
				grp.RenderBar(self.xBar, self.yBar + (self.heightBar - self.curHeightBar) + 10, self.widthBar, self.curHeightBar)
			chat.Render(self.chatID)
		elif self.boardState == chat.BOARD_STATE_VIEW:
			if systemSetting.IsViewChat():
				grp.RenderGradationBar(self.xBar, self.yBar + (self.heightBar - self.curHeightBar), self.widthBar, self.curHeightBar, self.BOARD_START_COLOR, self.BOARD_END_COLOR)
				chat.Render(self.chatID)

	##########
	## Event
	def OnTop(self):
		self.btnChatSizing.SetTop()
		self.scrollBar.SetTop()

	def OnScroll(self):
		if not self.scrollLock:
			self.scrollBarPos = self.scrollBar.GetPos()

		lineCount = chat.GetLineCount(self.chatID)
		visibleLineCount = chat.GetVisibleLineCount(self.chatID)
		endLine = visibleLineCount + int(float(lineCount - visibleLineCount) * self.scrollBarPos)

		chat.SetEndPos(self.chatID, self.scrollBarPos)

	def OnChangeChatMode(self):
		self.chatInputSet.OnChangeChatMode()

	def SetChatFocus(self):
		self.chatInputSet.SetChatFocus()			

	def BindInterface(self, interface):
		self.interface = interface
		self.chatInputSet.BindInterface(interface)

	if app.ENABLE_CHATTING_WINDOW_RENEWAL:
		def CreateTab(self, tooltip, tabIndex = -1):
			btnChatTab = ui.ToggleButton()
			btnChatTab.SetParent(self.btnChatSizing)
			btnChatTab.SetUpVisual("d:/ymir work/ui/chat/chatmenutab_default.tga")
			btnChatTab.SetOverVisual("d:/ymir work/ui/chat/chatmenutab_down.tga")
			btnChatTab.SetDownVisual("d:/ymir work/ui/chat/chatmenutab_down.tga")
			btnChatTab.SetToolTipText(tooltip, 0, -23)
			btnChatTab.SetTextAddPos(tooltip, -2)
			btnChatTab.SetToggleUpEvent(ui.__mem_func__(self.__SelectTab), tabIndex)
			btnChatTab.SetToggleDownEvent(ui.__mem_func__(self.__SelectTab), tabIndex)
			btnChatTab.Show()
			return btnChatTab

		def HideTab(self, tabIndex):
			self.userDefinedTabs[tabIndex].Hide()
			self.__RefreshSizingBar()

		def ShowTab(self, tabIndex):
			self.userDefinedTabs[tabIndex].Show()
			self.userDefinedTabs[tabIndex].SetUp()
			self.__RefreshSizingBar()

			if tabIndex in self.userDefinedTabLogs:
				self.userDefinedTabLogs[tabIndex].Hide()
				del self.userDefinedTabLogs[tabIndex]

		def DeleteTab(self, tabIndex):
			del self.userDefinedTabs[tabIndex]
			self.__RefreshSizingBar()

			self.wndChatSettingOption.DeleteOptionFile(tabIndex + 1)

			if tabIndex in self.userDefinedTabLogs:
				self.userDefinedTabLogs[tabIndex].Hide()
				del self.userDefinedTabLogs[tabIndex]

		def SetTabName(self, tabIndex, title):
			if tabIndex in self.userDefinedTabs:
				if title == "":
					title = str(tabIndex + 1)
				self.userDefinedTabs[tabIndex].SetToolTipText(title, 0, -23)
				self.userDefinedTabs[tabIndex].SetTextAddPos(title, -2)
				self.__RefreshSizingBar()

		def GetTabName(self, tabIndex):
			if tabIndex in self.userDefinedTabs:
				return self.userDefinedTabs[tabIndex].GetText()
			return ""

		def __AddNewTab(self):
			freeIndex = -1
			for i in range(self.MAX_TAB_NUMBER):
				if i not in self.userDefinedTabs:
					freeIndex = i
					break
			if freeIndex == -1:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CHATTING_SETTING_ADD_MAX)
				return

			tab = self.CreateTab(str(freeIndex + 1), freeIndex)
			self.userDefinedTabs[freeIndex] = tab
			self.__RefreshSizingBar()

			if self.wndChatSettingOption:
				self.wndChatSettingOption.CreateTabFile(freeIndex + 1)

		def AddTab(self, index, name):
			if index == -1:
				return
			tab = self.CreateTab(name, index)
			self.userDefinedTabs[index] = tab

		def __SelectTab(self, tabIndex, forceSelect = False):
			if not forceSelect and (app.IsPressed(app.DIK_LCONTROL) or (tabIndex > -1 and tabIndex == self.selectedTab)):
				self.__OpenTab(tabIndex)
				return

			self.btnChatTab.SetUp()
			for i in range(self.MAX_TAB_NUMBER):
				if i in self.userDefinedTabs:
					self.userDefinedTabs[i].SetUp()

			if tabIndex in self.userDefinedTabs:
				self.userDefinedTabs[tabIndex].Down()
			else:
				tabIndex = -1
				self.btnChatTab.Down()

			self.wndChatSettingOption.SetSelectedChat(tabIndex)
			self.selectedTab = tabIndex
			self.RefreshChatWindow()

		def isOverlap(self, a, b):
			return a[0] < b[0] + b[2] and a[0] + a[2] > b[0] and a[1] < b[1] + b[3] and a[1] + a[3] > b[1]

		def __OpenTab(self, tabIndex):
			self.HideTab(tabIndex)
			newTab = ChatLogTabWindow(self, tabIndex)
			newTab.BindInterface(self.interface)
			newTab.Open()

			xPosition = 0
			yPosition = 0
			screenWidth = wndMgr.GetScreenWidth()
			screenHeight = wndMgr.GetScreenHeight()

			if tabIndex == self.selectedTab:
				leftTab = -1
				if tabIndex > 0:
					for i in range(tabIndex - 1, -1, -1):
						if i in self.userDefinedTabs:
							leftTab = i
							break
				self.__SelectTab(leftTab, True)

			isDownOne = False
			for i in range(self.MAX_TAB_NUMBER):
				if i in self.userDefinedTabs:
					if self.userDefinedTabs[i].IsDown():
						isDownOne = True
						break
			if not isDownOne:
				self.__SelectTab(-1, True)

			usedPositions = []
			for i in range(self.MAX_TAB_NUMBER):
				if i in self.userDefinedTabLogs:
					elem = self.userDefinedTabLogs[i]
					ex, ey = elem.GetGlobalPosition()
					ewidth = elem.GetWidth()
					eheight = elem.GetHeight()
					usedPositions.append([ex - 10, ey - 10, ewidth + 10, eheight + 10])

			if len(usedPositions) > 0:
				for y in range(20, screenHeight, 20):
					for x in range(20, screenWidth, 10):
						thisPosition = [x, y, newTab.GetWidth(), newTab.GetHeight()]

						if x > screenWidth - thisPosition[2]:
							break

						maxXInRow = 0
						posIsOk = True
						for p in usedPositions:
							if self.isOverlap(p, thisPosition):
								posIsOk = False
								if p[0] + p[2] > maxXInRow:
									maxXInRow = p[0] + p[2]

						if posIsOk:
							xPosition = x
							yPosition = y
						else:
							x = maxXInRow

						if xPosition + yPosition > 0:
							break

					if xPosition + yPosition > 0:
						break

				if xPosition + yPosition > 0:
					newTab.SetPosition(xPosition, yPosition)

			self.userDefinedTabLogs[tabIndex] = newTab

		def __SettingOptionWndOpen(self):
			if self.wndChatSettingOption:
				if self.wndChatSettingOption.IsShow():
					self.wndChatSettingOption.Close()
				else:
					self.wndChatSettingOption.Open(self.selectedTab + 1)

		def RefreshChatWindow(self, tabIndex = -1):
			selectedChatId = self.chatID

			if tabIndex == -1:
				tabIndex = self.selectedTab
			else:
				selectedChatId = chat.CHAT_SET_LOG_WINDOW + tabIndex + 1

			if self.wndChatSettingOption:
				for mode in OPTION_CHECKBOX_MODE.iterkeys():
					enable = self.wndChatSettingOption.GetChatModeSetting(tabIndex + 1, mode)
					if enable:
						chat.EnableChatMode(selectedChatId, mode)
					else:
						chat.DisableChatMode(selectedChatId, mode)

## ChatLogWindow
class ChatLogWindow(ui.Window):

	BLOCK_WIDTH = 32
	CHAT_MODE_NAME = ( localeInfo.CHAT_NORMAL, localeInfo.CHAT_PARTY, localeInfo.CHAT_GUILD, localeInfo.CHAT_SHOUT, localeInfo.CHAT_INFORMATION, localeInfo.CHAT_NOTICE, )
	CHAT_MODE_INDEX = ( chat.CHAT_TYPE_TALKING,
						chat.CHAT_TYPE_PARTY,
						chat.CHAT_TYPE_GUILD,
						chat.CHAT_TYPE_SHOUT,
						chat.CHAT_TYPE_INFO,
						chat.CHAT_TYPE_NOTICE, )

	CHAT_LOG_WINDOW_MINIMUM_WIDTH = 450
	CHAT_LOG_WINDOW_MINIMUM_HEIGHT = 120

	class ResizeButton(ui.DragButton):

		def __init__(self):
			ui.DragButton.__init__(self)

		def __del__(self):
			ui.DragButton.__del__(self)

		def OnMouseOverIn(self):
			app.SetCursor(app.HVSIZE)

		def OnMouseOverOut(self):
			app.SetCursor(app.NORMAL)

	def __init__(self):

		self.allChatMode = True
		self.chatInputSet = None

		ui.Window.__init__(self)
		self.AddFlag("float")
		self.AddFlag("movable")
		self.SetWindowName("ChatLogWindow")
		self.__CreateChatInputSet()
		self.__CreateWindow()
		self.__CreateButton()
		self.__CreateScrollBar()

		self.chatID = chat.CreateChatSet(chat.CHAT_SET_LOG_WINDOW)
		chat.SetBoardState(self.chatID, chat.BOARD_STATE_LOG)
		for i in self.CHAT_MODE_INDEX:
			chat.EnableChatMode(self.chatID, i)

		if app.ENABLE_CHATTING_WINDOW_RENEWAL:
			chat.EnableChatMode(self.chatID, chat.CHAT_TYPE_EXP_INFO)
			chat.EnableChatMode(self.chatID, chat.CHAT_TYPE_ITEM_INFO)
			chat.EnableChatMode(self.chatID, chat.CHAT_TYPE_MONEY_INFO)

		self.SetPosition(20, 20)
		self.SetSize(self.CHAT_LOG_WINDOW_MINIMUM_WIDTH, self.CHAT_LOG_WINDOW_MINIMUM_HEIGHT)
		self.btnSizing.SetPosition(self.CHAT_LOG_WINDOW_MINIMUM_WIDTH-self.btnSizing.GetWidth(), self.CHAT_LOG_WINDOW_MINIMUM_HEIGHT-self.btnSizing.GetHeight()+2)

		self.OnResize()

	def __CreateChatInputSet(self):
		chatInputSet = ChatInputSet()
		chatInputSet.SetParent(self)
		chatInputSet.SetEscapeEvent(ui.__mem_func__(self.Close))
		chatInputSet.SetWindowVerticalAlignBottom()
		chatInputSet.Open()
		self.chatInputSet = chatInputSet

	def __CreateWindow(self):
		imgLeft = ui.ImageBox()
		imgLeft.AddFlag("not_pick")
		imgLeft.SetParent(self)				

		imgCenter = ui.ExpandedImageBox()
		imgCenter.AddFlag("not_pick")
		imgCenter.SetParent(self)
		
		imgRight = ui.ImageBox()
		imgRight.AddFlag("not_pick")
		imgRight.SetParent(self)			
		
		if localeInfo.IsARABIC():
			imgLeft.LoadImage("locale/ae/ui/pattern/titlebar_left.tga")
			imgCenter.LoadImage("locale/ae/ui/pattern/titlebar_center.tga")
			imgRight.LoadImage("locale/ae/ui/pattern/titlebar_right.tga")
		else:
			imgLeft.LoadImage("d:/ymir work/ui/pattern/chatlogwindow_titlebar_left.tga")
			imgCenter.LoadImage("d:/ymir work/ui/pattern/chatlogwindow_titlebar_middle.tga")
			imgRight.LoadImage("d:/ymir work/ui/pattern/chatlogwindow_titlebar_right.tga")		

		imgLeft.Show()
		imgCenter.Show()
		imgRight.Show()

		btnClose = ui.Button()
		btnClose.SetParent(self)
		btnClose.SetUpVisual("d:/ymir work/ui/public/close_button_01.sub")
		btnClose.SetOverVisual("d:/ymir work/ui/public/close_button_02.sub")
		btnClose.SetDownVisual("d:/ymir work/ui/public/close_button_03.sub")
		btnClose.SetToolTipText(localeInfo.UI_CLOSE, 0, -23)
		btnClose.SetEvent(ui.__mem_func__(self.Close))
		btnClose.Show()

		btnSizing = self.ResizeButton()
		btnSizing.SetParent(self)
		btnSizing.SetMoveEvent(ui.__mem_func__(self.OnResize))
		btnSizing.SetSize(16, 16)
		btnSizing.Show()

		titleName = ui.TextLine()
		titleName.SetParent(self)
		
		if localeInfo.IsARABIC():
			titleName.SetPosition(self.GetWidth()-20, 6)
		else:
			titleName.SetPosition(20, 6)
			
		titleName.SetText(localeInfo.CHAT_LOG_TITLE)
		titleName.Show()

		self.imgLeft = imgLeft
		self.imgCenter = imgCenter
		self.imgRight = imgRight
		self.btnClose = btnClose
		self.btnSizing = btnSizing
		self.titleName = titleName

	def __CreateButton(self):
	
		if localeInfo.IsARABIC():
			bx = 20
		else:
			bx = 13

		btnAll = ui.RadioButton()
		btnAll.SetParent(self)
		btnAll.SetPosition(bx, 24)
		btnAll.SetUpVisual("d:/ymir work/ui/public/xsmall_button_01.sub")
		btnAll.SetOverVisual("d:/ymir work/ui/public/xsmall_button_02.sub")
		btnAll.SetDownVisual("d:/ymir work/ui/public/xsmall_button_03.sub")
		btnAll.SetText(localeInfo.CHAT_ALL)
		btnAll.SetEvent(ui.__mem_func__(self.ToggleAllChatMode))
		btnAll.Down()
		btnAll.Show()
		self.btnAll = btnAll

		x = bx + 48
		i = 0
		self.modeButtonList = []
		for name in self.CHAT_MODE_NAME:
			btn = ui.ToggleButton()
			btn.SetParent(self)
			btn.SetPosition(x, 24)
			btn.SetUpVisual("d:/ymir work/ui/public/xsmall_button_01.sub")
			btn.SetOverVisual("d:/ymir work/ui/public/xsmall_button_02.sub")
			btn.SetDownVisual("d:/ymir work/ui/public/xsmall_button_03.sub")
			btn.SetText(name)
			btn.Show()

			mode = self.CHAT_MODE_INDEX[i]
			btn.SetToggleUpEvent(lambda arg=mode: self.ToggleChatMode(arg))
			btn.SetToggleDownEvent(lambda arg=mode: self.ToggleChatMode(arg))
			self.modeButtonList.append(btn)

			x += 48
			i += 1

	def __CreateScrollBar(self):
		scrollBar = ui.SmallThinScrollBar()
		scrollBar.SetParent(self)
		scrollBar.Show()
		scrollBar.SetScrollEvent(ui.__mem_func__(self.OnScroll))
		self.scrollBar = scrollBar
		self.scrollBarPos = 1.0

	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		self.imgLeft = None
		self.imgCenter = None
		self.imgRight = None
		self.btnClose = None
		self.btnSizing = None
		self.modeButtonList = []
		self.scrollBar = None
		self.chatInputSet = None

	def ToggleAllChatMode(self):
		if self.allChatMode:
			return

		self.allChatMode = True

		for i in self.CHAT_MODE_INDEX:
			chat.EnableChatMode(self.chatID, i)
		if app.ENABLE_CHATTING_WINDOW_RENEWAL:
			chat.EnableChatMode(self.chatID, chat.CHAT_TYPE_EXP_INFO)
			chat.EnableChatMode(self.chatID, chat.CHAT_TYPE_ITEM_INFO)
			chat.EnableChatMode(self.chatID, chat.CHAT_TYPE_MONEY_INFO)
		for btn in self.modeButtonList:
			btn.SetUp()

	def ToggleChatMode(self, mode):
		if self.allChatMode:
			self.allChatMode = False

			for i in self.CHAT_MODE_INDEX:
				chat.DisableChatMode(self.chatID, i)

			chat.EnableChatMode(self.chatID, mode)
			if app.ENABLE_CHATTING_WINDOW_RENEWAL:
				if mode == chat.CHAT_TYPE_INFO:
					chat.EnableChatMode(self.chatID, chat.CHAT_TYPE_EXP_INFO)
					chat.EnableChatMode(self.chatID, chat.CHAT_TYPE_ITEM_INFO)
					chat.EnableChatMode(self.chatID, chat.CHAT_TYPE_MONEY_INFO)
			self.btnAll.SetUp()
		else:
			chat.ToggleChatMode(self.chatID, mode)
			
			if not chat.GetChatMode(self.chatID):
				self.btnAll.Down()
				self.ToggleAllChatMode()

	def SetSize(self, width, height):
		self.imgCenter.SetRenderingRect(0.0, 0.0, float((width - self.BLOCK_WIDTH*2) - self.BLOCK_WIDTH) / self.BLOCK_WIDTH, 0.0)
		self.imgCenter.SetPosition(self.BLOCK_WIDTH, 0)
		self.imgRight.SetPosition(width - self.BLOCK_WIDTH, 0)
		
		if localeInfo.IsARABIC():
			self.titleName.SetPosition(self.GetWidth()-20, 3)
			self.btnClose.SetPosition(3, 3)
			self.scrollBar.SetPosition(1, 45)
		else:
			self.btnClose.SetPosition(width - self.btnClose.GetWidth() - 5, 5)			
			self.scrollBar.SetPosition(width - 15, 45)
			
		self.scrollBar.SetScrollBarSize(height - 45 - 12)
		self.scrollBar.SetPos(self.scrollBarPos)
		ui.Window.SetSize(self, width, height)

	def Open(self):
		self.OnResize()
		self.chatInputSet.SetChatFocus()
		self.Show()

		if app.__BL_MOUSE_WHEEL_TOP_WINDOW__:
			wndMgr.SetWheelTopWindow(self.hWnd)

	def Close(self):
		if self.chatInputSet:
			self.chatInputSet.KillChatFocus()
		self.Hide()

		if app.__BL_MOUSE_WHEEL_TOP_WINDOW__:
			wndMgr.ClearWheelTopWindow()

	if app.__BL_MOUSE_WHEEL_TOP_WINDOW__:
		def OnMouseWheelButtonUp(self):
			if self.scrollBar and self.scrollBar.IsShow():
				self.scrollBar.OnUp()
				return True
			return False

		def OnMouseWheelButtonDown(self):
			if self.scrollBar and self.scrollBar.IsShow():
				self.scrollBar.OnDown()
				return True
			return False

	def OnResize(self):
		x, y = self.btnSizing.GetLocalPosition()
		width = self.btnSizing.GetWidth()
		height = self.btnSizing.GetHeight()

		if x < self.CHAT_LOG_WINDOW_MINIMUM_WIDTH - width:
			self.btnSizing.SetPosition(self.CHAT_LOG_WINDOW_MINIMUM_WIDTH - width, y)
			return
		if y < self.CHAT_LOG_WINDOW_MINIMUM_HEIGHT - height:
			self.btnSizing.SetPosition(x, self.CHAT_LOG_WINDOW_MINIMUM_HEIGHT - height)
			return

		self.scrollBar.LockScroll()
		self.SetSize(x + width, y + height)
		self.scrollBar.UnlockScroll()

		if localeInfo.IsARABIC():
			self.chatInputSet.SetPosition(20, 25)
		else:
			self.chatInputSet.SetPosition(0, 25)
			
		self.chatInputSet.SetSize(self.GetWidth() - 20, 20)
		self.chatInputSet.RefreshPosition()
		self.chatInputSet.SetChatMax(self.GetWidth() / 8)

	def OnScroll(self):
		self.scrollBarPos = self.scrollBar.GetPos()

		lineCount = chat.GetLineCount(self.chatID)
		visibleLineCount = chat.GetVisibleLineCount(self.chatID)
		endLine = visibleLineCount + int(float(lineCount - visibleLineCount) * self.scrollBarPos)

		chat.SetEndPos(self.chatID, self.scrollBarPos)

	def OnRender(self):
		(x, y, width, height) = self.GetRect()
		
		if localeInfo.IsARABIC():
			grp.SetColor(0x77000000)
			grp.RenderBar(x+2, y+45, 13, height-45)
			
			grp.SetColor(0x77000000)
			grp.RenderBar(x, y, width, height)
			grp.SetColor(0x77000000)
			grp.RenderBox(x, y, width-2, height)
			grp.SetColor(0x77000000)
			grp.RenderBox(x+1, y+1, width-2, height)

			grp.SetColor(0xff989898)
			grp.RenderLine(x+width-13, y+height-1, 11, -11)
			grp.RenderLine(x+width-9, y+height-1, 7, -7)
			grp.RenderLine(x+width-5, y+height-1, 3, -3)
		else:
			grp.SetColor(0x77000000)
			grp.RenderBar(x+width-15, y+45, 13, height-45)

			grp.SetColor(0x77000000)
			grp.RenderBar(x, y, width, height)
			grp.SetColor(0x77000000)
			grp.RenderBox(x, y, width-2, height)
			grp.SetColor(0x77000000)
			grp.RenderBox(x+1, y+1, width-2, height)

			grp.SetColor(0xff989898)
			grp.RenderLine(x+width-13, y+height-1, 11, -11)
			grp.RenderLine(x+width-9, y+height-1, 7, -7)
			grp.RenderLine(x+width-5, y+height-1, 3, -3)

		#####

		chat.ArrangeShowingChat(self.chatID)

		if localeInfo.IsARABIC():
			chat.SetPosition(self.chatID, x + width - 10, y + height - 25)
		else:
			chat.SetPosition(self.chatID, x + 10, y + height - 25)

		chat.SetHeight(self.chatID, height - 45 - 25)
		chat.Update(self.chatID)
		chat.Render(self.chatID)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def BindInterface(self, interface):
		self.interface = interface

	def OnMouseLeftButtonDown(self):
		hyperlink = ui.GetHyperlink()
		if hyperlink:
			if app.IsPressed(app.DIK_LALT):
				link = chat.GetLinkFromHyperlink(hyperlink)
				ime.PasteString(link)
			else:
				self.interface.MakeHyperlinkTooltip(hyperlink)

if app.ENABLE_CHATTING_WINDOW_RENEWAL:
	CHECK_BOX_X_POS = 145

	OPTION_CHECKBOX_TALKING = 1
	OPTION_CHECKBOX_PARTY = 2
	OPTION_CHECKBOX_GUILD = 3
	OPTION_CHECKBOX_SHOUT = 4
	OPTION_CHECKBOX_INFO = 5
	OPTION_CHECKBOX_NOTICE = 6
	OPTION_CHECKBOX_EXP_INFO = 7
	OPTION_CHECKBOX_ITEM_INFO = 8
	OPTION_CHECKBOX_MONEY_INFO = 9

	OPTION_CHECKBOX_MODE = {
		chat.CHAT_TYPE_TALKING : OPTION_CHECKBOX_TALKING,
		chat.CHAT_TYPE_INFO : OPTION_CHECKBOX_INFO,
		chat.CHAT_TYPE_NOTICE : OPTION_CHECKBOX_NOTICE,
		chat.CHAT_TYPE_PARTY : OPTION_CHECKBOX_PARTY,
		chat.CHAT_TYPE_GUILD : OPTION_CHECKBOX_GUILD,
		chat.CHAT_TYPE_SHOUT : OPTION_CHECKBOX_SHOUT,
		chat.CHAT_TYPE_EXP_INFO : OPTION_CHECKBOX_EXP_INFO,
		chat.CHAT_TYPE_ITEM_INFO : OPTION_CHECKBOX_ITEM_INFO,
		chat.CHAT_TYPE_MONEY_INFO : OPTION_CHECKBOX_MONEY_INFO,
	}

	## ChatLogTabWindow
	class ChatLogTabWindow(ui.Window):

		BLOCK_WIDTH = 32

		CHAT_LOG_WINDOW_MINIMUM_WIDTH = 450
		CHAT_LOG_WINDOW_MINIMUM_HEIGHT = 116

		class ResizeButton(ui.DragButton):

			def __init__(self):
				ui.DragButton.__init__(self)

			def __del__(self):
				ui.DragButton.__del__(self)

			def OnMouseOverIn(self):
				app.SetCursor(app.HVSIZE)

			def OnMouseOverOut(self):
				app.SetCursor(app.NORMAL)

		def __init__(self, chatWindow, chatIndex = 0):
			ui.Window.__init__(self)
			self.AddFlag("float")
			self.AddFlag("movable")
			self.SetWindowName("ChatLogTabWindow")

			self.interface = 0
			self.chatWindow = chatWindow
			self.chatIndex = chatIndex

			self.__CreateWindow()
			self.__CreateScrollBar()

			self.chatID = chat.CreateChatSet(chat.CHAT_SET_LOG_WINDOW + chatIndex + 1)
			chat.SetBoardState(self.chatID, chat.BOARD_STATE_LOG)

			self.chatWindow.RefreshChatWindow(self.chatIndex)

			self.SetPosition(20, 20)
			self.SetSize(self.CHAT_LOG_WINDOW_MINIMUM_WIDTH, self.CHAT_LOG_WINDOW_MINIMUM_HEIGHT)
			self.btnSizing.SetPosition(self.CHAT_LOG_WINDOW_MINIMUM_WIDTH-self.btnSizing.GetWidth(), self.CHAT_LOG_WINDOW_MINIMUM_HEIGHT-self.btnSizing.GetHeight()+2)

			self.OnResize()

		def __CreateWindow(self):
			imgLeft = ui.ImageBox()
			imgLeft.AddFlag("not_pick")
			imgLeft.SetParent(self)

			imgCenter = ui.ExpandedImageBox()
			imgCenter.AddFlag("not_pick")
			imgCenter.SetParent(self)

			imgRight = ui.ImageBox()
			imgRight.AddFlag("not_pick")
			imgRight.SetParent(self)

			imgLeft.LoadImage("d:/ymir work/ui/chat/titlebar_chat_left.tga")
			imgCenter.LoadImage("d:/ymir work/ui/chat/titlebar_chat_middle.tga")
			imgRight.LoadImage("d:/ymir work/ui/chat/titlebar_chat_right.tga")

			imgLeft.Show()
			imgCenter.Show()
			imgRight.Show()

			btnClose = ui.Button()
			btnClose.SetParent(self)
			btnClose.SetUpVisual("d:/ymir work/ui/public/close_button_01.sub")
			btnClose.SetOverVisual("d:/ymir work/ui/public/close_button_02.sub")
			btnClose.SetDownVisual("d:/ymir work/ui/public/close_button_03.sub")
			btnClose.SetToolTipText(localeInfo.UI_CLOSE, 0, -23)
			btnClose.SetEvent(ui.__mem_func__(self.Close))
			btnClose.Show()

			btnHide = ui.Button()
			btnHide.SetParent(self)
			btnHide.SetUpVisual("d:/ymir work/ui/chat/btn_hide01_default.tga")
			btnHide.SetOverVisual("d:/ymir work/ui/chat/btn_hide01_over.tga")
			btnHide.SetDownVisual("d:/ymir work/ui/chat/btn_hide01_down.tga")
			btnHide.SetToolTipText(localeInfo.CHATTING_SETTING_HIDE, 0, -23)
			btnHide.SetEvent(ui.__mem_func__(self.OnPressHide))
			btnHide.Show()

			btnSizing = self.ResizeButton()
			btnSizing.SetParent(self)
			btnSizing.SetMoveEvent(ui.__mem_func__(self.OnResize))
			btnSizing.SetSize(16, 16)
			btnSizing.Show()

			titleName = ui.TextLine()
			titleName.SetParent(self)
			titleName.SetPosition(20, 6)
			titleName.SetText(self.chatWindow.GetTabName(self.chatIndex))
			titleName.Show()

			self.imgLeft = imgLeft
			self.imgCenter = imgCenter
			self.imgRight = imgRight
			self.btnClose = btnClose
			self.btnHide = btnHide
			self.btnSizing = btnSizing
			self.titleName = titleName

		def __CreateScrollBar(self):
			scrollBar = ui.SmallThinScrollBar()
			scrollBar.SetParent(self)
			scrollBar.Show()
			scrollBar.SetScrollEvent(ui.__mem_func__(self.OnScroll))
			self.scrollBar = scrollBar
			self.scrollBarPos = 1.0

		def __del__(self):
			ui.Window.__del__(self)

		def Destroy(self):
			self.imgLeft = None
			self.imgCenter = None
			self.imgRight = None
			self.btnClose = None
			self.btnHide = None
			self.btnSizing = None
			self.scrollBar = None

		def SetSize(self, width, height):
			self.imgCenter.SetRenderingRect(0.0, 0.0, float((width - self.BLOCK_WIDTH*2) - self.BLOCK_WIDTH) / self.BLOCK_WIDTH, 0.0)
			self.imgCenter.SetPosition(self.BLOCK_WIDTH, 0)
			self.imgRight.SetPosition(width - self.BLOCK_WIDTH, 0)

			self.btnClose.SetPosition(width - self.btnClose.GetWidth() - 5, 5)
			self.btnHide.SetPosition(width - self.btnClose.GetWidth() - self.btnHide.GetWidth() - 5 - 2, 2)
			self.scrollBar.SetPosition(width - 15, 25)

			self.scrollBar.SetScrollBarSize(height - 25 - 12)
			self.scrollBar.SetPos(self.scrollBarPos)
			ui.Window.SetSize(self, width, height)

		def Open(self):
			self.OnResize()
			self.Show()

		def Close(self):
			self.Hide()
			if self.chatWindow:
				self.chatWindow.DeleteTab(self.chatIndex)

		def OnPressHide(self):
			self.Hide()
			if self.chatWindow:
				self.chatWindow.ShowTab(self.chatIndex)

		def OnResize(self):
			x, y = self.btnSizing.GetLocalPosition()
			width = self.btnSizing.GetWidth()
			height = self.btnSizing.GetHeight()

			if x < self.CHAT_LOG_WINDOW_MINIMUM_WIDTH - width:
				self.btnSizing.SetPosition(self.CHAT_LOG_WINDOW_MINIMUM_WIDTH - width, y)
				return
			if y < self.CHAT_LOG_WINDOW_MINIMUM_HEIGHT - height:
				self.btnSizing.SetPosition(x, self.CHAT_LOG_WINDOW_MINIMUM_HEIGHT - height)
				return

			self.scrollBar.LockScroll()
			self.SetSize(x + width, y + height)
			self.scrollBar.UnlockScroll()

		def OnScroll(self):
			self.scrollBarPos = self.scrollBar.GetPos()
			chat.SetEndPos(self.chatID, self.scrollBarPos)

		def OnUpdate(self):
			chat.Update(self.chatID)

		def OnRender(self):
			(x, y, width, height) = self.GetRect()

			grp.SetColor(0x77000000)
			grp.RenderBar(x+width-15, y+25, 13, height-25)

			grp.SetColor(0x77000000)
			grp.RenderBar(x, y, width, height)
			grp.SetColor(0x77000000)
			grp.RenderBox(x, y, width-2, height)
			grp.SetColor(0x77000000)
			grp.RenderBox(x+1, y+1, width-2, height)

			grp.SetColor(0xff989898)
			grp.RenderLine(x+width-13, y+height-1, 11, -11)
			grp.RenderLine(x+width-9, y+height-1, 7, -7)
			grp.RenderLine(x+width-5, y+height-1, 3, -3)

			chat.SetPosition(self.chatID, x + 10, y + height)
			chat.SetHeight(self.chatID, height - 45)
			chat.ArrangeShowingChat(self.chatID)

			chat.Render(self.chatID)

		def OnPressEscapeKey(self):
			self.OnPressHide()
			return True

		def BindInterface(self, interface):
			self.interface = interface

		def OnMouseLeftButtonDown(self):
			hyperlink = ui.GetHyperlink()
			if hyperlink and self.interface:
				self.interface.MakeHyperlinkTooltip(hyperlink)

	## ChatSettingWindow
	class ChatSettingWindow(ui.ScriptWindow):

		class MouseReflector(ui.Window):
			def __init__(self, parent):
				ui.Window.__init__(self)
				self.SetParent(parent)
				self.AddFlag("not_pick")
				self.width = self.height = 0
				self.isDown = False

			def __del__(self):
				ui.Window.__del__(self)

			def Down(self):
				self.isDown = True

			def Up(self):
				self.isDown = False

			def OnRender(self):
				if self.isDown:
					grp.SetColor(ui.WHITE_COLOR)
				else:
					grp.SetColor(ui.HALF_WHITE_COLOR)

				x, y = self.GetGlobalPosition()
				grp.RenderBar(x + 2, y + 2, self.GetWidth() - 4, self.GetHeight() - 4)

		class CheckBox(ui.ImageBox):
			def __init__(self, parent, x, y, event, filename = "d:/ymir work/ui/chat/chattingoption_check_box_off.sub"):
				ui.ImageBox.__init__(self)
				self.SetParent(parent)
				self.SetPosition(x, y)
				self.LoadImage(filename)

				self.mouseReflector = parent.MouseReflector(self)
				self.mouseReflector.SetSize(self.GetWidth(), self.GetHeight())

				image = ui.MakeImageBox(self, "d:/ymir work/ui/public/check_image.sub", 0, 0)
				image.AddFlag("not_pick")
				image.SetWindowHorizontalAlignCenter()
				image.SetWindowVerticalAlignCenter()
				image.Hide()

				self.check = False
				self.enable = True
				self.image = image
				self.event = event
				self.Show()

				self.mouseReflector.UpdateRect()

			def __del__(self):
				ui.ImageBox.__del__(self)

			def GetCheck(self):
				return self.check

			def SetCheck(self, flag):
				if flag:
					self.check = True
					self.image.Show()
				else:
					self.check = False
					self.image.Hide()

			def Disable(self):
				self.enable = False

			def OnMouseOverIn(self):
				if not self.enable:
					return
				self.mouseReflector.Show()

			def OnMouseOverOut(self):
				if not self.enable:
					return
				self.mouseReflector.Hide()

			def OnMouseLeftButtonDown(self):
				if not self.enable:
					return
				self.mouseReflector.Down()

			def OnMouseLeftButtonUp(self):
				if not self.enable:
					return
				self.mouseReflector.Up()
				self.event()

		def __init__(self, parent):
			ui.ScriptWindow.__init__(self)
			self.isLoaded = False

			from _weakref import proxy
			self.parent = proxy(parent)
			self.questionDialog = None

			self.checkBoxSlotDict = {}
			self.tmpCheckBoxSettingDict = {}
			self.chatTabOptions = {}
			self.globalOptions = {}

			self.selectedTabIndex = -1

			self.__LoadWindow()

		def __del__(self):
			ui.ScriptWindow.__del__(self)
			self.isLoaded = False
			self.parent = None
			self.questionDialog = None
			self.checkBoxSlotDict = {}
			self.tmpCheckBoxSettingDict = {}
			self.chatTabOptions = {}

		def __LoadWindow(self):
			if self.isLoaded:
				return

			self.isLoaded = 1

			try:
				pyScrLoader = ui.PythonScriptLoader()
				pyScrLoader.LoadScriptFile(self, "uiscript/chatsettingwindow.py")
			except:
				import exception
				exception.Abort("ChatSettingWindow.LoadWindow.LoadScript")

			try:
				self.__BindObject()
			except:
				import exception
				exception.Abort("ChatSettingWindow.LoadWindow.BindObject")

			try:
				self.__CreateObject()
			except:
				import exception
				exception.Abort("ChatSettingWindow.LoadWindow.CreateObject")

			for i in range(0, self.parent.MAX_TAB_NUMBER + 1):
				self.__LoadChattingOptionFile(i, True)

		def __BindObject(self):
			self.GetChild("board").SetCloseEvent(ui.__mem_func__(self.Close))

			self.resetBtn = self.GetChild("reset_button")
			self.resetBtn.SetEvent(ui.__mem_func__(self.__OnClickPopUpSetting), localeInfo.CHATTING_SETTING_CLEAR_QUESTION)

			self.saveBtn = self.GetChild("save_button")
			self.saveBtn.SetEvent(ui.__mem_func__(self.__OnClickSave))

			self.cancelBtn = self.GetChild("cancle_button")
			self.cancelBtn.SetEvent(ui.__mem_func__(self.Close))

			self.tabNameValue = self.GetChild("tab_name_value")
			self.tabNameAcceptBtn = self.GetChild("tabname_accept_button")
			self.tabNameAcceptBtn.SetEvent(ui.__mem_func__(self.__OnClickTabNameAccept))

		def __CreateObject(self):
			for key in xrange(1, len(OPTION_CHECKBOX_MODE) + 1):
				event = lambda index = key : ui.__mem_func__(self.SetCurrentChatOption)(index)

				# chatting_setting_talking_bg.y + (31 * y)
				yPos = 64 + (31 * 0)
				if key >= OPTION_CHECKBOX_EXP_INFO:
					yPos = 64 + (31 * 1)

				self.checkBoxSlotDict[key] = self.CheckBox(self, CHECK_BOX_X_POS, yPos + (18 * (key - 1)), event)

		def __OnClickTabNameAccept(self):
			if self.selectedTabIndex == 0:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CHATTING_SETTING_CHANGE_TITLE_NOT)
				return

			name = self.tabNameValue.GetText()
			if len(name) > 8:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CHATTING_SETTING_CHANGE_TITLE_MAX)
				return

			questionDialog = uiCommon.QuestionDialog()
			questionDialog.SetText(localeInfo.CHATTING_SETTING_CHANGE_TITLE_NAME)
			questionDialog.SetAcceptEvent(ui.__mem_func__(self.__QuestionNamePopupAccept))
			questionDialog.SetCancelEvent(ui.__mem_func__(self.__QuestionNamePopupCancle))
			questionDialog.Open()
			questionDialog.set_name = name
			self.questionDialog = questionDialog

		def __QuestionNamePopupAccept(self):
			if not self.questionDialog:
				return

			self.tmpCheckBoxSettingDict.update({'name': self.questionDialog.set_name})
			self.__SaveFile(self.selectedTabIndex)

			if self.parent:
				self.parent.SetTabName(self.selectedTabIndex - 1, self.questionDialog.set_name)

			self.__QuestionNamePopupCancle()

		def __QuestionNamePopupCancle(self):
			self.questionDialog.Close()
			self.questionDialog = None

		def __OnClickSave(self):
			self.__SaveFile(self.selectedTabIndex)
			self.Close()

		def __GetChattingFile(self, chatIndex):
			path = ["UserData", "chatting"]
			try:
				if not os.path.exists(os.getcwd() + os.sep + path[0] + os.sep + path[1]):
					os.makedirs(os.getcwd() + os.sep + "UserData" + os.sep + "chatting")
			except WindowsError as error: pass
			return "%s/%s/%s_%d" % (path[0], path[1], player.GetName(), chatIndex)

		def __GetChattingGlobalFile(self):
			path = ["UserData", "chatting"]
			try:
				if not os.path.exists(os.getcwd() + os.sep + path[0] + os.sep + path[1]):
					os.makedirs(os.getcwd() + os.sep + "UserData" + os.sep + "chatting")
			except WindowsError as error: pass
			return "%s/%s/%s" % (path[0], path[1], player.GetName())

		def DeleteOptionFile(self, chatIndex):
			try:
				fileName = self.__GetChattingFile(chatIndex)
				os.remove(fileName)
				return True
			except:
				return False

		def CreateTabFile(self, chatIndex):
			self.tmpCheckBoxSettingDict = {}
			self.__SaveDefault(chatIndex)

		def __LoadTmpSettings(self, chatIndex, appendToChat):
			for key in xrange(1, len(OPTION_CHECKBOX_MODE) + 1):
				if key in self.tmpCheckBoxSettingDict:
					self.chatTabOptions[chatIndex][key] = self.tmpCheckBoxSettingDict[key]
				else:
					self.chatTabOptions[chatIndex][key] = True
				self.checkBoxSlotDict[key].SetCheck(self.chatTabOptions[chatIndex][key])

			tabName = str(chatIndex)
			if 'name' in self.tmpCheckBoxSettingDict:
				tabName = self.tmpCheckBoxSettingDict['name']
				self.tabNameValue.SetText("" if tabName == str(chatIndex) else tabName)
			else:
				self.tabNameValue.SetText("")

			self.chatTabOptions[chatIndex]['name'] = tabName

			if appendToChat:
				self.parent.AddTab(chatIndex - 1, tabName)

		def __LoadChattingOptionFile(self, chatIndex, appendToChat = False):
			load = False
			self.tmpCheckBoxSettingDict = {}
			self.chatTabOptions[chatIndex] = {}
			try:
				fileName = self.__GetChattingFile(chatIndex)
				file = open(fileName)
				try:
					load = True
					self.tmpCheckBoxSettingDict = cPickle.load(file)
				except (ValueError, EOFError, cPickle.PicklingError, cPickle.UnpicklingError): pass
				file.close()
			except IOError: pass

			for key in xrange(1, len(OPTION_CHECKBOX_MODE) + 1):
				if key not in self.tmpCheckBoxSettingDict:
					self.tmpCheckBoxSettingDict[key] = True

			self.__LoadTmpSettings(chatIndex, load and appendToChat)

		def __SaveFile(self, chatIndex):
			if not self.tmpCheckBoxSettingDict:
				return

			try:
				fileName = self.__GetChattingFile(chatIndex)
				file = open(fileName, 'wb')
				cPickle.dump(self.tmpCheckBoxSettingDict, file)
				file.close()
			except IOError:
				return

			self.__LoadTmpSettings(chatIndex, False)

			if self.parent:
				self.parent.RefreshChatWindow(chatIndex - 1)
				self.parent.RefreshChatWindow()

		def __SaveDefault(self, chatIndex):
			for key in xrange(1, len(OPTION_CHECKBOX_MODE) + 1):
				self.tmpCheckBoxSettingDict[key] = True

			self.tmpCheckBoxSettingDict['name'] = str(chatIndex)

			try:
				fileName = self.__GetChattingFile(chatIndex)
				file = open(fileName, 'wb')
				cPickle.dump(self.tmpCheckBoxSettingDict, file)
				file.close()
			except IOError:
				return

			self.__LoadTmpSettings(chatIndex, False)

			if self.parent:
				self.parent.RefreshChatWindow(chatIndex - 1)
				self.parent.RefreshChatWindow()

		def LoadGlobalFile(self):
			load = False
			self.globalOptions = {}
			try:
				fileName = self.__GetChattingGlobalFile()
				file = open(fileName)
				try:
					load = True
					self.globalOptions = cPickle.load(file)
				except (ValueError, EOFError, cPickle.PicklingError, cPickle.UnpicklingError): pass
				file.close()
			except IOError: pass

			if not load:
				self.globalOptions['selected'] = -1
				self.SaveGlobalFile()

		def SaveGlobalFile(self):
			try:
				fileName = self.__GetChattingGlobalFile()
				file = open(fileName, 'wb')
				cPickle.dump(self.globalOptions, file)
				file.close()
			except IOError:
				return

		def GetSelectedChat(self):
			if 'selected' in self.globalOptions:
				return int(self.globalOptions['selected'])
			return -1

		def SetSelectedChat(self, selected):
			self.globalOptions['selected'] = selected
			self.SaveGlobalFile()

		def __OnClickPopUpSetting(self, text):
			questionDialog = uiCommon.QuestionDialog()
			questionDialog.SetText(text)
			questionDialog.SetAcceptEvent(ui.__mem_func__(self.__QuestionPopupAccept))
			questionDialog.SetCancelEvent(ui.__mem_func__(self.__QuestionPopupCancle))
			questionDialog.Open()
			self.questionDialog = questionDialog

		def __QuestionPopupAccept(self):
			if not self.questionDialog:
				return

			self.__SaveDefault(self.selectedTabIndex)

			self.__QuestionPopupCancle()
			self.Close()

		def __QuestionPopupCancle(self):
			self.questionDialog.Close()
			self.questionDialog = None

		def SetCurrentChatOption(self, index):
			value = False
			if not self.checkBoxSlotDict[index].GetCheck():
				value = True

			self.checkBoxSlotDict[index].SetCheck(value)
			self.tmpCheckBoxSettingDict.update({index: value})

		def GetChatModeSetting(self, tabIndex, mode):
			try:
				value = OPTION_CHECKBOX_MODE[mode]
				return self.chatTabOptions[tabIndex][value]
			except KeyError:
				return True

		def OnPressEscapeKey(self):
			self.Close()
			return True

		def Open(self, tabIndex):
			if not self.isLoaded:
				self.__LoadWindow()

			self.selectedTabIndex = tabIndex
			try:
				self.__LoadChattingOptionFile(tabIndex)
			except:
				self.__SaveDefault(tabIndex)

			self.Show()

		def Close(self):
			if self.questionDialog:
				self.questionDialog.Close()

			self.Hide()

