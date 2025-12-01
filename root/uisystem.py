import net
import app
import ui
import uiOption

import uiSystemOption
import uiGameOption
import uiScriptLocale
import networkModule
import constInfo
import localeInfo
import chat

SYSTEM_MENU_FOR_PORTAL = False

###################################################################################################
## System
class SystemDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
	
	def __Initialize(self):
		self.eventOpenHelpWindow = None
		self.systemOptionDlg = None
		self.gameOptionDlg = None
		if app.BL_MOVE_CHANNEL:
			self.moveChannelDlg = None
		
	def LoadDialog(self):	
		if SYSTEM_MENU_FOR_PORTAL:
			self.__LoadSystemMenu_ForPortal()
		else:
			self.__LoadSystemMenu_Default()
			
	def __LoadSystemMenu_Default(self):
		pyScrLoader = ui.PythonScriptLoader()
		if constInfo.IN_GAME_SHOP_ENABLE:
			pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "SystemDialog.py")
		else:
			pyScrLoader.LoadScriptFile(self, "uiscript/systemdialog.py")

		self.GetChild("system_option_button").SAFE_SetEvent(self.__ClickSystemOptionButton)
		self.GetChild("game_option_button").SAFE_SetEvent(self.__ClickGameOptionButton)
		self.GetChild("change_button").SAFE_SetEvent(self.__ClickChangeCharacterButton)
		self.GetChild("logout_button").SAFE_SetEvent(self.__ClickLogOutButton)
		self.GetChild("exit_button").SAFE_SetEvent(self.__ClickExitButton)
		self.GetChild("help_button").SAFE_SetEvent(self.__ClickHelpButton)
		self.GetChild("cancel_button").SAFE_SetEvent(self.Close)
		if app.BL_MOVE_CHANNEL:
			self.GetChild("movechannel_button").SAFE_SetEvent(self.__ClickMoveChannelButton)
		if constInfo.IN_GAME_SHOP_ENABLE:
			self.GetChild("mall_button").SAFE_SetEvent(self.__ClickInGameShopButton)
		

	def __LoadSystemMenu_ForPortal(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/systemdialog_forportal.py")

		self.GetChild("system_option_button").SAFE_SetEvent(self.__ClickSystemOptionButton)
		self.GetChild("game_option_button").SAFE_SetEvent(self.__ClickGameOptionButton)
		self.GetChild("change_button").SAFE_SetEvent(self.__ClickChangeCharacterButton)
		self.GetChild("exit_button").SAFE_SetEvent(self.__ClickExitButton)
		self.GetChild("help_button").SAFE_SetEvent(self.__ClickHelpButton)
		self.GetChild("cancel_button").SAFE_SetEvent(self.Close)
		if app.BL_MOVE_CHANNEL:
			self.GetChild("movechannel_button").SAFE_SetEvent(self.__ClickMoveChannelButton)

	def Destroy(self):
		self.ClearDictionary()
		
		if self.gameOptionDlg:
			self.gameOptionDlg.Destroy()
			
		if self.systemOptionDlg:
			self.systemOptionDlg.Destroy()
			
		self.__Initialize()

	def SetOpenHelpWindowEvent(self, event):
		self.eventOpenHelpWindow = event

	def OpenDialog(self):
		self.Show()

	def __ClickChangeCharacterButton(self):
		self.Close()

		net.ExitGame()

	def __OnClosePopupDialog(self):
		self.popup = None		

	def __ClickLogOutButton(self):
		if SYSTEM_MENU_FOR_PORTAL: 
			if app.loggined:
				self.Close()
				net.ExitApplication()
			else:
				self.Close()
				net.LogOutGame()
		else:
			self.Close()
			net.LogOutGame()


	def __ClickExitButton(self):
		self.Close()
		net.ExitApplication()
		
	def __ClickSystemOptionButton(self):
		self.Close()

		if not self.systemOptionDlg:
			self.systemOptionDlg = uiSystemOption.OptionDialog()

		self.systemOptionDlg.Show()

	def __ClickGameOptionButton(self):
		self.Close()

		if not self.gameOptionDlg:
			self.gameOptionDlg = uiGameOption.OptionDialog()

		self.gameOptionDlg.Show()

	
	def __ClickHelpButton(self):
		self.Close()

		if None != self.eventOpenHelpWindow:
			self.eventOpenHelpWindow()

	def __ClickInGameShopButton(self):
		self.Close()
		net.SendChatPacket("/in_game_mall")

	def Close(self):
		self.Hide()
		return True

	def RefreshMobile(self):
		if self.gameOptionDlg:
			self.gameOptionDlg.RefreshMobile()
		#self.optionDialog.RefreshMobile()

	def OnMobileAuthority(self):
		if self.gameOptionDlg:
			self.gameOptionDlg.OnMobileAuthority()
		#self.optionDialog.OnMobileAuthority()

	def OnBlockMode(self, mode):
		uiGameOption.blockMode = mode
		if self.gameOptionDlg:
			self.gameOptionDlg.OnBlockMode(mode)
		#self.optionDialog.OnBlockMode(mode)

	def OnChangePKMode(self):
		if self.gameOptionDlg:
			self.gameOptionDlg.OnChangePKMode()
		#self.optionDialog.OnChangePKMode()
	
	def OnPressExitKey(self):
		self.Close()
		return True

	def OnPressEscapeKey(self):
		self.Close()
		return True
		
	if app.BL_MOVE_CHANNEL:
		def __ClickMoveChannelButton(self):
			## 99 서버 예외 처리 
			if net.GetChannelNumber() == 99:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_CHANNEL_NOT_MOVE)
				return
			## 인스턴스 던전 예외처리
			elif net.GetMapIndex() >= 10000:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_CHANNEL_NOT_MOVE)
				return
			
			if self.moveChannelDlg:
				self.moveChannelDlg.Show()
			else:
				moveChannelDlg = MoveChannelDialog()
				moveChannelDlg.Show()
				self.moveChannelDlg = moveChannelDlg
			
			self.Close()
	

if app.BL_MOVE_CHANNEL:
	class MoveChannelDialog(ui.ScriptWindow):
		def __init__(self):
			ui.ScriptWindow.__init__(self)
			self.__LoadDialog()
			
			self.IsShow = False
			
		def __del__(self):
			ui.ScriptWindow.__del__(self)
			
		def __LoadDialog(self) :	
			try:
				pyScrLoader = ui.PythonScriptLoader()
				pyScrLoader.LoadScriptFile(self, "UIScript/MoveChannelDialog.py")
			except:
				import exception
				exception.Abort("MoveChannelDialog.__LoadDialog")
			

			self.ParentBoard = self.GetChild("MoveChannelBoard")
			self.ChildBoard = self.GetChild("BlackBoard")
			self.GetChild("MoveChannelTitle").SetCloseEvent(ui.__mem_func__(self.Close))
			
			self.ChannelList = []
			cnt = net.GetChannelCount()
			cnt = cnt - 1 # 99서버 제외
			
			self.DlgWidht = 190
			self.BlackBoardHeight = 23*cnt + 5*(cnt-1) + 13
			self.DlgHeight = self.BlackBoardHeight + 75
			
			self.AcceptBtn = ui.MakeButton(self.ParentBoard, 13, self.DlgHeight - 33, "", "d:/ymir work/ui/public/", "middle_button_01.sub", "middle_button_02.sub", "middle_button_03.sub")
			self.AcceptBtn.SetText( localeInfo.MOVE_CHANNEL_SELECT )
			self.AcceptBtn.SetEvent(ui.__mem_func__(self.AcceptButton))
			self.CloseBtn = ui.MakeButton(self.ParentBoard, self.DlgWidht - 73, self.DlgHeight - 33, "", "d:/ymir work/ui/public/", "middle_button_01.sub", "middle_button_02.sub", "middle_button_03.sub")
			self.CloseBtn.SetText( localeInfo.MOVE_CHANNEL_CANCEL )
			self.CloseBtn.SetEvent(ui.__mem_func__(self.Close))

			for i in xrange(cnt):
				btn = ui.MakeButton(self.ChildBoard, 8, 6 + i*28, "", "d:/ymir work/ui/game/myshop_deco/", "select_btn_01.sub", "select_btn_02.sub", "select_btn_03.sub")
				btn.SetText(net.GetChannelName(i+1))
				btn.SetEvent(ui.__mem_func__(self.__SelectChannel), i+1)
				self.ChannelList.append(btn)
			
			self.ParentBoard.SetSize(self.DlgWidht, self.DlgHeight)
			self.ChildBoard.SetSize(self.DlgWidht - 26, self.BlackBoardHeight)
			self.SetSize(self.DlgWidht, self.DlgHeight)
			
			self.UpdateRect()
			
		def __SelectChannel(self, idx):
			self.ChangeChannelNumber = idx
			
			for btn in self.ChannelList:
				btn.SetUp()
				btn.Enable()
				
			self.ChannelList[idx-1].Down()
			self.ChannelList[idx-1].Disable()
			
		def AcceptButton(self):
			if self.ChangeChannelNumber == self.StartChannelNumber:
				return
			
			net.MoveChannelGame(self.ChangeChannelNumber)
			self.StartChannelNumber = self.ChangeChannelNumber
			self.Close()
						
		def Show(self) :
			ui.ScriptWindow.Show(self)
			
			self.StartChannelNumber = net.GetChannelNumber()
			self.__SelectChannel(self.StartChannelNumber)
			
			self.IsShow = True
		
		def Close(self):
			self.Hide()
			
			self.IsShow = False
			
		def OnPressEscapeKey(self):
			self.Close()
			return True
			
		def IsShowWindow(self):
			return self.IsShow
if __name__ == "__main__":

	import app
	import wndMgr
	import systemSetting
	import mouseModule
	import grp
	import ui
	import chr
	import background
	import player

	#wndMgr.SetOutlineFlag(True)

	app.SetMouseHandler(mouseModule.mouseController)
	app.SetHairColorEnable(True)
	wndMgr.SetMouseHandler(mouseModule.mouseController)
	wndMgr.SetScreenSize(systemSetting.GetWidth(), systemSetting.GetHeight())
	app.Create("METIN2 CLOSED BETA", systemSetting.GetWidth(), systemSetting.GetHeight(), 1)
	mouseModule.mouseController.Create()


	wnd = SystemDialog()
	wnd.LoadDialog()
	wnd.Show()

	app.Loop()

