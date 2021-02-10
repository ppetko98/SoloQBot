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
    print('Vuelta del main')


@bot.command(name='leaderboard', help='Prints the actual leaderboard', pass_context=True)
async def leaderboard(ctx):
    msg_id = await ctx.send("Cargando el leaderboard de SoloQ...")
    # msg_id = msg_id.id
    table = statsLoL.get_table()
    msg = ''
    for i, r in table.iterrows():
        msg += f'{i}. {r["Alias"]} *\"{r["Summoner"]}\"*: {r["Division"]} {r["Rank"]} {r["LPs"]} PLs\n'
    await msg_id.edit(content=msg)


@tasks.loop(seconds=20)
async def update_leaderboard():
    print('Llamada a update')
    load_leaderboard()
    # check for message
    print('Ha pasado el load')
    channel = bot.get_channel(CHANNEL_ID)
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    global board_msg
    if board_msg is not None:
        with open('leaderboard.png', 'rb') as img:
            await board_msg.edit(content="SoloQ Leaderboard at {}".format(timestamp),
                           file=discord.File(img, 'leaderboard-{}.png'.format(timestamp)))
    else:
        with open('leaderboard.png', 'rb') as img:
            msg = await channel.send(content="SoloQ Leaderboard at {}".format(timestamp),
                                     file=discord.File(img, 'leaderboard-{}.png'.format(timestamp)))
            board_msg = msg
    print('Mensaje enviado')


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
    # await send_leaderboard()
    await update_leaderboard.start()


bot.run(TOKEN)

