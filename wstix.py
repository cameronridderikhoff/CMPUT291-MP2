from bsddb3 import db

def get_emails_with_email(email, field):
    database = db.DB()
    database.open("em.idx") 
    cur = database.cursor()
    result = cur.first()
    email_id = []

    while result:
        em=result[0].decode()
        ids=result[1].decode()
        if (field + "-" in em):
            if (em[len(field)+1:] == email):
                e_id = ids
                email_id.append(e_id)
                print(em[len(field)+1:],"|",e_id)
        result = cur.next()
    
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
