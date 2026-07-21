import grp
import ui
import wndMgr
import app

class PhaseCurtain(ui.Bar):

	def __init__(self):
		print "NEW CURTAIN  ----------------------------------------------------------------------------"
		ui.Bar.__init__(self, "CURTAIN")
		self.speed = 0.1
		self.curAlpha = 0.0
		self.event = 0
		self.args = -1
		self.FadeInFlag = False
		self.SetWindowName("PhaseCurtain")
		self.AddFlag("float")

	def __del__(self):
		print "---------------------------------------------------------------------------- DELETE CURTAIN"
		ui.Bar.__del__(self)

	def SAFE_FadeOut(self, event, args = -1):
		self.FadeOut(ui.__mem_func__(event), args)

	def FadeOut(self, event, args = -1):
		# Disabled - this used to animate the whole screen to black before running the phase-
		# switch callback (and FadeIn() below animated it back afterwards). That animated black
		# screen was the reported ' villanas' after map warps, so the callback now just runs
		# immediately - the curtain never becomes visible at all.
		if -1 != args:
			event(args)
		else:
			event()

	def FadeIn(self):
		# Disabled - nothing to fade back in, FadeOut() above never darkened the screen.
		pass

	def SetAlpha(self, alpha):
		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())

		color = grp.GenerateColor(0.0, 0.0, 0.0, alpha)
		self.SetColor(color)

	def OnUpdate(self):
		pass
