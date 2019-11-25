from bsddb3 import db
import datetime 
import sys
import menu 
import time

def get_emails_with_date(date, date_operator):
    database = db.DB()    
    database.open("da.idx") 
    cur = database.cursor()
    result = cur.first()
    #da=result[0].decode("utf-8")
    #print(da)    
    date_id = []    

    while result:
        time= result[0].decode("utf-8") 
        ids = result[1].decode("utf-8")
        if (':' in date_operator):
            if (time == date):
                date_id.append(ids)
        elif ('<=' in date_operator):
            if  (time <= date):
                date_id.append(ids)
        elif ('<' in date_operator):
            if  (time < date):
                date_id.append(ids)
        elif ('>' in date_operator):
            if  (time > date):
                date_id.append(ids)
        
        elif ('>=' in date_operator):
            if  (time >= date):
                date_id.append(ids)
        result = cur.next()
    cur.close()
    database.close()
    return date_id
    
    
    


  
                      
                  
          
          
          
          
      
   
      


   
