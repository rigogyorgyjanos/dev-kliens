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

RADIO_BUTTON_TEXT_X = 25
TOGGLE_BUTTON_TEXT_X = 45

SMALL_OPTION_HEIGHT = 65
NORMAL_OPTION_HEIGHT = 80
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
	),
}
