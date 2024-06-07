# code by eepysheepyy - https://linktr.ee/eepysheepyy
from twitchio.ext import commands   # main twitch control, to get chat, and handle commands
import json     # to play with the env_secrets file
import random   # for rolling the dice if needed
import obsws_python as obs      # OBS Websockets
from deep_translator import GoogleTranslator    # Google translate for the translate command

# Try OBS Connection - for Websockets

try:
    # run OBS through private port
    cl = obs.ReqClient(host='localhost', port=4455, password='YOUR OBS WEBSOCKET PASSWORD HERE')
    # GetVersion
    resp = cl.get_version()
except:
    # When OBS is not connected, print to console
    print(ConnectionError)

# Twitch Deets are stored in the file 'env_secrets.json', users need to put in their own details for their own individual bot
env_file = open("env_secrets.json", "r")
env_json = json.loads(env_file.read())
env_file.close()


# for storing the vars outside of functions
roll = 0
tran = ''
usrDict = {}

class Bot(commands.Bot):

    def __init__(self):
        # Initialise, read from file. 
        # Client ID: https://faq.demostoreprestashop.com/faq.php?fid=144&pid=41
        # Token: https://twitchapps.com/tmi/
        # Bot Prefix: What precurses a command (usually the '!' character)
        # Channel: Just the channel name
        super().__init__(client_id=env_json['CLIENT_ID'], token=env_json['TOKEN'], prefix=env_json['BOT_PREFIX'],
                         initial_channels=[env_json['CHANNEL']])

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        global tran
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return
        # Print the contents of our message to console...
        print(message.content)

        # TRANSLATION ADDON - Detects if message has string, and if matches, will route the rest of the message through google translate 
        split = message.content[0:10]
        if split == '!translate':
            to_translate = message.content[11:]
            translated = GoogleTranslator(source='auto', target='en').translate(to_translate)
            print('Translated to ' + translated)
            tran = translated   # stores the translation to trigger later (is global)

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    @commands.command()
    @commands.cooldown(1, 120, commands.Bucket.user) # You can add these to make cooldowns for commands. Commands are ASYNC, so you can mostly use multiple at once.
    async def YourCommandNameHere(self, ctx: commands.Context):
        # ctx.send() will send a message of your choosing to the twitch chat!
        await ctx.send("Your Text here")
        if ctx.author.mention == "@USER":    # you can add these if conditions to limit the commands only being to certain users, people with certain badges, and so on.
            cl.set_current_program_scene("OBS_SCENE") # you can add these to change the Scene inside OBS!
            cl.toggle_input_mute("AUDIO_DEVICE") # You can add these to mute an Audio Input Source inside OBS!

    @commands.command()
    @commands.cooldown(1, 1, commands.Bucket.user)
    async def translate(self, ctx: commands.Context): # This is where we execute that translate feature
        global tran
        await ctx.send(tran)

    @commands.command()
    @commands.cooldown(1, 15, commands.Bucket.user)
    async def color(self, ctx: commands.Context): # If a user has assigned a colour value to their namebadge, it will be printed in hexadecimal code 
        if ctx.author.color is True:
            await ctx.send(f'{ctx.author.mention} You are covered in the marvelous colour: {ctx.author.color}')

    @commands.command()
    @commands.cooldown(1, 15, commands.Bucket.user)
    async def cmd(self, ctx: commands.Context): # You can add custom command list
        await ctx.send(
            "This bot currently has the following commands: ")

    @commands.command()
    @commands.cooldown(1, 15, commands.Bucket.user)
    async def subcmd(self, ctx: commands.Context): # These will be explored in a little bit
        await ctx.send(
            "There are extra bonus Sub features for these commands: ")

    @commands.command()
    @commands.cooldown(1, 0, commands.Bucket.user)
    async def repeat(self, ctx: commands.Context, t): # This just echoes a message
        await ctx.send(t)

    @commands.command()
    @commands.cooldown(1, 15, commands.Bucket.user)
    async def hug(self, ctx: commands.Context, usr):
        await ctx.send(
            f'{ctx.author.mention}' + " gives " + usr + " a big warm hug!")
        if ctx.author.is_subscriber: # So you can make if conditions that add extra effects for certain people, or people with certain badges. For this instance, we're using subscriber data, so that if someone is subbed, their command experience is better than average
            #add functionality here
            return

    @commands.command()
    @commands.cooldown(1, 120, commands.Bucket.user)
    async def lurk(self, ctx: commands.Context): # I like lurk messages, a lot clearly. 
        global usrDict
        lurktext = ""
        roll = 0 #reset
        roll = random.randint(1, 20) #and roll
        print("Lurk Rolled a nat " + str(roll))
        rarity = 0 #reset // should mention that this adds extra spice so that there is MORE randomness
        rarity = random.randint(1, 100) #and roll
        print("And the fates decided... " + str(rarity))
        if roll == 1 and rarity > 50:
            lurktext = " is going in the shadows to lurk..."
        if roll == 1 and rarity < 50:
            lurktext = " has been consumed by shadow, never to be seen again...(maybe)"
        if roll == 1 and rarity == 50:
            lurktext = " vanished into the shadow realm. Poof!"
        else: 
             lurktext = " enjoy your lurk!"
    
        usr = str(ctx.author.name)
        usrDict[usr] = rarity # Adds the user to a dictionary
        await ctx.send(f'{ctx.author.mention}' + lurktext)

    @commands.command()
    @commands.cooldown(1, 5, commands.Bucket.user)
    async def unlurk(self, ctx: commands.Context):
        global usrDict
        roller = random.randint(1, 10000) # for fun
        usr = str(ctx.author.name)
        # and a mess.
        if usr in usrDict: # sees if the user is in the lurk dictionary
            await ctx.send("Welcome back " + ctx.author.mention + "! Let's see if you get lucky!")
            print('ROLLING POWER ' + str(usrDict[usr]))
            if usrDict[usr] == True:
                scene_item_id = 0 # scene item id has to be gained via obs-websockets (via item.py)
                cl.set_scene_item_enabled("SCENE_NAME", scene_item_id, True) # You can enable scene items in this way inside OBS!
                await ctx.send(f"{usr} has unlurked, and ended the stream lol")
                cl.stop_stream # for shits and giggles
        else: # not in lurk dictionary 
            await ctx.send(ctx.author.mention + " Sorry, I didn't see you lurk! Remember to !lurk when you do lurk! ") 
            
        if usrDict[usr] != None: # and erase from dictionary when done. 
            del usrDict[usr]


bot = Bot()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.
# code by eepysheepyy - https://linktr.ee/eepysheepyy
