import uiScriptLocale

IMG_DIR = "d:/ymir work/ui/game/advanced_game_options/"

TITLE_IMAGE_TEXT_X = 5
TITLE_IMAGE_TEXT_Y = 4

OPTION_START_X = 17
SLIDER_POSITION_X = 50

SLIDER_START_Y = 40
BUTTON_START_Y = 33
BUTTON_NEXT_Y = 20

RADIO_BUTTON_RANGE_X = 80
TOGGLE_BUTTON_RANGE_X = 65

RADIO_BUTTON_TEXT_X = 0
TOGGLE_BUTTON_TEXT_X = 45

SMALL_OPTION_HEIGHT = 90
NORMAL_OPTION_HEIGHT = 115
SLIDER_OPTION_HEIGHT = 65

PRIMARY_COLOR = 0xffd0c2b7
SECONDARY_COLOR = 0xff9f9892

window = {
	"name" : "GameOptionDialog",
	# Dont touch these lines!
	"style" : (),
	"x" : 222,
	"y" :1,
	"width" : 371,
	"height" : 404,
	# Dont touch these lines!
	"children" :
	(
		{
			"name" : "pvp_mode_window",
			"type" : "window",
			"x" : 0,
			"y" : 5,
			"width":304,
			"height":SMALL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "pvp_mode",
					"type" : "expanded_image",
					"x" : 5,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_pvp",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.OPTION_PVPMODE,
						},
					),
				},
				{
					"name" : "pvp_peace",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_PVPMODE_PEACE,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
				},
				{
					"name" : "pvp_revenge",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_PVPMODE_REVENGE,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
				},
				{
					"name" : "pvp_guild",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*2,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_PVPMODE_GUILD,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
				},
				{
					"name" : "pvp_free",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*3,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_PVPMODE_FREE,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
				},
			),
		},

		{
			"name" : "block_mode_window",
			"type" : "window",
			"x" : 0,
			"y" : SMALL_OPTION_HEIGHT,
			"width":304,
			"height":NORMAL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "block_mode_title_img",
					"type" : "expanded_image",
					"x" : 5,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_block",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.OPTION_BLOCK,
						},
					),
				},
				{
					"name" : "block_exchange_button",
					"type" : "toggle_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_BLOCK_EXCHANGE,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
				},
				{
					"name" : "block_party_button",
					"type" : "toggle_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_BLOCK_PARTY,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
				},
				{
					"name" : "block_guild_button",
					"type" : "toggle_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*2,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_BLOCK_GUILD,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
				},
				{
					"name" : "block_whisper_button",
					"type" : "toggle_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*3,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_BLOCK_WHISPER,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
				},
				{
					"name" : "block_friend_button",
					"type" : "toggle_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33+35,
					"text" : uiScriptLocale.OPTION_BLOCK_FRIEND,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
				},
				{
					"name" : "block_party_request_button",
					"type" : "toggle_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1,
					"y" : 33+35,
					"text" : uiScriptLocale.OPTION_BLOCK_PARTY_REQUEST,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
				},
			),
		},

		{
			"name" : "name_color_window",
			"type" : "window",
			"x" : 0,
			"y" : SMALL_OPTION_HEIGHT+NORMAL_OPTION_HEIGHT,
			"width":304,
			"height":SMALL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "name_color_title_img",
					"type" : "expanded_image",
					"x" : 5,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_name_color",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.OPTION_NAME_COLOR,
						},
					),
				},
				{
					"name" : "name_color_normal",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_NAME_COLOR_NORMAL,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
				},

				{
					"name" : "name_color_empire",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_NAME_COLOR_EMPIRE,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
				},
			),
		},
		{
			"name" : "target_board_window",
			"type" : "window",
			"x" : 0,
			"y" : SMALL_OPTION_HEIGHT+NORMAL_OPTION_HEIGHT+SMALL_OPTION_HEIGHT,
			"width":304,
			"height":SMALL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "target_board_title_img",
					"type" : "expanded_image",
					"x" : 5,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_target_board",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.OPTION_TARGET_BOARD,
						},
					),
				},
				{
					"name" : "target_board_view",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_TARGET_BOARD_VIEW,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
				},

				{
					"name" : "target_board_no_view",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_TARGET_BOARD_NO_VIEW,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
				},
			),
		},
		{
			"name" : "pick_up_filter_window",
			"type" : "window",
			"x" : 0,
			"y" : SMALL_OPTION_HEIGHT+NORMAL_OPTION_HEIGHT+SMALL_OPTION_HEIGHT+SMALL_OPTION_HEIGHT,
			"width":304,
			"height":SMALL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "pick_up_filter_title_img",
					"type" : "expanded_image",
					"x" : 5,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_pick_up_filter",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.PICK_UP,
						},
					),
				},
				{
					"name" : "pick_up_show_button",
					"type" : "button",
					"x" : 155,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_SETTING,
					"default_image" : IMG_DIR + "btn_0.png",
					"over_image" : IMG_DIR + "btn_1.png",
					"down_image" : IMG_DIR + "btn_2.png",
				},
			),
		},
	),
}
