
import extralives, random, discord, pickle, time
import asyncio
from _thread import start_new_thread

client = discord.Client()

def getLife(b):
    global r
    global totLives
    global numLives
    test = extralives.HQClient(b)
    test.make_it_rain()
    test2 = test.me()
    if test2.lives != None and test2.lives != "none" and test2.lives != "None" and test2.lives != 0 and test2.lives != "0":
        print((test2.lives))
        totLives += 1
        numLives += int(test2.lives)
    r += 1

@client.event
async def on_message(message):
    global ukNo
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
                if no.startswith("+44"):
                    ukNo = True
                else:
                    ukNo = False
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
                if lifeargs[1].startswith("+44"):
                    ukNo = True
                else:ukNo = False
                
                auth = str(extralives.verify2(lifeargs[1]))
                print(auth)
                await client.send_message(message.channel, "Calling you, listen closely for the verification code")
            except:
                await client.send_message(message.channel, "Invalid Phone Number. Example of valid phone number: +14242196850")
    elif message.content == "+money":
        for region in ("uk", "us"):
            if region == "us":
                await client.send_message(message.channel, "US accounts:")
                totalb = pickle.load(open("/root/acc.p", "rb"))
            else:
                await client.send_message(message.channel, "UK accounts:")
                totalb = pickle.load(open("/root/ukbearers.p", "rb"))
            index = 0
            for b in totalb:
                botuser = extralives.HQClient(b)
                bot_payout_info = botuser.payouts()
                if region == "us" and bot_bal.startswith("£"):
                    totalb.remove(b)
                    #pickle.dumps(totalb, 
                bot_bal = bot_payout_info.balance
                print(str(index) + " : " + str(bot_bal.unpaid))
                await client.send_message(message.channel, str(index) + " : " + str(bot_bal.unpaid))
                index += 1
    elif message.content == "+allbots":
        global r
        global totLives
        global numLives
        for region in ("uk", "us"):
            await client.send_message(message.channel, region.upper() + " Accounts:")
            if region == "us":totalb = pickle.load(open("/root/acc.p", "rb"))
            else:totalb = pickle.load(open("/root/ukbearers.p", "rb"))
            r = 0
            numLives = 0
            totLives = 0
            time.sleep(1)
            for b in totalb:
                start_new_thread(getLife, (b,)) 
            while r != len(totalb):
                time.sleep(1)
            print("%s out of %s bots have extra lives" % (str(totLives),str(len(totalb))))
            await client.send_message(message.channel, "%s out of %s bots have extra lives" % (str(totLives),str(len(totalb))))
            await client.send_message(message.channel, "The bots have a total of %s lives between them" % str(numLives))
                      
      
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
                        first = random.choice(("joe", "shazza", "sarah", "bob", "james", "edward", "steve", "jaye", "lola", "saad", "flynn", "peter", "yousif", "steven", "ben", "charlie", "josh", "robert", "beric"))
                        second = random.choice(("davis", "johnson", "stevenson", "tucker", "samuels", "byrne", "wynn", "moore", "peters", "flynn", "greig", "alvarado", "hardy", "curry", "esparza", "small", "valdez", "mustafa", "traynor", "kent", "matthews", "browne", "dietrich", "fuller", "capponi", "markus", "scheffler", "fekete", "accomazzi", "garson", "orsi", "hampton"))
                        c = random.choice(("1", "2", "3"))
                        if c == "1":uname = first + second
                        elif c == "2":uname = first.title() + second.title()
                        elif c == "3": uname = first + second.title()
                        c2 = random.choice(("1", "2", "3"))
                        if c2 == "1":pass
                        elif c2 == "2":uname = uname + random.choice(("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"))
                        elif c2 == "3":uname = uname + "19" + random.choice(("1", "2", "3", "4", "5", "6", "7", "8", "9")) + random.choice(("1", "2", "3", "4", "5", "6", "7", "8", "9"))
                        u = str(extralives.username_available(uname))
                            
                        
                try:
                    if str(extralives.submit_code(auth, int(verifyargs[1]))) == "True":
                        try:
                            auth = extralives.create_user(uname, auth, verifyargs[2], "US")['authToken']
                            if ukNo == False:
                                bearers = pickle.load(open("/root/bearers.p", "rb"))
                                totalb = pickle.load(open("/root/acc.p", "rb"))
                            
                                totalb.append(str(auth))
                                bearers.append(str(auth))
                                pickle.dump(bearers, open("/root/bearers.p", "wb"))
                                pickle.dump(totalb, open("/root/acc.p", "wb"))
                                await client.send_message(message.channel, "Life is Queued For Creation During Next US Game")
                            else:
                                try:
                                    b = pickle.load(open("/root/ukbearers.p", "rb"))
                                except:b = []
                                b.append(str(auth))
                                pickle.dump(b, open("/root/ukbearers.p", "wb"))
                                await client.send_message(message.channel, "Life is Queued For Creation During Next UK Game")
                     
                                
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
