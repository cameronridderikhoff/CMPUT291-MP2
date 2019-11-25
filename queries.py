from bsddb3 import db
def get_emails_with_terms(terms, field):
    database = db.DB() #handle for Berkeley DB database
    database.open("te.idx")
    cursor = database.cursor()
    row_ids = []
    for term in terms:
        
        if ("%" in term):#remove the %
            term = term[:-1]
            #do a range search of partial matches
            key_val = cursor.get((field[0] + "-" + term).encode(), flags=db.DB_SET_RANGE)
            while (field + "-" + term) in key_val[0].decode() and key_val != None:
                row_ids.append(key_val[1].decode())
                key_val = cursor.next()
        else:
            #do a range search
            key_val = cursor.get((field + "-" + term).encode(), flags=db.DB_SET_RANGE)
            while (field + "-" + term).encode() in key_val and key_val != None:
                row_ids.append(key_val[1].decode())
                key_val = cursor.next()
    cursor.close()
    database.close()
    return row_ids

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
    database.close()

# Using range serch for when input date and date in database are same
# Do the refular search for others
# Append the row_ID to date_id list
# Close database and return list
def get_emails_with_date(date, date_operator):
    
    database = db.DB()    
    database.open("da.idx") 
    cur = database.cursor()
    date_id = []    
    
   
        
    if (':' in date_operator):
        date=date.encode()
        result = cur.set_range(date)
        
        while result :
            row = result[1].decode()
            date_id.append(row)                     
            result = cur.next_dup() 
               
    elif ('<=' in date_operator):
        result=cur.first()     
        while result :
     
            time=result[0].decode()              
            if  (time <= date):
                d_id = result[1].decode()
                date_id.append(d_id)
            result = cur.next()
        
            
    elif ('<' in date_operator):
        result=cur.first()       
        while result :
            
            time=result[0].decode()             
            if  (time < date):
                d_id = result[1].decode() 
                date_id.append(d_id)
            result = cur.next()
            
    elif ('>=' in date_operator):
        result=cur.first()     
        while result :

            time=result[0].decode()             
            if  (time >= date):
                d_id = result[1].decode() 
                date_id.append(d_id)
            result = cur.next()
        
    
    elif ('>' in date_operator):
        result=cur.first()      
        while result :
            
            time=result[0].decode()             
            if  (time > date):
                d_id = result[1].decode()  
                date_id.append(d_id)
            result = cur.next()    
    cur.close()
    database.close() 
    return date_id
