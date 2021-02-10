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


def load_leaderboard():
    statsLoL.main()


@bot.command(name='leaderboard', help='Prints the actual leaderboard', pass_context=True)
async def leaderboard(ctx):
    msg_id = await ctx.send("Cargando el leaderboard de SoloQ...")
    # msg_id = msg_id.id
    table = statsLoL.get_table()
    msg = ''
    for i, r in table.iterrows():
        msg += f'{i}. {r["Alias"]} *\"{r["Summoner"]}\"*: {r["Division"]} {r["Rank"]} {r["LPs"]} PLs\n'
    await msg_id.edit(content=msg)


@tasks.loop(hours=1.0)
async def update_leaderboard():
    load_leaderboard()
    # check for message
    channel = bot.get_channel(CHANNEL_ID)
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    global board_msg
    with open('leaderboard', 'rb') as img:
        if board_msg is not None:
                await board_msg.delete()
                msg = await channel.send(content="SoloQ Leaderboard at {}".format(timestamp),
                               file=discord.File(img, 'leaderboard-{}.png'.format(timestamp)))
                board_msg = msg
                print('Leaderboard updated')
        else:
                msg = await channel.send(content="SoloQ Leaderboard at {}".format(timestamp),
                                         file=discord.File(img, 'leaderboard-{}.png'.format(timestamp)))
                board_msg = msg
                print('Leaderboard sent')


@bot.event
async def on_ready():
    channel_liga = bot.get_channel(CHANNEL_ID)
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print('Connected to ', guild)
    messages_liga = await channel_liga.history().flatten()
    if messages_liga:
        for m in messages_liga:
            print(m.id, ' borrado')
            await m.delete()
    await update_leaderboard.start()


bot.run(TOKEN)

