    
from bsddb3 import db
import sys
import re
import string
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring, tostringlist


#https://docs.python.org/2/library/xml.etree.elementtree.html

#First thing we want to use is element tree to iterate over the XML file and remove all of the useful info.
#Then we want to take that useful info and split it up into 4 files:

#terms.txt: This file includes terms extracted from email subject and body; for our purpose, suppose a term is a consecutive sequence of alphanumeric, underscore '_' and dashed '-' characters, i.e [0-9a-zA-Z_-]. 
#The format of the file is as follows: for every termT in the subject of an email with row id I, there is a row in this file of the form s-T':I whereT' is the lowercase form of T. 
#For every term T in the body field of an email with row id I, there is a row in this file of the form b-T':I, whereT' is again the lowercase form of T. Ignore all special characters coded as &#number; such as &#10; and &lt;, &gt;, &amp;, &apos; and &quot;. 
#Also ignore terms of length 2 or less. Convert the terms to all lowercase before writing them out. Here are the respective files for our input files with 10 records and 1000 records.

#emails.txt: This file includes one line for every email address that appears in a from, to, cc and bcc field. The format of each line is FLD-E:I where E is an email address all in lowercase, 
#I is the row id of the email and FLD is the field where the email is mentioned, which takes the values of from, to, cc and bcc. Email addresses that are not in lowercase are converted to lowercase before they are written to this file. 
#Here are the respective files for our input files with 10 records and 1000 records.

#dates.txt: This file includes one line for each email record in the form of d:l where d is the date of the email, and l is the row id. Here are the respective files for our input files with 10 records and 1000 records.

#recs.txt: This file includes one line for each email in the form of I:rec where I is the row id and rec is the full email record in XML. Here are the respective files for our input files with 10 records and 1000 records.

tree = ET.parse('10.xml')
root = tree.getroot()


def main():	
	get_terms()
	get_emails()
	get_dates()
	get_recs()


def get_terms():
	file = open("terms.txt","w") 
	#I tried both the translate and re.sub libraries to see what would be better. It looks like re.sub is better for removing special characters as we can choose what gets removed and what doesnt.
	for mail in root.findall('mail'):
		body = mail.find('body').text
		subject = mail.find('subj').text
		rowid = mail.find('row').text #This gets appended on to each of the words after they're split 
		
		if subject:
			lowersubject = subject.lower()
			splitsubject = re.split(r'[^0-9a-zA-Z_-]', lowersubject)
			splitsubjectnoempty = list(filter(None, splitsubject))
			finalsubject = list(filter(lambda word: len (word) > 2, splitsubjectnoempty))
			for i in finalsubject:			
				print("s-" + i + ":" + rowid)
				#print("length: " + str(len(term)))
				file.write("s-" + i + ":" + rowid + "\n")
		else:
			pass
		
		if body:
			lowerbody = body.lower()
			splitbody = re.split(r'[^0-9a-zA-Z_-]', lowerbody)
			splitbodynoempty = list(filter(None, splitbody))
			finalbody = list(filter(lambda word: len (word) > 2, splitbodynoempty))
			for j in finalbody:			
				print("b-" + j + ":" + rowid)
				#print("length: " + str(len(term)))
				file.write("b-" + j + ":" + rowid + "\n")
		else:
			pass
	file.close()


def get_emails():
	file = open("emails.txt", "w")
	for mail in root.findall('mail'):
		data = []
		fromTxt = mail.find('from').text
		fromTxt = fromTxt.lower()
		toTxt = mail.find('to').text
		toTxt = toTxt.lower()
		row = mail.find('row').text
		print("from-" + fromTxt + ":" + row)
		print("to-" + toTxt + ":" + row)
		file.write("from-" + fromTxt + ":" + row + "\n")
		file.write("to-" + toTxt + ":" + row + "\n")

		cc = mail.find('cc').text
		bcc = mail.find('bcc').text

		if cc != None:
			file.write("cc-"+ cc + ":" + row + "\n")
		
		if bcc != None:
			file.write("bcc-"+ bcc + ":" + row + "\n")

	file.close()


def get_dates():
	file = open("dates.txt", "w")
	for mail in root.findall('mail'):
		date = mail.find('date').text
		row = mail.find('row').text
		if date:
			file.write(date + ':' + row + '\n')
		else:
			pass
	file.close()


def get_recs():
	file = open('recs.txt', 'w')
	#xml_str = tostringlist(root.find('mail'))
	#mails = root.findall('.//mail')
	#print(mails)

	for mail in root.findall('mail'):
		row = mail.find('row').text
		body_xml = str(tostring(mail))
		stripped_xml_left = body_xml.lstrip("b'")
		stripped_xml_right = stripped_xml_left.rstrip("'")
		stripped_xml_right2 = stripped_xml_right.rstrip('n')
		stripped_xml_final = stripped_xml_right2.rstrip("\\")

		print(row + ":" + stripped_xml_final)
		file.write(row + ":" + stripped_xml_final)
		file.write("\n")

	#print(body_xml)
	#for mail in root.findall('mail'):
	#	row = mail.find('row').text
		#raw_xml = str(ET.tostring(mail))
		#stripped = re.sub('[^A-Za-z0-9]+', '&#10', raw_xml)
		#file.write(row + ':' + stripped + '\n')
		
	file.close()



