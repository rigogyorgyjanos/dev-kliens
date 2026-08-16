import uiScriptLocale

IMG_DIR = "d:/ymir work/ui/game/advanced_game_options/"

TITLE_IMAGE_TEXT_X = 7
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
			"y" : NORMAL_OPTION_HEIGHT,
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
				},
			),
		},
	),
}
