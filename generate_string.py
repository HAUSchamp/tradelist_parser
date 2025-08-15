from tradelist_parser.mon_family_map import mon_family_map
def resolve_mon(mon, fam_mon_map):
	"""
	Resolves name name of family to base Pokemon name, if applicable.
	Otherwise returns name given.
	"""
	if "_UPTO_" in mon:
		added_mon = []
		family, stop_at_mon = mon.split("_UPTO_")
		for m in fam_mon_map[family]:
			added_mon.append(m)
			if stop_at_mon == m:
				break
		return added_mon
	elif "FAMILY" in mon:
		return ["+"+fam_mon_map[mon][0]]
	else:
		return [mon]

def generate_trade_list(trade_list = "", string_const = "&!traded&!shiny&!favorite&!rocket&!4*&!#", evo_line_default = "+"):
	"""
	Function to generate trade strings. `trade_list` is a string 
	including mon names and modifiers, `string_const` is a constant
	appended to the end of the string, and `evo_line_default` is
	"+" (include all family members), "^" (include the line up to the
	specified mon), and "--" (only include that species).
	"""
	trade_list = trade_list.lower()
	
	# Generate mon list from mon -> family map
	mon_list = [k.lower() for k in mon_family_map.keys()]
	
	# Generate family -> mon map
	family_mon_map = {} # use defaultdict
	for k in mon_family_map.keys():
		try:
			family_mon_map[mon_family_map[k]].append(k)
		except KeyError:
			family_mon_map[mon_family_map[k]] = [k]
	
	# In-game search modifiers
	modifiers = ["male", "female", 
	"normal", "fire", "water", "electric", "grass", "ice", "fighting", "poison", "ground", "flying", "psychic", "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy", 
	"kanto", "johto", "hoenn", "sinnoh", "unova", "kalos", "alola", "galar", "hisui", "paldea", 
	"dynamax", "gigantamax",
	"costume",
	"xxs", "xxl",
	"--", "+", "^"]
	
	# Map alternate spellings for modifiers
	mod_maps = {"paldean":"paldea", "hisuian":"hisui", "unovan":"unova", "alolan":"alola", "galarian":"galar"}
	
	# Special case: pokemon whose name contains a space
	space_mon = [mon for mon in mon_list if " " in mon]
	
	# Delimiters for pairing modifiers with mon names
	delimiters = [";", ":", "\n"] # comma implicit
	
	# Make all possible delimiters a comma
	for d in delimiters:
		trade_list = trade_list.replace(d,",")
	
	# Build search string
	mon_to_search = []
	search_modifiers = {}

	# Check evo line default
	if evo_line_default == "-":
		evo_line_default = "--"
		print("replacing '-' with '--' as the evolutionary line default")
	elif not evo_line_default in ["--", "+", "^"]:
		raise Exception("evo_line_default is "+str(evo_line_default)+" but must be in ['--', '+', '^']")
	
	# Loop through comma-delimited chunks to identify modifier + mon combos
	for chunk in trade_list.split(","):
	
		# Refresh the modifications and mon per chunk
		chunk_mods = []
		chunk_mon = ""
	
		# Adding space lets users put "+", "--", and "^" keywords next to the mon name
		chunk = chunk.replace("--", " -- ").replace("+", " + ").replace("^", " ^ ")
	
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
	
			non_evo_mods = []
	
			# Apply modifiers to the final string
			for mod in chunk_mods:
				if mod in ['--', '+', '^']: # line modifier
					chunk_evo_line = mod
				else: # all other modifiers
					non_evo_mods.append(mod)
			if len(chunk_mods) == 0:
				non_evo_mods.append("unmodified")
	
			# If searching for anything in the family, add the family
			if chunk_evo_line == "+": 
				new_mon = mon_family_map[chunk_mon]
			# If searching up to a particular evo, add the family and mon
			elif chunk_evo_line == "^":
				new_mon = mon_family_map[chunk_mon] + "_UPTO_" + chunk_mon
			# Or if searching for only that mon stage, add it to the mon list
			else: 
				new_mon = chunk_mon
			mon_to_search.append(new_mon)
			
			# Add modifiers for new mon, if there are any
			if len(non_evo_mods) > 0:
				if new_mon in search_modifiers:
					search_modifiers[new_mon] += non_evo_mods
				else:
					search_modifiers[new_mon] = non_evo_mods
	
			# Q: What happens if a user puts "+" and "--" keywords?
			# A: Get better users
	
	# Build the final string
	print(mon_to_search)
	all_mon_list = []
	for mon in mon_to_search:
		all_mon_list += resolve_mon(mon, family_mon_map)

	print(all_mon_list)
	all_mon_set = []
	for mon in all_mon_list:
		if mon not in all_mon_set and "+"+mon not in all_mon_set:
			all_mon_set.append(mon)
	print(all_mon_set)
	search_string = ",".join(sorted(all_mon_set))
	
	# Build the string of search modifiers
	mod_string = ""
	mod_errors = []
	
	for k in sorted(search_modifiers.keys()):
		mod_list = list(set(search_modifiers[k]))
		if len(mod_list) > 1:
			mod_errors.append("multiple modifiers found, " + str(mod_list) + ", ignoring modifiers for " +k)
		else:
			if mod_list[0] != "unmodified":
				mod_string += "&!".join([""]+[m + "," + mod_list[0] for m in resolve_mon(k, family_mon_map)])
	
	if len(search_string) > 0: # only print if any mon found
		print(search_string + mod_string + string_const)
	
	if len(mod_errors) > 0:
		print("\n"+"\n".join(mod_errors))

if __name__ == "__main__":
	my_trade_list = """
 	PASTE TRADE LIST HERE
 	"""
	generate_trade_list(my_trade_list, string_const = "&!traded&!shiny&!favorite&!rocket&!4*&!#", evo_line_default = "+")
