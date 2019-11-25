#Given the sorted files terms.txt, emails.txt, dates.txt and recs.txt, create the following four indexes:
#(1) a hash index on recs.txt with row ids as keys and the full email record as data
#(2) a B+-tree index on terms.txt with terms as keys and row ids as data
#(3) a B+-tree index on emails.txt with emails as keys and row ids as data
#(4) a B+-tree index on dates.txt with dates as keys and row ids as data.
# the character strings before colon ':' and the data is everything that comes after the colon.
#backslash as a special character
import os

#sort -u: delet the  repeted line
#sort -o: output=FILE Write resut to FILE insted of standard output
# Using break.pl to build idx
def sort():
    
    os.system("sort -u terms.txt -o terms.txt")
    os.system("sort -u emails.txt -o emails.txt")
    os.system("sort -u  dates.txt -o dates.txt")
    os.system("sort -u  recs.txt -o recs.txt")
    
    os.system('perl break.pl <emails.txt > emails_temp.txt')
    os.system('perl break.pl <recs.txt > recs_temp.txt')
    os.system('perl break.pl <terms.txt > terms_temp.txt')
    os.system('perl break.pl <dates.txt > dates_temp.txt')


#The mv command is a command similar to cp, but it is not a copy of a file or directory.
# remove old index
# If the option -T is specified, then the suboption -t;
# suboption -t must be appended, appended to the database type used to specify translation loading after the -T option.
# The -f parameter is followed by a text file containing the username and password. The contents of the file are: odd row username, even row password.
# hash is encrypted using hash code
def dbload():
    
    os.system("db_load -c duplicates=1 -T -t btree -f terms_temp.txt te.idx")
    os.system("db_load -c duplicates=1 -T -t btree -f emails_temp.txt em.idx")
    os.system("db_load -c duplicates=1 -T -t btree -f dates_temp.txt da.idx")
    os.system("db_load -c duplicates=1 -T -t hash -f recs_temp.txt re.idx")
    
    os.system("rm emails_temp.txt")
    os.system("rm recs_temp.txt ")
    os.system("rm dates_temp.txt ")
    os.system("rm terms_temp.txt ")
    
    #os.system('db_dump -p da.idx')
    #os.system('db_dump -p em.idx')
#os.system('db_dump -p te.idx')





if __name__ == "__main__":
    sort()
    dbload()


    

