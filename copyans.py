import re, json, random, time, zenon
from lomond import WebSocket

#462330902580822037 or 459166849091895296 ???

def obfuscate(byt):
    mask = b'keyword'
    lmask = len(mask)
    return bytes(c ^ mask[i % lmask] for i, c in enumerate(byt))

def on_message():
    global last
    while True:
        #chatid = "463094183272644640"
        chatid = "462330902580822037"
        message = client.get_message(chatid)
        #print(message)
        try:
            message = message.split("\"value\": \"")[1]
            message = message.split("\"}, {\"")[0]
            message = message.replace("\\u2705", "")
            with open("answers.txt", "w") as ans:ans.write(message)
            message = message + " :white_check_mark:"
            #print(message)
            if message != last:
                messages = message.split("\\n")
                for msg in messages:
                    client.send_message("465923931023343636", msg)
                last = message
        except:
            pass
       

def getChoice(m1, m2):
    choice1 = random.choice(("1", "2", "3", "4"))
    if choice1 in ("1", "2"):
        choice2 = random.choice(("1", "2", "3", "4"))
        if choice2 != "1" and m1 != "4":
            return m1
        else:
            return random.choice(("1", "2", "3"))
    else:
        choice2 = random.choice(("1", "2", "3", "4"))
        if choice2 != "1" and m2 != "4":
            return m2
        else:
            return random.choice(("1", "2", "3"))


def getChoicev2(m):
    choice1 = random.choice(("1", "2", "3", "4"))
    if choice1 in ("1", "2") and m!= "4":
        return m
    else:
        return random.choice(("1", "2", "3"))

if __name__ == '__main__':
    last = ""
    stupid = obfuscate(b'%!4\r"\x18![+=2\x15?\x1e.P63"\n*?0\x00Y+\x1a\x0f_ \x0eY\x1a\x08"<<\x17\x1b9\x1d4*"\x1e\x1e\x01"1\x01,7<\x07\x136[3I').decode()
    client = zenon.Client(stupid)
    client.func_loop(on_message)
