import praw, discord, asyncio, pickle, os, time
from discord.ext.commands import Bot

token   = ''
bot     = Bot(command_prefix='!')
isSet   = False
tempID  = '80ib9u' ## pinned Reddit Submission, which you'll have to hide separately in reddit
channel = ''

############################### REDDIT #########################################

reddit = praw.Reddit(client_id='',
                     client_secret='',
                     user_agent='',
                     username='',
                     password='')

subreddit = reddit.subreddit('me_irl')

############################### DISCORD ########################################

## SIMPLE COMMAND TO TEST IF THE BOT IS UP AND RUNNING
@bot.command(pass_context=True)
async def ping(ctx):
    await ctx.message.channel.send(ctx.message.author.mention + ' pong', delete_after=10)

## SET COMMAND TO START BROADCAST
@bot.command(pass_context=True)
async def set(ctx):
    isAdmin = ctx.message.author.guild_permissions.administrator
    if isAdmin:
        global isSet
        global channel
        isSet = True
        channel = ctx.message.channel
        pickle.dump(channel.id, open("channel.obj", "wb"))
        await channel.send("Broadcast started!")
        print("Broadcast started on " + str(channel) + " #" + str(channel.id))
        await broadcast()
    else:
        await ctx.message.channel.send(ctx.message.author.mention + " Insufficient Permission!")


## UNSET COMMAND TO STOP BROADCAST
@bot.command(pass_context=True)
async def unset(ctx):
    isAdmin = ctx.message.author.guild_permissions.administrator
    if isAdmin:
        global isSet
        isSet = False
        os.remove("channel.obj")
        await ctx.message.channel.send("Broadcast stopped!")
        print("Broadcast stopped!")
    else:
        await ctx.message.channel.send(ctx.message.author.mention + " Insufficient Permission!")

## START EVENT
@bot.event
async def on_ready():
    global isSet
    global channel
    global tempID
    print("We are logged in as " + bot.user.name)
    if os.path.isfile("channel.obj"):
        isSet = True
        channel = bot.get_channel(pickle.load(open("channel.obj", "rb")))
        tempID = pickle.load(open("tempID.obj", "rb"))
        print("Found old Session!")
        print("Broadcast started on " + str(channel) + " #" + str(channel.id))
        await broadcast()


## BROADCAST FUNCTION
async def broadcast():
    global tempID
    while isSet:
        for submission in subreddit.hot(limit=1):
            if submission.id != tempID:
                print(submission.url)
                reddit.submission(id=tempID).hide()
                await channel.send(submission.url)
                tempID = submission.id
                pickle.dump(tempID, open("tempID.obj", "wb"))
            else:
                print("----------------------")
        await asyncio.sleep(30)

bot.run(token)
