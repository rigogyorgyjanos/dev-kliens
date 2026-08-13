## Rebuilt against the real Solaris2 reference (uiscript/PrivateShopBuilderNew.py):
## a single unified 10x8 (80-slot) item grid sitting directly on the board, a plain
## name display up top, OK/Close buttons at the bottom - no decoration/render-target
## panel next to the grid (the reference builder never had one; that placeholder was
## carried over by mistake from an older, unrelated layout).
ROOT = "d:/ymir work/ui/game/offlineshop/"

BOARD_WIDTH  = 345
BOARD_HEIGHT = 383

window = {
	"name" : "OfflineShopBuilderWindow",
	"x" : SCREEN_WIDTH / 2 - BOARD_WIDTH / 2,
	"y" : SCREEN_HEIGHT / 2 - BOARD_HEIGHT / 2,
	"style" : ("float", "movable"),
	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,
	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",
			"style" : ("attach",),
			"x" : 0, "y" : 0,
			"width" : BOARD_WIDTH, "height" : BOARD_HEIGHT,
			"title" : "Offline Shop",
			"children" :
			(
				{
					"name" : "NameSlot",
					"type" : "slotbar",
					"x" : 12, "y" : 32,
					"width" : BOARD_WIDTH - 24, "height" : 20,
					"children" :
					(
						{
							"name" : "NameLine", "type" : "editline",
							"x" : 3, "y" : 3,
							"width" : BOARD_WIDTH - 24 - 6, "height" : 16,
							"input_limit" : 32,
							"text" : "",
						},
					),
				},

				{
					"name" : "ItemSlot",
					"type" : "grid_table",
					"x" : 12, "y" : 60,
					"start_index" : 0,
					"x_count" : 10, "y_count" : 8,
					"x_step" : 32, "y_step" : 32,
					"image" : "d:/ymir work/ui/public/Slot_Base.sub",
				},

				{
					"name" : "MoneySlot",
					"type" : "slotbar",
					"x" : 12, "y" : 60 + 8 * 32 + 5,
					"width" : BOARD_WIDTH - 24, "height" : 20,
					"children" :
					(
						{
							"name" : "MoneyIcon", "type" : "image",
							"x" : 3, "y" : 3,
							"image" : "d:/ymir work/ui/game/windows/money_icon.tga",
						},
						{
							"name" : "Money", "type" : "text",
							"x" : 20, "y" : 5,
							"text" : "0",
							"fontname" : "Tahoma:15",
						},
					),
				},

				{
					"name" : "FirstButton",
					"type" : "button",
					"x" : -60, "y" : 60 + 8 * 32 + 5 + 20 + 8,
					"horizontal_align" : "center",
					"width" : 61, "height" : 21,
					"text" : "OK",
					"default_image" : "d:/ymir work/ui/public/Middle_Button_01.sub",
					"over_image" : "d:/ymir work/ui/public/Middle_Button_02.sub",
					"down_image" : "d:/ymir work/ui/public/Middle_Button_03.sub",
				},

				{
					"name" : "SecondButton",
					"type" : "button",
					"x" : 60, "y" : 60 + 8 * 32 + 5 + 20 + 8,
					"horizontal_align" : "center",
					"width" : 61, "height" : 21,
					"text" : "Cancel",
					"default_image" : "d:/ymir work/ui/public/Middle_Button_01.sub",
					"over_image" : "d:/ymir work/ui/public/Middle_Button_02.sub",
					"down_image" : "d:/ymir work/ui/public/Middle_Button_03.sub",
				},
			),
		},
	),
}
