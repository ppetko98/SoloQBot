import discord
from discord.ext import commands, tasks
import statsLoL
import json
from time import sleep
from datetime import datetime


def load_conf():
    with open('config.json') as conf:
        global TOKEN, GUILD, COMMAND, CHANNEL_ID
        data = json.load(conf)
        TOKEN = data['discord-token']
        GUILD = data['guild']
        COMMAND = data['prefix']
        CHANNEL_ID = int(data['channel'])


TOKEN = ''
GUILD = ''
COMMAND = '!'
CHANNEL_ID = 0

load_conf()

bot = commands.Bot(command_prefix=COMMAND)

board_msg = None
leaderboard_message_id = ''


async def load_leaderboard():
    await statsLoL.main()


@bot.command(name='leaderboard', help='Prints the actual leaderboard', pass_context=True)
async def leaderboard(ctx):
    table = statsLoL.get_table()
    msg = ''
    for i, r in table.iterrows():
        msg += f'{i}. {r["Alias"]} *\"{r["Summoner"]}\"*: {r["Division"]} {r["Rank"]} {r["LPs"]} PLs\n'
    await ctx.send(msg)


@tasks.loop(hours=6)
async def update_leaderboard():
    await load_leaderboard()
    # check for message
    channel = bot.get_channel(CHANNEL_ID)
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    if board_msg is not None:
        with open('leaderboard.png', 'rb') as img:
            board_msg.edit(content="SoloQ Leaderboard at {}".format(timestamp), file=img)
    else:
        with open('leaderboard.png', 'rb') as img:
            msg = await channel.send(content="SoloQ Leaderboard at {}".format(timestamp),
                                     file=discord.File(img, 'leaderboard-{}.png'.format(timestamp)))
            global leaderboard_message_id
            leaderboard_message_id = msg.id


@bot.event
async def on_ready():
    channel_liga = bot.get_channel(CHANNEL_ID)
    messages_liga = await channel_liga.history().flatten()
    if messages_liga:
        for m in messages_liga:
            await m.delete()
    # await send_leaderboard()
    await update_leaderboard.start()
    # guild = discord.utils.get(bot.guilds, name=GUILD)

bot.run(TOKEN)

