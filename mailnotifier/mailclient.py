import imaplib
from email import message_from_string, message

class MailClient:
    def __init__(
            self,
            protocol="IMAP",
            domain="server.com",
            port="993",
            user="user@server.com",
            password="password"
            ):
        
        self.server = None

        if protocol == "IMAP":
            try:
                self.server = imaplib.IMAP4_SSL(domain, port)
                print("Successfully connected to : "+domain+":"+port)
            except:
                print("Can't connect to server "+domain+':'+port)
        
        try: 
            self.server.login(user, password)
            print("Successfully logged as " + user)
        except Exception as err:
            print("Error : " + repr(err))

    def get_last_unseen_message_id(self, box = "INBOX"):
        self.server.select(box, readonly=True)

        # create id list of unseen messages
        result, data = self.server.uid('search', None, "(UNSEEN)")
        ids = data[0].split()
        if ids != []:       # check if id list is empty
            return ids[-1]  # return last id
        return -1           # if id list empty, return -1

    def get_message_info(self, msg_id, box = "INBOX"):
        
        if msg_id == -1:
            print("Invalid ID")
            return message.Message() # return empty message
        self.server.select(box, readonly=True)
        result, mail_header = self.server.uid('fetch',
                                              msg_id,
                                              '(BODY[HEADER.FIELDS (FROM SUBJECT)])')
        raw_header = mail_header[0][1].decode('utf-8')
        msg = message_from_string(raw_header)
        return msg

