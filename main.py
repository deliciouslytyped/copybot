#!/usr/bin/env python3.8
import discord
import asyncio, json, logging, sys, os.path, argparse, sqlite3

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", action="store_true")
parser.add_argument("-i", "--info", action="store_true")
args = parser.parse_args()

if args.debug:
  logLevel = logging.DEBUG
elif args.info:
  logLevel = logging.INFO
else:
  logLevel = logging.WARNING

logging.basicConfig(level=logLevel)

class ReplicationMap():
  def __init__(self, db_path):
    self.conn = sqlite3.connect(db_path)
    self.cur = self.conn.cursor()

    self.cur.execute("CREATE TABLE IF NOT EXISTS replications(src_channel_id INTEGER, src_message_id INTEGER, dst_channel_id INTEGER, dst_message_id INTEGER)")
    self.conn.commit()

  def __contains__(self, tup):
    result = self.cur.execute("SELECT dst_channel_id, dst_message_id FROM replications WHERE src_channel_id = ? AND src_message_id = ?", tup)
    tups = result.fetchall()
    self.conn.commit()
    logging.info(tup)
    logging.info(tups)
    return len(tups) > 0

  def __getitem__(self, tup):
    result = self.cur.execute("SELECT dst_channel_id, dst_message_id FROM replications WHERE src_channel_id = ? AND src_message_id = ?", tup)
    self.conn.commit()
    tups = result.fetchall()
    return tups

  def __setitem__(self, tup, data):
    self.cur.execute("DELETE FROM replications WHERE src_channel_id = ? AND src_message_id = ?", tup)
    for e in data:
      self.cur.execute("INSERT INTO replications(src_channel_id, src_message_id, dst_channel_id, dst_message_id) VALUES (?, ?, ?, ?)", (*tup, *e))
    self.conn.commit()

#TODO size limited log rotation
#TODO handle replication map inconsistencies?
class CopyBot(discord.Client):
  def __init__(self, *args, **kwargs):
    self.config = kwargs.pop("config")
    self.replication_map = kwargs.pop("replication_map")
    super().__init__(*args, **kwargs)

  async def on_ready(self):
    logging.info(f"Logged on as {self.user}.")
    print(f"Logged on as {self.user}.")

  async def on_message(self, message):
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
          new_message = await channel.send(message.content) #TODO this could include attachments and other such things?
          if new_message and new_message.id:
            self.replication_map[(message.channel.id, message.id)] += [(new_message.channel.id, new_message.id)]

    logging.info(f"Message {message.id}:{message.content[0:20]} from {message.author} was replicated to {targets}")

  async def on_raw_message_edit(self, payload): #TODO edge cases in documentation, see on_raw_message_edit?
    logging.info(f"Message edited: {payload}")
    #TODO need to handle ignoring notifications of message updates we caused (to avoid loops when bot message editing is implemented)
    if (payload.channel_id, payload.message_id) not in self.replication_map: #TODO handle edits of bot messages (reverse)
      logging.info(f"Message not in replication map.")
      return

    payload_message = await self.get_channel(payload.channel_id).fetch_message(payload.message_id)
    new_content = payload_message.content
    await self.replicate_edit(payload.channel_id, payload.message_id, new_content)

  async def replicate_edit(self, src_channel_id, src_message_id, new_content):
    logging.info("Replicating edit.")
    targets = self.replication_map[(src_channel_id, src_message_id)]
    edited_replicas = list()
    for target in targets:
      channel_id, message_id = target
      message = await self.get_channel(channel_id).fetch_message(message_id) #TODO possible error handling?
      logging.info(f"Old content: {message.content} \n \n want: {new_content}")
      await message.edit(content=new_content)
      logging.info(f"New content: {message.content}")
      edited_replicas.append(target)
    logging.info(f"Edited replicas: {edited_replicas}.")

if __name__ == "__main__":
  wd = sys.path[0]
  replication_map = ReplicationMap(os.path.join(wd, "replication_map.sqlite"))
  config = json.load(open(os.path.join(wd, "config.json"), "rb"))
  bot = CopyBot(config=config, replication_map=replication_map)
  bot.run(config["token"])
