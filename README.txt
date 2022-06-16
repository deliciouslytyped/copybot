Usage:
  Configure a bot as normal, as explained in https://discordpy.readthedocs.io/en/stable/discord.html .
  The bot needs the following permissions enabled: (TODO check)
    - Read Messages / View Channels
    - Send Messages
    - (TODO) Read Message History (for edits?)
  The bot needs a config.json file set up in the same folder as the bot.py script, with the following content:
    {"token":"your token goes here",
     "copyuserid":your_user_id_goes_here}
  The replication_map.sqlite file stores information needed to propagate edits. (Which replicated messages belong to an original message.)
Developer documentation can be found at:
  libraries:
    discord.py - https://discordpy.readthedocs.io/en/stable/ (this is the best resource)
  infrastructure:
    poetry - https://python-poetry.org/
    discord bot quickie -
      https://discordpy.readthedocs.io/en/stable/discord.html
      https://discordpy.readthedocs.io/en/stable/intro.html
      https://tannerabraham.com/how-to-code-a-discord-bot-in-python-copy-and-paste/
