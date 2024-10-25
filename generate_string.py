#######
# User-modifiable paramaters

string_const = "&!traded&!shiny&!#&!favorite"
include_evo_line = True


trade_list = """

PASTE TRADE LIST HERE

""".lower()


#######

evo = "+"*include_evo_line

search_string = ""

for mon in mon_list:
	if mon in trade_list:
		search_string += ","+evo+mon

print(search_string[1:]+string_const)
