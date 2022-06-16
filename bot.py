#!/usr/bin/env python3.9
import discord
import asyncio, json, logging, sys, os.path

#TODO toggle debug output
#TODO size limited log rotation
#TODO propagate message edits
logging.basicConfig(level=logging.INFO)

class CopyBot(discord.Client):
  def __init__(self, *args, **kwargs):
    self.config = kwargs.pop("config")
    super().__init__(*args, **kwargs)

  async def on_ready(self):
    logging.info(f"Logged on as {self.user}.")

  async def on_message(self, message): #TODO
    if message.author.id == self.user.id:
      return

    if message.author.id == self.config["copyuserid"]:
      await self.replicate_message(message)

  async def replicate_message(self, message):
    logging.info(f"Replicating message.")
    targets = list()
    for guild in self.guilds:
      if guild.id == message.guild.id:
        continue
      targets.append(guild)
      for channel in guild.channels:
        if channel.name == message.channel.name:
          await channel.send(message.content) #TODO this could include attachments and other such things?
    logging.info(f"Message {message.id}:{message.content[0:20]} from {message.author} was replicated to {targets}")

  async def on_edit(self, before, after):
    pass #TODO

  async def replicate_edit(self, before, after):
    pass #TODO

if __name__ == "__main__":
  wd = sys.path[0]
  config = json.load(open(os.path.join(wd, "config.json"), "rb"))
  bot = CopyBot(config=config)
  bot.run(config["token"])
