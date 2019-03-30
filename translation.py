import csv
import re
import sys

changed = [False] * 1150

def filetranslate(dataset,filename):
	"""
		This translations works with two loops. In the first instance, all patterns of english 
		that should be translated are replaced with temporary text. Based on the ording in translation.csv,
		long patterns are checked before short ones. This way, already translated portions of the text aren't 
		changed again if a different pattern happens to match the already translated text by chance.
		Then in the second loop, the temporary replacements are changed to the actual translation
	"""

	with open('translation.csv', newline='', encoding='utf-8') as csv_file:
		reader_csv = csv.reader(csv_file)
		iter_csv = iter(reader_csv)
		header = next(iter_csv, None)
		if header[0] != "en":
			return	
		translation = []
		if(filename[-3:] == "ini"):
			f = open("en/"+dataset+"/"+filename,'rt', encoding='iso-8859-1')				
		else:
			f = open("en/hd"+dataset+"/"+filename,'rt', encoding='utf-8')
		translation.append(f.read())
		f.close()
		#english version is now in translation[0]
		count = 0
		required_groups = []
		for row in iter_csv:
			#Add possible modifiers like <i> to the pattern. Only the first instance of the modifier is captured
			row[0] = row[0].replace("+",r"\+").replace("(",r"\(").replace(")",r"\)")
			parts = row[0].split(' ')
			first = True
			pattern = ""
			for part in parts:
				if first:
					pattern += "(?:(<b><i>|<i><b>|<b>|<i>)" + part + "(?:<b><i>|<i><b>|<b>|<i>)|" + part + ")"
				if not first:
					pattern += " (?:(?:<b><i>|<i><b>|<b>|<i>)" + part + "(?:<b><i>|<i><b>|<b>|<i>)|" + part + ")"
				first = False
			regex = re.compile(pattern)
			required_groups.append(regex.groups) #Remember how many capturing groups this has for later
			repl = "€"+str(count)
			for i in range(regex.groups):
				repl += "#\\"+str(i+1)
			repl += "€"
			# The A replacement looks e.g. like €27#<i>#2.7€ or €34#€. Split on # (remove the outer €€ first) to get the capturing groups
			# The first is the id, the second is a potential text modifier or empty string. The rest are other capturing groups
			temp = regex.sub(repl, translation[0])
			if temp != translation[0]:
				changed[count] = True
			translation[0] = temp
			count += 1
		for i in range(len(header[4:])):
			translation.append(translation[0])
	with open('temp.txt', newline='', mode="w", encoding='utf-8') as file:
		file.write(translation[0])
		
			
	with open('translation.csv', newline='', encoding='utf-8') as csv_file:
		reader_csv = csv.reader(csv_file)
		iter_csv = iter(reader_csv)
		header = next(iter_csv, None)
		count = 0
		for row in iter_csv:
			#construct the pattern based on how many capturing groups were used for this row in the previous loop
			capture_group = r"#([^#€]*)"
			pattern = "€"+str(count)
			for i in range(required_groups[count]):
				pattern += capture_group
			pattern += "€"
			regex = re.compile(pattern)
			for i in range(len(header[3:])):
				parts = row[i+3].split(' ')
				repl = ""
				for part in parts: # If there are text modifiers, they're added to the replacement
					repl += r"\g<1>" + part + r"\g<1> "
				repl = repl[:-1]
				translation[i] = regex.sub(repl, translation[i])
			count += 1				
		count = 0
		for lang in header[3:]:
			if(filename[-3:] == "ini"):	
				f = open(lang+"/"+dataset+"/"+filename,'w', encoding='iso-8859-1')				
			else:
				f = open(lang+"/hd"+dataset+"/"+filename,'w', encoding='utf-8')
			f.write(translation[count])
			f.close()				
			count += 1
	

def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
	csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),dialect=dialect, **kwargs)
	for row in csv_reader:
		yield [unicode(cell, encoding='utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
	for line in unicode_csv_data:
		yield line.encode(encoding='utf-8')

if __name__ == '__main__':
	assert sys.version_info >= (3, 0)
	filetranslate("aoc","key-value-modded-strings-utf8.txt")
	filetranslate("aoc","language.ini")
	filetranslate("ak","key-value-modded-strings-utf8.txt")
	filetranslate("ak","language.ini")
	for i in range(len(changed)):
		if not changed[i]:
			print (str(i+2) + " hasn't been used")