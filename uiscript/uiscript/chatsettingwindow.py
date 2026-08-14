import uiScriptLocale
import app

PATTERN_PATH = "d:/ymir work/ui/pattern/"
ROOT_PATH = "d:/ymir work/ui/public/"
CHATTING_PATH = "d:/ymir work/ui/chat/"

## Mini version: no per-tab language filter / dice-roll section, only the
## per-category message checkboxes this build actually implements (Talking
## through Notice, plus Exp/Item/Money once ENABLE_CHATTING_WINDOW_RENEWAL
## split those out of plain Info). One header+row block (49px) shorter than
## the original reference layout because of that.
WINDOW_WIDTH = 254
WINDOW_HEIGHT = 350

PATTERN_WINDOW_WIDTH = 232
PATTERN_WINDOW_HEIGHT = 280

PATTERN_X_COUNT = (PATTERN_WINDOW_WIDTH - 32) / 16
PATTERN_Y_COUNT = (PATTERN_WINDOW_HEIGHT - 32) / 16

window = {
	"name" : "ChatSettingWindow",
	"style" : ("movable", "float",),

	"x" : SCREEN_WIDTH / 2 - WINDOW_WIDTH / 2,
	"y" : SCREEN_HEIGHT / 2 - WINDOW_HEIGHT / 2,

	"width" : WINDOW_WIDTH,
	"height" : WINDOW_HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : WINDOW_WIDTH,
			"height" : WINDOW_HEIGHT,

			"title" : uiScriptLocale.CHATTING_SETTING_TITLE,

			"children" :
			(
				## Base pattern
				{
					"name" : "base_pattern",
					"type" : "window",
					"style" : ("attach", "ltr",),

					"x" : 10,
					"y" : 32,

					"width" : PATTERN_WINDOW_WIDTH,
					"height" :PATTERN_WINDOW_HEIGHT,

					"children" :
					(
						## LeftTop 1
						{
							"name" : "pattern_left_top_img",
							"type" : "image",
							"style" : ("ltr",),

							"x" : 0,
							"y" : 0,

							"image" : PATTERN_PATH + "border_A_left_top.tga",
						},
						## RightTop 2
						{
							"name" : "pattern_right_top_img",
							"type" : "image",
							"style" : ("ltr",),

							"x" : PATTERN_WINDOW_WIDTH - 16,
							"y" : 0,

							"image" : PATTERN_PATH + "border_A_right_top.tga",
						},
						## LeftBottom 3
						{
							"name" : "pattern_left_bottom_img",
							"type" : "image",
							"style" : ("ltr",),

							"x" : 0,
							"y" : PATTERN_WINDOW_HEIGHT - 16,

							"image" : PATTERN_PATH + "border_A_left_bottom.tga",
						},
						## RightBottom 4
						{
							"name" : "pattern_right_bottom_img",
							"type" : "image",
							"style" : ("ltr",),

							"x" : PATTERN_WINDOW_WIDTH - 16,
							"y" : PATTERN_WINDOW_HEIGHT - 16,

							"image" : PATTERN_PATH + "border_A_right_bottom.tga",
						},
						## TopCenterImg 5
						{
							"name" : "pattern_top_cetner_img",
							"type" : "expanded_image",
							"style" : ("ltr",),

							"x" : 16,
							"y" : 0,

							"image" : PATTERN_PATH + "border_A_top.tga",
							"rect" : (0.0, 0.0, PATTERN_X_COUNT, 0),
						},
						## LeftCenterImg 6
						{
							"name" : "pattern_left_center_img",
							"type" : "expanded_image",
							"style" : ("ltr",),

							"x" : 0,
							"y" : 16,

							"image" : PATTERN_PATH + "border_A_left.tga",
							"rect" : (0.0, 0.0, 0, PATTERN_Y_COUNT),
						},
						## RightCenterImg 7
						{
							"name" : "pattern_right_center_img",
							"type" : "expanded_image",
							"style" : ("ltr",),

							"x" : PATTERN_WINDOW_WIDTH - 16,
							"y" : 16,

							"image" : PATTERN_PATH + "border_A_right.tga",
							"rect" : (0.0, 0.0, 0, PATTERN_Y_COUNT),
						},
						## BottomCenterImg 8
						{
							"name" : "pattern_bottom_center_img",
							"type" : "expanded_image",
							"style" : ("ltr",),

							"x" : 16,
							"y" : PATTERN_WINDOW_HEIGHT - 16,

							"image" : PATTERN_PATH + "border_A_bottom.tga",
							"rect" : (0.0, 0.0, PATTERN_X_COUNT, 0),
						},
						## CenterImg
						{
							"name" : "pattern_center_img",
							"type" : "expanded_image",
							"style" : ("ltr",),

							"x" : 16,
							"y" : 16,

							"image" : PATTERN_PATH + "border_A_center.tga",
							"rect" : (0.0, 0.0, PATTERN_X_COUNT, PATTERN_Y_COUNT),
						},
					),
				},

				## Chat channel section header
				{
					"name" : "chatting_setting_menu_bg", "type" : "image", "x" : 15, "y" : 37,
					"image" : CHATTING_PATH + "chattingoption_menu_bg.sub",
					"children" :
					(
						{ "name" : "chatting_setting", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.CHATTING_SETTING_TITLE, "all_align" : "center" },
					),
				},
				## Talking
				{
					"name" : "chatting_setting_talking_bg", "type" : "image", "x" : 18, "y" : 65,
					"image" : CHATTING_PATH + "chattingoption_sub_large_bg.sub",
					"children" :
					(
						{ "name" : "chatting_setting_talking", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.CHATTING_SETTING_TALKING, "all_align":"center" },
					),
				},
				## Party
				{
					"name" : "chatting_setting_party_bg", "type" : "image", "x" : 18, "y" : 83,
					"image" : CHATTING_PATH + "chattingoption_sub_large_bg.sub",
					"children" :
					(
						{ "name" : "chatting_setting_party", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.CHATTING_SETTING_PARTY, "all_align":"center" },
					),
				},
				## Guild
				{
					"name" : "chatting_setting_guild_bg", "type" : "image", "x" : 18, "y" : 101,
					"image" : CHATTING_PATH + "chattingoption_sub_large_bg.sub",
					"children" :
					(
						{ "name" : "chatting_setting_guild", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.CHATTING_SETTING_GUILD, "all_align":"center" },
					),
				},
				## Shout
				{
					"name" : "chatting_setting_shout_bg", "type" : "image", "x" : 18, "y" : 119,
					"image" : CHATTING_PATH + "chattingoption_sub_large_bg.sub",
					"children" :
					(
						{ "name" : "chatting_setting_shout", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.CHATTING_SETTING_SHOUT, "all_align":"center" },
					),
				},
				## System (plain CHAT_TYPE_INFO messages)
				{
					"name" : "chatting_setting_info_bg", "type" : "image", "x" : 18, "y" : 137,
					"image" : CHATTING_PATH + "chattingoption_sub_large_bg.sub",
					"children" :
					(
						{ "name" : "chatting_setting_info", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.CHATTING_SETTING_SYSTEM, "all_align":"center" },
					),
				},
				## Notice
				{
					"name" : "chatting_setting_notice_bg", "type" : "image", "x" : 18, "y" : 155,
					"image" : CHATTING_PATH + "chattingoption_sub_large_bg.sub",
					"children" :
					(
						{ "name" : "chatting_setting_notice", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.CHATTING_SETTING_NOTICE, "all_align":"center" },
					),
				},

				## System-detail section header (Exp / Item / Money)
				{
					"name" : "system_setting_menu_bg", "type" : "image", "x" : 15, "y" : 176,
					"image" : CHATTING_PATH + "chattingoption_menu_bg.sub",
					"children" :
					(
						{ "name" : "system_setting", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.CHATTING_SETTING_DETAIL, "all_align":"center" },
					),
				},
				## Experience
				{
					"name" : "chatting_setting_exp_bg", "type" : "image", "x" : 18, "y" : 204,
					"image" : CHATTING_PATH + "chattingoption_sub_large_bg.sub",
					"children" :
					(
						{ "name" : "chatting_setting_exp", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.CHATTING_SETTING_EXP, "all_align":"center" },
					),
				},
				## Item
				{
					"name" : "chatting_setting_item_bg", "type" : "image", "x" : 18, "y" : 222,
					"image" : CHATTING_PATH + "chattingoption_sub_large_bg.sub",
					"children" :
					(
						{ "name" : "chatting_setting_item", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.CHATTING_SETTING_ITEM, "all_align":"center" },
					),
				},
				## Money
				{
					"name" : "chatting_setting_gold_bg", "type" : "image", "x" : 18, "y" : 240,
					"image" : CHATTING_PATH + "chattingoption_sub_large_bg.sub",
					"children" :
					(
						{ "name" : "chatting_setting_gold", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.CHATTING_SETTING_GOLD, "all_align":"center" },
					),
				},

				## Tab name section header
				{
					"name" : "tabname_setting_menu_bg", "type" : "image", "x" : 15, "y" : 261,
					"image" : CHATTING_PATH + "chattingoption_menu_bg.sub",
					"children" :
					(
						{ "name" : "tabname_setting", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.CHATTING_SETTING_TABNAME, "all_align" : "center" },
					),
				},
				## Tab name edit field
				{
					"name" : "tab_name_slot",
					"type" : "slotbar",
					"x" : 17,
					"y" : 289,
					"width" : 123,
					"height" : 18,
					"children" :
					(
						{
							"name" : "tab_name_value",
							"type" : "editline",
							"x" : 2,
							"y" : 3,
							"width" : 160,
							"height" : 15,
							"input_limit" : 8,
							"check_width" : 1,
							"text" : "",
						},
					),
				},
				## Tab name accept button
				{
					"name" : "tabname_accept_button",
					"type" : "button",

					"x" : 143,
					"y" : 288,

					"default_image" : CHATTING_PATH + "chattingoption_enter_btn_01.sub",
					"over_image" : CHATTING_PATH + "chattingoption_enter_btn_02.sub",
					"down_image" : CHATTING_PATH + "chattingoption_enter_btn_03.sub",
				},

				## ResetButton
				{
					"name" : "reset_button",
					"type" : "button",

					"x" : 10,
					"y" : WINDOW_HEIGHT - 31,

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",

					"text" : uiScriptLocale.CHATTING_SETTING_CLEAR,
				},
				## SaveButton
				{
					"name" : "save_button",
					"type" : "button",

					"x" : 88,
					"y" : WINDOW_HEIGHT - 31,

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",

					"text" : uiScriptLocale.CHATTING_SETTING_SAVE,
				},
				## CancelButton
				{
					"name" : "cancle_button",
					"type" : "button",

					"x" : 166,
					"y" : WINDOW_HEIGHT - 31,

					"default_image" : ROOT_PATH + "middle_button_01.sub",
					"over_image" : ROOT_PATH + "middle_button_02.sub",
					"down_image" : ROOT_PATH + "middle_button_03.sub",

					"text" : uiScriptLocale.CHATTING_SETTING_CANCLE,
				},
			),
		},
	),
}
