from notifypy import Notify
from time import sleep
from email import message

from .mailclient import MailClient 

def send_notif(client,mail_id):
    infos = client.get_message_info(mail_id)
    notif = Notify()
    
    notif.title = "Subject : "+infos['Subject']
    notif.message = "From : "+infos['From'] 
    notif.send()

def routine(client):
 
    last_id = client.get_last_unseen_message_id()
    
    if last_id != -1:
        send_notif(client,last_id)

    while(1):
        sleep(2) # send request for new message every 2 seconds
        new_id = client.get_last_unseen_message_id()
        if (new_id != last_id and new_id != -1):
            last_id = new_id
            send_notif(client,last_id)
