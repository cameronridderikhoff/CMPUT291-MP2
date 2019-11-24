from bsddb3 import db
import datetime 
import sys
import menu 
import time

def get_emails_from(email):
    database = db.DB()
    database.open("em.idx") 
    cur = database.cursor()
    result = cur.first()
    email_id = []
    while result:
        em=result[0].decode("utf-8")
        ids=result[1].decode("utf-8")

        if ("from-" in em):
            if (em[5:] == email):
                e_id=ids
                email_id.append(e_id)
                print(em[5:],"|",e_id)
                email_id.append(e_id)
        result = cur.next()
    
    cur.close()
    database.close() 
    


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
                date_id.append(d_id)
                print(time,"|",d_id)
        elif ('<=' in date_operator):
            if  (time <= date):
                d_id = ids 
                date_id.append(d_id)
                print(time,"|",d_id)
        elif ('<' in date_operator):
            if  (time < date):
                d_id = ids
                date_id.append(d_id)
                print(time,"|",d_id)
        elif ('>=' in date_operator):
            if  (time >= date):
                d_id = ids 
                date_id.append(d_id)
                print(time,"|",d_id)
        
        elif ('>' in date_operator):
            if  (time > date):
                d_id = ids 
                date_id.append(d_id)
                print(time,"|",d_id)
        result = cur.next()
    cur.close()
    database.close() 

def get_emial_cc(email):
    database = db.DB()
    database.open("em.idx") 
    cur = database.cursor()
    result = cur.first()
    #em=result[0].decode("utf-8")
    #print(em)
    cc_id = []
    while result:
        em=result[0].decode("utf-8")
        ids=result[1].decode("utf-8")
        #print(em)
        #print(ids)
        if ("cc-" in em):
            if (em[4:] == email):
                #print(em)
                e_id=ids
                #print(e_id)
                cc_id.append(e_id)
                print(em[4:],"|",e_id)
        result = cur.next()
    
        #print(em)
    cur.close()
    database.close() 
    
def get_email_with_body(body):
    database = db.DB()
    database.open("te.idx")
    cur = database.cursor()
    result = cur.first() 
    cody_id = []
    while result:
        bod=result[0].decode("utf-8")
        ids=result[1].decode("utf-8")
        if ( "b-" in bod):
            if (bod[2:] == body ):
                b_id=ids
                cody_id.append(b_id)
                print(bod[2:],"|",b_id)
        result = cur.next()  
    cur.close()
    database.close()         
    
    
    


  
                      
                  
          
          
          
          
      
   
      


   
