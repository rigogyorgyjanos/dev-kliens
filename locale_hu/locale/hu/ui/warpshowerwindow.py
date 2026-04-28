import uiScriptLocale

window = {
	"name" : "WarpShowerWindow",
	"sytle" : ("float", "ltr",),

	"x" : 0,
	"y" : 0,

	"width" : SCREEN_WIDTH,
	"height" : SCREEN_HEIGHT,

	"children" :
	[
		{
			"name" : "BackgroundBar",
			"type" : "bar",

			"x" : 0,
			"y" : 0,

			"width" : SCREEN_WIDTH,
			"height" : SCREEN_HEIGHT,

			"color" : 0x66000000,

			"children" :
			[
				{
					"name" : "LoadingWindow",
					"type" : "window",

					"x" : 0,
					"y" : 0,

					"width" : 317,
					"height": 317,

					"horizontal_align" : "center",
					"vertical_align" : "center",

					"children" :
					[
						{
							"name" : "LoadingAniImage",
							"type" : "ani_image",

							"x" : 0,
							"y" : 0,

							"delay" : 1,

							"images" :
							(
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0000.png",
                                uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0001.png",
                                uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0002.png",
                                uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0003.png",
                                uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0004.png",
                                uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0005.png",
                                uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0006.png",
                                uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0007.png",
                                uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0008.png",
                                uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0009.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0010.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0011.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0012.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0013.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0014.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0015.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0016.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0017.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0018.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0019.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0020.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0021.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0022.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0023.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0024.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0025.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0026.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0027.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0028.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0029.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0030.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0031.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0032.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0033.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0034.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0035.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0036.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0037.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0038.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0039.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0040.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0041.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0042.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0043.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0044.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0045.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0046.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0047.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0048.png",
								uiScriptLocale.LOCALE_UISCRIPT_PATH + "loading/frame_0049.png",
							)
						},
					],
				},
			],
		}
	],
}
