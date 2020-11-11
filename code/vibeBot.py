import discord
from discord.ext import commands
from discord.utils import get
import time as t
import random as r
import requests, shutil, os
from subprocess import call
import string

file = open('vibeToken.txt', 'r')
for a in file:
    TOKEN = a.replace('\n','')

bot = commands.Bot(command_prefix='>> ')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="your every step"))


alphabet_upper = list(string.ascii_uppercase)
alphabet_lower = list(string.ascii_lowercase)


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




@bot.event
async def on_message(message):
    if 'vibe' in message.content.lower():
        if r.randint(1, 7) == 3:
            await message.channel.send('https://cdn.discordapp.com/attachments/774745923552542780/775781069592199198/852bdc314b0541ab75f4f1598dad2dcb.png')
            t.sleep(5)
            await message.channel.send('https://cdn.discordapp.com/attachments/774745923552542780/775781248546635796/rizhg2qrqqv31.png')

    await bot.process_commands(message)



@bot.command()
async def killswitch(ctx, password):
    if password == "adios":
        await ctx.send('```// i have failed you... again...```')
        exit('KILLSWITCH ACTIVATED')


@bot.command()
async def vibe(ctx):
    # ADD RANDOM VIBING SONG MUSIC BOT REQUESTER yaeah a list of random songs and then asks other bots to play or just add music player
    await ctx.send('```// https://www.youtube.com/watch?v=yAGIqCRnNW4```')


@bot.command()
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
async def memeify(ctx, msgID: int, upper_text, bottom_text):

    # ---- GET FILE LINK ----
    msg = await ctx.fetch_message(msgID)
    image_url = msg.attachments[0].url

    # ---- DOWNLOAD -----
    resp = requests.get(image_url, stream=True)
    local_file = open('local_image.jpg', 'wb')
    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
    resp.raw.decode_content = True
    # Copy the response stream raw data to local image file.
    shutil.copyfileobj(resp.raw, local_file)
    # Remove the image url response object.
    del resp

    # ---- ADD CAPTION ----
    call(['python3', 'memegenSTOLEN.py','local_image', upper_text, bottom_text])

    # ---- SEND READY IMAGE ----
    await ctx.send(file=discord.File('edit.jpg'))

    # ---- REMOVE REMAINING FILES ----
    os.remove('local_image.jpg')
    os.remove('edit.jpg')


@bot.command()
async def annoy(ctx, message):
    if len(message)*5 > 1994:
        await ctx.send('```// MESSAGE TOO LONG. RESTRICT TO 398 CHARACTERS```')
    else:
        out = ''
        for char in message:
            out += f'||{char}||'

        await ctx.send(out)


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
async def list(ctx):
    out = '```\n'
    saved_dict = fileToDict('saved.txt')

    for element in saved_dict:
        out += f'{calcSpaces(element, saved_dict)}{element} - {saved_dict[element]}\n'

    await ctx.send(out + '```')





bot.remove_command('help')
helpMessages = open('helpMessages.txt','r').read().split('\n')
file.close()

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="[REDACTED]", description=f"||// {r.choice(helpMessages)}||")
    embed.add_field(name=">> caesar [mode] [i] [text]", value='CAESAR CIPHER SCRIPT. [D]ECIPHER/[C]IPHER. WHEN i = 0, BRUTE FORCE MODE ACTIVE.')
    embed.add_field(name=">> annoy [text]", value="SPOILERS EVERY CHARACTER. MAX 398 CHARS.")
    embed.add_field(name=">> spammypasta [text]", value="REPEATS TEXT TO THE DISCORD CHARACTER MESSAGE LIMIT.")
    embed.add_field(name=">> save [name] [link]", value="SAVE A PHOTO LINK. LOAD THE LINK WITH '>> load'.")
    embed.add_field(name=">> load [name]", value="LOAD A PHOTO LINK.")
    embed.add_field(name=">> list", value="LISTS ALL CURRENTLY SAVED LINKS.")

    await ctx.send(embed=embed)


bot.run(TOKEN)

