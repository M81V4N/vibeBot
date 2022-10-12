import discord
from discord.ext import commands
from discord.utils import get
from discord.ext import tasks
import time as t
import random as r
import requests, shutil, os
import subprocess
import string, datetime
from discord.ext.commands import MemberConverter
from discord.ext.commands import CommandNotFound
import wikipedia
import asyncio
import faker
#import youtube_dl
import os
from bs4 import BeautifulSoup
#from aternosapi import AternosAPI
from datetime import datetime, timedelta

import ffmpeg

import NumberGrater
import fetch_face

import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

import logging
logging.basicConfig(filename='redacted.log', encoding='utf-8', level=logging.INFO, filemode='a', format='%(asctime)s [%(levelname)s]: %(message)s')

#discord.Intents.all()
#intents = discord.Intents()
#intents.messages = True

f = faker.Faker()



file = open('vibeToken.txt', 'r')
for a in file:
	TOKEN = a.replace('\n','')

bot = commands.Bot(command_prefix='>> ')# intents = intents)

@bot.event
async def on_ready():
	logging.info(f'LOGGED IN AS {bot.user.name} {bot.user.id}')
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="your conversations"))

	initRedditThingy()
	#tormenting.start() !! CHANGE

alphabet_upper = list(string.ascii_uppercase)
alphabet_lower = list(string.ascii_lowercase)

converter = MemberConverter()

global queue_tasks
queue_tasks = []


@bot.event 
async def on_command_error(ctx, error): 
	if isinstance(error, commands.CommandNotFound):
		logging.warning(f'{ctx.author} invoked "{ctx.message.content}"; command not found')
		await ctx.send("```// COMMAND NOT FOUND. CHECK YOUR SPELLING```")


def caesar_loop(text, mode, i):

	out = ''

	for key in text:

		if key in alphabet_upper:
			out += mode(alphabet_upper, key, i)

		elif key in alphabet_lower:
			out += mode(alphabet_lower, key, i)

		else:
			out += key

	return out


def cipher(alphabet, key, i):

	if alphabet.index(key) + i < len(alphabet):
		return alphabet[alphabet.index(key) + i]

	else:
		return alphabet[alphabet.index(key) + i - len(alphabet)]


def decipher(alphabet, key, i):

	if alphabet.index(key) - i > 0:
		return alphabet[alphabet.index(key) - i]

	else:
		return alphabet[alphabet.index(key) - i]


def fileToDict(filename):

	file = open(filename, 'r')

	out = file.read().splitlines()
	for line in out:
		out[out.index(line)] = line.split('|')

	file.close()
	return dict(out)
		

def dictToFile(dc, filename):
	try:
		file.close()
	except:
		pass

	file = open(filename, 'w')
	out = ''

	for element in dc:
		out += f'{element}|{dc[element]}\n'

	file.write(out)
	file.close()


def calcSpaces(el, list):
	return ' ' * ( len(max(list, key=len)) - len(el))




gunWhitelist = ['[REDACTED]#4230'] # Place your trusted people in this variable


@bot.event
async def on_message(message):

	if 'vibe' in message.content.lower() and str(message.author) not in gunWhitelist:

		print(f'[{t.ctime()}] {str(message.author)} WANTS THEIR VIBES CHECKED')
		
		if r.randint(1, 7) == 3:
			await message.channel.send('https://cdn.discordapp.com/attachments/774745923552542780/775781069592199198/852bdc314b0541ab75f4f1598dad2dcb.png')
			await asyncio.sleep(3)
			await message.channel.send('https://cdn.discordapp.com/attachments/774745923552542780/775781248546635796/rizhg2qrqqv31.png')

	if 'wiesz co robić, [redacted]' in message.content.lower() and str(message.author) in gunWhitelist:
		await message.channel.send('https://cdn.discordapp.com/attachments/774745923552542780/775781069592199198/852bdc314b0541ab75f4f1598dad2dcb.png')
		await asyncio.sleep(3)
		await message.channel.send('https://cdn.discordapp.com/attachments/774745923552542780/775781248546635796/rizhg2qrqqv31.png')

	if 'h' == message.content.lower():
		if r.randint(1, 3) == 3:
			await message.channel.send('h')

	if message.content.lower() in ["amongus","amogus","sus", 'among us', 'stop posting about among us', "||amongus||","||amogus||","||sus||", '||among us||', '||stop posting about among us||'] and str(message.author) != '[REDACTED]#4230':
		await message.channel.send('sus')

	if '[redacted]' in message.content.lower() and '>>' not in message.content and str(message.author) not in ['[REDACTED]#4230']:
		responses = ["READY", "AWAITING COMMAND", "ON STANDBY", "RECEIVING", "WHAT ARE YOUR ORDERS", "PREPARED FOR ACTION"]
		await message.channel.send(f'```// {r.choice(responses)}```')


	if str(message.author) == 'MEE6#4876':
		await message.channel.send('https://cdn.discordapp.com/attachments/774745923552542780/775781069592199198/852bdc314b0541ab75f4f1598dad2dcb.png')
		await asyncio.sleep(3)
		await message.channel.send('https://cdn.discordapp.com/attachments/774745923552542780/775781248546635796/rizhg2qrqqv31.png')
		await message.author.kick(reason="// STINKY")


	await bot.process_commands(message)

	"""
	if str(message.author) != "[REDACTED]#4230":
		file = open(f'log/log_{str(message.channel)}.txt', 'a')
		file.write(f'[{t.ctime()}] {str(message.author)}: {str(message.content)}\n')
		file.close()
	"""

@bot.event
async def on_message_delete(message):

	file = open(f'deleted/{str(message.author)}_DELETED_LOG.txt', 'a')
	file.write(f'[{t.ctime()}] {str(message.author)}: {str(message.content)}\n')
	file.close()

	#file download if possibleś



@tasks.loop(seconds=15)
async def check_queued_tasks():
	"""TODO: to be added file handling; serializing
		TODO: implement it actually well so it works on any server
		TODO: also do it better so it can do backlogged stuff

	with open('task_queue.txt', 'r') as file:
		pass
	"""

	# task is dict and has:
	# time, command, args(dict)

	for task in queue_tasks:
		if datetime.ctime(datetime.now()) >= datetime.ctime(task['time']):

			if task['command'] == "REMIND":

				channel = bot.get_channel('<channel>')
				uid = task['args']['id']

				mention = f'<@{uid}>'

				await channel.send(f'''**=== REMINDER FOR {mention}===**\n```{task['args']['message']}```''')

				queue_tasks.remove(task)

			else:
				pass


@bot.command()
async def remind(ctx, time, message, person):
	"""
	Set a reminder.

	Time: how many hours and minutes since now
	you have to write this sticked together
	examples:
		5h
		1h30m
		65m

	Message: the message you want to send.
	You have to use "" when your message has multiple words.
	Example:
		"This is an example message argument"

	Person: UserID or MENTION of target user.
	Ping yourself if you want to remind something yourself later


	example:
	>> remind 1m "text goes here" 354158625323562624
	>> remind 1h30m "text goes h" @viberunner
	"""
	if person == '':
		person = ctx.author.id
	elif "<@" in person:
		person = int(person.replace('<@!', '').replace('>', ''))
	else:
		person = int(person)


	# time is basically string how late from now should it be sent
	# for now i will just do h and m like this:
	#	1h
	#	3h30m
	#	25m

	if 'h' not in time.lower() and 'm' in time.lower():
		tmod = int(time.replace('m', ''))
		ftime = datetime.now() + timedelta(minutes=tmod)

	elif 'h' in time.lower() and 'm' not in time.lower():
		tmod = int(time.replace('h', ''))
		ftime = datetime.now() + timedelta(hours=tmod)

	elif 'h' in time.lower() and 'm' in time.lower():
		tmod_h = int( time[0:time.lower().index('h')] )
		tmod_m = int( time[time.lower().index('h')+1:time.lower().index('m')] )
		ftime = datetime.now() + timedelta(hours=tmod_h, minutes=tmod_m)

	else:
		await ctx.send('```// INCORRECT TIME ARGUMENT```')

	try:
		queue_tasks.append({'time':ftime, 'command':'REMIND', 'args':{'message':message, 'id':person}})
		await ctx.send(f'```// REMINDER ADDED. WAIT UNTIL {datetime.ctime(ftime)}```')
	except Exception as ex:
		await ctx.send('```// INCORRECT PROMPT. CHECK ">> help remind"```')
		print(ex)


@bot.command()
async def debug_tasks(ctx):
	print(queue_tasks)


@bot.command()
async def time(ctx):
	await ctx.send(f'```// {datetime.ctime(datetime.now())}```')


@bot.command()
async def killswitch(ctx, password):
	if password == "goodbye":
		logging.info(f'{ctx.author} TRIGGERED THE KILLSWITCH. THE BOT IS EXITING.')
		await ctx.send('```// i have failed you... again...```')
		exit('KILLSWITCH ACTIVATED')
	else:
		logging.info(f'{ctx.author} attempted to invoke killswitch. Wrong password.')
		await ctx.send("```// COMMAND NOT FOUND. CHECK YOUR SPELLING, DUMBASS```")


@bot.command(help="caesar cipher, decrypt and encrypt")
async def caesar(ctx, mode, i: int, text):

	#mode = int(input('1 to cipher, 2 to decipher: '))
	# brute ON when i == 0, else i

	if mode.lower() in ['c', 'cipher', 'e', 'encrypt']:

		if i == 0:
			out = '```'
			for i in range(1, 27):  # 26x for EN
				out += caesar_loop(text, cipher, i) + '\n'

			await ctx.send(out+'```')

		else:
			await ctx.send(f'```{caesar_loop(text, cipher, i)}```')

	elif mode.lower() in ['d', 'decipher']:

		if i == 0:
			out = '```'
			for i in range(1, 27):  # 26x for EN
				out += caesar_loop(text, decipher, i) + '\n'

			await ctx.send(out+'```')

		else:
			await ctx.send(f'```{caesar_loop(text, decipher, i)}```')


@bot.command()
async def memeify(ctx, msgID: int, upper_text, bottom_text): # USE WITH CAUTION, VERY UNSTABLE

	logging.info(f'{ctx.author} invoked memeify.')

	# ---- GET FILE LINK ----
	msg = await ctx.fetch_message(msgID)
	image_url = msg.attachments[0].url

	# ---- DOWNLOAD -----
	status_message = await ctx.send('```// FETCHING THE IMAGE...```')

	resp = requests.get(image_url, stream=True)
	local_file = open('local_image.jpg', 'wb')
	# Set decode_content value to True, otherwise the downloaded image file's size will be zero.
	resp.raw.decode_content = True
	# Copy the response stream raw data to local image file.
	shutil.copyfileobj(resp.raw, local_file)
	# Remove the image url response object.
	del resp

	# ---- ADD CAPTION -----------------------------------------------------------------------
	await status_message.edit(content="```// ADDING CAPTION...```")
	filename = "local_image.jpg"
	topString = upper_text.upper()
	bottomString = bottom_text.upper()
	
	img = Image.open(filename)
	imageSize = img.size

	# find biggest font size that works
	fontSize = int(imageSize[1]/5)
	font = ImageFont.truetype("Impact.ttf", fontSize)
	topTextSize = font.getsize(topString)
	bottomTextSize = font.getsize(bottomString)
	while topTextSize[0] > imageSize[0]-20 or bottomTextSize[0] > imageSize[0]-20:
		fontSize = fontSize - 1
		font = ImageFont.truetype("Impact.ttf", fontSize)
		topTextSize = font.getsize(topString)
		bottomTextSize = font.getsize(bottomString)

	# find top centered position for top text
	topTextPositionX = (imageSize[0]/2) - (topTextSize[0]/2)
	topTextPositionY = 0
	topTextPosition = (topTextPositionX, topTextPositionY)

	# find bottom centered position for bottom text
	bottomTextPositionX = (imageSize[0]/2) - (bottomTextSize[0]/2)
	bottomTextPositionY = imageSize[1] - bottomTextSize[1]
	bottomTextPosition = (bottomTextPositionX, bottomTextPositionY)

	draw = ImageDraw.Draw(img)

	# draw outlines
	# there may be a better way
	outlineRange = int(fontSize/15)
	for x in range(-outlineRange, outlineRange+1):
		for y in range(-outlineRange, outlineRange+1):
			draw.text((topTextPosition[0]+x, topTextPosition[1]+y), topString, (0,0,0), font=font)
			draw.text((bottomTextPosition[0]+x, bottomTextPosition[1]+y), bottomString, (0,0,0), font=font)

	draw.text(topTextPosition, topString, (255,255,255), font=font)
	draw.text(bottomTextPosition, bottomString, (255,255,255), font=font)

	img.save("temp.png")


	# ---- SEND READY IMAGE ---------------------------------------------------------------
	await status_message.edit(content="```// SENDING...```")

	await ctx.send(file=discord.File('temp.png'))

	# ---- REMOVE REMAINING FILES ----
	os.remove('local_image.jpg')
	os.remove('temp.png')
	del img

	await status_message.delete()

	logging.info(f'{ctx.author}\'s memeify is somehow successful')


@bot.command(help="redact every char in text")
async def annoy(ctx, message):
	if len(message)*5 > 1994:
		await ctx.send('```// MESSAGE TOO LONG. RESTRICT TO 398 CHARACTERS```')
	else:
		out = ''
		for char in message:
			out += f'||{char}||'

		await ctx.send(f'`{out}`')


@bot.command()
async def spammypasta(ctx, message):

	await ctx.send("```" + message*int(1994/len(message)) + "```")


@bot.command()
async def save(ctx, name, link):
	saved_dict = fileToDict('saved.txt')

	if name not in saved_dict:
		saved_dict.update({name:link})
		dictToFile(saved_dict, 'saved.txt')
		await ctx.send('```// LINK SAVED```')

	else:
		await ctx.send('```// NAME TAKEN```')


@bot.command()
async def load(ctx, name):
	try:
		await ctx.send(fileToDict('saved.txt')[name])

	except:
		await ctx.send('```// FILE NOT FOUND```')


@bot.command()
async def list(ctx): # ADD SEVERAL PAGES AND SKIPPING SIDES BY REACTIONS > < (only the command caller can flip it)
	saved_dict = fileToDict('saved.txt')
	out = ''
			
	for element in saved_dict:
		new = f'{calcSpaces(element, saved_dict)}{element} - {saved_dict[element]}\n'
				
		if (len(out) + len(new)) < 2000:
			out += new
		else:
			await ctx.send(f'```\n{out}```')
			out = ''
			out += new

	if out != '':
		await ctx.send(f'```\n{out}```')


@bot.command(help="fetch random historic message from channel and then guess who made it")
async def getRMSG(ctx, channelID: int, substractDays: int):

	if substractDays > 300:
		await ctx.send('```// CHOOSE DAYS LESSER THAN 300```')

	else:
		try:
			await ctx.send("```// FETCHING...```")
			channel = bot.get_channel(channelID)
			beforeDate = datetime.today() - timedelta(days=substractDays)
			messages = await channel.history(limit=700, before=beforeDate).flatten() # AMOUNT IS DEFAULT 200

			chosen = r.choice(messages)
			if 'https://' in chosen.content or 'http://' in chosen.content:
				while 'https://' not in chosen.content and 'http://' not in chosen.content:
					chosen = r.choice(messages)

			msgg = chosen.content.replace('||', '')
			await ctx.send(f'```"{msgg}"```')
			if len(chosen.attachments) > 0:
				await ctx.send(chosen.attachments[0].url)
			await asyncio.sleep(30)
			await ctx.send(f'```THE ANSWER IS {chosen.author}, CREATED ON {chosen.created_at.day}.{chosen.created_at.month}.{chosen.created_at.year}```')
		
		except Exception as ex:
			await ctx.send(f'```{ex}```')

@bot.command()
async def cleanup(ctx, msgID: int):
	if str(ctx.author) in gunWhitelist:
		msg = await ctx.channel.fetch_message(msgID)
		await msg.delete()
	else:
		await ctx.send('```// INSUFFICIENT PERMISSIONS```')




@bot.command()
async def eightball(ctx, question):
	await ctx.send(f"```// {r.choice(FileToList('eightball.txt'))}```")




## SECRET SANDSa -----------------

def listToFile(dc, filename):

	try:
		file.close()
	except:
		pass

	file = open(filename, 'w')
	out = ''

	for element in dc:
		out += f'{element}\n'

	file.write(out)
	file.close()


def FileToList(filename):

	file = open(filename, 'r')
	out = file.read().splitlines()
	file.close()

	return out
		

# fileToDict(filename) i DictToFile(dc, filename) są wyżej zrobione

def getPeopleLeft(pplList, assigneDict):

	out = []

	for nick in pplList:
		if nick not in assigneDict:
			out.append(nick)

	return out

@bot.command()
async def getAllSignedUp(ctx, channel_id: int, message_id: int):

	message = await bot.get_channel(channel_id).fetch_message(message_id)
	participants = set()

	for reaction in message.reactions:

		async for user in reaction.users():
			participants.add(user)

	if len(participants) % 2 != 0:
		botid = await converter.convert(ctx, '[REDACTED]#4230')
		participants.add(botid)

	await ctx.send(f"users: {', '.join(user.name for user in participants)}")

	# save them
	listToFile(participants, 'peopleLeft.txt')
	listToFile(participants, 'participants.txt')
	open('victimDict.txt', 'w').close() # erase previous hits



@bot.command()
async def secsan(ctx):

	participants = FileToList('participants.txt')
	peopleLeft = FileToList('peopleLeft.txt') # left to be a victim yknow
	victimDict = fileToDict('victimDict.txt') # {user:victim}

	if str(ctx.author) not in victimDict and str(ctx.author) in participants:

		while True:
			victim = r.choice(peopleLeft)
			if victim != str(ctx.author):
				break

		victimDict.update({ctx.author:victim})
		peopleLeft.remove(victim)

		await ctx.author.send(f"""```// SECSAN INITIATIVE
//
//           [  E  D  I  T  I  O  N :  2 . 0 ]
//
// VICTIM ASSIGNED: {victim}
// YOU ARE OBLIGED TO KEEP YOUR VICTIM'S IDENTITY SECRET.
// FAILURE TO COMPLY WILL RESULT WITH TERMINATION.
// THIS REGULATION WILL BE LIFTED DURING THE EXECUTION PHASE.
//
// OBJECTIVE: FABRICATE A DIGITAL ENDOWMENT PACKAGE FOR THE VICTIM.
//            FEEL FREE TO DISCUSS THE OPERATION WITH OTHER AGENTS.
//            DO NOT MENTION OR HINT YOUR VICTIM'S IDENTITY!
//            DO WHAT YOU DO BEST, THE EFFORT MATTERS.
//
// DEADLINE: 31.12.2021
//
//
//
// DON'T LET US DOWN```""")
		

		await ctx.send("```// VICTIM HAS BEEN ASSIGNED TO YOU. CHECK YOUR DM'S.```")

	elif str(ctx.author) in victimDict:
		await ctx.send("```// YOU ALREADY HAVE A VICTIM ASSIGNED.```")

	elif str(ctx.author) not in participants:
		await ctx.send("```// YOU HAVEN'T SIGNED UP.```")

	else:
		await ctx.send("// wtf")

	listToFile(peopleLeft, 'peopleLeft.txt')
	dictToFile(victimDict, 'victimDict.txt')


@bot.command()
async def lazybones(ctx):

	participants = FileToList('participants.txt')
	victimDict = fileToDict('victimDict.txt')

	out = []

	for user in participants:
		if user not in victimDict:
			out.append(user)

	if len(out) == 0:
		await ctx.send('```// ALL AGENTS HAVE VICTIMS ASSIGNED```')
	else:
		await ctx.send(f"```// LAZYBONES: {out}```")


## END OF SS ----------------



## dumb commands cuz shiro wanted
@bot.command()
async def sexscan(ctx):

	await ctx.send(f'```// SEXSCAN RESULT: {str(r.randrange(1,101))}%```')

@bot.command()
async def simpometer(ctx, name):

	#user = ctx.guild.get_member(int(mentioned.replace('<@!', '').replace('>', '')))
	randomed = r.randrange(1,101)

	if randomed >= 70:
		await ctx.send(f"""```// SIMP'O'METER
// {name} IS A SIMP IN {str(randomed)}%```""")
	else:
		await ctx.send(f"""```// SIMP'O'METER
// {name}'s SIMP PERCENTAGE: {str(randomed)}%```""")
##-


def getChannels():
	text_channel_list = []
	for server in Client.servers:
		for channel in server.channels:
			if channel.type == 'Text':
				text_channel_list.append(channel)

	return text_channel_list


def getHighestValueDictItem(inDict):
	outWord = ''
	outTimes = 1

	for item in inDict:
		if inDict[item] > outTimes:
			outWord = item
			outTimes = inDict[item]

	return outWord


# WIKIPEDIA STUFF START HERE
@bot.command()
async def summary(ctx, thing, lang='en'):

	try:
		wikipedia.set_lang(lang)
	except:
		await ctx.send('```WRONG LANGUAGE. DEFAULTING TO ENGLISH.```')
		wikipedia.set_lang('en')

	try: 
		result = wikipedia.summary(thing, sentences = 3)
	except:
		await ctx.send('```NO RESULTS FOUND.```')


	await ctx.send(f'```{result}```')

# WIKIPEDIA STUFF ENDS HERE


#dżownica's request for some reason
@bot.command()
async def cage(ctx):
	"""
	if str(ctx.author) == <REDACTED USERNAME>:
		cages = ['https://upload.wikimedia.org/wikipedia/commons/c/c0/Nicolas_Cage_Deauville_2013.jpg', 
		'https://image.cnbcfm.com/api/v1/image/106069731-1565297100509gettyimages-1052370114.jpeg?v=1565297156&w=1400&h=950', 
		'https://images.firstpost.com/wp-content/uploads/2018/04/nicolas-cage-380.jpg?impolicy=website&width=1200&height=800',
		'https://th.bing.com/th/id/OIP.xsQqTXNooiu_eCt1okPU9QHaE7?pid=Api&rs=1',
		'https://cdn.mediaworks.hu/wp-content/uploads/2019/08/+otf/1200x630/NocholasCage.jpg',
		'https://theplaylist.net/wp-content/uploads/2017/06/Nicolas-Cage-The-Runner.jpg',
		'https://s.abcnews.com/images/US/nicolas-cage-gty-er-190331_hpMain_16x9_992.jpg',
		'https://s3media.freemalaysiatoday.com/wp-content/uploads/2019/01/FMT-NicolasCage24012019-AFP.jpg',
		'https://www.cheatsheet.com/wp-content/uploads/2020/10/Nicolas-Cage-1024x683.jpg',
		'https://ksassets.timeincuk.net/wp/uploads/sites/55/2018/07/Nicholas-Cage.jpg',
		'https://d.ibtimes.co.uk/en/full/1609228/nicholas-cage.jpg',
		'https://slappedham.com/wp-content/uploads/2016/01/nicolas-cage-didnt-last-long-bong-in-60-seconds-1389873714-view-1.jpg',
		'https://th.bing.com/th/id/OIP.PJXT25-4OVwA4Sk33U4qhAHaGq?pid=Api&rs=1']
	else:
		cages = ['https://upload.wikimedia.org/wikipedia/commons/c/c0/Nicolas_Cage_Deauville_2013.jpg', 'https://image.cnbcfm.com/api/v1/image/106069731-1565297100509gettyimages-1052370114.jpeg?v=1565297156&w=1400&h=950', 'https://images.firstpost.com/wp-content/uploads/2018/04/nicolas-cage-380.jpg?impolicy=website&width=1200&height=800']
		
	"""
	with open('cages.txt', 'r') as file:

		caged = r.choice(file.readlines()).replace('\n', '')
		await ctx.send(caged)



@bot.command()

async def roll(ctx, querry):

	addValue = 0
	timesRoll = 1
	roll = 1


	if "+" in querry:
		addValue = int(querry[querry.index('+') + 1 : len(querry)])
		querry = querry[0 : querry.index('+')]

	if "d" in querry.lower():
		if querry[0 : querry.index('d')] != '':
			timesRoll = int(querry[0 : querry.index('d')])

		roll = querry[querry.index('d') + 1: len(querry)]

	else:

		try:
			roll = int(querry)

		except:
			await ctx.send('```// INCORRECT PROMPT```')
			return 1

	rolls = []
	for i in range(timesRoll):
		rolls.append(r.randint(1, int(roll)))


	if len(rolls) == 1:
		await ctx.send(f'```// {ctx.author}: {str(rolls[0]+addValue)}```')

	else:
		suma = 0
		for i in rolls:
			suma += i

		await ctx.send(f'```// {ctx.author}: {rolls}```')
		await ctx.send(f'```// {ctx.author}: {suma + addValue}```')


@bot.command()
async def echo(ctx, message):

	if "jestem" in message:
		message = message.replace('jestem', f'{ctx.author} jest')
	elif "i am" in message.lower():
		message = message.lower().replace('i am', f'{ctx.author} is')

	await ctx.send(f"```// {message.upper()}```")


def initRedditThingy():
	### INIT
	import random as r
	import praw

	postLimit = 120
	
	print('\nConnecting... ', end='') 
	
	global reddit#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	reddit = praw.Reddit(client_id="",  # https://www.reddit.com/prefs/apps
			client_secret="",
			password="",
			user_agent="vibebot",
			username="")
	print('done\n')
	
	global posts
	posts = []
	subredditsList = ['godtiersuperpowers', 'titantiersuperpowers', 'superpowerswithacatch']#, 'shittysuperpowers'
	for sub in subredditsList:
		print('Fetching posts from ' + sub + '... ', end='')
		posts.extend([post for post in reddit.subreddit(sub).hot(limit=postLimit)])
		print('done')
		
	r.shuffle(posts)

	global cats_wolves_horses
	cats_wolves_horses = [] # here be image links
	for sub in ['Horses', 'wolves', 'cats']:
		print(f"Fething posts from {sub}... ", end='')

		for submission in reddit.subreddit(sub).hot(limit=postLimit):
			if "jpg" in submission.url.lower() or "png" in submission.url.lower() or "jpeg" in submission.url.lower():
				cats_wolves_horses.append(submission.url)

	r.shuffle(cats_wolves_horses)


	global bread_or_YES_MAN
	bread_or_YES_MAN = []
	bread_or_YES_MAN.append('http://img2.wikia.nocookie.net/__cb20110511135907/fallout/images/a/a5/Yes_Man.jpg')
	bread_or_YES_MAN.append('https://pm1.narvii.com/6203/3bfcddab8c3666ea08b309738adae8bea496dea8_hq.jpg')
	bread_or_YES_MAN.append('https://avante.biz/wp-content/uploads/Yes-man-fallout-wallpaper/Yes-man-fallout-wallpaper13.jpg')
	bread_or_YES_MAN.append('https://ih1.redbubble.net/image.352019669.1140/sticker,375x360-bg,ffffff.u2.png')
	bread_or_YES_MAN.append('https://pm1.narvii.com/6203/dde0b5adbd65bc9ea7460800dc1e4b65c4747bf6_hq.jpg')
	bread_or_YES_MAN.append('https://staticdelivery.nexusmods.com/images/130/45039397-1555555036.png')

	print("hella BREAD")
	for submission in reddit.subreddit('Bread').hot(limit=40):
		if "jpg" in submission.url.lower() or "png" in submission.url.lower() or "jpeg" in submission.url.lower():
			bread_or_YES_MAN.append(submission.url)	


	global doors_list
	doors_list = []
	for sub in ['doors']:
		print(f"It's {sub} time.")

		for submission in reddit.subreddit(sub).hot(limit=postLimit):
			if "jpg" in submission.url.lower() or "png" in submission.url.lower() or "jpeg" in submission.url.lower():
				doors_list.append(submission.url)

	r.shuffle(doors_list)

	print('===== ALL DONE =====')


@bot.command()
async def rsp(ctx):
	randomPostIndex = r.randint(0, len(posts) - 1)
	randomPost = posts[randomPostIndex]

	await ctx.send(f"""```
{randomPost.subreddit}
{randomPost.title}
{randomPost.selftext}```""")
	posts.pop(posts.index(randomPost))


@bot.command() # CATS, WOLVES AND HORSES FOR SYLWANA SECSAN 2021
async def cwh(ctx):
	randomPostIndex = r.randint(0, len(cats_wolves_horses) - 1)
	await ctx.send(cats_wolves_horses[randomPostIndex])


@bot.command() # hella bread for the bread herself SECSAN 2021
async def bread(ctx):
	randomPostIndex = r.randint(0, len(bread_or_YES_MAN) - 1)
	await ctx.send(bread_or_YES_MAN[randomPostIndex])



def genNPC(n0):

	# 1. rola
	roles = { # ADD IMP ORDER SO THE STATS ARE ASSIGNED SMARTLY
	'Rockman':{'imp_order':"OP|"},
	'Businessman':{'imp_order':"INT|"},
	'Netrunner':{'imp_order':"INT|REF|TECH|EMP|OP|SZ|SZYB|BC|ATR", "ultimate":"interface"},
	'Fixer':{'imp_order':"OP|"},
	'Tech':{'imp_order':"TECH|"},
	'Medtech':{'imp_order':"TECH|"},
	'Nomad':{'imp_order':"INT|"},
	'Cop':{'imp_order':"OP|"},
	'Solo':{'imp_order':"REF|BC|"},
	'Journalist':{'imp_order':"INT|"}
	}

	#role = r.choice(list(roles.keys())) # TOTAL RANDOM MODE
										# IMPORTANT!!!! ALSO ADD SMART MODE!! like selecting cop team or crime team oppnts

	role = 'Netrunner' ## TEMPORARY!!!!!!!!! DELETE WHEN ALL ROLES ARE DONE! ALSO FIX THE RANDOMISER!

	# 2. cechy
	rolls = []
	for i in range(9):
		rolls.append(r.randrange(3,11))
	rolls.sort(reverse=True)

	stats = {"INT":0, "REF":0, "TECH":0, "EMP":0, "OP":0, "SZ":0, "SZYB":0, "BC":0, "ATR":0}
	ordered_stats = roles[role]['imp_order'].split('|')
	for i in range(9):
		stats[ordered_stats[i]] = rolls[i]


	# 3. wszczepy
	cyber = []
	roll_times = 3
	if role == "Solo":
		roll_times  = 6

	for i in range(roll_times):
		pass #### CYBERWSZCZEPY


	# 4. sprzęt
	extra_points = -1 # BECAUSE LIST STARTS AT INDEX 0
	if role in ['Nomad', 'Cop']:
		extra_points += 2
	elif role == 'Solo':
		extra_points += 3

	# TODO: MODIFY WEAPON TO AUTO-ADD STATS!
	gear_list = [
	{'armor':"ciężka skóra", 'weapon':"nóż"}, #this is index 0, so one extra point was taken away before!!
	{'armor':"koszulka kuloodporna", 'weapon':"lekki pistolet"},
	{'armor':"lekka kurtka pancerna", 'weapon':"średni pistolet"},
	{'armor':"lekka kurtka pancerna", 'weapon':"ciężki pistolet"},
	{'armor':"średnia kurtka pancerna", 'weapon':"ciężki pistolet"},
	{'armor':"średnia kurtka pancerna", 'weapon':"lekki pistolet maszynowy"},
	{'armor':"średnia kurtka pancerna", 'weapon':"lekki karabin"},
	{'armor':"ciężka kurtka pancerna", 'weapon':"średni karabin"},
	{'armor':"ciężka kurtka pancerna", 'weapon':"ciężki karabin"},
	{'armor':"MetalGear", 'weapon':"ciężki karabin"} 	# 10+ converts to index 9
	]

	armor_data = {"ciężka skóra":{'HEAD':0,'TORSO':4,'LHAND':4,'RHAND':4, 'LLEG':4, 'RLEG':4, 'WZ':0},
				  "koszulka kuloodporna":{'HEAD':0,'TORSO':10,'LHAND':0,'RHAND':0, 'LLEG':0, 'RLEG':0, 'WZ':0},
				  "lekka kurtka pancerna":{'HEAD':0,'TORSO':14,'LHAND':14,'RHAND':14, 'LLEG':0, 'RLEG':0, 'WZ':0},
				  "średnia kurtka pancerna":{'HEAD':0,'TORSO':18,'LHAND':18,'RHAND':18, 'LLEG':0, 'RLEG':0, 'WZ':1},
				  "ciężka kurtka pancerna":{'HEAD':0,'TORSO':20,'LHAND':20,'RHAND':20, 'LLEG':0, 'RLEG':0, 'WZ':2},
				  "MetalGear":{'HEAD':25,'TORSO':25,'LHAND':25,'RHAND':25, 'LLEG':25, 'RLEG':25, 'WZ':2}}

	weapon_data = {"nóż":"",
				   "lekki pistolet":"",
				   "ciężki pistolet":"",
				   "lekki pistolet maszynowy":"",
				   "lekki karabin":"",
				   "średni karabin":"",
				   "ciężki karabin":""}

	try:
		gear = gear_list[r.randrange(1,11)+extra_points]
	except IndexError:
		gear = gear_list[9]



	#### UWAGA!!!! UPEWNIJ SIĘ ŻE W TABELI DRUKUJE SIĘ ZAWSZE TYLE SAMO ZNAKÓW!
	#### czyli np. jak jest pancerz jednocyfrowy to dopisz dodatkową spację

	armor_line = "|" # pretty-ify'ing that chart or whatever
	for point in [ armor_data[gear['armor']]['HEAD'], armor_data[gear['armor']]['TORSO'], armor_data[gear['armor']]['RHAND'], armor_data[gear['armor']]['LHAND'], armor_data[gear['armor']]['RLEG'], armor_data[gear['armor']]['LLEG'] ]:

		point = str(point)
		if len(point) == 1:
			armor_line += f"    {point}    |"

		elif len(point) == 2:
			armor_line += f"    {point}   |"


	return f"""```===== {n0} =====

{f.name()}, {role.upper()}

INT [{str(stats['INT'])}] REF [{str(stats['REF'])}/{str( stats['REF'] - armor_data[gear['armor']]['WZ'] )}] TECH [{str(stats['TECH'])}] OP [{str(stats['OP'])}]
ATR [{str(stats['ATR'])}] SZ   [{str(stats['SZ'])}]   SZYB [{str(stats['SZYB'])}] BC [{str(stats['BC'])}]
EMP [{str(stats['EMP'])}] BIEG [{str(stats['SZYB']*3)}m]   SKOK [{str(int(stats['SZYB']/4))}m]


PANCERZ: {gear['armor']}
-------------------------------------------------------------
|  GŁOWA  |  TUŁÓW  | P. RĘKA | L. RĘKA | P. NOGA | L. NOGA |
|    1    |   2-4   |    5    |    6    |   7-8   |   9-10  |
-------------------------------------------------------------
{armor_line}
-------------------------------------------------------------

CYBORGIZACJE: {cyber}PLACEHOLDER

ZDOLNOŚĆ:    {roles[role]['ultimate']}

BROŃ:  {gear['weapon']}PLACEHOLDER!!!```"""

# CYBERPUNK 2020 RPG
@bot.command()
async def qNPC(ctx, quantity: int = 1): # qNPC stands for quickNonPlayerCharacter

	if quantity > 6:
		await ctx.send("```// CHANGING QUANTITY TO 6.```")
		quantity = 6

	elif quantity < 1:
		await ctx.send("```// CHANGING QUANTITY TO 1.```")
		quantity = 1

	for i in range(quantity):
		await ctx.send(genNPC(i))


@bot.command()
async def napalm(ctx):

	logging.warning(f'!!! {ctx.author} INVOKED NAPALM IN {ctx.channel} !!!')

	a = ":fire:"
	for i in range(5):
		await ctx.send(f'{a}{a}{a}{a}{a}')
		await asyncio.sleep(0.75)


# BRI'ISH FAXX
# SOURCE: http://www.londonbeerengine.co.uk/1001oneliners
# copy all these to a file, clear them up slightly
@bot.command()
async def thought(ctx):
	file = open('facts.txt', 'r')
	line = next(file)
	for num, aline in enumerate(file, 2):
		if r.randrange(num):
			continue
		line = aline
	
	# get rid of stinky numbers on the beginning
	line = line.split(' ')
	line.pop(0)
	out = line.pop(0)
	for word in line:
		if word != '':
			out += f" {word}"

	await ctx.send(f"```//{out.upper()}```")


@bot.command()
async def split(ctx, number:int):

	if len(str(number)) > 7:
		await ctx.send("```// NUMBER TOO LARGE. TRY SMALLER.```")
	elif number <= 0:
		await ctx.send('```// HAVE SOME MERCY FOR ME...```')
	else:
		await ctx.send(f"```{NumberGrater.split(number)}```") # the numbergrater script can be found on my github: https://github.com/vibeRunner/scrapyard/blob/master/math/NumberGrater.py



# To be improved
admin_permissions = ['<INSERT_ADMIN_USERNAME#1234>']
@bot.command()
async def control(ctx, command):
	print(f'{ctx.author} # {command}')
	if str(ctx.author) in admin_permissions:
		await ctx.send(subprocess.check_output(command.split(' ')))

	else:
		await ctx.send('```// INSUFFICIENT PERMISSIONS.```')

#===== BEGIN RP write-as-bot commands

#use this channel you execute this command in with wt
@bot.command()
async def s4ve(ctx):
	if str(ctx.author) in admin_permissions:
		global saved_msg
		saved_msg = ctx

# write messages as bot to the saved channel (execute this command in dm's for example
@bot.command()
async def wt(ctx, message):
	if str(ctx.author) in admin_permissions:
		await saved_msg.send(f"```// {message.upper()}```")
		#await saved_msg.send(message)
		
# ====== END RP write-as-bot commands

@bot.command()    
async def gen_char(ctx, locale="pl_PL"):
	f = faker.Faker(locale)
	addr = f.address().replace('\n', ', ') 
	nm = f.name()

	file_pl = open('polish_adj.txt', 'r')
	adj_list = file_pl.read().split('\n')
	file_pl.close()
	chosen_adj = ""
	for i in range(3):
		temp = r.choice(adj_list)
		if temp not in chosen_adj:
			chosen_adj += f'    - {temp}/a\n'

	file_hobby = open('hobby_list_pl.txt', 'r')
	hobby_list = file_hobby.read().split('\n')

	file_meals = open('meal_list_pl.txt', 'r')
	meals_list = file_meals.read().split('\n')

	dob = str(f.date_of_birth)

	await ctx.send(f"""```----- {str(ctx.author)}'s GENERATED CHARACTER: -----

Name:          {nm}
Job:           {f.job()}
Date Of Birth: {f.date_of_birth()}
Address:       {addr}
E-Mail:        {f.email()}

Personality:   
{chosen_adj}
Favorite Meal: {r.choice(meals_list)}
Hobby:         {r.choice(hobby_list)}

Sentence:      {f.sentence()}
```""")
#E-Mail:        {"".join(nm.split(' '))}@{f.email().split('@')[1]}
	file_meals.close()
	file_hobby.close()

@bot.command()
async def gen_billing(ctx, locale="en_US"):
	f = faker.Faker(locale)
	await ctx.send(f"""```----- {str(ctx.author)}'s BILLING INFORMATION -----
	
--- Credit Card: ---
{f.credit_card_full()}          
--- Address: ---        
{f.address()}

Phone Number:   {f.phone_number()}

protip: use temp-mail
```""")

@bot.command(pass_context=True)
async def start_mindnight(ctx, message_id): # WORK IN PROGRESS

	# check if the dev is calling this
	if str(ctx.author) in admin_permissions:
		ctx.author.send('```// u idot only dev can call this command u dumbass```')

	else:
		# get all ppl who reacted
		message = await ctx.channel.fetch_message(message_id)
		participants = set()
		#guild = bot.get_guild()
		await bot.request_offline_members()
		guild = ctx.message.guild

		for reaction in message.reactions:

			async for user in reaction.users():
				participants.add(guild.get_member(user.id))

		# give them game role

		for person in participants:
			
			person.add_roles(guild.get_role(819517647477145660)) # change ID!!!!!!!!!!!!!!!!!!!!!!!!!!


	# DM ppl roles
	# may the talking start
		# talking time
		# select crew up to 5 propositions/node (then hammer) (display vote stats)
			# mission
		# if not GAME OVER
		# display round stats
	# game over? display nicely





########### MUSIC PROJECT STOLEN FROM https://github.com/afazio1/robotic-nation-proj/blob/master/projects/discord-bot/voice.py#L14 ###
# it has been modified slightly, though
# change the default voice channel

@bot.command()
async def play(ctx, url : str):
	song_there = os.path.isfile("song.mp3")
	try:
		if song_there:
			os.remove("song.mp3")
	except PermissionError:
		await ctx.send("Wait for the current playing music to end or use the 'stop' command")
		return

	voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='Ogólne')
	await voiceChannel.connect()
	voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	"""
	ydl_opts = {
		'format': 'bestaudio/best',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([url])
	for file in os.listdir("./"):
		if file.endswith(".mp3"):
			os.rename(file, "song.mp3")
	"""

	os.system(f"yt-dlp -f 'ba' -x --audio-format mp3 {url} -o 'song.mp3'")

	await voice.play(discord.FFmpegPCMAudio("song.mp3"))
	await voice.disconnect()


@bot.command()
async def leave(ctx):
	voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	if voice.is_connected():
		await voice.disconnect()
	else:
		await ctx.send("The bot is not connected to a voice channel.")


@bot.command()
async def pause(ctx):
	voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	if voice.is_playing():
		voice.pause()
	else:
		await ctx.send("Currently no audio is playing.")


@bot.command()
async def resume(ctx):
	voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	if voice.is_paused():
		voice.resume()
	else:
		await ctx.send("The audio is not paused.")


@bot.command()
async def stop(ctx):
	voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	voice.stop()

##### Music thing over


@bot.command()
async def roulette(ctx):
	if r.randint(1, 6) > 1:
		await ctx.send('```// CLICK```')
	else:
		await ctx.send('https://giphy.com/gifs/rick-roll-lgcUUCXgC8mEo')


@bot.command(name='purge', help='[ADMIN ONLY] this command will clear msgs')
async def purge(ctx, amount:int = 6):
	if str(ctx.author) in admin_permissions:
		await ctx.channel.purge(limit=amount)
		logging.info(f'{ctx.author} cleared {amount} messages in {ctx.channel}')
	else:
		await ctx.send('```// INSUFFICIENT PERMISSIONS.```')
		logging.warning(f'{ctx.author} attempted to clear {amount} messages')


@bot.command()
async def face(ctx):
	logging.info(f'{ctx.author} invoked face')
	fetch_face.main("http://thispersondoesnotexist.com", 'fakeface/')

	file = "fakeface/image"
	pre, ext = os.path.splitext(file)
	os.rename(file, pre + '.jpg')

	await ctx.send(file=discord.File('fakeface/image.jpg'))



@bot.command()
async def shoot(ctx, target: str): # one-upping those idots
	
	logging.info(f'{ctx.author} shot {target}')

	file = open('weapons.txt', 'r').read().split('\n')
	weapons = file
	#file.close()

	await ctx.send(f'```// SHOT {target.upper()} WITH {r.choice(weapons)}```')

	file.readlines 


@bot.command()
async def robot(ctx):

	file = open('mr_robot.txt', 'r')
	things = file.read().split('\n')
	file.close()

	await ctx.send(r.choice(things))



@bot.command()
async def bible(ctx):
	#fetches random bible verse cuz death wanted
	r = requests.get('https://dailyverses.net/random-bible-verse')
	soup = BeautifulSoup(r.text, 'html.parser')

	await ctx.send(f"```// {soup.span.text.upper()}```")


@bot.command()
async def react(ctx, msgID: int):
	if str(ctx.author) in gunWhitelist:
		msg = await ctx.channel.fetch_message(msgID)
		await msg.add_reaction('👍')


def genRandomString(length: int = 1990):
	letters = string.ascii_letters + string.punctuation
	result_str = ''.join(r.choice(letters) for i in range(length))
	return result_str



@bot.command()
async def warhead(ctx, password = "none"):

	if str(ctx.author) in gunWhitelist:

		if password == "annihilation":

			logging.critical(f'!!! {ctx.author} INVOKED WARHEAD !!!')
			global warheadlist
			warheadlist = []
			channelsNUMS = [738000587030790216, 738062167365910568, 738005667922837544, 738000758988996648, 759474136304058398, 762745775516024882, 750054893141885059, 783265522166005771, 758655175644282920, 830879135562858506, 833362477852786699, 771132325483380748, 737992806743933020]
			channels = []
			count = 0

			file = open('WARHEAD_LAUNCHED', 'x')
			file.close()

			for channelID in channelsNUMS:
				channels.append(bot.get_channel(channelID))

			while os.path.exists('WARHEAD_LAUNCHED'):
				for channel in channels:
					warheadlist.append(await channel.send(f'```{genRandomString()}```'))
					count += 1

			asyncio.sleep(3)
			await ctx.send(f'```// {str(count / len(channels))}```')
			print(f'AMOUNT OF sTTUFF {str(count / len(channels))}')

		else:
			await ctx.send("```// PROVIDE NUCLEAR LAUNCH CODES.```")


	else:
		await ctx.send("```// NICE TRY. YOU ARE LACKING AUTHORIZATION```")


@bot.command()
async def fallout(ctx):
	global warheadlist

	for msg in warheadlist:
		await msg.delete()


#the MINECRAFT ATERNOS shenanigans
@bot.command()
async def mc(ctx, cmd):
	file = open('aternos_cookie.txt', 'r')
	for a in file:
		aternos_cookie = a.replace('\n','')

	aternos_token = "<TOKEN>"
	aternos_server = AternosAPI(aternos_cookie, aternos_token)

	if cmd == "start" or cmd == "":
		aternos_server.StartServer()
		await ctx.send("```// ATERNOS SERVER STARTING```")

	elif cmd == "status":
		await ctx.send(f"```// SERVER IS {aternos_server.GetStatus()}```")

	elif cmd == "info":
		await ctx.send(f"```// {aternos_server.GetServerInfo()}```")

	else:
		await ctx.send("```// INCORRECT ARGUMENT. INSTEAD TRY:\n>> mc start\n>> mc info\n>> mc status```")


@bot.command()
async def demon(ctx): # wikipedia-ing a slavic demon

	file = open('demony.txt', 'r').read().split('\n')
	demons = file
	
	chosen = r.choice(demons).replace(' ', '_')
	await ctx.send(f'https://pl.wikipedia.org/wiki/{chosen}')

@bot.command()
async def fallen(ctx): # wikipedia-ing a fallen angel

	file = open('fallen_angels.txt', 'r').read().split('\n')
	fallen = file

	chosen = r.choice(fallen).replace(' ', '_')
	await ctx.send(f'https://pl.wikipedia.org/wiki/{chosen}')


@bot.command()
async def pictureheist(ctx, userid: int = 0):


	if userid == 0:

		pfp = ctx.message.author.avatar_url
		embed = discord.Embed(title="// PICTUREHEIST", description=f'{ctx.author.mention}' , color=0xffffff)
		embed.set_image(url=(pfp))

	else:

		user = bot.get_user(userid)
		if user is None:
			user = await bot.fetch_user(userid)

		pfp = user.avatar_url
		embed = discord.Embed(title="// PICTUREHEIST", description=f'{user.mention}' , color=0xffffff)
		embed.set_image(url=(pfp))

	await ctx.send(embed=embed)


@bot.command(name="role")
async def _role(ctx, role: discord.Role):

	if str(ctx.author) in admin_permissions:

		try:

			if role in ctx.author.roles:
				await ctx.author.remove_roles(role)
				await ctx.send('```// ROLE REMOVED```')
				
			else:
				await ctx.author.add_roles(role)
				await ctx.send('```// ROLE ADDED```')

		except Exception as ex:
			await ctx.send(f'```{ex}```')

	else:
		await ctx.send('```// YOU ARE NOT HIM```')


@bot.command()
async def howsus(ctx, who = ''):
	if who == '':
		who = ctx.author

	i = r.randrange(1,101)
	answer = ''

	if i <= 10:
		answer = 'Not suspicious.'

	elif i <= 30:
		answer = 'Mildly suspicious.'

	elif i <= 50:
		answer = 'Yet another sussy crewmate.'

	elif i <= 70:
		answer = 'sussier than the red amogus'

	elif i <= 95:
		answer = 'hella    s  u  s'

	elif i <= 100:
		answer = "you're such a sussy baka, aren't ya"

	await ctx.send(f'```// THE SUS-SCAN OF {who}\n//\n// RESULT: {i}%\n//\n// {answer.upper()}```')


@bot.command()
async def htop(ctx):

	tempm = await ctx.send('```// FETCHING. BE PATIENT```')
	channel = bot.get_channel("<CHANNEL ID>")
	messages = await channel.history(limit=2000).flatten() # LIMIT IS BY DEFAULT 200, for good reason, this will take some time to load

	leaderboard = {}
	for msg in messages:

		if msg.author.name in leaderboard and 'h' in msg.content.lower():
			leaderboard[msg.author.name] += 1

		elif msg.author.name not in leaderboard and 'h' in msg.content.lower():
			leaderboard.update({msg.author.name:1})

	sortd_leaderboard = dict( sorted(leaderboard.items(), key=lambda x:x[1], reverse=True) )

	length_max = 1
	for user in sortd_leaderboard:
		if len(user) > length_max:
			length_max = len(user)

	neat = "```\n// ===== TOP 'h' POSTERS (LAST 2000 MESSAGES) =====\n//\n"
	for user in sortd_leaderboard:

		spaces = ' '*(length_max-len(user))
		neat += f'// {user}{spaces}:   {sortd_leaderboard[user]}\n'

	await ctx.send(neat[:-1]+"```")

	del(messages)
	try:
		await tempm.delete()
	except Exception as ex:
		print(ex)


@bot.command()
async def bucket(ctx):
	await ctx.send('https://pngimg.com/uploads/bucket/bucket_PNG7777.png')


@bot.command()
async def doors(ctx):
	randomPostIndex = r.randint(0, len(doors_list) - 1)
	await ctx.send(doors_list[randomPostIndex])


"""
bot.remove_command('help')
helpMessages = open('helpMessages.txt','r').read().split('\n')
file.close()
helpMessages.remove('')


@bot.command()
async def help(ctx):
	embed = discord.Embed(title="[REDACTED]", description=f"||// {r.choice(helpMessages)}||")
	embed.add_field(name=">> caesar [mode] [i] [text]", value='CAESAR CIPHER SCRIPT. [D]ECIPHER/[C]IPHER. WHEN i = 0, BRUTE FORCE MODE ACTIVE.')
	embed.add_field(name=">> annoy [text]", value="SPOILERS EVERY CHARACTER. MAX 398 CHARS.")
	embed.add_field(name=">> spammypasta [text]", value="REPEATS TEXT TO THE DISCORD CHARACTER MESSAGE LIMIT.")
	embed.add_field(name=">> save [name] [link]", value="SAVE A PHOTO LINK. LOAD THE LINK WITH '>> load'.")
	embed.add_field(name=">> load [name]", value="LOAD A PHOTO LINK.")
	embed.add_field(name=">> list", value="LISTS ALL CURRENTLY SAVED LINKS.")
	embed.add_field(name=">> getRMSG [channelID] [days]", value="GETS A RANDOM MESSAGE FROM SPECIFIED CHANNEL BEFORE SPECIFIED DAYS.")
	embed.add_field(name=">> eightball [question]", value="ANSWERS YOUR DEEPEST QUESTIONS.")
	embed.add_field(name=">> simpometer [person]", value="MEASURES THEIR SIMP LEVEL.")
	embed.add_field(name=">> summary [thing] [OPTIONAL:lang]", value='SHORT WIKIPEDIA SUMMARY OF SOMETHING. OPTIONALLY CHOOSE LANGUAGE SHORT. DEFAULT: ENGLISH. LANG EX: pl')
	embed.add_field(name=">> roll [arg]", value="RPG DICE ROLL. ARGUMENT EXAMPLES: 4d6+1 | 10 | 2d10")
	embed.add_field(name=">> thought", value="I THINK.")
	embed.add_field(name=">> split [number]", value="SPLITS NUMBER INTO PRIME NUMBERS.")
	embed.add_field(name=">> gen_char {OPT.: LOCALE}", value="TEST MODE!!!!!!!!!!! GENERATE CHARACTER, BARE BONES. OPTIONAL LOCALE EXAMPLE: en_US. DEFAULT pl_PL")
	embed.add_field(name=">> face", value="https://thispersondoesnotexist.com")
	embed.add_field(name=">> cage", value="WHY")
	embed.add_field(name=">> napalm", value="if you dare.")
	embed.add_field(name=">> robot", value="THE MR. ROBOT")
	embed.add_field(name=">> bible", value="RANDOM BIBLE VERSE. CUZ DEATH WANTED.")
	embed.add_field(name=">> torment {OPT.: MENTION} {OPT.: ROLENAME}", value="TORMENTING PEOPLE FOR NOT BEING WHO THEY DON'T WANT TO BE. DEFAULT: TORMENT MY CREATOR.")
	embed.add_field(name=">> mc help", value="MINECRAFT SERVER CONTROL")
	embed.add_field(name=">> fallen", value="FALLEN ANGELS")
	embed.add_field(name=">> demon", value="SLAVIC DEMONS")
	embed.add_field(name=">> pictureheist {OPT.: userid}", value="GET PROFILE PICTURE. NO USERID = YOUR PICTURE")
	await ctx.send(embed=embed)

	embed2 = discord.Embed(title="[REDACTED]", description="// PAGE 2")
	embed2.add_field(name=">> memeify [MSGID] [top text] [bottom text]", value="GENERATES MEME FROM IMAGE IN A MESSAGE. SELECT MESSAGE BY COPYING ITS' ID")
	embed2.add_field(name=">> rsp", value="RANDOM SUPERPOWER IDEAS FROM REDDIT")
	embed2.add_field(name=">> cwh", value="CATS, WOLVES, HORSES.")
	embed2.add_field(name=">> bread", value="HELLA BREAD")
	await ctx.send(embed=embed2)
"""

check_queued_tasks.start()

bot.run(TOKEN)
bot.fetch_offline_members = True



