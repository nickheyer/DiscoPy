import discord
import sys
import os


client = discord.Client()
embed = discord.Embed() 


save_dir = os.path.join(os.path.dirname(__file__), f'code_to_run.txt')
allowed_persons_dir = os.path.join(os.path.dirname(__file__), f'whitelisted.txt')

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
    og_stdout = sys.stdout
    with open(save_dir, "w") as input_code:
      sys.stdout = input_code
      exec(code_message)
      sys.stdout = og_stdout
    with open(save_dir, "r") as output_code:
      read_code = output_code.read()
      await message.channel.send(read_code)
  elif message.content.startswith("!c! add user") and message.author.name in allowed_users:
      added_user = message.content.strip()[13:]
      with open(allowed_persons_dir, "a") as users:
        users.write(f"\n{added_user.strip()}")
      await message.channel.send(f"{added_user.strip()} has been appended to allowed persons.")
  elif message.content.startswith("!c! list users"):
      await message.channel.send(f"These users can run code using me: \n{allowed_users}")


#Put your discord provided token here
client.run("TOKEN GOES HERE")