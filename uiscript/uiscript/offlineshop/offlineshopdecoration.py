COLS = 4
ROWS = 4
BTN_W = 60
BTN_H = 28
MARGIN = 10

WINDOW_WIDTH = MARGIN * 2 + COLS * BTN_W
WINDOW_HEIGHT = 40 + ROWS * BTN_H + MARGIN

DECO_PATH = "d:/ymir work/ui/game/myshop_deco/"

buttons = []
for row in xrange(ROWS):
	for col in xrange(COLS):
		idx = row * COLS + col
		buttons.append({
			"name" : "deco_%d" % idx, "type" : "button",
			"x" : MARGIN + col * BTN_W, "y" : 34 + row * BTN_H,
			"width" : BTN_W - 2, "height" : BTN_H - 2,
			"text" : str(idx),
			"default_image" : DECO_PATH + "select_btn_01.sub",
			"over_image" : DECO_PATH + "select_btn_02.sub",
			"down_image" : DECO_PATH + "select_btn_03.sub",
		})

window = {
	"name" : "OfflineShopDecorationWindow",
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
			"title" : "Decoration",
			"children" : tuple(buttons),
		},
	),
}
