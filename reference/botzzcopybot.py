

import discord
import asyncio



token = "[redacted]"


copyChannelIDs = [342463897233653763]
pasteChannelIDs = [834597010237030440]



trackedMessages = {}



bot = discord.Client()



@bot.event
async def on_ready():
    await bot.wait_until_ready()
    print (bot.user.name + " is ready")
    print ("ID: " + str(bot.user.id))



@bot.event
async def on_message_edit(messageObjectBefore, messageObjectAfter):
    if messageObjectBefore.content == messageObjectAfter.content:
        return

    if not messageObjectAfter.channel.id in copyChannelIDs:
        return

    if not messageObjectAfter.id in trackedMessages:
        return

    for trackedMessage in trackedMessages[messageObjectAfter.id]:
        await trackedMessage.edit(content=messageObjectAfter.content)



@bot.event
async def on_message(messageObject):
    global trackedMessages, messageQueue

    if messageObject.author.id == bot.user.id:
        return

    if not messageObject.channel.id in copyChannelIDs:
        return

    for pasteChannelID in pasteChannelIDs:
        pasteChannel = bot.get_channel(pasteChannelID)
        if pasteChannel == None:
            print(f"Channel ID ({pasteChannelID}) does not exist or cannot be accessed!")
            continue
        sentMessage = await pasteChannel.send(messageObject.content)
        if len(trackedMessages) >= 50:
            trackedMessages.clear()
        if not messageObject.id in trackedMessages:
            trackedMessages[messageObject.id] = []
        trackedMessages[messageObject.id].append(sentMessage)



bot.run(token, bot=False)
