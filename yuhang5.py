from bsddb3 import db
import sys


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


    


   
