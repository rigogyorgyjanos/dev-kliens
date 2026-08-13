WINDOW_WIDTH = 300
WINDOW_HEIGHT = 340

window = {
	"name" : "OfflineShopLogWindow",
	"style" : ("movable", "float",),
	"x" : 0, "y" : 0,
	"width" : WINDOW_WIDTH,
	"height" : WINDOW_HEIGHT,
	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",
			"style" : ("attach",),
			"x" : 0, "y" : 0,
			"width" : WINDOW_WIDTH, "height" : WINDOW_HEIGHT,
			"title" : "Sale Log",
			"children" :
			(
				{
					"name" : "log_list", "type" : "listbox",
					"x" : 10, "y" : 34,
					"width" : WINDOW_WIDTH - 20, "height" : WINDOW_HEIGHT - 80,
				},
				{
					"name" : "clear_button", "type" : "button",
					"x" : WINDOW_WIDTH / 2 - 40, "y" : WINDOW_HEIGHT - 34,
					"width" : 80, "height" : 25,
					"text" : "Clear",
					"default_image" : "d:/ymir work/ui/public/Middle_Button_01.sub",
					"over_image" : "d:/ymir work/ui/public/Middle_Button_02.sub",
					"down_image" : "d:/ymir work/ui/public/Middle_Button_03.sub",
				},
			),
		},
	),
}
