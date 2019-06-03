import praw, discord, asyncio, pickle, os, time
from discord.ext import commands
from discord.ext.commands import Bot

token   = ''
bot     = Bot(command_prefix='!')
isSet   = False
tempID  = '80ib9u'
channel = ''

############################### REDDIT #########################################
reddit = praw.Reddit(client_id='',
                     client_secret='',
                     user_agent='',
                     username='',
                     password='')

subreddit = reddit.subreddit('me_irl')

############################### DISCORD ########################################
## PING COMMAND
@bot.command(pass_context=True)
async def ping(ctx):
    await ctx.send(ctx.message.author.mention + ' pong!', delete_after=5)
    await ctx.message.delete(delay=5)

## SET COMMAND TO START BROADCAST
@bot.command(pass_context=True)
@commands.is_owner()
async def set(ctx):
    global isSet
    global channel
    if not isSet:
        isSet = True
        channel = ctx.message.channel
        pickle.dump(channel.id, open("channel.obj", "wb"))
        await ctx.send("Broadcast started!", delete_after=5)
        await ctx.message.delete(delay=5)
        await broadcast()
    else:
        await ctx.send("Already broadcasting!", delete_after=5)
        await ctx.message.delete(delay=5)

## UNSET COMMAND TO STOP BROADCAST
@bot.command(pass_context=True)
@commands.is_owner()
async def unset(ctx):
    global isSet
    if isSet:
        isSet = False
        os.remove("channel.obj")
        await ctx.send("Broadcast stopped!", delete_after=5)
        await ctx.message.delete(delay=5)
    else:
        await ctx.send("Bot is not broadcasting!", delete_after=5)
        await ctx.message.delete(delay=5)

## ERROR HANDLER
@bot.event
async def on_command_error(ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("Insufficient permission!", delete_after=5)
            await ctx.message.delete(delay=5)
        else:
            await ctx.send("Error!", delete_after=5)
            await ctx.message.delete(delay=5)

## START EVENT
@bot.event
async def on_ready():
    global isSet
    global channel
    global tempID
    print("Logged in as " + bot.user.name)
    if os.path.isfile("channel.obj"):
        isSet = True
        channel = bot.get_channel(pickle.load(open("channel.obj", "rb")))
        tempID = pickle.load(open("tempID.obj", "rb"))
        print("Found old session!")
        await broadcast()

## BROADCAST FUNCTION
async def broadcast():
    global tempID
    print("Broadcast started on " + str(channel) + " #" + str(channel.id))
    await bot.change_presence(activity=discord.Game(name='me_irl broadcast'))
    while isSet:
        for submission in subreddit.hot(limit=1):
            if submission.id != tempID:
                print(submission.url)
                reddit.submission(id=tempID).hide()
                await channel.send(submission.url)
                tempID = submission.id
                pickle.dump(tempID, open("tempID.obj", "wb"))
            else:
                print("----- " + str(time.ctime()) + " -----")
        await asyncio.sleep(60)
    print("Broadcast stopped!")
    await bot.change_presence(activity=None)

bot.run(token)
