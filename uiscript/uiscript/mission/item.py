import localeInfo

IMG_DIR = "d:/ymir work/ui/game/mission/"
BUTTON_ROOT = "d:/ymir work/ui/public/"
window = {
	"name" : "MissionItem",
	"x" : 0,
	"y" : 0,
	"width" : 620,
	"height" : 47,
	"children" :
	(
		{
			"name": "board",
			"type": "expanded_image",
			"x": 0,
			"y": 0,
			"image":IMG_DIR+"mission_0.png",
			"children":
			(
				{
					"name":"icon",
					"type":"expanded_image",
					"x": 10,
					"y": 10,
					"image": "icon/item/50309.tga",
				},

				{
					"name":"status_text",
					"type":"text",
					"x": 290,
					"y": 15,
					"text_horizontal_align":"left",
					"text":"",
				},
				{
					"name":"type_text",
					"type":"text",
					"x": 40,
					"y": 9,
					"text_horizontal_align":"left",
					"text":"",
				},
				{
					"name":"time_text",
					"type":"text",
					"x": 40,
					"y": 21,
					"text_horizontal_align":"left",
					"text":"",
				},
				{
					"name" : "reward_btn",
					"type" : "button",
					"x" : 181+194,
					"y" : 15-3,
					"default_image" : IMG_DIR + "btn_reward_normal.png",
					"over_image" : IMG_DIR + "btn_reward_hover.png",
					"down_image" : IMG_DIR + "btn_reward_down.png",
					"disable_image" : IMG_DIR + "btn_reward_down.png",
				},
				{
					"name" : "delete_btn",
					"type" : "button",
					"x" : 181+223,
					"y" : 15+30-33,
					"default_image" : IMG_DIR + "btn_delete_normal.png",
					"over_image" : IMG_DIR + "btn_delete_hover.png",
					"down_image" : IMG_DIR + "btn_delete_down.png",
				},
			),
		},
	),
}
