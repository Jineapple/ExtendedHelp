import csv
import codecs


def filetranslate(dataset,langcode,filename):	
	if(filename[-3:] == "ini"):
		hd = ""
	else:
		hd = "hd"
	column = 2
	if hd:
		column += 1
	if dataset != "ak":
		column += 2
	with codecs.open(langcode+'/translation step 2.csv', 'r', 'utf-8') as csvfile:
		reader_csv = unicode_csv_reader(csvfile)
		header = next(reader_csv, None)
		if header[0] != "old":
			return
		if not hd:
			f = codecs.open(langcode+"/"+dataset+"/"+filename,'r', 'iso-8859-1')	
		else:
			f = codecs.open(langcode+"/hd"+dataset+"/"+filename,'r', 'utf-8')
		print ""
		print hd+dataset+"/"+filename
		translation = f.read()
		f.close()
		#current version of lang is now in translation
		count = 1
		for row in reader_csv:
			#old = len(translation)
			if row[column]:
				translation = translation.replace(row[0],"["+str(count)+"]")
			#print "change: " + str(old - len(translation))
			count += 1		
	with codecs.open(langcode+'/translation step 2.csv', 'r', 'utf-8') as csvfile:	
		reader_csv = unicode_csv_reader(csvfile)
		next(reader_csv, None)
		count = 1		
		for row in reader_csv:		
			translation = translation.replace("["+str(count)+"]",row[column])					
			count += 1				
		if not hd:	
			f = codecs.open(langcode+"/"+dataset+"/"+filename,'w', 'iso-8859-1')				
		else:
			f = codecs.open(langcode+"/hd"+dataset+"/"+filename,'w', 'utf-8')
		f.write(translation)
		f.close()					
			
def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
	csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),dialect=dialect, **kwargs)
	for row in csv_reader:
		yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
	for line in unicode_csv_data:
		yield line.encode('utf-8')

if __name__ == '__main__':
	filetranslate("aoc","de","key-value-modded-strings-utf8.txt")
	filetranslate("aoc","de","language.ini")
	filetranslate("ak","de","key-value-modded-strings-utf8.txt")
	filetranslate("ak","de","language.ini")
	filetranslate("aoc","it","key-value-modded-strings-utf8.txt")
	filetranslate("aoc","it","language.ini")
	filetranslate("ak","it","key-value-modded-strings-utf8.txt")
	filetranslate("ak","it","language.ini")
	filetranslate("aoc","es","key-value-modded-strings-utf8.txt")
	filetranslate("aoc","es","language.ini")
	filetranslate("ak","es","key-value-modded-strings-utf8.txt")
	filetranslate("ak","es","language.ini")