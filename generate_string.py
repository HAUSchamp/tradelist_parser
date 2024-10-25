#######
# User-modifiable paramaters

string_const = "&!traded&!shiny&!#&!favorite&!rocket&!4*"

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

modifiers = ["male", "female", 
"normal", "fire", "water", "electric", "grass", "ice", "fighting", "poison", "ground", "flying", "psychic", "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy", 
"kanto", "johto", "hoenn", "sinnoh", "unova", "kalos", "alola", "galar", "hisui", "paldea", 
"dynamax", "gigantamax", 
"--", "+"]

delimiters = [";", ":", "\n"] #comma implicit

for d in delimiters:
	trade_list = trade_list.replace(d,",")

mod_string = ""
no_line_mon = []
yes_line_mon = []

for chunk in trade_list.split(','):
	for mod in modifiers:
		if mod in chunk: # jellicent bug
			for mon in mon_list: # abra/mew bug
				if mon in chunk:
					if mod == "--":
						no_line_mon.append(mon)
					elif mod == "+":
						yes_line_mon.append(mon)
					else:
						mod_string += "&!" + evo + mon + "," + mod

for mon in no_line_mon: # only search for a specific mon in the evolutionary line
	search_string = search_string.replace(",+" + mon + ",", "," + mon + ",")
	search_string = search_string.replace(",+" + mon + "&", "," + mon + "&")

for mon in yes_line_mon: # search for any mon in the evolutionary line
	search_string = search_string.replace("," + mon + ",", ",+" + mon + ",")
	search_string = search_string.replace("," + mon + "&", ",+" + mon + "&")

print(search_string[1:] + string_const + mod_string)
