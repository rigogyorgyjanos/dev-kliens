import app
import ui
import uiScriptLocale
import constInfo

class WarpShowerWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.loadingAniImage = None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Open(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "WarpShowerWindow.py")
		except:
			import exception
			exception.Abort("WarpShowerWindow.Open - LoadScriptFile Error")

		try:
			self.loadingAniImage = self.GetChild("LoadingAniImage")
		except:
			import exception
			exception.Abort("WarpShowerWindow.Open - LoadScriptFile Error")

		self.Show()

	def Close(self):
		constInfo.SavePMInfo = True
		self.loadingAniImage = None
		self.Hide()

	def Destroy(self):
		self.Close()

	def OnPressEscapeKey(self):
		constInfo.SavePMInfo = True
		return True
