from bsddb3 import db
import sys
import menu 




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
    
def get_email_with_subject(subjects):
    database = db.DB()
    database.open("te.idx")
    cur = database.cursor()
    result = cur.first() 
    subject_id = []
    while result:
        sub=result[0].decode("utf-8")
        ids=result[1].decode("utf-8")
        if ( "s-" in sub):
            if (sub[2:] in subjects ):
                s_id=ids
                subject_id.append(s_id)
                print(sub[2:],"|",s_id)
        result = cur.next()  
    cur.close()
    database.close()        
    
    
    


  
                      
                  
          
          
          
          
      
   
      


   
