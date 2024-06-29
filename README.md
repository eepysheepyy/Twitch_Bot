Python-Based Twitch Bot (TwitchIO + OBS_WS)
--

So, hi!
I wanted to globalise this twitch bot I've been modifying over the last few months, and make it readily available for people, as I think it to be a really good addition to streams!

Basically, this is a python scripted Twitch Chat Bot, that uses a combination of TwitchIO, OBS Websockets to create a multi-function/purpose bot that can read and act upon chat messages and executes custom chat commands. You can also directly interact with OBS, get all the info from the twitch side of things, and also have full python functionality too. 

I've also included a way for messages in foreign languages to be translated in real time, via the Google Translate API, you can remove this if you don't like it. 

It's rather simple at the moment, I know, but it has a lot of potential! I've kept some of the things I use for my own streams private. 

I want to eventually add Twitch Auto-modding to this whole thing, but that can wait for now. 

So what do you need? 
Great Question.

REQUIREMENTS
--

Apparently Python 3.10.14, on a Virtual Environment, with 
*(and make sure your pip is updated)*

Twitchio - *pip install twitchio*

OBSWS_Python - *pip install obsws-python*

DeepTranslator - *pip install deep-translator*


**You ALSO need to go into the env_secrets.json file and add the following under the categories:**

Token: Your OAUTH Twitch token that can be found at: https://twitchapps.com/tmi/

Client_ID: Either obtained via https://twitchtokengenerator.com/ OR through the TwitchDev console (https://dev.twitch.tv/) and setting up a application 

Bot_Nick: What username your bot has (please use either your username, or a profile that you own) 

Bot_Prefix: What character you want before your commands, usually set to '!'

Channel: The channel name of the chat you're moderating


Also, there's the item.py file which can tell you what scene_item_id's are (when selected inside OBS) because theres seemingly no other way to check, and it was pissing me off, so I assume that I can alleviate someone else's pain if someone went looking. 

**JUST TO CLARIFY: THIS PYTHON SCRIPT (item.py) CAN FIND THE scene_item_id of OBS ITEMS when SELECTED inside OBS, when it's connected to your OBS-Websockets.**


Links
--

You can find my website is https://eepysheepyy.com/

And uou can find my Twitch here: https://www.twitch.tv/eepysheepyy

You can feel free to check out all my other socials and stuff here: https://linktr.ee/eepysheepyy

I hope you all have a BAA-Rilliant Day <33

