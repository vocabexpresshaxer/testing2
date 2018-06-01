import asyncio, os, time, colorama, networking, socket
from datetime import datetime
from _thread import start_new_thread


# Set up color-coding
colorama.init()

uk = True

def processConn():
    global lastCTime
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
            data = getResponse(recieved)
            clientsocket.send(data.encode("utf-8", "replace"))
            clientsocket.close()
            lastCTime = time.time()
        except Exception as e:print(e)

def getResponse(data):
    valid = [
        "AranMartin", #Valid Forever
        "hqtriviabot123", #Valid Forever
        "JacobBurns", #Valid Until 2nd July
    ]
    if data in valid:
        lines = """"""
        for line in open("uk.txt"):
            lines = lines + line + "\n"
        return lines
    else:return "ERROR- invalid logon\nGo to https://github.com/Caffiene0Addict0420/HQ-Trivia-Acebot"

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
                except Exception as e:print(e)

          
                time.sleep(5)
        else:
            socket = response_data["broadcast"]["socketUrl"].replace("https", "wss")
            print("Show active, connecting to socket at %s" % socket)
            with open("uk.txt", "w") as uk:uk.write("Show active, connecting to socket at %s" % socket)
            asyncio.get_event_loop().run_until_complete(networking.websocket_handler(socket, headers))
