import ui, wndMgr, time, app, locale, chat, constInfo, player

pText_x = 65
pText_y = 5

def pTableTranslate(i):
	pTextColor = (
					"|cFFf2e2bc|H|h",	"|cFFc9ff00|H|h",
					"|cFF80f076|H|h",	"|cFF80f076|H|h")
	translate = {
					1	:	pTextColor[0] + "Karbantartásig hátralévő idő: " + pTextColor[2] + "[%s]",
					2	:	pTextColor[1] + "Várható időtartam: 				 	  " + pTextColor[3] + "[%s]",
					3	:	"Indoklás: Szerver karbantartás!",
					4	:	"Indoklás: " + "%s",
					5	:	" Nap",
					6	:	" Óra",
					7	:	" Perc",
				}

	if translate.has_key(i):
		return translate[i]

global_t = (0,24,60)

def CalculateTimeLeft(iTime):
	A, B = divmod(iTime, global_t[2])
	C, A = divmod(A, global_t[2])
	return "%02d:%02d:%02d" % (C, A, B)

def CalculateDuration(iDuration):
	if iDuration < global_t[2]:
		return "0" + (pTableTranslate(7))

	pMin = int((iDuration / global_t[2]) % global_t[2])
	pHour = int((iDuration / global_t[2]) / global_t[2]) % global_t[1]
	pDay = int(int((iDuration / global_t[2]) / global_t[2]) / global_t[1])

	iText = ""
	if pDay > global_t[0]:
		iText += str(pDay) + (pTableTranslate(5))
		iText += " "
	if pHour > global_t[0]:
		iText += str(pHour) + (pTableTranslate(6))
		iText += " "
	if pMin > global_t[0]:
		iText += str(pMin) + (pTableTranslate(7))

	return iText

class MaintenanceClass(ui.ThinBoard):
	def __init__(self):
		ui.ThinBoard.__init__(self)
		self.AddFlag("float")
		self.AddFlag("movable")

		self.sLogo = ui.AniImageBox()
		self.sTime = ui.TextLine()
		self.sDuration = ui.TextLine()
		self.sReason = ui.TextLine()

		self.sTime.SetPosition(pText_x - 30, pText_y)
		self.sDuration.SetPosition(pText_x - 30, pText_y + 15)
		self.sReason.SetPosition(pText_x - 30, pText_y + 29)

		pWindow = [self.sTime,self.sDuration,self.sReason]
		pLogo = [self.sLogo]

		for i in pWindow:
			i.SetFontName("Tahoma:15")
			i.SetParent(self)
			i.Show()

		for i in pLogo:
			i.SetParent(self)
			i.Show()
			i.SetDelay(4.5)
			i.AppendImage("animations_maintenance/pc_1.tga")
			i.AppendImage("animations_maintenance/pc_2.tga")
			i.AppendImage("animations_maintenance/pc_3.tga")
			i.AppendImage("animations_maintenance/pc_4.tga")
			i.SetPosition(367, 3)
			i.SetSize(32, 55)

		self.SetSize(420, 55)

		# Default: bottom-left, just above the Help button.
		self.SetPosition(10, wndMgr.GetScreenHeight() - 240)

		if app.ENABLE_SAVE_LAST_WINDOW_POSITION:
			self.SetLastPosition()

	def __del__(self):
		ui.ThinBoard.__del__(self)

	def SetTime(self, iLeft):
		timeLeft = iLeft - app.GetGlobalTimeStamp()

		if timeLeft < 0:
			timeLeft = 0
			self.Hide()

		self.sTime.SetText((pTableTranslate(1) % (CalculateTimeLeft(timeLeft))))

	def OpenMaintenance(self, iTime, iDuration, iReason):
		self.leftTime = app.GetGlobalTimeStamp() + int(iTime)

		self.sDuration.SetText((pTableTranslate(2) % (CalculateDuration(int(iDuration)))))

		if str(iReason) == "no_reason":
			self.sReason.SetText((pTableTranslate(3)))
		else:
			self.sReason.SetText((pTableTranslate(4) % (str(iReason).replace("//"," "))))

		self.Show()

	def OnUpdate(self):
		self.SetTime(int(self.leftTime))

	def Hide(self):
		if app.ENABLE_SAVE_LAST_WINDOW_POSITION:
			if self.IsShow():
				self.SaveLastPosition()
		ui.ThinBoard.Hide(self)

	def Close(self):
		self.Hide()

	if app.ENABLE_SAVE_LAST_WINDOW_POSITION:
		def SetLastPosition(self):
			try:
				file = open("data/user_data/wnd/" + player.GetName() + "/" + "maintenance" + ".pos", 'r')
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
			file = open("data/user_data/wnd/" + player.GetName() + "/" + "maintenance" + ".pos", "w")
			file.write(str(pos_x)+","+str(pos_y))
			file.close()
