# Work with Python 3.6
import praw
import discord
from discord.ext.commands import Bot
from discord import Game
import asyncio

TOKEN = 'DISCORD_TOKEN'
client = Bot(command_prefix='!')
memechannel = 0
run = False

############################### REDDIT #########################################

reddit = praw.Reddit(client_id='REDDIT_ID',
                     client_secret='REDDIT_SECRET',
                     user_agent='REDDIT_USERNAME')

subreddit = reddit.subreddit('me_irl')

############################### DISCORD ########################################

## REMOVES DEFAULT HELP MESSAGE
client.remove_command('help')

## COMMAND TO DISPLAY HELP PAGE
@client.command(name='help',
                description='displays the help page',
                aliases=['h'],
                pass_context=True)
async def help(ctx):
    await client.say('i\'ve sent u a private help message!')
    author = ctx.message.author

    embed=discord.Embed(title='help message',
                        color=0x008080,
                        url='http://trumpdonald.org')
    embed.set_thumbnail(url='https://png.icons8.com/help/color/200')
    embed.add_field(name=client.command_prefix + 'help',
                    value='sends this message',
                    inline=True)
    embed.add_field(name=client.command_prefix + 'prefix',
                    value='let\'s you change the prefix',
                    inline=True)
    embed.add_field(name=client.command_prefix + 'clear',
                    value='deletes a specific amount of messages',
                    inline=True)
    embed.add_field(name=client.command_prefix + 'setchannel',
                    value='starts automatic meme broadcast',
                    inline=True)
    embed.add_field(name=client.command_prefix + 'post',
                    value='posts the hottest submission',
                    inline=True)
    embed.add_field(name=client.command_prefix + 'stop',
                    value='stops automatic meme broadcast',
                    inline=True)
    embed.set_footer(text="very helpful right?")

    await client.send_message(author, embed=embed)

## SIMPLE COMMAND TO TEST IF THE BOT IS UP AND RUNNING
@client.command(name='ping',
                description='tests the ping!',
                aliases=[],
                pass_context=True)
async def ping(ctx):
    await client.say(ctx.message.author.mention + ' pong')

## COMMMAND TO CHANGE THE BOT PREFIX
@client.command(name='prefix',
                description='lets u change the prefix!',
                aliases=['p'],
                pass_context=True)
async def prefix(ctx, newprefix='!'):
    isAuthor = ctx.message.author.server_permissions.administrator
    if isAuthor:
        client.command_prefix = newprefix
        await client.say('prefix is now: ' + client.command_prefix)
        await client.change_presence(game=Game(name=client.command_prefix + "help"))
    else:
        await client.say('you don\'t have admin rights')

## COMMAND TO DELETE MESSAGES
@client.command(name='clear',
                description='deletes messages',
                aliases=['c'],
                pass_context=True)
async def clear(ctx, amount=100):
    channel = ctx.message.channel
    isAuthor = ctx.message.author.server_permissions.administrator
    if isAuthor:
        messages = []
        async for message in client.logs_from(channel, limit=int(amount)):
            messages.append(message)
        await client.delete_messages(messages)
        await client.say( str(amount) + ' messages deleted')
    else:
        await client.say('you don\'t have admin rights')

## COMMAND TO SET MEMECHANNEL
@client.command(name='setchannel',
                description='sets meme channel!',
                aliases=['sc'],
                pass_context=True)
async def setchannel(ctx):
    global run
    run = True
    tmp = 0
    memechannel = ctx.message.channel
    isAuthor = ctx.message.author.server_permissions.administrator
    if isAuthor:
        await client.say('this is the new memechannel!')
        while not client.is_closed and run == True:
            for submission in subreddit.hot(limit=2):
                if submission.id != '80ib9u' and submission.id != tmp:
                    await client.send_message(memechannel, submission.title)
                    await client.send_message(memechannel, submission.url)
                    tmp = submission.id
            print('subreddit visited!')
            await asyncio.sleep(400)
    else:
        await client.say('you don\'t have admin rights')

## COMMAND TO STOP POST BOT (SEE SETCHANNEL)
@client.command(name='stop',
                description='stops automatic meme broadcast',
                aliases=[],
                pass_context=True)
async def stop(ctx):
    global run
    isAuthor = ctx.message.author.server_permissions.administrator
    if isAuthor:
        if run == True:
            await client.say('you stopped the postbot')
            run = False
            print("run: " + str(run))
        else:
            await client.say('postbot isn\'t even running')
            print('run now is: ' + str(run))
    else:
        await client.say('you don\'t have admin rights')

## COMMAND TO POST THE HOTTEST POST IN ME_IRL
@client.command(name='post',
                description='posts hottest post from r/me_irl!',
                aliases=[],
                pass_context=True)
async def post(ctx):
    for submission in subreddit.hot(limit=2):
        if submission.id != '80ib9u':
            await client.say(submission.title)
            await client.say(submission.url)

## START EVENT
@client.event
async def on_ready():
    await client.change_presence(game=Game(name=client.command_prefix + "help"))
    print("logged in as " + client.user.name)

client.run(TOKEN)