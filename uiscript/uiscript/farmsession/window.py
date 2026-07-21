import uiScriptLocale

ROOT_PATH = "d:/ymir work/ui/public/"

WINDOW_SIZE = (260, 350)

window = {
	"name" : "FarmSessionWindow",
	"style" : ("movable", "float",),
	"x" : 0,
	"y" : 0,
	"width" : WINDOW_SIZE[0],
	"height" : WINDOW_SIZE[1],
	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",
			"x" : 0,
			"y" : 0,
			"width" : WINDOW_SIZE[0],
			"height" : WINDOW_SIZE[1],
			"title" : uiScriptLocale.FARM_SESSION_TITLE,
			"children" :
			(
				{
					"name" : "time_text",
					"type" : "text",
					"x" : 15,
					"y" : 35,
					"text_horizontal_align" : "left",
					"text" : "",
				},
				{
					"name" : "yang_net_text",
					"type" : "text",
					"x" : 15,
					"y" : 53,
					"text_horizontal_align" : "left",
					"text" : "",
				},
				{
					"name" : "stone_text",
					"type" : "text",
					"x" : 15,
					"y" : 71,
					"text_horizontal_align" : "left",
					"text" : "",
				},
				{
					"name" : "boss_text",
					"type" : "text",
					"x" : 15,
					"y" : 89,
					"text_horizontal_align" : "left",
					"text" : "",
				},
				{
					"name" : "normal_text",
					"type" : "text",
					"x" : 15,
					"y" : 107,
					"text_horizontal_align" : "left",
					"text" : "",
				},
				{
					"name" : "list_title_text",
					"type" : "text",
					"x" : 15,
					"y" : 130,
					"text_horizontal_align" : "left",
					"text" : "",
				},
				{
					"name" : "startstop_btn",
					"type" : "button",
					"x" : 15,
					"y" : 278,
					"text" : uiScriptLocale.FARM_SESSION_START,
					"default_image" : ROOT_PATH + "Middle_Button_01.sub",
					"over_image" : ROOT_PATH + "Middle_Button_02.sub",
					"down_image" : ROOT_PATH + "Middle_Button_03.sub",
				},
				{
					"name" : "save_btn",
					"type" : "button",
					"x" : 140,
					"y" : 278,
					"text" : uiScriptLocale.FARM_SESSION_SAVE,
					"default_image" : ROOT_PATH + "Middle_Button_01.sub",
					"over_image" : ROOT_PATH + "Middle_Button_02.sub",
					"down_image" : ROOT_PATH + "Middle_Button_03.sub",
				},
				{
					"name" : "toggle_btn",
					"type" : "button",
					"x" : 15,
					"y" : 305,
					"text" : uiScriptLocale.FARM_SESSION_TOGGLE_LIST,
					"default_image" : ROOT_PATH + "Middle_Button_01.sub",
					"over_image" : ROOT_PATH + "Middle_Button_02.sub",
					"down_image" : ROOT_PATH + "Middle_Button_03.sub",
				},
				{
					"name" : "history_btn",
					"type" : "button",
					"x" : 140,
					"y" : 305,
					"text" : uiScriptLocale.FARM_SESSION_HISTORY,
					"default_image" : ROOT_PATH + "Middle_Button_01.sub",
					"over_image" : ROOT_PATH + "Middle_Button_02.sub",
					"down_image" : ROOT_PATH + "Middle_Button_03.sub",
				},
			),
		},
	),
}
