import asyncio, os, time, colorama, networking, socket, random
from datetime import datetime
from _thread import start_new_thread
from discord import Webhook
import extralives


# Set up color-coding
colorama.init()

uk = True

AREconnected = []

def processConn():
    global AREconnected
    global lastCTime
    startMSG = """
    ##############
    #Using ACEBOT#
    ##############
    
    Version 1.2.6
    

    New Features (Since Last Version)):
    -> Even More Bug Fixes (fingers crossed)
    -> More Progress with both the account creator and extra lives bot
    
    Upcoming Features:
    -> Better Anti-Bot Question detection
    -> Points displayed for each answer
    -> Android App (possible)
    -> Semi-Auto UK or US Account Creator Bot (in development)
    -> Semi-Auto Extra Lives Bot (in development)
    
    Contact me at caffiene0addict0420@gmail.com to suggest features / improvements
    
    If you like the bot, please tell colleagues or friends about us :)
    
    
    """

    ip2 = "0.0.0.0"
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((ip2, 80))
    serversocket.listen(20)
    while True:
        try:
            clientsocket, addr = serversocket.accept()
            recieved = clientsocket.recv(1024)
            recieved = recieved.decode("utf-8", "replace")
            if addr[0] in AREconnected:
                data = getResponse(recieved)
            else:
                data = startMSG
                AREconnected.append(addr[0])
                
            clientsocket.send(data.encode("utf-8", "replace"))
            clientsocket.close()
            lastCTime = time.time()
        except Exception as e:print(e)

def getResponse(data): 
    valid = [
        "AranMartin", #Valid Forever
        "7vsquad", #Valid Forever
        "LittleBird", #Valid Until 13th July
        "Pardeep", #Valid Until 13th July
        #"LmaoMaxi", #Valid Until 13th June
        "JacobBurns", #Valid Until 5th July
        "DKAMV", #Valid Until 6th July
        #"yoelZ", #14th June
        #"JustinS", #15th June
        "upflare", #17th July
        #"jeffery", #17th June
        "hexcruncher", # 19th June
        "jacobpotter", #23rd June
        "chris", #23rd Jun
    ]
    if ":" in data:
        data = data.split(":")
        if data[0] not in valid:return "Invalid Login"
        if data[1] == "verify":
            try:return "Your Extra Life Auth Code is " + str(extralives.verify(data[2]))
            except:return "Invalid Phone Number. Example of valid phone number: +14242196850"
        elif data[1] == "create":
            if len(data) != 5:
                return("Invalid Number of Arguments to create an account")
            ver = data[2]
            code = data[3]
            region = data[4].upper()
            u = "False"
            while u == "False":
                uname = str(random.randint(1000, 100000))
                u = str(extralives.username_available(uname))
            if str(extralives.submit_code(ver, code)) == "True":
                try:
                    auth = extralives.create_user(uname, ver, "sovietSpy666", region)['authToken']
                    test = extralives.HQClient(auth)
                    if test.make_it_rain() != True:return("Could not provide extra life to account")
                    else:return("Wahoo! Extra life given to the account!") 
                except:
                    return("Invalid")
            else:
                return("Invalid Code")
        else:
            return("Invalid Method")
    else:
        if data in valid:
            try:
                lines = """"""
                for line in open("uk.txt"):
                    lines = lines + line + "\n"
                return lines
            except:return("An exception occured server-side, please bear with us")
        else:return """ERROR- invalid logon - check you have the right password, and your access is still valid.
    https://github.com/Caffiene0Addict0420/HQ-Trivia-Acebot
    Has been taken down so this bot doesn't attract the attention of HQ Trivia, and there are enough people subscribed to fund the server.
    
    To extend your access / buy access (you can still refer friends etc) email me at caffiene0addict0420
            """


if uk == True:c = "ukconn.txt"
else:c = "usconn.txt"

# Read in bearer token and user ID
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), c), "r") as conn_settings:
    settings = conn_settings.read().splitlines()

    try:
        BEARER_TOKEN = settings[0].split("=")[1]
        USER_ID = settings[1].split("=")[1]
    except IndexError as e:
        raise e

print("Starting up Bot...")
main_url = "https://api-q
