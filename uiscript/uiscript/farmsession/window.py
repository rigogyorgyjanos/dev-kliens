import uiScriptLocale

ROOT_PATH = "d:/ymir work/ui/public/"

WINDOW_SIZE = (260, 320)

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
					"name" : "kill_text",
					"type" : "text",
					"x" : 15,
					"y" : 53,
					"text_horizontal_align" : "left",
					"text" : "",
				},
				{
					"name" : "item_text",
					"type" : "text",
					"x" : 15,
					"y" : 71,
					"text_horizontal_align" : "left",
					"text" : "",
				},
				{
					"name" : "yang_gained_text",
					"type" : "text",
					"x" : 15,
					"y" : 89,
					"text_horizontal_align" : "left",
					"text" : "",
				},
				{
					"name" : "yang_spent_text",
					"type" : "text",
					"x" : 15,
					"y" : 107,
					"text_horizontal_align" : "left",
					"text" : "",
				},
				{
					"name" : "yang_net_text",
					"type" : "text",
					"x" : 15,
					"y" : 125,
					"text_horizontal_align" : "left",
					"text" : "",
				},
				{
					"name" : "list_title_text",
					"type" : "text",
					"x" : 15,
					"y" : 148,
					"text_horizontal_align" : "left",
					"text" : "",
				},
				{
					"name" : "listbox",
					"type" : "listbox_new",
					"x" : 15,
					"y" : 166,
					"width" : WINDOW_SIZE[0] - 30,
					"height" : 100,
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
					"x" : 95,
					"y" : 278,
					"text" : uiScriptLocale.FARM_SESSION_SAVE,
					"default_image" : ROOT_PATH + "Middle_Button_01.sub",
					"over_image" : ROOT_PATH + "Middle_Button_02.sub",
					"down_image" : ROOT_PATH + "Middle_Button_03.sub",
				},
				{
					"name" : "history_btn",
					"type" : "button",
					"x" : 175,
					"y" : 278,
					"text" : uiScriptLocale.FARM_SESSION_HISTORY,
					"default_image" : ROOT_PATH + "Middle_Button_01.sub",
					"over_image" : ROOT_PATH + "Middle_Button_02.sub",
					"down_image" : ROOT_PATH + "Middle_Button_03.sub",
				},
			),
		},
	),
}
