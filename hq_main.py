import asyncio, os, time, colorama, networking, socket
from datetime import datetime
from _thread import start_new_thread
from discord import Webhook



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
    
    Version 1.2.2
    
    New Features (Since Last Version)):
    -> This Screen
    
    Upcoming Features:
    -> Reduce the number of times Method 1 is inconclusive (can't find an answer)
    -> Better Anti-Bot Question detection
    -> Points displayed for each answer
    -> Android App (possible)
    
    Contact me at caffiene0addict0420@gmail.com to suggest features / improvements
    
    If you like the bot, please tell colleagues or friends about us :)
    
    
    """

    ip2 = "0.0.0.0"
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((ip2, 80))
    serversocket.listen(5)
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
        "hqtriviabot123", #Valid Forever
        "LittleBird", #Valid Until 12th July
        "Pardeep", #Valid Until 12th July
        "LmaoMaxi", #Valid Until 12th June
        "JacobBurns", #Valid Until 4th July
        "DKAMV", #Valid Until 5th July
        "yoelZ", #13th June
        "JustinS", #14th June
        "upflare", #16th June
        "jeffery", #16th June
        "hexcruncher", # 18th June
    ]
    if data in valid:
        lines = """"""
        for line in open("uk.txt"):
            lines = lines + line + "\n"
        return lines
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
main_url = "https://api-quiz.hype.space/shows/now?type=hq&userId=%s" % USER_ID
headers = {"Authorization": "Bearer %s" % BEARER_TOKEN,
           "x-hq-client": "Android/1.3.0"}
# "x-hq-stk": "MQ==",
# "Connection": "Keep-Alive",
# "User-Agent": "okhttp/3.8.0"}
start_new_thread(processConn, ())
lastCTime = time.time()
while True:
    offse = time.time() - lastCTime
    if int(offse) < 60: 
        print()
        try:
            response_data = asyncio.get_event_loop().run_until_complete(
                networking.get_json_response(main_url, timeout=1.5, headers=headers))
        except:
            print("Server response not JSON, retrying...")
            time.sleep(1)
            continue

        if "broadcast" not in response_data or response_data["broadcast"] is None:
            if "error" in response_data and response_data["error"] == "Auth not valid":
                raise RuntimeError("Connection settings invalid")
            else:
                print("Show not on.")
                try:
                    next_time = datetime.strptime(response_data["nextShowTime"], "%Y-%m-%dT%H:%M:%S.000Z")
                    now = time.time()
                    offset = datetime.fromtimestamp(now) - datetime.utcfromtimestamp(now)
                    print("Next UK game will be at: %s UTC" % str((next_time + offset).strftime('%Y-%m-%d %I:%M %p')))
                    print("Prize: " + response_data["nextShowPrize"])
                    with open("uk.txt", "w") as uk:uk.write("Next UK game will be at: %s UTC" % str((next_time + offset).strftime('%I:%M %p')) + "\n" + "Prize: " + response_data["nextShowPrize"])
                    #Webhook("https://discordapp.com/api/webhooks/452560674116337674/nxpS2Qn7pOBsE_sJqAANWqXQzh1Xar0DsdS5sARojRsLfuSVAVk20vQxVMSHbde46ri4",msg="Next UK game will be at: %s UTC" % str((next_time + offset).strftime('%I:%M %p')) + "\n" + "Prize: " + response_data["nextShowPrize"]).post()
                    #https://discordapp.com/api/webhooks/452830709401255936/9VRsugrmKPqSzV9HoAH8CHDFL4M5yWNAW3fpCZJDTTgVgh-Ttbb4I_pQyC-kssFhSijt
                except Exception as e:print(e)

          
                time.sleep(5)
        else:
            socket = response_data["broadcast"]["socketUrl"].replace("https", "wss")
            print("Show active, connecting to socket at %s" % socket)
            AREconnected = []
            with open("uk.txt", "w") as uk:uk.write("Show active, connecting...")
            #Webhook("https://discordapp.com/api/webhooks/452560674116337674/nxpS2Qn7pOBsE_sJqAANWqXQzh1Xar0DsdS5sARojRsLfuSVAVk20vQxVMSHbde46ri4",msg="Show active, connecting to socket at %s" % socket).post()
            try:Webhook("https://discordapp.com/api/webhooks/452830709401255936/9VRsugrmKPqSzV9HoAH8CHDFL4M5yWNAW3fpCZJDTTgVgh-Ttbb4I_pQyC-kssFhSijt",msg="Show active, connecting to socket at %s" % socket).post()
            except:pass
            asyncio.get_event_loop().run_until_complete(networking.websocket_handler(socket, headers))
