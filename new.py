from bsddb3 import db
from datetime import datetime
import sys
import numpy
def getvalue(string,i):
    value = ""
    while True:
        if string[i] == ' ':
            i+=1
        else: 
            while i<len(string):
                value  += string[i]
                
                if string[i] == ' ' or i==len(string)-1:
                    
                    return value, i
                else:
                    i += 1


while True:
    database = db.DB()    
    inp = input("enter:")
    string = ""
    i=0
    oprator =''
    d_id=''
    while i < len(inp) :
        if inp=="e":
            sys.exit()
        elif inp[i] != ' ':
            if inp[i] == ':':
                i+=1
                string = str(string)   
                if string=="date":
                    database.open("da.idx") 
                    cur = database.cursor()
                    result = cur.first()
                    date_id = []    
                
                    while result:
                        time= result[0].decode("utf-8")
                        ids = result[1].decode("utf-8")
                        if ('=' or':' in inp):
                            if  (datetime.strptime(time, "%y/%m/%d") == datetime.strptime(date, "%y/%m/%d")):
                                print(time)
                                d_id = ids(result[1])  
                                print(d_id)
                        elif ('<=' in inp):
                            if  (datetime.strptime(time, "%d/%m/%y") <= datetime.strptime(date, "%d/%m/%y")):
                                d_id = ids(result[1]) 
                        elif ('<' in inp):
                            if  (datetime.strptime(time, "%d/%m/%y") < datetime.strptime(date, "%d/%m/%y")):
                                d_id = ids(result[1])         
                        elif ('>' in inp):
                            if  (datetime.strptime(time, "%d/%m/%y") > datetime.strptime(date, "%d/%m/%y")):
                                d_id = ids(result[1])    
                        elif ('>=' in inp):
                            if (datetime.strptime(time, "%d/%m/%y") >= datetime.strptime(date, "%d/%m/%y")):
                                d_id = ids(result[1])     
                        if (d_id != ''):
                            date_id.append(d_id)
                            print(date_id)
                            item_id = ''
                        result = cur.next()                        
                    [date,i] = getvalue(inp,i)
                    string = ""
                    print("date:",date)
                    cur.close()
                    database.close() 
                
                
                elif string== "from":
                    [email,i] = getvalue(inp,i)
                    string = ""
                    print("enter email is:",email)
                    database.open("em.idx") 
                    cur = database.cursor()
                    result = cur.first()
                    #em=result[0].decode("utf-8")
                    #print(em)
                    email_id = []
                    while result:
                        em=result[0].decode("utf-8")
                        ids=result[1].decode("utf-8")
                        #print(em)
                        #print(ids)
                        if ("from-" in em):
                            #print(em[5:])
                            if (em[5:] == email):
                                #print(em)
                                e_id=ids
                                #print(e_id)
                                email_id.append(e_id)
                                print(em[5:],"|",e_id)
                        result = cur.next()
                    
                        #print(em)
                    cur.close()
                    database.close() 
                    
                    
                            
                        
                        
                        
                    
            
            
            
            
            else:
                string += inp[i]
        i +=1
   
      


   
