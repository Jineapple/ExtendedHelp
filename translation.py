import csv
import codecs

changed = [False] * 1150

def filetranslate(dataset,filename):	
	with codecs.open('translation.csv', 'r', 'utf-8') as csvfile:
		reader_csv = unicode_csv_reader(csvfile)
		header = next(reader_csv, None)
		if header[0] != "en":
			return	
		translation = []
		if(filename[-3:] == "ini"):
			f = codecs.open("en/"+dataset+"/"+filename,'r', 'iso-8859-1')				
		else:
			f = codecs.open("en/hd"+dataset+"/"+filename,'r', 'utf-8')
		translation.append(f.read())
		f.close()
		#english version is now in translation[0]
		count = 1
		for row in reader_csv:
			temp = translation[0].replace(row[0],"["+str(count)+"]")
			if temp != translation[0]:
				changed[count-1] = True
			translation[0] = temp
			parts = row[0].split(' ')
			first = True
			fullital = ""
			fullbold = ""
			fullboth = ""
			for part in parts:
				ital = "<i>"+part+"<i>"
				bold = "<b>"+part+"<b>"
				both = "<b><i>"+part+"<i><b>"
				if not first:
					ital = " "+ital
					bold = " "+bold
					both = " "+both
				fullital = fullital+ital
				fullbold = fullbold+bold
				fullboth = fullboth+both
				first = False
			temp = translation[0].replace(fullboth,"["+str(count)+"#]")
			if temp != translation[0]:
				changed[count-1] = True
			translation[0] = temp
			temp = translation[0].replace(fullital,"["+str(count)+"*]")
			if temp != translation[0]:
				changed[count-1] = True
			translation[0] = temp
			temp = translation[0].replace(fullbold,"["+str(count)+"~]")
			if temp != translation[0]:
				changed[count-1] = True
			translation[0] = temp
			count += 1
			
					
		for i in range(len(header[4:])):
			translation.append(translation[i])	
	with codecs.open('translation.csv', 'r', 'utf-8') as csvfile:	
		reader_csv = unicode_csv_reader(csvfile)
		next(reader_csv, None)
		count = 1		
		for row in reader_csv:
			for i in range(len(header[3:])):
				translation[i] = translation[i].replace("["+str(count)+"]",row[i+3])		
				parts = row[i+3].split(' ')
				first = True
				fullital = ""
				fullbold = ""
				fullboth = ""
				for part in parts:
					ital = "<i>"+part+"<i>"
					bold = "<b>"+part+"<b>"
					both = "<b><i>"+part+"<i><b>"
					if not first:
						ital = " "+ital
						bold = " "+bold
						both = " "+both
					fullital = fullital+ital
					fullbold = fullbold+bold
					fullboth = fullboth+both
					first = False
				translation[i] = translation[i].replace("["+str(count)+"#]", fullboth)
				translation[i] = translation[i].replace("["+str(count)+"*]", fullital)
				translation[i] = translation[i].replace("["+str(count)+"~]", fullbold)
			count += 1				
		count = 0
		for lang in header[3:]:
			if(filename[-3:] == "ini"):	
				f = codecs.open(lang+"/"+dataset+"/"+filename,'w', 'iso-8859-1')				
			else:
				f = codecs.open(lang+"/hd"+dataset+"/"+filename,'w', 'utf-8')
			f.write(translation[count])
			f.close()				
			count += 1		
			
def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
	csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),dialect=dialect, **kwargs)
	for row in csv_reader:
		yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
	for line in unicode_csv_data:
		yield line.encode('utf-8')

if __name__ == '__main__':
	filetranslate("aoc","key-value-modded-strings-utf8.txt")
	filetranslate("aoc","language.ini")
	filetranslate("ak","key-value-modded-strings-utf8.txt")
	filetranslate("ak","language.ini")
	for i in range(len(changed)):
		if not changed[i]:
			print str(i+2) + " hasn't been used"