import app
import localeInfo

SRV1 = {
	"name":"dev-Krikal",
	"host":"192.168.1.232", #vps
	"auth1":11000,
	"ch1":13000,
	"ch2":13010,
	"ch3":13020,
	"ch4":13030,

}

SRV_TESTE = {
	"name": "Oriole2 - DEV",
	"host":"192.168.0.117", #local ip
	"auth1":11000,
	"ch1":13000,
	"ch2":13010,
	"ch3":13020,
	"ch4":13030,
}

# SERVER_NAME			= "dev-Krikal"
# SERVER_NAME_TEST	= "Test"
# SERVER_IP			= "192.168.0.75"
# SERVER_IP_TEST		= "127.0.0.1"
# CH1_NAME			= "CH1"
# CH2_NAME			= "CH2"
# CH3_NAME			= "CH3"
# CH4_NAME			= "CH4"
# PORT_1				= 13000
# PORT_2				= 13010
# PORT_3				= 13020
# PORT_4				= 13030
# PORT_AUTH			= 11000
# PORT_MARK			= 13000

STATE_NONE = "..."

STATE_DICT = {
	0 : "....",
	1 : "NORM",
	2 : "BUSY",
	3 : "FULL"
}
STATE_DICT_NAME = {
	"...." : "Offline",
	"NORM" : "Normál",
	"BUSY" : "Majdnem tele",
	"FULL" : "Tele"
}
STATE_DICT_IMAGES = {
	"...." : "channel_offline.tga",
	"NORM" : "channel_normal.tga",
	"BUSY": "channel_busy.tga",
	"FULL" : "channel_full.tga"
}

we = {
	1:{"key":11,"name":"Csatorna 1","ip":SRV1["host"],"tcp_port":SRV1["ch1"],"udp_port":SRV1["ch1"],"state":STATE_NONE,},
	2:{"key":12,"name":"Csatorna 2","ip":SRV1["host"],"tcp_port":SRV1["ch2"],"udp_port":SRV1["ch2"],"state":STATE_NONE,},
	3:{"key":13,"name":"Csatorna 3","ip":SRV1["host"],"tcp_port":SRV1["ch3"],"udp_port":SRV1["ch3"],"state":STATE_NONE,},
	4:{"key":14,"name":"Csatorna 4","ip":SRV1["host"],"tcp_port":SRV1["ch4"],"udp_port":SRV1["ch4"],"state":STATE_NONE,},
}
we_teste = {
	1:{"key":21,"name":"Csatorna 1","ip":SRV_TESTE["host"],"tcp_port":SRV_TESTE["ch1"],"udp_port":SRV_TESTE["ch1"],"state":STATE_NONE,},
	2:{"key":22,"name":"Csatorna 2","ip":SRV_TESTE["host"],"tcp_port":SRV_TESTE["ch2"],"udp_port":SRV_TESTE["ch2"],"state":STATE_NONE,},
	# 3:{"key":23,"name":"Channel 3","ip":SRV_TESTE["host"],"tcp_port":SRV_TESTE["ch3"],"udp_port":SRV_TESTE["ch3"],"state":STATE_NONE,},
	# 4:{"key":24,"name":"Channel 4","ip":SRV_TESTE["host"],"tcp_port":SRV_TESTE["ch4"],"udp_port":SRV_TESTE["ch4"],"state":STATE_NONE,},
}



REGION_NAME_DICT = {
	0 : SRV1["name"],
	1 : SRV_TESTE["name"],
}
REGION_AUTH_SERVER_DICT = {
	0 : {
		1 : { "ip":SRV1["host"], "port":SRV1["auth1"], },
		2 : { "ip":SRV_TESTE["host"], "port":SRV_TESTE["auth1"], },
	}
}
REGION_DICT = {
	0 : {
		1 : { "name" :SRV1["name"], "channel" : we, },
		2 : { "name" :SRV_TESTE["name"], "channel" : we_teste, },
	},
}
MARKADDR_DICT = {
	10 : { "ip" : SRV1["host"], "tcp_port" : SRV1["ch1"], "mark" : "10.tga", "symbol_path" : "10", },
	11 : { "ip" : SRV1["host"], "tcp_port" : SRV1["ch2"], "mark" : "10.tga", "symbol_path" : "11", },
	12 : { "ip" : SRV1["host"], "tcp_port" : SRV1["ch3"], "mark" : "10.tga", "symbol_path" : "12", },
	13 : { "ip" : SRV1["host"], "tcp_port" : SRV1["ch4"], "mark" : "10.tga", "symbol_path" : "13", },
	20 : { "ip" : SRV_TESTE["host"], "tcp_port" : SRV_TESTE["ch1"], "mark" : "10.tga", "symbol_path" : "10", },
}
TESTADDR = { "ip" : SRV1["host"], "tcp_port" : SRV1["ch1"], "udp_port" : SRV1["ch1"], }
