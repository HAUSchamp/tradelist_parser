############################
# User-modifiable paramaters

# Constant to add to each string (e.g. exclude shinies or alr. traded mon)
string_const = "&!traded&!shiny&!#&!favorite&!rocket&!4*"

# Include a mon's evolutionary line by default?
include_evo_line = True

# Paste a plaintext list of mon here, can have other text too
trade_list = """
PASTE TRADE LIST HERE
""".lower()

############################

# In-game search modifiers
modifiers = ["male", "female", 
"normal", "fire", "water", "electric", "grass", "ice", "fighting", "poison", "ground", "flying", "psychic", "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy", 
"kanto", "johto", "hoenn", "sinnoh", "unova", "kalos", "alola", "galar", "hisui", "paldea", 
"dynamax", "gigantamax", 
"--", "+"]

# Map alternate spellings for modifiers
mod_maps = {"paldean":"paldea", "hisuian":"hisui", "unovan":"unova", "alolan":"alola"}

# Special case: pokemon whose name contains a space
space_mon = [mon for mon in mon_list if " " in mon]

# Delimiters for pairing modifiers with mon names
delimiters = [";", ":", "\n"] # comma implicit

# Make all possible delimiters a comma
for d in delimiters:
	trade_list = trade_list.replace(d,",")

# Add "+" to each species by default?
evo_line_default = "+"*include_evo_line

# Build search string

search_string = ""
mod_string = ""

# Loop through comma-delimited chunks to identify modifier + mon combos
for chunk in trade_list.split(","):

	# Refresh the modifications and mon per chunk
	chunk_mods = []
	chunk_mon = ""

	# Adding space lets users put "+" and "--" keywords next to the mon name
	chunk = chunk.replace("--", "-- ").replace("+", "+ ")

	# Loop through all whitespace- or underscore-delimited bits
	for subchunk in chunk.replace("_", " ").split():

		if subchunk in modifiers: # found a modifier
			chunk_mods.append(subchunk)
		elif subchunk in mod_maps.keys(): # found alternate modifier spelling
			chunk_mods.append(mod_maps[subchunk])
		elif subchunk in mon_list: # found mon name
			chunk_mon = subchunk

	# check for whitespace-containing mon name if none were previously found
	if len(chunk_mon) == 0: 
		for mon in space_mon:
			if mon in chunk:
				chunk_mon = mon

	# Only do anything if chunk contains a mon
	if len(chunk_mon) > 0: 
		
		# Start with default incl/exclusion of line
		chunk_evo_line = evo_line_default 

		# Apply modifiers to the final string
		for mod in chunk_mods:
			if mod == "--": # exclude evos
				chunk_evo_line = ""
			elif mod == "+": # include evos
				chunk_evo_line = "+"
			else: # all other modifiers
				mod_string += "&!" + chunk_evo_line + chunk_mon + "," + mod
		# Add new mon to string
		search_string += chunk_evo_line + chunk_mon + ","

		# Q: What happens if a user puts "+" and "--" keywords?
		# A: Get better users

# Build the final string
if len(search_string) > 0: # only print if any mon found
	print(search_string[:-1] + string_const + mod_string)
