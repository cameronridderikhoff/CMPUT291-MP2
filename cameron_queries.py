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
