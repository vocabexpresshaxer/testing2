import extralives, random, discord, pickle
import asyncio


client = discord.Client()

@client.event
async def on_message(message):
    global auth
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.lower() == "+status":
        msg = 'The Bot Is Currently Active'
        await client.send_message(message.channel, msg)
    elif message.content.lower() == "+help":
        helpmsg = """
Bot made by @CaffieneAddict420 
-------------------------------
Usage:
-------------------------------
*+status* (Check if the bot is active)
*+help* (Show this message)
*+queue* (Shows how many lives are queued to be added)
-------------------------------
*+life [phone number]*
*+call [phone number]*
*+verify [code] [referal code]*
-------------------------------
*+set [uk/us/de]* (Sets next game for answerbot to join if bot isn't set to right game next)
[Will be removed in the future]
-------------------------------
        """
        await client.send_message(message.channel, helpmsg)
    
    elif message.content.lower() == "+queue":
        bearers = pickle.load(open("/root/bearers.p", "rb"))
        totalb = pickle.load(open("/root/acc.p", "rb"))
        total = str(len(totalb))
        await client.send_message(message.channel, "There are %s lives queued to be added next US game\nThis bot has processed a total of %s Lives" % (str(len(bearers)), total))
    elif message.content.startswith('+life'):
        lifeargs = message.content.split(" ")
        if len(lifeargs) != 2:
            await client.send_message(message.channel, "Invalid no. of args\n See +help for usage")
        else:
            try:
                no = lifeargs[1]
                if not no.startswith("+"):
                    no = "+1" + no
                auth = str(extralives.verify(no)) 
                await client.send_message(message.channel, "Code Sent. Check your messages")
            except:
                await client.send_message(message.channel, "Invalid Phone Number. Example of valid phone number: +14242196850")
    elif message.content.startswith('+call'):
        lifeargs = message.content.split(" ")
        if len(lifeargs) != 2:
            await client.send_message(message.channel, "Invalid no. of args\n See +help for usage")
        else:
            try:
                 auth = str(extralives.verify2(lifeargs[1]))
                 print(auth)
                 await client.send_message(message.channel, "Code Sent. Check your messages")
            except:
                await client.send_message(message.channel, "Invalid Phone Number. Example of valid phone number: +14242196850")
    elif message.content.startswith('+set '):
        if message.content == "+set uk":
            next = "uk"
            with open("nextG.txt", "w") as nex:nex.write(next)
            await client.send_message(message.channel, "Set Next Game to UK")
        elif message.content == "+set us":
            next = "us"
            with open("nextG.txt", "w") as nex:nex.write(next)
            await client.send_message(message.channel, "Set Next Game to US")
        elif message.content == "+set de":
            next = "de"
            with open("nextG.txt", "w") as nex:nex.write(next)
            await client.send_message(message.channel, "Set Next Game to DE")
        else:
            pass
    elif message.content == "+allbots":
        totLives = 0
        totalb = pickle.load(open("/root/acc.p", "rb"))
        for b in totalb:
            test = extralives.HQClient(b)
            test.make_it_rain()
            test2 = test.me()
            if test2.lives != None:
                totLives += 1
        print("%s out of %s bots have extra lives" % (str(totLives),str(len(totalb))))
        await client.send_message(message.channel, "%s out of %s bots have extra lives" % (str(totLives),str(len(totalb))))
      
    elif message.content.startswith('+verify'):
        verifyargs = message.content.split(" ")
        if len(verifyargs) != 3:
            await client.send_message(message.channel, "Invalid no. of args\n See +help for usage")
        else:
            if auth == "":
                await client.send_message(message.channel, "You need to do +life [number] first")
            else:
                naming = random.choice(("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"))
                if naming == "1":
                    u = "False"
                    while u == "False":
                        uname = str(random.randint(1000, 100000))
                        u = str(extralives.username_available(uname))
                else:
                    u = "False"
                    while u == "False":
                        first = random.choice(("joe", "shazza", "sarah", "bob", "james", "edward", "steve", "steven", "ben", "charlie", "josh", "robert", "beric"))
                        second = random.choice(("davis", "johnson", "stevenson", "tucker", "moore", "browne", "dietrich", "fuller", "capponi", "markus", "scheffler", "fekete", "accomazzi", "garson", "orsi", "hampton"))
                        c = random.choice(("1", "2", "3"))
                        if c == "1":name = first + second
                        elif c == "2":name = first.title() + second.title()
                        elif c == "3": name = first + second.title()
                        c2 = random.choice(("1", "2", "3"))
                        if c2 == "1":pass
                        elif c2 == "2":name = name + random.choice(("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"))
                        elif c2 == "3":name = name + "19" + random.choice(("1", "2", "3", "4", "5", "6", "7", "8", "9")) + random.choice(("1", "2", "3", "4", "5", "6", "7", "8", "9"))
                        u = str(extralives.username_available(uname))
                            
                        
                try:
                    if str(extralives.submit_code(auth, int(verifyargs[1]))) == "True":
                        try:
                            auth = extralives.create_user(uname, auth, verifyargs[2], "US")['authToken']
                            bearers = pickle.load(open("/root/bearers.p", "rb"))
                            totalb = pickle.load(open("/root/acc.p", "rb"))
                            totalb.append(str(auth))
                            bearers.append(str(auth))
                            pickle.dump(bearers, open("/root/bearers.p", "wb"))
                            pickle.dump(totalb, open("/root/acc.p", "wb"))
                            await client.send_message(message.channel, "Life is Queued For Creation During Next US Game")
                            test = extralives.HQClient(auth)
                            test.make_it_rain()

                        except Exception as e:
                            await client.send_message(message.channel, "Uh oh. The an error has occured server-side " + str(e))
                    else:
                        await client.send_message(message.channel, "Invalid Code")
                except:
                    await client.send_message(message.channel, "Invalid Code -  It needs to be a number e.g. 1234")
     
@client.event
async def on_ready():
    global auth
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    auth = ""


examplerandomChars = 'NDYzMDk4MTYwOTk1MzY4OTgw.DhrhIg.500IytHVDh_46kE5rjNG9NbnI8k'
client.run(examplerandomChars)
