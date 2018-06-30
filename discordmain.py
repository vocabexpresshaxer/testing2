import extralives, random, discord, pickle
import asyncio

TOKEN = 'NDYyNDg2Mzk2NTY1ODQ4MDY1.Dhijsg.JieDm5C74rSoGIkdfCXgUsSjyo4'

client = discord.Client()

@client.event
async def on_message(message):
    global auth
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('status?'):
        msg = 'The Bot Is Currently Active'
        await client.send_message(message.channel, msg)

    
    elif message.content.startswith('+life'):
        lifeargs = message.content.split(" ")
        if len(lifeargs) != 2:
            await client.send_message(message.channel, "Invalid no. of args")
        else:
            try:
                 auth = str(extralives.verify(lifeargs[1]))
                 await client.send_message(message.channel, "Code Sent. Check your messages")
            except:
                await client.send_message(message.channel, "Invalid Phone Number. Example of valid phone number: +14242196850")
    elif message.content.startswith('+verify'):
        verifyargs = message.content.split(" ")
        if len(verifyargs) != 3:
            await client.send_message(message.channel, "Invalid no. of args")
        else:
            if auth == "":
                await client.send_message(message.channel, "You need to do +life [number] first")
            else:
                u = "False"
                while u == "False":
                    uname = str(random.randint(1000, 100000))
                    u = str(extralives.username_available(uname))
                if str(extralives.submit_code(auth, int(verifyargs[1]))) == "True":
                    try:
                        auth = extralives.create_user(uname, auth, verifyargs[2], "US")['authToken']
                        bearers = pickle.load(open("/root/bearers.p", "rb"))
                        bearers.append(str(auth))
                        pickle.dump(bearers, open("/root/bearers.p", "wb"))
                        await client.send_message(message.channel, "Life is Queued For Creation During Next US Game\n*Life wasn't added as the functionality hasn't been added yet*")
                        await client.send_message(message.channel, "Bearer for life (testing purposes only):\n" + str(auth))
                    except Exception as e:
                        await client.send_message(message.channel, str(e))
                else:
                    await client.send_message(message.channel, "Invalid Code")

            
@client.event
async def on_ready():
    global auth
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    auth = ""

client.run(TOKEN)
