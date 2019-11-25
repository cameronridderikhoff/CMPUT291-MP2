from bsddb3 import db
def get_emails_with_body(bodies):
    database = db.DB() #handle for Berkeley DB database
    database.open("te.idx")
    cursor = database.cursor()
    row_ids = []
    for body in bodies:
        
        if ("%" in body):#remove the %
            body = body[:-1]
            #do a range search of partial matches
            key_val = cursor.get(b"b-" + body.encode(), flags=db.DB_SET_RANGE)
            while ("b-" + body) in key_val[0].decode() and key_val != None:
                row_ids.append(key_val[1].decode())
                key_val = cursor.next()
        else:
            #do a range search
            key_val = cursor.get(b"b-" + body.encode(), flags=db.DB_SET_RANGE)
            while ("b-" + body).encode() in key_val and key_val != None:
                row_ids.append(key_val[1].decode())
                key_val = cursor.next()
    cursor.close()
    database.close()
    return row_ids

def get_emails_with_subject(subjects):
    database = db.DB() #handle for Berkeley DB database
    database.open("te.idx")
    cursor = database.cursor()
    row_ids = []
    for subject in subjects:
        
        if ("%" in subject):#remove the %
            subject = subject[:-1]
             #do a range search of partial matches
            key_val = cursor.get(b"s-" + subject.encode(), flags=db.DB_SET_RANGE)
            while ("s-" + subject) in key_val[0].decode() and key_val != None:
                row_ids.append(key_val[1].decode())
                key_val = cursor.next()
        else:
            #do a range search
            key_val = cursor.get(b"s-" + subject.encode(), flags=db.DB_SET_RANGE)
            while ("s-" + subject).encode() in key_val and key_val != None:
                row_ids.append(key_val[1].decode())
                key_val = cursor.next()
    cursor.close()
    database.close()
    return row_ids

