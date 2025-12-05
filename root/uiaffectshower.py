import ui, localeInfo
import chr, app, skill, player, uiToolTip, constInfo

if app.ENABLE_RENEWAL_AFFECT_SHOWER:
	import uiCommon, constInfo, net
	from _weakref import proxy
	overInImage = None
	affectDict={}
	def TypeToAffect(affect):
		_dict = {
			chr.AFFECT_JEONGWI : 3,
			chr.AFFECT_GEOMGYEONG : 4,
			chr.AFFECT_CHEONGEUN : 19,
			chr.AFFECT_GYEONGGONG : 49,
			chr.AFFECT_EUNHYEONG : 34,
			chr.AFFECT_GWIGEOM : 63,
			chr.AFFECT_GONGPO : 64,
			chr.AFFECT_JUMAGAP : 65,
			chr.AFFECT_HOSIN : 94,
			chr.AFFECT_BOHO : 95,
			chr.AFFECT_KWAESOK : 110,
			chr.AFFECT_HEUKSIN : 79,
			chr.AFFECT_MUYEONG : 78,
			chr.AFFECT_GICHEON : 96,
			chr.AFFECT_JEUNGRYEOK : 111,
			chr.AFFECT_PABEOP : 66,
		}
		return _dict[affect] if _dict.has_key(affect) else affect

class LovePointImage(ui.ExpandedImageBox):
	def __del__(self):
		ui.ExpandedImageBox.__del__(self)
	def __init__(self):
		ui.ExpandedImageBox.__init__(self)
		self.loverName = ""
		self.lovePoint = 0
	def SetLoverInfo(self, name, lovePoint):
		self.loverName = name
		self.lovePoint = lovePoint
		self.__Refresh()
	def OnUpdateLovePoint(self, lovePoint):
		self.lovePoint = lovePoint
		self.__Refresh()
	def __Refresh(self):
		self.lovePoint = max(0, self.lovePoint)
		self.lovePoint = min(100, self.lovePoint)
		loveGrade = 0 if 0 == self.lovePoint else self.lovePoint / 25 + 1
		FILE_PATH = "d:/ymir work/ui/pattern/LovePoint/"
		FILE_DICT = {
			0 : FILE_PATH + "01.dds",
			1 : FILE_PATH + "02.dds",
			2 : FILE_PATH + "02.dds",
			3 : FILE_PATH + "03.dds",
			4 : FILE_PATH + "04.dds",
			5 : FILE_PATH + "05.dds",
		}
		fileName = self.FILE_DICT.get(loveGrade, self.FILE_PATH+"00.dds")

		try:
			self.LoadImage(fileName)
			self.SetScale(0.7, 0.7)
		except:
			import dbg
			dbg.TraceError("LovePointImage.SetLoverInfo(lovePoint=%d) - LoadError %s" % (self.lovePoint, fileName))
	def OnMouseOverIn(self):
		interface = constInfo.GetInterfaceInstance()
		if interface:
			tooltipItem = interface.tooltipItem
			if tooltipItem:
				tooltipItem.ClearToolTip()
				tooltipItem.AutoAppendNewTextLineResize(self.loverName, 0xffE9E7D2)
				tooltipItem.AppendSpace(5)
				tooltipItem.AutoAppendNewTextLineResize(localeInfo.AFF_LOVE_POINT % self.lovePoint)
				tooltipItem.ShowToolTip()
	def OnMouseOverOut(self):
		interface = constInfo.GetInterfaceInstance()
		if interface:
			if interface.tooltipItem:
				interface.tooltipItem.HideToolTip()

class HorseImage(ui.ExpandedImageBox):
	def __del__(self):
		ui.ExpandedImageBox.__del__(self)
	def __init__(self):
		ui.ExpandedImageBox.__init__(self)
		self.descriptions = []
	def __GetHorseGrade(self, level):
		return 0 if level == 0 else (level-1)/10 + 1
	def SetState(self, level, health, battery):
		self.descriptions = []
		if level>0:
			try:
				grade = self.__GetHorseGrade(level)
				self.__AppendText(localeInfo.LEVEL_LIST[grade])
			except IndexError:
				return
			try:
				healthName=localeInfo.HEALTH_LIST[health]
				if len(healthName)>0:
					self.__AppendText(healthName)
			except IndexError:
				return
			if health>0:
				if battery==0:
					self.__AppendText(localeInfo.NEEFD_REST)
			try:
				FILE_PATH = "d:/ymir work/ui/pattern/HorseState/"
				FILE_DICT = {
					00 : FILE_PATH+"00.dds",
					01 : FILE_PATH+"00.dds",
					02 : FILE_PATH+"00.dds",
					03 : FILE_PATH+"00.dds",
					10 : FILE_PATH+"10.dds",
					11 : FILE_PATH+"11.dds",
					12 : FILE_PATH+"12.dds",
					13 : FILE_PATH+"13.dds",
					20 : FILE_PATH+"20.dds",
					21 : FILE_PATH+"21.dds",
					22 : FILE_PATH+"22.dds",
					23 : FILE_PATH+"23.dds",
					30 : FILE_PATH+"30.dds",
					31 : FILE_PATH+"31.dds",
					32 : FILE_PATH+"32.dds",
					33 : FILE_PATH+"33.dds",
				}
				fileName=FILE_DICT[health*10+battery]
			except KeyError:
				return
			try:
				self.LoadImage(fileName)
				self.SetScale(0.7, 0.7)
			except:
				return
	def __AppendText(self, text):
		self.descriptions.append(text)
	def OnMouseOverIn(self):
		interface = constInfo.GetInterfaceInstance()
		if interface:
			tooltipItem = interface.tooltipItem
			if tooltipItem:
				tooltipItem.ClearToolTip()
				for text in self.descriptions:
					tooltipItem.AutoAppendNewTextLineResize(text)
				if len(self.descriptions):
					tooltipItem.ShowToolTip()
	def OnMouseOverOut(self):
		interface = constInfo.GetInterfaceInstance()
		if interface:
			if interface.tooltipItem:
				interface.tooltipItem.HideToolTip()

class AffectImage(ui.ExpandedImageBox):
	def __init__(self):
		ui.ExpandedImageBox.__init__(self)

		self.toolTipText = None
		self.isSkillAffect = False
		self.description = None
		self.endTime = 0
		self.affect = None
		self.isClocked = TRUE
		if app.ENABLE_RENEWAL_AFFECT_SHOWER:
			self.isCanRemove=False

	def SetAffect(self, affect):
		self.affect = affect
	def GetAffect(self):
		return self.affect
	def SetDescription(self, description):
		self.description = description
	def SetDuration(self, duration):
		self.endTime = 0
		if duration > 0:
			self.endTime = app.GetGlobalTimeStamp() + duration

	if not app.ENABLE_RENEWAL_AFFECT_SHOWER:
		def SetToolTipText(self, text, x = 0, y = -19):
			if not self.toolTipText:
				textLine = ui.TextLine()
				textLine.SetParent(self)
				textLine.SetSize(0, 0)
				textLine.SetOutline()
				textLine.Hide()
				self.toolTipText = textLine
			self.toolTipText.SetText(text)
			w, h = self.toolTipText.GetTextSize()
			self.toolTipText.SetPosition(max(0, x + self.GetWidth()/2 - w/2), y)
		def UpdateAutoPotionDescription(self):
			potionType = 0
			if self.affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY:
				potionType = player.AUTO_POTION_TYPE_HP
			else:
				potionType = player.AUTO_POTION_TYPE_SP	
			isActivated, currentAmount, totalAmount, slotIndex = player.GetAutoPotionInfo(potionType)
			amountPercent = 0.0
			try:
				amountPercent = (float(currentAmount) / totalAmount) * 100.0
			except:
				amountPercent = 100.0
			self.SetToolTipText(self.description % amountPercent, 0, 40)
		def SetClock(self, isClocked):
			self.isClocked = isClocked
		def UpdateDescription(self):
			if not self.isClocked:
				self.__UpdateDescription2()
				return
			if not self.description:
				return
			toolTip = self.description
			if self.endTime > 0:
				leftTime = localeInfo.SecondToDHM(self.endTime - app.GetGlobalTimeStamp())
				toolTip += " (%s : %s)" % (localeInfo.LEFT_TIME, leftTime)
			self.SetToolTipText(toolTip, 0, 40)
		def __UpdateDescription2(self):
			if not self.description:
				return
			toolTip = self.description
			self.SetToolTipText(toolTip, 0, 40)

	def SetSkillAffectFlag(self, flag):
		self.isSkillAffect = flag

	def IsSkillAffect(self):
		return self.isSkillAffect

	if app.ENABLE_RENEWAL_AFFECT_SHOWER:
		def FormatTime(self, seconds):
			if seconds <= 0:
				return "0s"
			m, s = divmod(seconds, 60)
			h, m = divmod(m, 60)
			d, h = divmod(h, 24)
			timeText = ""
			if d > 0:
				timeText += "{}d".format(d)
				timeText += " "
			if h > 0:
				timeText += "{}h".format(h)
				timeText += " "
			if m > 0:
				timeText += "{}m".format(m)
				timeText += " "
			if s > 0:
				timeText += "{}s".format(s)
			return timeText

		def AddAffect(self, pointIdx, pointVal):
			if not [pointIdx, pointVal] in self.affectList:
				self.affectList.append([pointIdx, pointVal])
		def RemoveAffect(self, pointIdx, pointVal):
			if [pointIdx, pointVal] in self.affectList:
				del self.affectList[self.affectList.index([pointIdx, pointVal])]

	def OnMouseOverIn(self):
		if app.ENABLE_RENEWAL_AFFECT_SHOWER:
			interface = constInfo.GetInterfaceInstance()
			if interface:
				tooltip = interface.tooltipSkill if self.IsSkillAffect() else interface.tooltipItem

				if tooltip:
					tooltip.ClearToolTip()


					global overInImage, affectDict
					overInImage = proxy(self)
					affect = TypeToAffect(self.GetAffect()) if self.IsSkillAffect() else self.GetAffect()


					if affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY or affect == chr.NEW_AFFECT_AUTO_SP_RECOVERY:
						potionType = player.AUTO_POTION_TYPE_HP if affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY else player.AUTO_POTION_TYPE_SP
						(isActivated, currentAmount, totalAmount, slotIndex) = player.GetAutoPotionInfo(potionType)
						amountPercent = 0.0
						try:
							amountPercent = (float(currentAmount) / totalAmount) * 100.0
						except:
							amountPercent = 100.0
						tooltip.AutoAppendNewTextLineResize(self.description % amountPercent, 0xffC5C7C4)
					else:
						affectData = affectDict[affect] if affectDict.has_key(affect) else {}
						affectList = affectData["affect"] if affectData.has_key("affect") else []
						maxDuration = affectData["duration"] if affectData.has_key("duration") else 0
						if self.description:
							tooltip.AutoAppendNewTextLineResize(self.description, 0xffE9E7D2)
							tooltip.AppendSpace(5)

						if self.IsSkillAffect():
							tooltip.ClearToolTip()
							tooltip.AutoAppendNewTextLineResize(skill.GetSkillName(TypeToAffect(self.GetAffect())), 0xffE9E7D2 )
							tooltip.AppendSpace(5)
							
							for data in affectList:
								if data[0] != 0 and uiToolTip.ItemToolTip.POINT_DICT.has_key(data[0]):
									tooltip.AutoAppendNewTextLineResize(uiToolTip.ItemToolTip.POINT_DICT[data[0]](data[1]), 0xff95A693)
						else:
							for data in affectList:
								if data[0] != 0 and uiToolTip.ItemToolTip.POINT_DICT.has_key(data[0]):
									tooltip.AutoAppendNewTextLineResize(uiToolTip.ItemToolTip.POINT_DICT[data[0]](data[1]), 0xff95A693)

						if self.endTime > 0:
							tooltip.AppendSpace(5)
							tooltip.AutoAppendNewTextLineResize("%s: %s" % (localeInfo.LEFT_TIME, self.FormatTime(self.endTime - app.GetGlobalTimeStamp())), 0xffC5C7C4)
						elif maxDuration > 0:
							tooltip.AppendSpace(5)
							tooltip.AutoAppendNewTextLineResize("%s: %s" % (localeInfo.LEFT_TIME, self.FormatTime(maxDuration - app.GetGlobalTimeStamp())), 0xffC5C7C4)
						if self.isCanRemove:
							tooltip.AppendSpace(7)
							tooltip.AutoAppendNewTextLineResize(localeInfo.AFFECTSHOWER_REMOVE_TEXT)
					tooltip.ShowToolTip()
		else:
			if self.toolTipText:
				self.toolTipText.Show()

	def OnMouseOverOut(self):
		if app.ENABLE_RENEWAL_AFFECT_SHOWER:
			global overInImage
			overInImage = None
			interface = constInfo.GetInterfaceInstance()
			if interface:
				if interface.tooltipItem:
					interface.tooltipItem.HideToolTip()
				if interface.tooltipSkill:
					interface.tooltipSkill.HideToolTip()
		else:
			if self.toolTipText:
				self.toolTipText.Hide()

class AffectShower(ui.Window):

	MALL_DESC_IDX_START = 1000
	DEW_DESC_IDX_START = 1100
	WATER_DESC_IDX_START = 1300
	DRAGON_GOD_DESC_IDX_START = 1500
	IMAGE_STEP = 25
	AFFECT_MAX_NUM = 32
	INFINITE_AFFECT_DURATION = 0x1FFFFFFF 
	END_STRING = "_03"
	AFFECT_DATA_DICT =	{

			chr.AFFECT_POISON : (localeInfo.SKILL_TOXICDIE, "d:/ymir work/ui/skill/common/affect/poison.sub", 4, 0),
			chr.AFFECT_SLOW : (localeInfo.SKILL_SLOW, "d:/ymir work/ui/skill/common/affect/slow.sub", 4, 0),
			chr.AFFECT_STUN : (localeInfo.SKILL_STUN, "d:/ymir work/ui/skill/common/affect/stun.sub", 4, 0),

			chr.AFFECT_ATT_SPEED_POTION : (localeInfo.SKILL_INC_ATKSPD, "d:/ymir work/ui/skill/common/affect/Increase_Attack_Speed.sub", 3, 0),
			chr.AFFECT_MOV_SPEED_POTION : (localeInfo.SKILL_INC_MOVSPD, "d:/ymir work/ui/skill/common/affect/Increase_Move_Speed.sub", 3, 0),
			chr.AFFECT_FISH_MIND : (localeInfo.SKILL_FISHMIND, "d:/ymir work/ui/skill/common/affect/fishmind.sub", 3, 0),

			chr.AFFECT_JEONGWI : (localeInfo.SKILL_JEONGWI, "d:/ymir work/ui/skill/warrior/jeongwi" + END_STRING + ".sub", 2, 0),
			chr.AFFECT_GEOMGYEONG : (localeInfo.SKILL_GEOMGYEONG, "d:/ymir work/ui/skill/warrior/geomgyeong" + END_STRING + ".sub", 2, 0),
			chr.AFFECT_CHEONGEUN : (localeInfo.SKILL_CHEONGEUN, "d:/ymir work/ui/skill/warrior/cheongeun" + END_STRING + ".sub", 2, 0),
			chr.AFFECT_GYEONGGONG : (localeInfo.SKILL_GYEONGGONG, "d:/ymir work/ui/skill/assassin/gyeonggong" + END_STRING + ".sub", 2, 0),
			chr.AFFECT_EUNHYEONG : (localeInfo.SKILL_EUNHYEONG, "d:/ymir work/ui/skill/assassin/eunhyeong" + END_STRING + ".sub", 2, 0),
			chr.AFFECT_GWIGEOM : (localeInfo.SKILL_GWIGEOM, "d:/ymir work/ui/skill/sura/gwigeom" + END_STRING + ".sub", 2, 0),
			chr.AFFECT_GONGPO : (localeInfo.SKILL_GONGPO, "d:/ymir work/ui/skill/sura/gongpo" + END_STRING + ".sub", 2, 0),
			chr.AFFECT_JUMAGAP : (localeInfo.SKILL_JUMAGAP, "d:/ymir work/ui/skill/sura/jumagap" + END_STRING + ".sub", 2, 0),
			chr.AFFECT_HOSIN : (localeInfo.SKILL_HOSIN, "d:/ymir work/ui/skill/shaman/hosin" + END_STRING + ".sub", 2, 0),
			chr.AFFECT_BOHO : (localeInfo.SKILL_BOHO, "d:/ymir work/ui/skill/shaman/boho" + END_STRING + ".sub", 2, 0),
			chr.AFFECT_KWAESOK : (localeInfo.SKILL_KWAESOK, "d:/ymir work/ui/skill/shaman/kwaesok" + END_STRING + ".sub", 2, 0),
			chr.AFFECT_HEUKSIN : (localeInfo.SKILL_HEUKSIN, "d:/ymir work/ui/skill/sura/heuksin" + END_STRING + ".sub", 2, 0),
			chr.AFFECT_MUYEONG : (localeInfo.SKILL_MUYEONG, "d:/ymir work/ui/skill/sura/muyeong" + END_STRING + ".sub", 2, 0),
			chr.AFFECT_GICHEON : (localeInfo.SKILL_GICHEON, "d:/ymir work/ui/skill/shaman/gicheon" + END_STRING + ".sub", 2, 0),
			chr.AFFECT_JEUNGRYEOK : (localeInfo.SKILL_JEUNGRYEOK, "d:/ymir work/ui/skill/shaman/jeungryeok" + END_STRING + ".sub", 2, 0),
			chr.AFFECT_PABEOP : (localeInfo.SKILL_PABEOP, "d:/ymir work/ui/skill/sura/pabeop" + END_STRING + ".sub", 2, 0),
			chr.AFFECT_FALLEN_CHEONGEUN : (localeInfo.SKILL_CHEONGEUN, "d:/ymir work/ui/skill/warrior/cheongeun" + END_STRING + ".sub", 2, 0),
			# chr.AFFECT_FIRE : (localeInfo.SKILL_FIRE, "d:/ymir work/ui/skill/sura/hwayeom" + END_STRING + ".sub", 2, 0),
			chr.AFFECT_CHINA_FIREWORK : (localeInfo.SKILL_POWERFUL_STRIKE, "d:/ymir work/ui/skill/common/affect/powerfulstrike.sub", 2, 0),

			chr.NEW_AFFECT_EXP_BONUS : (localeInfo.TOOLTIP_MALL_EXPBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/exp_bonus.sub",3, 0),
			chr.NEW_AFFECT_ITEM_BONUS : (localeInfo.TOOLTIP_MALL_ITEMBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/item_bonus.sub",3, 0),
			chr.NEW_AFFECT_SAFEBOX : (localeInfo.TOOLTIP_MALL_SAFEBOX, "d:/ymir work/ui/skill/common/affect/safebox.sub",3, 0),
			chr.NEW_AFFECT_AUTOLOOT : (localeInfo.TOOLTIP_MALL_AUTOLOOT, "d:/ymir work/ui/skill/common/affect/autoloot.sub",3, 0),
			chr.NEW_AFFECT_FISH_MIND : (localeInfo.TOOLTIP_MALL_FISH_MIND, "d:/ymir work/ui/skill/common/affect/fishmind.sub",3, 0),
			chr.NEW_AFFECT_MARRIAGE_FAST : (localeInfo.TOOLTIP_MALL_MARRIAGE_FAST, "d:/ymir work/ui/skill/common/affect/marriage_fast.sub",3, 0),
			chr.NEW_AFFECT_GOLD_BONUS : (localeInfo.TOOLTIP_MALL_GOLDBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/gold_bonus.sub",3, 0),
			chr.NEW_AFFECT_NO_DEATH_PENALTY : (localeInfo.TOOLTIP_APPLY_NO_DEATH_PENALTY, "d:/ymir work/ui/skill/common/affect/gold_premium.sub",3, 0),

			chr.NEW_AFFECT_SKILL_BOOK_BONUS : (localeInfo.TOOLTIP_APPLY_SKILL_BOOK_BONUS, "d:/ymir work/ui/skill/common/affect/gold_premium.sub", 3, 1),
			chr.NEW_AFFECT_SKILL_BOOK_NO_DELAY : (localeInfo.TOOLTIP_APPLY_SKILL_BOOK_NO_DELAY, "d:/ymir work/ui/skill/common/affect/gold_premium.sub", 3, 1),

			chr.NEW_AFFECT_AUTO_HP_RECOVERY : (localeInfo.TOOLTIP_AUTO_POTION_REST, "d:/ymir work/ui/pattern/auto_hpgauge/05.dds", 3, 2),
			chr.NEW_AFFECT_AUTO_SP_RECOVERY : (localeInfo.TOOLTIP_AUTO_POTION_REST, "d:/ymir work/ui/pattern/auto_spgauge/05.dds", 3, 2),

			chr.NEW_AFFECT_DRAGON_SOUL_DECK1 : (localeInfo.TOOLTIP_DRAGON_SOUL_DECK1, "d:/ymir work/ui/dragonsoul/buff_ds_sky1.tga"),
			chr.NEW_AFFECT_DRAGON_SOUL_DECK2 : (localeInfo.TOOLTIP_DRAGON_SOUL_DECK2, "d:/ymir work/ui/dragonsoul/buff_ds_land1.tga"),

			# chr.AFFECT_FULL_PENDANT : (localeInfo.AFFECT_TOOLTIP_PENDANT, "d:/ymir work/ui/special_equipment/full_pendant.sub"),
			# chr.AFFECT_IS_MARRIAGE : (localeInfo.AFFECT_TOOLTIP_MARRIAGE, "d:/ymir work/ui/skill/common/affect/is_marriage.sub"),

			MALL_DESC_IDX_START+player.POINT_MALL_ATTBONUS : (localeInfo.TOOLTIP_MALL_ATTBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/att_bonus.sub", 3, 0),
			MALL_DESC_IDX_START+player.POINT_MALL_DEFBONUS : (localeInfo.TOOLTIP_MALL_DEFBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/def_bonus.sub", 3, 0),
			MALL_DESC_IDX_START+player.POINT_MALL_EXPBONUS : (localeInfo.TOOLTIP_MALL_EXPBONUS, "d:/ymir work/ui/skill/common/affect/exp_new.sub", 3, 0),
			MALL_DESC_IDX_START+player.POINT_MALL_ITEMBONUS : (localeInfo.TOOLTIP_MALL_ITEMBONUS, "d:/ymir work/ui/skill/common/affect/item_bonus.sub", 3, 0),
			MALL_DESC_IDX_START+player.POINT_MALL_GOLDBONUS : (localeInfo.TOOLTIP_MALL_GOLDBONUS, "d:/ymir work/ui/skill/common/affect/gold_bonus.sub", 3, 0),
			MALL_DESC_IDX_START+player.POINT_CRITICAL_PCT : (localeInfo.TOOLTIP_APPLY_CRITICAL_PCT,"d:/ymir work/ui/skill/common/affect/critical.sub", 3, 0),
			MALL_DESC_IDX_START+player.POINT_PENETRATE_PCT : (localeInfo.TOOLTIP_APPLY_PENETRATE_PCT, "d:/ymir work/ui/skill/common/affect/gold_premium.sub", 3, 0),
			MALL_DESC_IDX_START+player.POINT_MAX_HP_PCT : (localeInfo.TOOLTIP_MAX_HP_PCT, "d:/ymir work/ui/skill/common/affect/gold_premium.sub", 3, 0),
			MALL_DESC_IDX_START+player.POINT_MAX_SP_PCT : (localeInfo.TOOLTIP_MAX_SP_PCT, "d:/ymir work/ui/skill/common/affect/gold_premium.sub", 3, 0),
			MALL_DESC_IDX_START+player.POINT_PC_BANG_EXP_BONUS : (localeInfo.TOOLTIP_MALL_EXPBONUS_P_STATIC, "d:/ymir work/ui/skill/common/affect/EXP_Bonus_p_on.sub", 3, 0),
			MALL_DESC_IDX_START+player.POINT_PC_BANG_DROP_BONUS: (localeInfo.TOOLTIP_MALL_ITEMBONUS_P_STATIC, "d:/ymir work/ui/skill/common/affect/Item_Bonus_p_on.sub", 3, 0),
			
			WATER_DESC_IDX_START+player.POINT_PENETRATE_PCT : (localeInfo.TOOLTIP_APPLY_PENETRATE_PCT, 	"d:/ymir work/ui/game/affectshower/50813.sub", 5, 0),
			WATER_DESC_IDX_START+player.POINT_CRITICAL_PCT : (localeInfo.TOOLTIP_APPLY_CRITICAL_PCT, 	"d:/ymir work/ui/game/affectshower/50814.sub", 5, 0),
			WATER_DESC_IDX_START+player.ATT_BONUS: (localeInfo.TOOLTIP_ATT_GRADE, 			"d:/ymir work/ui/game/affectshower/50817.sub", 5, 0),
			WATER_DESC_IDX_START+player.DEF_BONUS: (localeInfo.TOOLTIP_DEF_GRADE, 			"d:/ymir work/ui/game/affectshower/50818.sub", 5, 0),
			WATER_DESC_IDX_START+player.ATT_SPEED: (localeInfo.TOOLTIP_ATT_SPEED, 			"d:/ymir work/ui/game/affectshower/50820.sub", 5, 0),
			DEW_DESC_IDX_START+player.POINT_CRITICAL_PCT : (localeInfo.TOOLTIP_APPLY_CRITICAL_PCT, 	"d:/ymir work/ui/game/affectshower/50821.sub", 5, 0),
			DEW_DESC_IDX_START+player.POINT_PENETRATE_PCT : (localeInfo.TOOLTIP_APPLY_PENETRATE_PCT, 	"d:/ymir work/ui/game/affectshower/50822.sub", 5, 0),
			DEW_DESC_IDX_START+player.ATT_SPEED : (localeInfo.TOOLTIP_ATT_SPEED, 			"d:/ymir work/ui/game/affectshower/50823.sub", 5, 0),
			DEW_DESC_IDX_START+player.ATT_BONUS : (localeInfo.TOOLTIP_ATT_GRADE, 			"d:/ymir work/ui/game/affectshower/50825.sub", 5, 0),
			DEW_DESC_IDX_START+player.DEF_BONUS : (localeInfo.TOOLTIP_DEF_GRADE, 			"d:/ymir work/ui/game/affectshower/50826.sub", 5, 0),
			DEW_DESC_IDX_START+player.RESIST_MAGIC : (localeInfo.TOOLTIP_RESIST_MAGIC, 			"d:/ymir work/ui/game/affectshower/50824.sub", 5, 0),
			DEW_DESC_IDX_START+player.ENERGY : (localeInfo.TOOLTIP_ENERGY, 			"d:/ymir work/ui/game/affectshower/51002.sub", 5, 0),
			DRAGON_GOD_DESC_IDX_START+player.POINT_MAX_HP_PCT : (localeInfo.TOOLTIP_MAX_HP_PCT, "d:/ymir work/ui/game/affectshower/71027.sub", 5, 0),
			DRAGON_GOD_DESC_IDX_START+player.POINT_MALL_ATTBONUS : (localeInfo.TOOLTIP_MALL_ATTBONUS_STATIC, "d:/ymir work/ui/game/affectshower/71029.sub", 5, 0),
			DRAGON_GOD_DESC_IDX_START+player.POINT_MALL_ATTBONUS : (localeInfo.TOOLTIP_MALL_ATTBONUS_STATIC, "d:/ymir work/ui/game/affectshower/71028.sub", 5, 0),
			DRAGON_GOD_DESC_IDX_START+player.POINT_MALL_DEFBONUS : (localeInfo.TOOLTIP_MALL_DEFBONUS_STATIC, "d:/ymir work/ui/game/affectshower/71030.sub", 5, 0),
			DRAGON_GOD_DESC_IDX_START+player.POINT_CRITICAL_PCT : (localeInfo.TOOLTIP_APPLY_CRITICAL_PCT, "d:/ymir work/ui/game/affectshower/71044.sub", 5, 0),
			DRAGON_GOD_DESC_IDX_START+player.POINT_PENETRATE_PCT : (localeInfo.TOOLTIP_APPLY_PENETRATE_PCT, "d:/ymir work/ui/game/affectshower/71045.sub", 5, 0),
	}

	if app.ENABLE_RENEWAL_AFFECT_SHOWER:
		AFFECT_DATA_DICT[chr.NEW_AFFECT_POLYMORPH] =  (localeInfo.POLYMORPH_AFFECT_TOOLTIP, "icon/item/70104.tga")

	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		self.ClearAllAffects()
		self.serverPlayTime=0
		self.clientPlayTime=0
		self.lastUpdateTime=0
		if app.ENABLE_RENEWAL_AFFECT_SHOWER:
			self.removeAffectDialog = None
			global affectDict, overInImage
			affectDict={}
			overInImage=None
		self.horseImage=None
		self.lovePointImage=None

	def __init__(self):
		ui.Window.__init__(self)
		self.affectImageDict={}
		self.Destroy()

		self.SetPosition(10, 10)
		self.Show()

	def ClearAllAffects(self):
		self.horseImage=None
		self.lovePointImage=None
		self.affectImageDict={}
		self.__ArrangeImageList()

	def ClearAffects(self):
		self.living_affectImageDict={}
		for key, image in self.affectImageDict.items():
			if not image.IsSkillAffect():
				self.living_affectImageDict[key] = image
		self.affectImageDict = self.living_affectImageDict
		self.__ArrangeImageList()

	def BINARY_NEW_AddAffect(self, type, pointIdx, value, duration):
		#print "BINARY_NEW_AddAffect", type, pointIdx, value, duration

		if type == chr.NEW_AFFECT_MALL:
			affect = self.MALL_DESC_IDX_START + pointIdx
		elif constInfo.ENABLE_POTIONS_AFFECTSHOWER and type == chr.NEW_AFFECT_EXP_BONUS_EURO_FREE:
			affect = self.WATER_DESC_IDX_START + pointIdx
		elif constInfo.ENABLE_POTIONS_AFFECTSHOWER and type == chr.NEW_AFFECT_BLEND:
			affect = self.DEW_DESC_IDX_START + pointIdx
		else:
			affect = type

		if app.ENABLE_RENEWAL_AFFECT_SHOWER:
			global affectDict
			affectNew = self.AffectToRealIndex(affect)
			affectData = affectDict[affectNew] if affectDict.has_key(affectNew) else {}
			affectList = affectData["affect"] if affectData.has_key("affect") else []
			maxDuration = affectData["duration"] if affectData.has_key("duration") else 0
			if not [pointIdx, value] in affectList:
				affectList.append([pointIdx, value])
			if duration+app.GetGlobalTimeStamp() > maxDuration:
				affectData["duration"] = duration+app.GetGlobalTimeStamp()
			affectData["affect"] = affectList
			affectDict[affectNew] = affectData

			if type < 500 and self.CheckRemoveAffect(type) == False:
				return
		else:
			if type < 500:
				return

		if self.affectImageDict.has_key(affect):
			return

		if not self.AFFECT_DATA_DICT.has_key(affect):
			return

		if affect == chr.NEW_AFFECT_NO_DEATH_PENALTY or affect == chr.NEW_AFFECT_SKILL_BOOK_BONUS or affect == chr.NEW_AFFECT_AUTO_SP_RECOVERY or affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY or affect == chr.NEW_AFFECT_SKILL_BOOK_NO_DELAY:
			duration = 0

		affectData = self.AFFECT_DATA_DICT[affect]
		description = affectData[0]
		filename = affectData[1]

		if pointIdx == player.POINT_MALL_ITEMBONUS or pointIdx == player.POINT_MALL_GOLDBONUS:
			value = 1 + float(value) / 100.0

		try:
			if affect != chr.NEW_AFFECT_AUTO_SP_RECOVERY and affect != chr.NEW_AFFECT_AUTO_HP_RECOVERY:
				description = description(float(value))
		except:
			return

		image = AffectImage()
		image.SetParent(self)
		image.LoadImage(filename)
		image.SetDescription(description)
		image.SetDuration(duration)
		image.SetAffect(affect)

		if app.ENABLE_RENEWAL_AFFECT_SHOWER:
			if self.CheckRemoveAffect(affect):
				image.isCanRemove=True
				image.SetEvent(ui.__mem_func__(self.__OnClickAffect),"mouse_click", affect, description)
		else:
			if affect == chr.NEW_AFFECT_EXP_BONUS_EURO_FREE or affect == chr.NEW_AFFECT_EXP_BONUS_EURO_FREE_UNDER_15 or self.INFINITE_AFFECT_DURATION < duration:
				image.SetClock(FALSE)
				image.UpdateDescription()
			elif affect == chr.NEW_AFFECT_AUTO_SP_RECOVERY or affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY:
				image.UpdateAutoPotionDescription()
			else:
				image.UpdateDescription()

		isDSAffect = (affect == chr.NEW_AFFECT_DRAGON_SOUL_DECK1 or affect == chr.NEW_AFFECT_DRAGON_SOUL_DECK2)
		image.SetScale(1.0 if isDSAffect else 0.7, 1.0 if isDSAffect else 0.7)
		image.Show()
		self.affectImageDict[affect] = image
		self.__ArrangeImageList()
		#except Exception, e:
		#	pass

	def BINARY_NEW_RemoveAffect(self, type, pointIdx):
		if type == chr.NEW_AFFECT_MALL:
			affect = self.MALL_DESC_IDX_START + pointIdx
		elif constInfo.ENABLE_POTIONS_AFFECTSHOWER and type == chr.NEW_AFFECT_EXP_BONUS_EURO_FREE:
			affect = self.WATER_DESC_IDX_START + pointIdx
		elif constInfo.ENABLE_POTIONS_AFFECTSHOWER and type == chr.NEW_AFFECT_BLEND:
			affect = self.DEW_DESC_IDX_START + pointIdx
		else:
			affect = type

		if app.ENABLE_RENEWAL_AFFECT_SHOWER:
			global affectDict
			affectNew = self.AffectToRealIndex(affect)
			affectData = affectDict[affectNew] if affectDict.has_key(affectNew) else {}
			affectList = affectData["affect"] if affectData.has_key("affect") else []
			removeIndex = -1
			for data in affectList:
				if data[0] == pointIdx:
					removeIndex = affectList.index(data)
					break
			if removeIndex != -1:
				del affectList[removeIndex]
				affectData["affect"] = affectList
				affectDict[affectNew] = affectData

		self.__RemoveAffect(affect)
		self.__ArrangeImageList()

	def SetAffect(self, affect):
		self.__AppendAffect(affect)
		self.__ArrangeImageList()

	def ResetAffect(self, affect):
		self.__RemoveAffect(affect)
		self.__ArrangeImageList()

	def SetLoverInfo(self, name, lovePoint):
		image = LovePointImage()
		image.SetParent(self)
		image.SetLoverInfo(name, lovePoint)
		self.lovePointImage = image
		self.__ArrangeImageList()

	def ShowLoverState(self):
		if self.lovePointImage:
			self.lovePointImage.Show()
			self.__ArrangeImageList()

	def HideLoverState(self):
		if self.lovePointImage:
			self.lovePointImage.Hide()
			self.__ArrangeImageList()

	def ClearLoverState(self):
		self.lovePointImage = None
		self.__ArrangeImageList()

	def OnUpdateLovePoint(self, lovePoint):
		if self.lovePointImage:
			self.lovePointImage.OnUpdateLovePoint(lovePoint)

	def SetHorseState(self, level, health, battery):
		if level==0:
			self.horseImage=None
		else:
			image = HorseImage()
			image.SetParent(self)
			image.SetState(level, health, battery)
			image.Show()

			self.horseImage=image
		self.__ArrangeImageList()

	def SetPlayTime(self, playTime):
		self.serverPlayTime = playTime
		self.clientPlayTime = app.GetTime()

	def __AppendAffect(self, affect):
		if self.affectImageDict.has_key(affect):
			return
		try:
			affectData = self.AFFECT_DATA_DICT[affect]
		except KeyError:
			return

		name = affectData[0]
		filename = affectData[1]

		skillIndex = player.AffectIndexToSkillIndex(affect)
		if 0 != skillIndex:
			name = skill.GetSkillName(skillIndex)

		image = AffectImage()
		image.SetParent(self)
		image.SetSkillAffectFlag(TRUE)
		try:
			image.LoadImage(filename)
		except:
			pass

		if app.ENABLE_RENEWAL_AFFECT_SHOWER:
			image.SetAffect(affect)
			image.SetDescription(name)
			if self.CheckRemoveAffect(affect):
				image.isCanRemove=True
				image.SetEvent(ui.__mem_func__(self.__OnClickAffect),"mouse_click", affect, name)

		image.SetScale(0.7, 0.7)
		image.Show()
		self.affectImageDict[affect] = image

	def __RemoveAffect(self, affect):
		if not self.affectImageDict.has_key(affect):
			return
		del self.affectImageDict[affect]
		self.__ArrangeImageList()

	def get_idx(self, j):
		return j[0]

	def __ArrangeImageList(self):
		imageDict = self.affectImageDict
		sortDict = [[] for i in xrange(10)]
		if self.lovePointImage:
			sortDict[0].append([2, self.lovePointImage])
		if self.horseImage:
			sortDict[0].append([1,self.horseImage])

		for affect, affectImage in self.affectImageDict.iteritems():
			affectData = self.AFFECT_DATA_DICT[affect]
			yIdx = affectData[2] if len(affectData) > 3 else 1
			xIdx = affectData[3] if len(affectData) > 3 else 0
			sortDict[yIdx-1].append([xIdx, affectImage])

		ySize, xSize, xSizeTotal = (0, 0, 0)
		for imageList in sortDict:
			isHasImage = False

			if len(imageList) > 1:
				imageList = sorted(imageList, key= self.get_idx, reverse=False)

			for image in imageList:
				isHasImage = True
				image[1].SetPosition(xSize, ySize)
				xSize += self.IMAGE_STEP
			if xSize > xSizeTotal:
				xSizeTotal = xSize
			xSize = 0
			if isHasImage:
				ySize+=26
		self.SetSize(xSizeTotal, ySize)

	def OnUpdate(self):
		try:
			if app.GetGlobalTime() - self.lastUpdateTime > 500:
				self.lastUpdateTime = app.GetGlobalTime()
				if app.ENABLE_RENEWAL_AFFECT_SHOWER:
					global overInImage
					if overInImage:
						overInImage.OnMouseOverIn()
				else:
					for image in self.affectImageDict.values():
						if image.GetAffect() == chr.NEW_AFFECT_AUTO_HP_RECOVERY or image.GetAffect() == chr.NEW_AFFECT_AUTO_SP_RECOVERY:
							image.UpdateAutoPotionDescription()
							continue
						if not image.IsSkillAffect():
							image.UpdateDescription()
		except Exception, e:
			return

	if app.ENABLE_RENEWAL_AFFECT_SHOWER:
		def AffectToRealIndex(self, affect):
			_dict = {
				209:chr.AFFECT_POISON,
				211:chr.AFFECT_SLOW,
				210:chr.AFFECT_STUN,
				201:chr.AFFECT_ATT_SPEED_POTION,
				200:chr.AFFECT_MOV_SPEED_POTION,
				208:chr.AFFECT_FISH_MIND,
			}
			return _dict[affect] if _dict.has_key(affect) else affect
		def __OnClickAffect(self, arg, affect, name):
			self.removeAffectDialog = uiCommon.QuestionDialog()
			self.removeAffectDialog.SetText(localeInfo.AFFECT_REMOVE_QUESTION % name)
			self.removeAffectDialog.SetAcceptEvent(lambda arg = True: self.OnCloseRemoveAffect(arg))
			self.removeAffectDialog.SetCancelEvent(lambda arg = False: self.OnCloseRemoveAffect(arg))
			self.removeAffectDialog.affect = affect
			self.removeAffectDialog.Open()
		def OnCloseRemoveAffect(self, answer):
			if not self.removeAffectDialog:
				return
			if answer:
				net.SendChatPacket("/remove_affect %d"%TypeToAffect(self.removeAffectDialog.affect))
			self.removeAffectDialog.Close()
			self.removeAffectDialog = None
		def CheckRemoveAffect(self, type):
			if type == chr.NEW_AFFECT_POLYMORPH:
				return True
			return True if TypeToAffect(type) != type else False
