import localeInfo

IMG_DIR = "d:/ymir work/ui/game/mission/"

BG_IMAGE_SIZE = (492, 324)
WINDOW_SIZE = (BG_IMAGE_SIZE[0]+12, BG_IMAGE_SIZE[1]+30+10)

window = {
	"name" : "MissionWindow",
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
			"title" : "Mission Books",
			"children" :
			(
				{
					"name" : "bg",
					"type" : "image",
					"x" : 6,
					"y" : 32,
					"image":IMG_DIR+"bg.tga",
					"children":
					(
						{
							"name" : "listbox",
							"type" : "listbox_new",
							"x" : 3,
							"y" : 3,
							"width" : BG_IMAGE_SIZE[0] - 15,
							"height" : BG_IMAGE_SIZE[1]-6,
						},
					),
				},
			),
		},
	),
}
