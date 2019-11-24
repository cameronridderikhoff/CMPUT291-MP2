import re
class prep_data:
    # This function does the "menu" portion of this program, allowing the user to prepare as many files as they would like
    def main(self):
        while True:
            print("Press 'e' at any time to exit this program.")
            file_name = input("Please enter the name of the XML file: ")
            if (file_name == "e"):
                return
            self.parse_xml(file_name)

    # This function does the actual parsing of the xml file, and creates 4 new files with the parsed data:
    # terms.txt, emails.txt, dates.txt, recs.txt
    def parse_xml(self, xml_file):
        #try:
            # automatically closes file once the "with" ends
            with open(xml_file) as file_object:
                #the data files we will write to
                terms = open("terms.txt", 'w')
                emails = open("emails.txt", 'w')
                dates = open("dates.txt", 'w')
                recs = open("recs.txt", 'w')

                for line in file_object:
                    # check the split of <mail> to ensure we only add emails
                    if len(line.split("<mail>")) > 1:
                        # Get the row number of this record by
                        # splitting the line "<mail><row>532</row><date>..." into ["<mail>", "532</row><date>"]
                        # and get the integers 5, 3, 2 and set the row variable to that set of integers.
                        row = self.parse_data_single(line, "row")
                        # Add the full record to recs.txt
                        recs.write(row + ":" + line)


                        # Get the date of this record by splitting the line 
                        # "<mail><row>532</row><date>2000/09/13</date>..." into 
                        # ["<mail><row>532</row>", "2000/09/13</date>"]
                        # and get the characters 2, 0, 0, 0, /, 0 ,9, /, 1, 3 
                        # and save them in the dates file
                        date = self.parse_data_single(line, "date")
                        dates.write(date.lower() + ":" + row + "\n")

                        # Get the email addresses of this record by splitting the line 
                        # "<mail>...<from>phillip.allen@enron.com</from><to>david.delainey@enron.com</to><subj></subj><cc></cc><bcc></bcc>..."
                        # into ["<mail>...", "phillip.allen@enron.com</from>..."] to get the "from" field
                        # into ["<mail>...", "david.delainey@enron.com</to>..."] to get the "to" field
                        # into ["<mail>...", "</cc>..."] to get the cc field
                        # into ["<mail>...", "</bcc>..."] to get the bcc field
                        # get the characters that comprise the email addresses and save them in the emails file
                        addresses = self.parse_data_single(line, "from")
                        emails.write("from-" + addresses.lower() + ":" + row + "\n")

                        addresses = self.parse_data_multiple(line, "to")
                        for address in addresses:
                            emails.write("to-" + address.lower() + ":" + row + "\n")

                        addresses = self.parse_data_multiple(line, "cc")
                        for address in addresses:
                            emails.write("cc-" + address.lower() + ":" + row + "\n")

                        addresses = self.parse_data_multiple(line, "bcc")
                        for address in addresses:
                            emails.write("bcc-" + address.lower() + ":" + row + "\n")

                        # Get the terms of this record by splitting the line
                        # "<mail>...<subj>This email is very important</subj><body>Blah blah blah</body>..."
                        # into ["<mail>...", "This email is very important</subj>..."]
                        # into ["<mail>...", "Blah blah blah</body>..."]
                        subjs = self.parse_terms(line, "subj")
                        for subj in subjs:
                            terms.write("s-" + subj.lower() + ":" + row + "\n")

                        bodies = self.parse_terms(line, "body")
                        for body in bodies:
                            terms.write("b-" + body.lower() + ":" + row + "\n")
                        
                terms.close()
                emails.close()
                dates.close()
                recs.close()
                print("Files successfully generated")
        #except:
        #    print("Unable to open file, please try again.\n")

    # This method is used to parse a line, given a split factor.
    # It only looks for a single item, and returns a string.
    # line is the line we are currently parsing
    # split_factor is the tag we want to split the line by
    def parse_data_single(self, line, split_factor):
        line_split = line.split("<" + split_factor + ">")
        # Checks that "<split_factor>" appears in the line, should always go into this if statement
        # if we dont, then that means that there may be no data in the "<split_factor>" tag
        if len(line_split) > 1: 
            word = ""
            i=0
            char = line_split[1][i]
            while char != "<":
                word = word + char
                i += 1
                char = line_split[1][i]
        else:
            # if the "</split_factor>" tag exists, then we know the data file is fine, but there is no data in this record
            # under this split_factor, so we return None
            if len(line.split("</" + split_factor)) > 1:
                return None
            else:
                # This means that the "</split_factor>" tag does not exist, so the data file is formatted incorrectly
                raise(ValueError("The input file is incorrect."))
        return word
    
    # This method is used to parse a line, given a split factor.
    # It looks for multiple items separted by a ",", and returns a list of strings.
    # line is the line we are currently parsing
    # split_factor is the tag we want to split the line by
    def parse_data_multiple(self, line, split_factor):
        line_split = line.split("<" + split_factor + ">")        # Checks that "<split_factor>" appears in the line, should always go into this if statement
        # if we dont, then that means that there may be no data in the "<split_factor>" tag
        if len(line_split) > 1: 
            i=0
            char = line_split[1][i]
            word = ""
            words = []
            while char != "<":
                if char == ",":
                    words.append(word)
                    word = ""
                else:
                    word = word + char
                    i += 1
                    char = line_split[1][i]
            if word != "":
                words.append(word)
                
        else:
            # if the "</split_factor>" tag exists, then we know the data file is fine, but there is no data in this record
            # under this split_factor, so we return None
            if len(line.split("</" + split_factor)) > 1:
                return None
            else:
                # This means that the "</split_factor>" tag does not exist, so the data file is formatted incorrectly
                raise(ValueError("The input file is incorrect."))
        return words

    # This method is used to parse a line, given a split factor.
    # It looks for multiple terms, and returns a list of strings.
    # The terms are defined in our requirements as
    # "a consecutive sequence of alphanumeric, underscore '_' and dashed '-' characters".
    # line is the line we are currently parsing
    # split_factor is the tag we want to split the line by
    def parse_terms(self, line, split_factor):
        line_split = line.split("<" + split_factor + ">")
         # if we dont, then that means that there may be no data in the "<split_factor>" tag
        if len(line_split) > 1: 
            i=0
            char = line_split[1][i]
            word = ""
            words = []
            while char != "<":
                if re.match("[0-9a-zA-Z_-]", char):
                    word = word + char
                    i += 1
                    char = line_split[1][i]

                #this means we have a special character that we need to ignore
                if re.match("[&]", char):
                    special = ""
                    while not re.match("[;]", char):
                        i += 1
                        char = line_split[1][i]
                        special = special + char
                    #make sure it is not a number, which we simply ignore
                    if not "#" in special:
                        if (len(word) <= 2):
                            word = ""
                # ignore terms of length <= 2, such as "if", "or", and "by"
                if len(word) > 2 and not re.match("[0-9a-zA-Z_-]", char):
                    words.append(word)
                    word = ""
                # if the term is of length <= 2 and we have reached a space, remove this term from 
                # the "word" variable
                elif len(word) <= 2 and re.match("[ :]", char):
                    word = ""
                # we do the re.match() check to ensure we aren't skipping any important characters
                if not re.match("[0-9a-zA-Z<_-]", char):
                    i += 1
                    char = line_split[1][i] 
        else:
            # if the "</split_factor>" tag exists, then we know the data file is fine, but there is no data in this record
            # under this split_factor, so we return None
            if len(line.split("</" + split_factor)) > 1:
                return None
            else:
                # This means that the "</split_factor>" tag does not exist, so the data file is formatted incorrectly
                raise(ValueError("The input file is incorrect."))
        return words
if __name__ == "__main__":
    m = prep_data()
    m.main()