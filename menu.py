import queries
class menu:
    def __init__(self):
        self.star = "*************************"
        self.size = "brief"
        super().__init__()
    
    # This method controls the users queries to the database index files.
    # It interacts with the user to get their queries, and converts the plain
    # text input into a format useable by the methods we are producing.
    # Possible query entries: date, subject, body, from, to, cc and bcc
    def main_menu(self):
        print(self.star)
        print("Welcome to the Mini Project 2")
        print("Press e to exit.")
        print("Enter output=full to see full record.")
        print("Enter output=brief to see just the id and title.")
        print(self.star)
        i = input("Please enter your query: ")
        while i.lower() != "e":
            if i.lower() == "output=full":
                self.size = "full"
            elif i.lower() == "output=brief":
                self.size = "brief"
            else:
                q = i.lower().split() # splits by whitespace, and there must be a space between each item of the query
                query = []
                for j in range(len(q)):
                    # combine the query commands with their respective symbols
                    # Eg. "date     :     2019/10/10 becomes ["date:", "2019/10/10"]
                    if q[j] == ":" or q[j] == ">" or q[j] == "<" or q[j] == ">=" or q[j] == "<=":
                        query.append(q[j-1] + q[j])
                    else:
                        # check to see if the first character is a symbol, if it
                        # is, we need to append the symbol to the previous entry
                        # and remove it from the current entry
                        if q[j][0] == ":":
                            query.append(q[j-1] + ":")
                            q[j] = q[j][1:]
                        elif q[j][0] == "<":
                            if  q[j][1] == "=":
                                q[j] = q[j][2:]
                                query.append(q[j-1] + "<=")
                            else:
                                q[j] = q[j][1:] 
                                query.append(q[j-1] + "<")
                        elif q[j][0] == ">":
                            if q[j][1] == "=":
                                q[j] = q[j][2:]
                                query.append(q[j-1] + ">=")
                            else:
                                q[j] = q[j][1:]
                                query.append(q[j-1] + ">")

                        # split the : using commands by their colon, and the <,
                        # >, >=, <= commands (date) by that character
                        if not (q[j] == "date" or q[j] == "subj" or q[j] == "body" or q[j] == "from" or q[j] == "to" or q[j] == "cc" or q[j] == "bcc"):
                            if len(q[j].split(":")) > 1:
                                query.append(q[j].split(":")[0] + ":")
                                query.append(q[j].split(":")[1])
                            # must check ">=" and "<=" first, since they will
                            # also have a result of len() > 1 if we split them
                            # on ">" or "<"
                            elif len(q[j].split(">=")) > 1:
                                query.append(q[j].split(">=")[0] + ">=")
                                query.append(q[j].split(">=")[1])
                            elif len(q[j].split("<=")) > 1:
                                query.append(q[j].split("<=")[0] + "<=")
                                query.append(q[j].split("<=")[1])
                            elif len(q[j].split(">")) > 1:
                                query.append(q[j].split(">")[0] + ">")
                                query.append(q[j].split(">")[1])
                            elif len(q[j].split("<")) > 1:
                                query.append(q[j].split("<")[0] + "<")
                                query.append(q[j].split("<")[1])
                            else:
                                query.append(q[j])

                #used to let the system know what the next item will be
                next_item = ""

                date = ""
                date_operator = ""
                from_who = ""
                subject = []
                body = []
                to_who = []
                cc = []
                bcc = []
                subj_or_body = []
                for item in query:
                    if item == "":
                        continue
                    if next_item == "d":
                        date = item
                        next_item = "" #reset next_item
                    elif next_item =="s":
                        subject.append(item)
                        next_item = ""
                    elif next_item == "b":
                        body.append(item)
                        next_item = ""
                    elif next_item == "f":
                        from_who = item
                        next_item = ""
                    elif next_item == "t":
                        to_who.append(item)
                        next_item = ""
                    elif next_item == "c":
                        cc.append(item)
                        next_item = ""
                    elif next_item == "bc":
                        bcc.append(item)
                        next_item = ""
                    elif "date:" in item or "date>" in item or "date<" in item:
                        next_item = "d"
                        date_operator = item.split("date")[1]
                    elif "subj:" in item:
                        next_item = "s"
                    elif "body:" in item:
                        next_item = "b"
                    elif "from:" in item:
                        next_item = "f"
                    elif "to:" in item:
                        next_item = "t"
                    elif "bcc:" in item:
                        next_item = "bc"
                    elif "cc:" in item:
                        next_item = "c"
                    else:
                        subj_or_body.append(item)
                #call query methods here!!
                self.call_query(date, date_operator, subject, body, from_who,
                                to_who, cc, bcc, subj_or_body, self.size)
            print(self.star)
            print("Press e to exit.")
            print("Enter output=full to see full record.")
            print("Enter output=brief to see just the id and title.")
            i = input("Please enter your query: ")

    def call_query(self, date, date_operator, subject, body, from_who, to_who,
                   cc, bcc, subj_or_body, size):

        match = {"date":set(), "from":set(), "to":set(), "cc":set(),
                 "bcc":set(), "subj":set(), "body":set(), "term":set()}

        if date:
            [match["date"].add(record) for record in queries.get_emails_with_date(date, date_operator)]
        if from_who:
            [match["from"].add(record) for record in queries.get_emails_with_email(from_who, "from")]
        if to_who:
            recipients = [set(queries.get_emails_with_email(email, "to")) for email in to_who]
            # Returns intersection of all row ids with given emails in "to" field
            # set intersection from https://stackoverflow.com/a/2541814
            if recipients:
                match["to"] = set.intersection(*recipients)
        if cc:
            recipients = [set(queries.get_emails_with_email(email, "cc")) for email in cc]
            if recipients:
                match["cc"] = set.intersection(*recipients)
        if bcc:
            recipients = [set(queries.get_emails_with_email(email, "bcc")) for email in bcc]
            if recipients:
                match["bcc"] = set.intersection(*recipients)
        if subject:
            match["subj"] = set(queries.get_emails_with_terms(subject, "s"))
        if body:
            match["body"] = set(queries.get_emails_with_terms(body, "b"))
        if subj_or_body:
            # sets emails to all the rows where the terms in subj_or_body are in
            # the subject or the body fields
            emails = [set(queries.get_emails_with_terms(subj_or_body, "b")),
                      set(queries.get_emails_with_terms(subj_or_body, "s"))]
            if emails:
                match["term"] = set.union(*emails)

        row_ids = []
        for key in match:
            if match[key]:
                row_ids.append(match[key])
        if row_ids:
            row_ids = set.intersection(*row_ids)

        for row in row_ids:
            queries.show_rec(row, size)
        

if __name__ == "__main__":
    m = menu()
    m.main_menu()
