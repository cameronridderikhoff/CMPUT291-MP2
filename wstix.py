from bsddb3 import db
import menu

# field is the option for "from-", "cc-", "bcc-", "to-"
# Using range search to get check does the input email which is plus to field and encode in our database.
# If it in, get the row_id and append it to email_id list

def get_emails_with_email(email,field):
       database = db.DB()
       database.set_flags(db.DB_DUP)
       database.open("em.idx",None, db.DB_BTREE, db.DB_CREATE) 
       cur = database.cursor()
       email_id = []    
       result = cur.set_range((field + "-" + email).encode())
       while (result !=None):
              row = result[1].decode()
              result = cur.next_dup()
              email_id.append(row)                     

       
       cur.close()
       database.close()              
       return email_id








def show_rec(row, size):
       database = db.DB()
       database.open("re.idx")
       record = database.get(row.encode()).decode()
       if size == "brief":
           # Splits record between subject tags
              print(row, record.split("<subj>")[1].split("</subj>")[0])
       else:
           # Prints record in full
              print(record)
