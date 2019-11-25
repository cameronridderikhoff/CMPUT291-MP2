from bsddb3 import db

# field is the option for "from-", "cc-", "bcc-", "to-"
# Using range search to get check does the input email which is plus to field and encode in our database.
# If it in, get the row_id and append it to email_id list

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
