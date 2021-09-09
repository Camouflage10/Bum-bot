import pandas as pd
import matplotlib.pyplot as plt
import discord
import os
from replit import db
from discord.ext import commands
from webserver import keep_alive
#make bum object string-member @ and int bumpoints
bums = []


#totalCol=[]
#nameCol=[]
#dateCol=[]
#addedCol=[]
#data=pd.dataframe()
class bum:
    def __init__(self, name):
        self.name = str(name)
        self.points = 0

    def setpoints(self, num):
        self.points = num

    def addpoints(self, num):
        self.points = self.points + num

    def subpoints(self, num):
        self.points = self.points - num

    def printScore(self):
        return self.name + ": " + (str(self.points))


def isCopy(name):
    for b in bums:
        if (b.name == name):
            return True
        else:
            return False


def addPlayer(name):
    if not isCopy(name):
        bums.append(bum(name=name))
        saveBums()


def saveList(key, lis):
    if key in db.keys():
        db[key] = lis


def saveBums():
    print("saving bums")
    global bums
    if "names" in db.keys() and "points" in db.keys():
        names = []
        points = []
        for i in range(0, len(bums)):
            names.append(bums[i].name)
            points.append(bums[i].points)
        db["names"] = names
        db["points"] = points


def dbBums():
    global bums
    if "names" in db.keys() and "points" in db.keys():
        names = db["names"]
        points = db["points"]
        for i in range(0, len(names)):
            bums.append(bum(name=names[i]))
            bums[i].setpoints(points[i])
    else:
        db["names"] = []
        db["points"] = []


def scoreboard():
    s = ""
    for b in bums:
        s = s + b.printScore() + "\t"
    return s


def help():
    return "!bum initial command \nadd me: adds the author to the list of bums\nscore: shows list of bums and their respective bum points\n(+/-)n @bum: adds or subtracts n from the bum mentioned\nset n @bum: sets thats bums total to n\nBums can not change your own bum points. Points must be dished by a different bum\npie: sends a pie chart of the current bum points\nbar: sends a bar graph of the current bum points\n----------------------------"


def pie():  #returns path of saved fig
    global bums
    names = []
    points = []
    for i in range(0, len(bums)):
        if (bums[i].points > 0):
            points.append(bums[i].points)
            names.append(bums[i].name)
    fig1, ax1 = plt.subplots()
    ax1.pie(points, labels=names, autopct='%1.1f%%')
    ax1.axis('equal')
    plt.savefig("images/pie.png")
    plt.close()
    return discord.File('images/pie.png')


def bar():  #returns path of saved fig
    global bums
    names = []
    points = []
    for i in range(0, len(bums)):
        points.append(bums[i].points)
        names.append(bums[i].name)
    fig1, ax1 = plt.subplots()
    ax1.barh(names, points)
    ax1.axis('equal')
    plt.savefig("images/bar.png")
    plt.close()
    return discord.File('images/bar.png')


def line():  #returns path of saved fig
    return


def getBumIndex(name):
    for i in range(0, len(bums)):
        if bums[i].name == name:
            return i
    return -1


# make df that has datetime, name , points added/sudtracted, points
#graph line
#graph pie
#graph hist @bum
#head/tail
description = "desc"
intent = discord.Intents.default()
intent.members = True
bot = commands.Bot(command_prefix='!bum',
                   description=description,
                   intent=intent)


#startup command
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    dbBums()
    #make it work later


# for guild in bot.guilds:
# for member in guild.members:
# print(member.name+' ')
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if (message.content.startswith('!bum')):
        if ('add me' in message.content):
            if not isCopy(message.author.name):
                addPlayer(message.author.name)
                await message.channel.send(message.author.name + " bum added")
            else:
                await message.channel.send(message.author.name +
                                           " bum already exists u bum")
                # add a bum point
        elif ('score' in message.content):
            await message.channel.send(scoreboard())
        elif ('help' in message.content):
            await message.channel.send(help())
        elif len(message.mentions) != 0:  #needs a mention
            index = getBumIndex(message.mentions[0].name)
            if index == -1:
                await message.channel.send("bum does not exist")
            elif message.mentions[0] == message.author:  #change before live-
                await message.channel.send(
                    "you can not change your own bum points\n get another bum to do it"
                )

            elif ('+' in message.content):
                s = message.content
                s = s[s.find('+') + 1:]
                s = s[:s.find(' ')]
                bums[index].addpoints(int(s))
                await message.channel.send(bums[index].name + " now has " +
                                           str(bums[index].points) +
                                           " bum points")
            elif ('-' in message.content):
                s = message.content
                s = s[s.find('-') + 1:]
                s = s[:s.find(' ')]
                bums[index].subpoints(int(s))
                if bums[index].points < 0:
                    await message.channel.send(
                        "u can't have negitive bum points bum")
                    bums[index].setpoints(0)
                    # give author bum points
                await message.channel.send(bums[index].name + " now has " +
                                           str(bums[index].points) +
                                           " bum points")

            elif ('set ' in message.content):
                s = message.content
                s = s[s.find('set ') + 4:]
                s = s[:s.find(' ')]
                bums[index].setpoints(int(s))
                await message.channel.send(bums[index].name + " now has " +
                                           str(bums[index].points) +
                                           " bum points")
            saveBums()
        elif (' pie' in message.content):
            await message.channel.send(file=pie())
        elif (' bar' in message.content):
            await message.channel.send(file=bar())


keep_alive()
bot.run(os.getenv('TOKEN'))
