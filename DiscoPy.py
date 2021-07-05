import discord
import sys
import os
from time import sleep
import re

TOKEN = "ENTER YOUR DISCORD PROVIDED TOKEN HERE"

client = discord.Client()
embed = discord.Embed() 


save_dir = os.path.join(os.path.dirname(__file__), f'code_to_run.txt')
allowed_persons_dir = os.path.join(os.path.dirname(__file__), f'whitelisted.txt')
last_code_path = os.path.join(os.path.dirname(__file__), f'last_code.txt')

#checks if code running cache and user whitelist exists, if not it creates one. 
with open(save_dir, "a") as instance_1:
  instance_1.write("")
with open(allowed_persons_dir, "a") as instance_2:
  instance_2.write("")

#greets admin
@client.event
async def on_ready():
  print("Bot is ready to code, logged in as {0.user}.".format(client))


#everytime a user sends discord message, the below is checked
@client.event
async def on_message(message):
  with open(allowed_persons_dir, "r") as listed_users:
    allowed_users = listed_users.read()
  if message.author == client.user:
    return
  elif message.content.startswith("!c! ```") and message.content.endswith("```") and message.author.name in allowed_users:
    code_message = message.content[7:-3]
    with open(last_code_path, "w") as last_code_w:
      last_code_w.write(code_message)
    with open(last_code_path, "r") as last_code_r:
      last_code_doc = last_code_r.read()
    if "input(" in last_code_doc:
      await message.channel.send("There is an input in here...") ; sleep(1)
      await message.channel.send("Unfortunately, typing input() values directly into a python shell from a discord message is beyond my comprehension. Initiating a find-and-replace-with-a-value for all input() functions...") ; sleep(1)
    while "input(" in last_code_doc:
      def input_searcher(text):
        newex = re.search(r'input\(.+?,?([)]|$)', text)
        return newex.group(0)
      await message.channel.send(f"The input is: \"{input_searcher(last_code_doc)}\"") ; sleep(1)
      await message.channel.send(f"What would you like to enter for this input?") ; sleep(1)
      msg = await client.wait_for('message')
      new_msg = msg.content
      if "!c! false positive" in new_msg.lower():
        await message.channel.send("False positive has been noted, pushing your code through as is...") ; sleep(1)
        break
      def input_replacer(repl_text, text):
        newex = re.sub(r'input\(.+?,?([)]|$)', repl_text, text, count = 1)
        return newex
      with open(last_code_path, "w") as last_code_w:
        last_code_w.write(input_replacer(new_msg, last_code_doc))
      with open(last_code_path, "r") as last_code_r:
        last_code_doc = last_code_r.read()
    og_stdout = sys.stdout
    try:
      with open(save_dir, "w") as input_code:
          sys.stdout = input_code  
          exec(last_code_doc)
          sys.stdout = og_stdout
      with open(save_dir, "r") as output_code:
        read_code = output_code.read()
        await message.channel.send(read_code)
    except:
      await message.channel.send("Unfortunately that code errored out. Check what you've written and try again!") ; sleep(1)
  elif message.content.startswith("!c! add user") and message.author.name in allowed_users:
      added_user = message.content.strip()[13:]
      with open(allowed_persons_dir, "a") as users:
        users.write(f"\n{added_user.strip()}")
      await message.channel.send(f"{added_user.strip()} has been appended to allowed persons.")
  elif message.content.startswith("!c! list users"):
      await message.channel.send(f"These users can run code using me: \n{allowed_users}")


#Put your discord provided token here
client.run(TOKEN)