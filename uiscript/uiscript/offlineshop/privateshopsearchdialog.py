## Rebuilt to match the Solaris2 reference client's uiscript/searchshop.py structure
## (flat colored boxes: SearchBox/MenuBox/ResultBox/PaginationBox) instead of the old
## private_*-textured skin. Category tree, result rows, pagination buttons and the
## filter-panel combobox overlays are all built in Python (PrivateShopSearchWindow),
## exactly like the reference does it - this file only lays out the static frame.
ROOT = "d:/ymir work/ui/search/"

BOARD_WIDTH  = 640
BOARD_HEIGHT = 520

window = {
	"name" : "PrivateShopSearchWindow",
	"x" : (SCREEN_WIDTH - BOARD_WIDTH) / 2,
	"y" : (SCREEN_HEIGHT - BOARD_HEIGHT) / 2,
	"style" : ("movable", "float",),
	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,
	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),
			"x" : 0, "y" : 0,
			"width" : BOARD_WIDTH, "height" : BOARD_HEIGHT,
			"children" :
			(
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),
					"x" : 8, "y" : 7,
					"width" : BOARD_WIDTH - 16,
					"color" : "red",
					"children" :
					(
						{ "name" : "TitleName", "type" : "text", "x" : 0, "y" : -1, "text" : "Shop Search", "all_align" : "center" },
						{
							"name" : "TooltipButton", "type" : "button",
							"x" : BOARD_WIDTH - 16 - 40, "y" : 2,
							"default_image" : "d:/ymir work/ui/pattern/q_mark_01.tga",
							"over_image" 	: "d:/ymir work/ui/pattern/q_mark_02.tga",
							"down_image" 	: "d:/ymir work/ui/pattern/q_mark_01.tga",
						},
					),
				},

				{
					"name" : "SearchBox",
					"type" : "box",
					"x" : 15, "y" : 35,
					"width" : 170, "height" : 80,
					"color" : 0xFF6C6359,
					"children" :
					(
						{
							"name" : "NameBox",
							"type" : "box",
							"x" : 5, "y" : 5,
							"width" : 160, "height" : 20,
							"color" : 0xFF6C6359,
							"children" :
							(
								{ "name" : "NameBar", "type" : "bar", "x" : 1, "y" : 1, "width" : 160, "height" : 19 },
								{
									"name" : "InputName", "type" : "editline",
									"x" : 3, "y" : 3,
									"width" : 138, "height" : 18,
									"text_horizontal_align" : "left",
									"input_limit" : 35,
								},
								{
									"name" : "SearchButton", "type" : "button",
									"x" : 18, "y" : 1,
									"horizontal_align" : "right",
									"default_image" : ROOT + "search_btn1.png",
									"over_image" 	: ROOT + "search_btn2.png",
									"down_image" 	: ROOT + "search_btn3.png",
								},
							),
						},

						## ExactSearch/PlayerSearch are NOT declared here as "checkbox2" -
						## the uiscript loader (ui.py PythonScriptLoader) has no handler for
						## that type (only plain ui.CheckBox exists, and it isn't loader-
						## registered either) - they're built in Python instead, see
						## PrivateShopSearchWindow.__BuildFilterPanel.

						{
							"name" : "FilterButton", "type" : "toggle_button",
							"x" : 5, "y" : 48,
							"horizontal_align" : "left",
							"text" : "Filter",
							"default_image" : ROOT + "filter_btn1.png",
							"over_image" 	: ROOT + "filter_btn2.png",
							"down_image" 	: ROOT + "filter_btn3.png",
						},
						{
							"name" : "ClearFilterButton", "type" : "button",
							"x" : 5 + 128 + 5, "y" : 48,
							"horizontal_align" : "left",
							"default_image" : ROOT + "clear_btn1.png",
							"over_image" 	: ROOT + "clear_btn2.png",
							"down_image" 	: ROOT + "clear_btn3.png",
						},
					),
				},

				{
					"name" : "MenuBox",
					"type" : "box",
					"x" : 15, "y" : 35 + 80 + 5,
					"width" : 170, "height" : BOARD_HEIGHT - 35 - 80 - 5 - 35,
					"color" : 0xFF6C6359,
				},

				{
					"name" : "ResultBox",
					"type" : "box",
					"x" : 15 + 170 + 5, "y" : 35,
					"width" : BOARD_WIDTH - (15 + 170 + 5) - 15, "height" : BOARD_HEIGHT - 35 - 35 - 5,
					"color" : 0xFF6C6359,
				},

				{
					"name" : "PaginationBox",
					"type" : "box",
					"x" : 15 + 170 + 5, "y" : BOARD_HEIGHT - 35 - 30,
					"width" : BOARD_WIDTH - (15 + 170 + 5) - 15, "height" : 30,
					"color" : 0xFF6C6359,
					"children" :
					(
						{
							"name" : "BuySelectedButton", "type" : "button",
							"x" : 5, "y" : 5,
							"horizontal_align" : "left",
							"text" : "Buy Selected",
							"default_image" : "d:/ymir work/ui/public/Middle_Button_01.sub",
							"over_image" 	: "d:/ymir work/ui/public/Middle_Button_02.sub",
							"down_image" 	: "d:/ymir work/ui/public/Middle_Button_03.sub",
						},
					),
				},
			),
		},
	),
}
