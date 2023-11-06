import os
import time
import getpass
import tomllib

from .mailclient import MailClient
from . import notifier

# get every path needed
home_dir = os.path.expanduser("~")
config_dir  = os.path.join(home_dir, ".config/MailNotifier")
config_file = "cred.toml"
config_file_path = os.path.join(config_dir, config_file)

def ask_credentials():
    credentials = {"Protocol":"IMAP",
                   "Domain":"", 
                   "Port":"993",
                   "User":""}
    
    for key in credentials:
        val = input(key+" ["+credentials[key]+"] : ")
        if val != "":
            credentials[key] = val
       
    return credentials

def check_if_file():
    if os.path.isdir(config_dir):
        if os.path.exists(config_file_path):
            return True
    return False

def create_file():
    if check_if_file():
        print("A file already exist !")
        return

    if os.path.isdir(config_dir):
        if os.path.exists(config_file_path):
            try:
                open(config_file_path, 'a').close() # create empty file
            except Exception as e:
                raise e
    else:
        try:
            os.makedirs(config_dir)
            create_file()
        except:
            print("Unable to create config directory.")   


def save_or_not():
    save_cred = input("Would you like your credentials to be saved ? [Y/n]")
    save_it = True
    if(save_cred == "n" or save_cred == "N" or save_cred == "No"):
        save_it = False

    return save_it

def load_credentials():
    with open(config_file_path, 'rb') as tom:
        credentials = tomllib.load(tom)
    return credentials

def write_credentials(creds):
    
    creds_str = ""
    for key in creds:
        # parsing dict to toml-like str
        creds_str+=key+' = "'+creds[key]+'"\n'

    with open(config_file_path, 'w') as tom:
        tom.write(creds_str)

def start():
    
    if check_if_file():
        credentials = load_credentials()
    else:
        credentials = ask_credentials()
        if(save_or_not()):
            create_file()
            write_credentials(credentials)
    
    passwaurd = getpass.getpass("Password per favor : ")
    client = MailClient(protocol = credentials["Protocol"],
                        domain = credentials["Domain"],
                        port = credentials["Port"],
                        user = credentials["User"],
                        password = passwaurd)

    # infinite loop
    notifier.routine(client)
