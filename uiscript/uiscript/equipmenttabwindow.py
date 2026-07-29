window = {
	"name" : "EquipmentTabWindow",

	"x" : 0,
	"y" : 0,

	"width" : 100,
	"height" : 100+22+22,

	"style" : ("float", "not_pick",),

	"children" :
	(
		{
			"name" : "Equipment_Tab_01",
			"type" : "radio_button",

			"x" : 26,
			"y" : 23,

			"tooltip_text" : "Felszerel\xe9s",

			"default_image" : "d:/ymir work/ui/inventory/eqtabclosed_1.tga",
			"over_image" : "d:/ymir work/ui/inventory/eqtabclosed_1.tga",
			"down_image" : "d:/ymir work/ui/inventory/eqtabopen_1.tga",

			"children" :
			(
				{
					"name" : "Equipment_Tab_01_Print",
					"type" : "text",

					"x" : 0,
					"y" : 0,

					"all_align" : "center",

					"text" : "I",
				},
			),
		},
		{
			"name" : "Equipment_Tab_02",
			"type" : "radio_button",

			"x" : 26,
			"y" : 45,

			"tooltip_text" : "Koszt\xfcm",

			"default_image" : "d:/ymir work/ui/inventory/eqtabclosed_2.tga",
			"over_image" : "d:/ymir work/ui/inventory/eqtabclosed_2.tga",
			"down_image" : "d:/ymir work/ui/inventory/eqtabopen_2.tga",

			"children" :
			(
				{
					"name" : "Equipment_Tab_02_Print",
					"type" : "text",

					"x" : 0,
					"y" : 0,

					"all_align" : "center",

					"text" : "II",
				},
			),
		},
	),
}
