## Rebuilt against the real Solaris2 reference (uishop.py LoadDialog/Open) instead of
## guesswork: the reference uses ONE unified 10x8 (80-slot) item grid sitting directly
## on the board - no thinboard backing, no separate decoration/render-target panel
## next to it. The dark title/expire/gold/shop-value boxes and the icon-button row are
## all built in Python (OfflineShopWindow.__BuildSolarisChrome), exactly like the
## reference builds shopTitleBox/shopExpireBox/shopGoldBox/shopLockButton etc in
## uishop.py - this file only lays out the static frame + item grid.
ROOT = "d:/ymir work/ui/game/offlineshop/"

BOARD_WIDTH  = 345
BOARD_HEIGHT = 431

window = {
	"name" : "OfflineShopWindow",
	"style" : ("movable", "float",),
	"x" : SCREEN_WIDTH / 2 - BOARD_WIDTH / 2,
	"y" : SCREEN_HEIGHT / 2 - BOARD_HEIGHT / 2,
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
					"name" : "ItemSlot",
					"type" : "grid_table",
					"x" : 12, "y" : 56,
					"start_index" : 0,
					"x_count" : 10, "y_count" : 8,
					"x_step" : 32, "y_step" : 32,
					"image" : "d:/ymir work/ui/public/Slot_Base.sub",
				},

				{
					## Log rows + their scrollbar are built in Python (OfflineShopWindow.
					## __RefreshLogs) as HistoryLogItem widgets styled after the reference's
					## HistoryWindow.Item (line.png divider + name/price/date columns) -
					## a generic listboxex/textline dump looked nothing like it.
					"name" : "LogsWindow",
					"type" : "window",
					"x" : 12, "y" : 56,
					"width" : 320, "height" : 256,
					"children" :
					(
						{
							"name" : "close_log_button", "type" : "button",
							"x" : 320 / 2 - 30, "y" : 256 - 26,
							"width" : 60, "height" : 24,
							"text" : "Back",
							"default_image" : "d:/ymir work/ui/public/Middle_Button_01.sub",
							"over_image" : "d:/ymir work/ui/public/Middle_Button_02.sub",
							"down_image" : "d:/ymir work/ui/public/Middle_Button_03.sub",
						},
					),
				},
			),
		},
	),
}
