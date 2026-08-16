import uiScriptLocale

IMG_DIR = "d:/ymir work/ui/game/advanced_game_options/"

TITLE_IMAGE_TEXT_X = 5
TITLE_IMAGE_TEXT_Y = 4

OPTION_START_X = 17
SLIDER_POSITION_X = 30

SLIDER_START_Y = 50
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
			"name" : "chat_window",
			"type" : "window",
			"x" : 0,
			"y" : 5,
			"width":304,
			"height":NORMAL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "chat_mode_title_img",
					"type" : "expanded_image",
					"x" : 5,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_chat_mode",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.OPTION_VIEW_CHAT,
						},
					),
				},
				{
					"name" : "view_chat_off_button",
					"type" : "toggle_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,

					"default_image" : IMG_DIR + "toggle_unselected.png",
					"over_image" : IMG_DIR + "toggle_unselected.png",
					"down_image" : IMG_DIR + "toggle_selected.png",
					"children" :
					(
						{
							"name" : "chat_button_title",
							"type" : "text",
							"x" : TOGGLE_BUTTON_TEXT_X,
							"y" : 0,
							"text_horizontal_align":"left",
							"text" : "Chat",
							"color" : PRIMARY_COLOR,
						},
						{
							"name" : "toggle2_button_description",
							"type" : "text",
							"x" : TOGGLE_BUTTON_TEXT_X,
							"y" : 15,
							"text_horizontal_align":"left",
							"text" : "A cset sor ki-/bekapcsolása a képernyő alján.",
							"color" : SECONDARY_COLOR,
						},
					),
				},
			),
		},
		{
			"name" : "always_show_name_window",
			"type" : "window",
			"x" : 0,
			"y" : 5,
			"width":304,
			"height":SMALL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "always_show_name_title_img",
					"type" : "expanded_image",
					"x" : 5,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_always_show_name",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.OPTION_ALWAYS_SHOW_NAME,
						},
					),
				},
				{
					"name" : "always_show_name_on_button",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_ALWAYS_SHOW_NAME_ON,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
					"color" : PRIMARY_COLOR,
				},
				{
					"name" : "always_show_name_off_button",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_ALWAYS_SHOW_NAME_OFF,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
					"color" : PRIMARY_COLOR,
				},
			),
		},

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
					"color" : PRIMARY_COLOR,
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
					"color" : PRIMARY_COLOR,
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
					"color" : PRIMARY_COLOR,
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
					"color" : PRIMARY_COLOR,
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
					"color" : PRIMARY_COLOR,
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
					"color" : PRIMARY_COLOR,
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
					"color" : PRIMARY_COLOR,
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
					"color" : PRIMARY_COLOR,
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
					"color" : PRIMARY_COLOR,
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
					"color" : PRIMARY_COLOR,
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
					"color" : PRIMARY_COLOR,
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
					"color" : PRIMARY_COLOR,
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
					"color" : PRIMARY_COLOR,
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
					"color" : PRIMARY_COLOR,
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

		{
			"name" : "show_damage_window",
			"type" : "window",
			"x" : 0,
			"y" : 5,
			"width":304,
			"height":NORMAL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "show_damage_title_img",
					"type" : "expanded_image",
					"x" : 5,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_show_damage",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.OPTION_EFFECT,
						},
					),
				},
				{
					"name" : "show_damage_on_button",
					"type" : "toggle_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,

					"default_image" : IMG_DIR + "toggle_unselected.png",
					"over_image" : IMG_DIR + "toggle_unselected.png",
					"down_image" : IMG_DIR + "toggle_selected.png",
					"children" :
					(
						{
							"name" : "show_damage_button_title",
							"type" : "text",
							"x" : TOGGLE_BUTTON_TEXT_X,
							"y" : 0,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.OPTION_EFFECT,
							"color" : PRIMARY_COLOR,
						},
						{
							"name" : "show_damage_button_description",
							"type" : "text",
							"x" : TOGGLE_BUTTON_TEXT_X,
							"y" : 15,
							"text_horizontal_align":"left",
							"text" : "A sebzés-kijelzés ki-/bekapcsolása, mind a sajátodnál, mind a szörnyeknél.",
							"color" : SECONDARY_COLOR,
						},
					),
				},
			),
		},
		{
			"name" : "camera_mode_window",
			"type" : "window",
			"x" : 0,
			"y" : NORMAL_OPTION_HEIGHT,
			"width":304,
			"height":SMALL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "camera_mode_title_img",
					"type" : "expanded_image",
					"x" : 5,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_camera_mode",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.OPTION_CAMERA_DISTANCE,
						},
					),
				},
				{
					"name" : "camera_short",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_CAMERA_DISTANCE_SHORT,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
					"color" : PRIMARY_COLOR,
				},
				{
					"name" : "camera_long",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_CAMERA_DISTANCE_LONG,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
					"color" : PRIMARY_COLOR,
				},
			),
		},
		{
			"name" : "fog_mode_window",
			"type" : "window",
			"x" : 0,
			"y" : NORMAL_OPTION_HEIGHT+SMALL_OPTION_HEIGHT,
			"width":304,
			"height":SMALL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "fog_mode_title_img",
					"type" : "expanded_image",
					"x" : 5,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_fog_mode",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.OPTION_FOG,
						},
					),
				},
				{
					"name" : "fog_level0",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_FOG_DENSE,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
					"color" : PRIMARY_COLOR,
				},
				{
					"name" : "fog_level1",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_FOG_MIDDLE,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
					"color" : PRIMARY_COLOR,
				},
				{
					"name" : "fog_level2",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*2,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_FOG_LIGHT,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
					"color" : PRIMARY_COLOR,
				},
			),
		},
		{
			"name" : "sales_text_window",
			"type" : "window",
			"x" : 0,
			"y" : NORMAL_OPTION_HEIGHT+SMALL_OPTION_HEIGHT+SMALL_OPTION_HEIGHT,
			"width":304,
			"height":SMALL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "sales_text_title_img",
					"type" : "expanded_image",
					"x" : 5,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_sales_text",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.OPTION_SALESTEXT,
						},
					),
				},
				{
					"name" : "salestext_on_button",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_SALESTEXT_VIEW_ON,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
					"color" : PRIMARY_COLOR,
				},
				{
					"name" : "salestext_off_button",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_SALESTEXT_VIEW_OFF,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
					"color" : PRIMARY_COLOR,
				},
			),
		},

		{
			"name" : "volume_window",
			"type" : "window",
			"x" : 0,
			"y" : 5,
			"width":304,
			"height":SLIDER_OPTION_HEIGHT*2,
			"children":
			(
				{
					"name" : "volume_title_img",
					"type" : "expanded_image",
					"x" : 5,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_sound",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : "Volume", #uiScriptLocale.OPTION_SOUND
						},
					),
				},
				{
					"name" : "sound_text",
					"type" : "text",
					"text_horizontal_align":"left",
					"x" : OPTION_START_X,
					"y" : SLIDER_START_Y-20,
					"text":uiScriptLocale.OPTION_SOUND,
					"color" : PRIMARY_COLOR,
				},
				{
					"name" : "sound_volume_controller",
					"type" : "sliderbar_advancedgameoptions",
					"x" : OPTION_START_X,
					"y" : SLIDER_START_Y,
				},
				{
					"name" : "music_text",
					"type" : "text",
					"text_horizontal_align":"left",
					"x" : OPTION_START_X,
					"y" : SLIDER_START_Y*2-20,
					"text":uiScriptLocale.OPTION_MUSIC,
					"color" : PRIMARY_COLOR,
				},
				{
					"name" : "music_volume_controller",
					"type" : "sliderbar_advancedgameoptions",
					"x" : OPTION_START_X,
					"y" : SLIDER_START_Y*2,
				},
			),
		},
		{
			"name" : "bgm_window",
			"type" : "window",
			"x" : 0,
			"y" : SLIDER_OPTION_HEIGHT*2,
			"width":304,
			"height":SLIDER_OPTION_HEIGHT*2,
			"children":
			(
				{
					"name" : "bgm_title_img",
					"type" : "expanded_image",
					"x" : 5,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_bgm",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.MUSICLIST_TITLE,
						},
					),
				},
				{
					"name" : "bgm_file",
					"type" : "text",
					"text_horizontal_align":"left",
					"x" : OPTION_START_X,
					"y" : BUTTON_START_Y+5,
					"text":uiScriptLocale.OPTION_MUSIC_DEFAULT_THEMA,
					"color" : PRIMARY_COLOR,
				},
				{
					"name" : "bgm_button",
					"type" : "toggle_button",
					"x" : 155,
					"y" : BUTTON_START_Y,
					"text" : uiScriptLocale.OPTION_MUSIC_CHANGE,
					"default_image" : IMG_DIR + "btn_0.png",
					"over_image" : IMG_DIR + "btn_1.png",
					"down_image" : IMG_DIR + "btn_2.png",
				},
			),
		},

		{
			"name" : "fps_limit_window",
			"type" : "window",
			"x" : 0,
			"y" : 5,
			"width":304,
			"height":SMALL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "fps_limit_title_img",
					"type" : "expanded_image",
					"x" : 5,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_fps_limit",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : "FPS limit",
						},
					),
				},
				{
					"name" : "fps_limit_60",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : "60",
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
					"color" : PRIMARY_COLOR,
				},
				{
					"name" : "fps_limit_90",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1,
					"y" : 33,
					"text" : "90",
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
					"color" : PRIMARY_COLOR,
				},
				{
					"name" : "fps_limit_144",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*2,
					"y" : 33,
					"text" : "144",
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
					"color" : PRIMARY_COLOR,
				},
				{
					"name" : "fps_limit_nocap",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*3,
					"y" : 33,
					"text" : "Korlátlan",
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
					"color" : PRIMARY_COLOR,
				},
			),
		},
	),
}

import app
if app.__BL_SHADOW_RENDER_QUALITY_OPTION__:
	window["children"] += (
		{
			"name" : "shadow_target_window",
			"type" : "window",
			"x" : 0,
			"y" : 5,
			"width":304,
			"height":SMALL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "shadow_target_title_img",
					"type" : "expanded_image",
					"x" : 5,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_shadow_target",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : "Target shadow",
						},
					),
				},
				{
					"name" : "shadow_target_none",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : "Nincs",
					"tooltip_text" : "Nincs árnyék megjelenítve.",
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
					"color" : PRIMARY_COLOR,
				},
				{
					"name" : "shadow_target_ground",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1,
					"y" : 33,
					"text" : "Talaj",
					"tooltip_text" : "Csak a talaj árnyékai jelennek meg.",
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
					"color" : PRIMARY_COLOR,
				},
				{
					"name" : "shadow_target_ground_and_solo",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*2,
					"y" : 33,
					"text" : "Talaj+Saját",
					"tooltip_text" : "Talaj és a saját karakter árnyéka jelenik meg.",
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
					"color" : PRIMARY_COLOR,
				},
				{
					"name" : "shadow_target_all",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*3,
					"y" : 33,
					"text" : "Mind",
					"tooltip_text" : "Minden árnyék megjelenik (talaj, játékosok, szörnyek).",
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
					"color" : PRIMARY_COLOR,
				},
			),
		},
		{
			"name" : "shadow_quality_window",
			"type" : "window",
			"x" : 0,
			"y" : 5,
			"width":304,
			"height":SMALL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "shadow_quality_title_img",
					"type" : "expanded_image",
					"x" : 5,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_shadow_quality",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : "Shadow quality",
						},
					),
				},
				{
					"name" : "shadow_quality_bad",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : "Alacsony",
					"tooltip_text" : "Alacsony minőségű árnyékok (jobb teljesítmény).",
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
					"color" : PRIMARY_COLOR,
				},
				{
					"name" : "shadow_quality_average",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1,
					"y" : 33,
					"text" : "Közepes",
					"tooltip_text" : "Közepes minőségű árnyékok.",
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
					"color" : PRIMARY_COLOR,
				},
				{
					"name" : "shadow_quality_good",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*2,
					"y" : 33,
					"text" : "Magas",
					"tooltip_text" : "Magas minőségű árnyékok (nagyobb terhelés).",
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
					"color" : PRIMARY_COLOR,
				},
			),
		},
	)

if app.ENABLE_FOV_OPTION:
	window["children"] += (
		{
			"name" : "fov_window",
			"type" : "window",
			"x" : 0,
			"y" : 5,
			"width":304,
			"height":SMALL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "fov_title_img",
					"type" : "expanded_image",
					"x" : 5,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_fov",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : "Kiterjesztett FOV",
						},
					),
				},
				{
					"name" : "fov_on",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : "Be",
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
					"color" : PRIMARY_COLOR,
				},
				{
					"name" : "fov_off",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1,
					"y" : 33,
					"text" : "Ki",
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.png",
					"over_image" : IMG_DIR + "radio_unselected.png",
					"down_image" : IMG_DIR + "radio_selected.png",
					"color" : PRIMARY_COLOR,
				},
			),
		},
	)
