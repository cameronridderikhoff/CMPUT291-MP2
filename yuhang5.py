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
                d_id = ids
                print(time,"|",d_id)
        elif ('<=' in date_operator):
            if  (time <= date):
                d_id = ids 
                print(time,"|",d_id)
        elif ('<' in date_operator):
            if  (time < date):
                d_id = ids       
                print(time,"|",d_id)
        elif ('>' in date_operator):
            if  (time > date):
                d_id = ids  
                print(time,"|",d_id)
        
        elif ('>=' in date_operator):
            if  (time >= date):
                d_id = ids 
                print(time,"|",d_id)
        result = cur.next()
    cur.close()
    database.close()
    
def get_email_with_body(body):
    database = db.DB()
    database.open("te.idx")
    cur = database.cursor()
    result = cur.first() 
    while result:
        bod=result[0].decode("utf-8")
        ids=result[1].decode("utf-8")
        if ( "b-" in bod):
            if (bod[2:] == body ):
                b_id=ids
                print(bod[2:],"|",b_id)
        result = cur.next()  
    cur.close()
    database.close()         
    
    
    


  
                      
                  
          
          
          
          
      
   
      


   
