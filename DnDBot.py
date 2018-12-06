'''
DnD Discord Bot v1.0
Adam Crick

Version Date: November 20, 2018

Purpose:
To facilitate the following to a DnD Discord Server
* Able to create roles per channel
* Able to whitelist/blacklist channels to work in DONE
* Able to allow anyone to add themselves to a group DONE
* Able to set an individual (or maybe multiple individuals) as allowed to broadcast to the group
* Possibly allow for automated messages to a group
'''

import discord
from discord.ext import commands
import datetime
import os
import json

version = "1.1"

config_dict = {}

with open('config.json') as file:
    config_dict=json.load(file)

TOKEN = config_dict["bot_key"] #Bot's token

client = commands.Bot(command_prefix = '!') #what prefix for the bot

#If the channels folder doesn't exist, make it in the current working directory
#chanfolder = os.getcwd() + "\\channels"
#if not os.path.exists(chanfolder):
#    os.makedirs(chanfolder)

#when ready
@client.event
async def on_ready():
    print("dndbot v" + version + " has started on " + str(datetime.datetime.now()))


#detects when message is sent into the server
@client.event
async def on_message(message):

    print(str(datetime.datetime.now()) + " | " + str(message.author) + " Message: " + message.content)
    await client.process_commands(message)

#Adds a channel
@client.command(pass_context=True)
async def addcampaign(ctx):
    '''
        Adds a campaign role for the current channel.
        Usage: "!addcampaign
    '''

    if isBlacklisted(ctx.message.channel.name):
        return
    author = ctx.message.author
    role_name = ctx.message.channel.name

    role_list = []

    for role in ctx.message.server.roles:
        role_list.append(role.name)

    # check if that role already exists
    if role_name not in role_list:# if the role doesn't exist
        # create the role
        await client.create_role(author.server, name=role_name, colour=discord.Colour(0x000000), mentionable = True)
        await client.say("The " + ctx.message.channel.name + " campaign role has been created. Use '@" +
                         ctx.message.channel.name + "' to tag all users in this campaign.")
    else:
        await client.say("Sorry, this campaign already exists.")

    '''
    channeldict = {
        ctx.message.author.mention : "dm"
    }

    with open(os.getcwd() + "\\channels\\" + ctx.message.channel.name + ".json", 'w') as jsonFile:
        json.dump(channeldict, jsonFile)

    print(str(datetime.datetime.now()) + " | " + str(ctx.message.author) + " Command(Add Channel): "
          + ctx.message.channel.name)
    await client.say("Campaign " + ctx.message.channel.name + " has been started with " + ctx.message.author.mention
                     + "as the DM.")
    '''

#Deletes campaign role from server
@client.command(pass_context = True)
async def removecampaign(ctx):
    '''
            Removes a campaign role for the current channel.
            Usage: "!removecampaign
    '''
    if isBlacklisted(ctx.message.channel.name):
        return

    author = ctx.message.author
    role_name = ctx.message.channel.name

    role_list = []

    for role in ctx.message.server.roles:
        role_list.append(role.name)

    if role_name in role_list:
        for role in ctx.message.server.roles:
            if role_name == role.name:
                thisrole = role

        await client.delete_role(ctx.message.server, thisrole)
        await client.say("Campaign has been deleted from this server.")
    else:
        await client.say("Sorry, this channel does not have a campaign.")

#Adds yourself to the current channel's campaign role
@client.command(pass_context=True)
async def addplayer(ctx):
    '''
            Adds you to the current channel's campaign role
            Usage: "!addplayer
    '''
    if isBlacklisted(ctx.message.channel.name):
        return
    author = ctx.message.author
    role_name = ctx.message.channel.name

    for role in ctx.message.server.roles:
        if role.name == role_name:
            if role not in author.roles:
                await client.add_roles(author, role)
                await client.say(author.mention + " has been added to the " + role_name + " campaign.")
            else:
                await client.say("Sorry, you already belong to this campaign.")
            return

    await client.say("Sorry, this channel does not have a campaign.")

#Removes yourself from a campaign
@client.command(pass_context =True)
async def removeplayer(ctx):
    '''
                Removes you from the current channel's campaign role
                Usage: "!removeplayer
    '''
    if isBlacklisted(ctx.message.channel.name):
        return
    author = ctx.message.author
    role_name = ctx.message.channel.name

    role_list = []

    for role in author.roles:
        role_list.append(role.name)

    if role_name in role_list:
        for role in author.roles:
            if role_name == role.name:
                thisrole = role

        await client.remove_roles(author, thisrole)
        await client.say("Removed " + author.mention + " from the campaign.")
    else:
        await client.say("Sorry, user is not a part of this campaign.")

#Blacklists channel that command was uttered in.
@client.command(pass_context=True)
async def blacklist(ctx):
    '''
                Blacklists the current channel from bot's commands.
                Usage: "!blacklist
    '''
    if isBlacklisted(ctx.message.channel.name):
        return

    #Get the name of the channel, add it to blacklist.
    channel = ctx.message.channel
    blacklistfile = open("blacklist.txt", "a+")

    blacklistfile.write(channel.name + "\n")
    blacklistfile.close()

    print(str(datetime.datetime.now()) + " | " + str(ctx.message.author) + " Command(Blacklist): " + channel.name)

    await client.say("Channel " + channel.name + " has been blacklisted from bot commands.")


#whitelists a channel
@client.command(pass_context=True)
async def whitelist(ctx):
    '''
                Allows the current channel to use bot commands
                Usage: "!whitelist
    '''
    channel = ctx.message.channel
    print(channel.name)
    if isBlacklisted(channel.name):
        blacklistfile = open("blacklist.txt", "a+")
        lines = blacklistfile.readlines()
        blacklistfile.close()

        newLines = []
        for line in lines:
            newLines.append(' '.join([word for word in line.split() if word != channel]))

        blacklistfile = open("blacklist.txt", 'w')
        for line in lines:
            blacklistfile.write("{}\n".format(line))
        blacklistfile.close()


        await client.say("Channel " + channel.name + " is no longer blacklisted.")

    else:
        await client.say("Channel " + channel.name + " is not blacklisted.")
        return


#Checks if channel is blacklisted
def isBlacklisted(channel):
    blacklistfile = open("blacklist.txt", "a+")
    blacklistfile.seek(0)

    if channel in blacklistfile.read():
        blacklistfile.close()
        return True
    else:
        blacklistfile.close()
        return False



client.run(TOKEN)

