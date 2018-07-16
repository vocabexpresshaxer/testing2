import asyncio, os, time, colorama, networking, socket, random, pickle
from datetime import datetime
from _thread import start_new_thread
from discordweb import Webhook
import extralives
from lomond import WebSocket

# Set up color-coding
colorama.init()

AREconnected = []
try:
    bearers = pickle.load(open("/root/bearers.p", "rb"))
except:
    bearers = []
    pickle.dump(bearers, open("/root/bearers.p", "wb"))

def runW(url, tosend):
    try:Webhook(url, msg=tosend).post()
    except:pass    
    

def playGame(uri, bearer):
    #global answer
    #global answerno
    broadid = "placeholderbroadid"
    headers = {"Authorization": "Bearer %s" % bearer,"x-hq-client": "Android/1.3.0"}
    websocket = WebSocket(uri)
    for header, value in headers.items():
        websocket.add_header(str.encode(header), str.encode(value))
    first = True
    for msg in websocket.connect(ping_rate=5):
        if msg.name == "text":
            message = msg.text
            message = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", message)
            message_data = json.loads(message)

            if "error" in message_data and message_data["error"] == "Auth not valid":
                print("Connection settings invalid")

            if first == True:
                websocket.send_json({"authToken":bearer, "type": "subscribe", "broadcastId": broadid})
                first = False
                
        if message_data["type"] == "question":
            ans = message_data["answers"]
            print(message_data["question"])
            qid = message_data["questionId"]
            print("Q ID: " + str(message_data["questionId"]))
            for a in ans:print(str(a["answerId"]) + " : " + a["text"])
            choice = ""
            while choice not in ("1", "2", "3", "4"):
                choice = input("Which Option? ") #Fetch Answers#
                
            if choice == "4":
                choice = random.choice(("1", "2", "3"))
                
            if choice == "1":
                aID = ans[0]["answerId"]
            elif choice == "2":
                aID = ans[1]["answerId"]
            else:
                aID = ans[2]["answerId"]
            websocket.send_json({"type":"answer", "authToken":bearer, "questionId":message_data["questionId"], "broadcastId":broadid, "answerId":aID})
        
        elif message_data["type"] == "questionSummary":
            ans = message_data["answerCounts"]
            if message_data["youGotItRight"] == True:
                print("[Correctly Answered Question]")
            else:
                print("[Incorrectly Answered Question]")
                #Option To Use Extra Life#
                if message_data["extraLivesRemaining"] > 0:
                    if message_data["savedByExtraLife"] == False:
                        #Save using life
                        websocket.send_json({"type":"useExtraLife", "authToken":bearer, "broadcastId":broadid, "questionId":qid})
                    else:
                        print("You Have already used an extra life- can't use another one")
                        
                else:
                    print("You don't have any extra lives to use (eliminated)")
            for a in ans:
                if a["correct"] == True:
                    print("The correct answer was %s" % a["answer"])
                    print("\n"*2)
def fix(mystring):
    higher = re.sub(r"[^\w]", "", mystring)
    return higher.lower()

def getChoicev2(m):
    choice1 = random.choice(("1", "2", "3", "4"))
    if choice1 in ("1", "2") and m!= "4":
        return m
    else:
        return random.choice(("1", "2", "3"))

def nextGame(uk, us, de):
    for r in ("uk", "us", "de"):
        if r == "us":
            USER_ID = us[1]
            BEARER_TOKEN = us[0]
        elif r == "de":
            USER_ID = de[1]
            BEARER_TOKEN = de[0]
        else:
            USER_ID = uk[1]
            BEARER_TOKEN = uk[0]
        main_url = "https://api-quiz.hype.space/shows/now?type="
        headers = {"Authorization": "Bearer %s" % BEARER_TOKEN,
               "x-hq-client": "Android/1.3.0"}
        done = False
        loops = 0
        while done == False:
            loops += 1
            if loops > 2: return (None , None)
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
                    try:
                        next_time = datetime.strptime(response_data["nextShowTime"], "%Y-%m-%dT%H:%M:%S.000Z")
                        now = time.time()
                        offset = datetime.fromtimestamp(now) - datetime.utcfromtimestamp(now)
                        
                        if r == "de":
                            timetode = next_time - datetime.strptime(datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z"), "%Y-%m-%dT%H:%M:%S.000Z")
                        elif r == "uk":
                            timetouk = next_time - datetime.strptime(datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z"), "%Y-%m-%dT%H:%M:%S.000Z")
                        elif r == "us":
                            timetous = next_time - datetime.strptime(datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z"), "%Y-%m-%dT%H:%M:%S.000Z")
                        done = True
                    except Exception as e:print(e)
    tTo = "Time to next UK game: %s\nTime to next US game: %s\nTime to next DE game: %s" % (timetouk, timetous, timetode)
    if timetouk < timetous and timetouk < timetode:return ("uk", tTo)
    elif timetode < timetouk and timetode < timetous:return("de", tTo)
    else:return ("us", tTo)

uk_bearer = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjE4NDY1MTU1LCJ1c2VybmFtZSI6IklDdWNrTmFucyIsImF2YXRhclVybCI6InMzOi8vaHlwZXNwYWNlLXF1aXovZGVmYXVsdF9hdmF0YXJzL1VudGl0bGVkLTFfMDAwMV9ibHVlLnBuZyIsInRva2VuIjoiVENRUEg4Iiwicm9sZXMiOltdLCJjbGllbnQiOiIiLCJndWVzdElkIjpudWxsLCJ2IjoxLCJpYXQiOjE1MjU3ODQ4OTcsImV4cCI6MTUzMzU2MDg5NywiaXNzIjoiaHlwZXF1aXovMSJ9.32laQw5QOA9FuBixO2LIaUKy6Lp6J8uadXud6OdjfuA", "18465155")
de_bearer = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjE1OTQ0MTI2LCJ1c2VybmFtZSI6IkFsZXhhbmRlclNpZmZpIiwiYXZhdGFyVXJsIjoiczM6Ly9oeXBlc3BhY2UtcXVpei9hL2JiLzE1OTQ0MTI2LUhpV0M3ci5qcGciLCJ0b2tlbiI6IlVYcW4wYyIsInJvbGVzIjpbXSwiY2xpZW50IjoiIiwiZ3Vlc3RJZCI6bnVsbCwidiI6MSwiaWF0IjoxNTIzOTY5NjA1LCJleHAiOjE1MzE3NDU2MDUsImlzcyI6Imh5cGVxdWl6LzEifQ.Nm0p2g7_DhsJoWmB3tSbLGpELe4zkchxRrrmS7my_Qc", "15944126")
us_bearer = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjIxMzIxOTcxLCJ1c2VybmFtZSI6IjMwMjAiLCJhdmF0YXJVcmwiOiJodHRwczovL2QyeHUxaGRvbWgzbnJ4LmNsb3VkZnJvbnQubmV0L2RlZmF1bHRfYXZhdGFycy9VbnRpdGxlZC0xXzAwMDRfZ29sZC5wbmciLCJ0b2tlbiI6bnVsbCwicm9sZXMiOltdLCJjbGllbnQiOiIiLCJndWVzdElkIjpudWxsLCJ2IjoxLCJpYXQiOjE1MzA0NzMzNjMsImV4cCI6MTUzODI0OTM2MywiaXNzIjoiaHlwZXF1aXovMSJ9.-LNtYjnlWG_5C4WpQis7prcZ5i1xXswhTuI9CotwvqM", "18465155")


print("Starting up Bot...")
lastCTime = time.time()
lastDE = time.time()

a = "us"
while True:
 #   try:
  #      for line in open("nextG.txt"):
   #         if line in ("uk", "us", "de"):
    #            a = line.lower()
    #except:
     #   pass
    #print(nextGame(uk_bearer, us_bearer, de_bearer)[1])
    if a == "us":
        USER_ID = us_bearer[1]
        BEARER_TOKEN = us_bearer[0]
        nextG = "US"
    elif a == "de":
        USER_ID = de_bearer[1]
        BEARER_TOKEN = de_bearer[0]    
        nextG = "DE"
    else:
        USER_ID = uk_bearer[1]
        BEARER_TOKEN = uk_bearer[0]
        nextG = "UK"
        
    main_url = "https://api-quiz.hype.space/shows/now?type="
    headers = {"Authorization": "Bearer %s" % BEARER_TOKEN,
           "x-hq-client": "Android/1.3.0"}

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
                prize = response_data["nextShowPrize"]

                print("Next game will be at: %s " % (str((next_time + offset).strftime('%I:%M %p')) + " UTC (" + nextG + " game)"))
                print("Prize: " + response_data["nextShowPrize"])
                with open("uk.txt", "w") as uk:uk.write("Next game will be at: %s " % (str((next_time + offset).strftime('%I:%M %p')) + " UTC (" + nextG + " game)\n" + "Prize: " + response_data["nextShowPrize"]))
            except Exception as e:print(e)


            time.sleep(5)
    else:
        socket = response_data["broadcast"]["socketUrl"].replace("https", "wss")
        print(response_data['broadcast'])
        try:
            broadid = response_data["broadcast"]["broadcastId"]
        except:
            print("Couldnt broadcast id")
            broadid = "placeholder"
        print("Show active, connecting to socket at %s" % socket)
        AREconnected = []
        with open("uk.txt", "w") as uk:uk.write("Show active, connecting...")

        bearers = pickle.load(open("/root/bearers.p", "rb"))

        if nextG == "US":
            print("Sending Lives")
            #need to send to discord
            asyncio.get_event_loop().run_until_complete(networking.websocket_lives_handler(socket, bearers, broadid))
            bearers = []
            pickle.dump(bearers, open("/root/bearers.p", "wb"))
            allbearers = pickle.load(open("/root/acc.p", "rb"))
            for b in allbearers:
                start_new_thread(playGame, (socket, b)) 
        #else:
         #   try:
          #      asyncio.get_event_loop().run_until_complete(networking.websocket_lives_handler(socket, bearers, broadid))
           # except Exception as e:
            #    print(e)
        #asyncio.get_event_loop().run_until_complete(networking.websocket_handler(socket, headers))

