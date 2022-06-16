#!/usr/bin/env python3.9
import discord
import asyncio
import json
import logging

logging.basicConfig(level=logging.DEBUG)

class CopyBot(discord.Client):
  async def on_ready(self):
    logging.info(f"Logged on as {self.user}.")

  async def on_message(self, message):
    if message.author.id == self.user.id:
      return

    logging.info(f"Message from {message.author}: {message.content}")
    await message.channel.send(f"Hello {message.author}!")

if __name__ == "__main__":
  config = json.load(open("config.json", "rb")) #TODO cwd
  bot = CopyBot()
  bot.run(config["token"])
