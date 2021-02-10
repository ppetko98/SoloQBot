import discord
from discord.ext import commands, tasks
import statsLoL
import json
from time import sleep


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
CHANNEL_ID = ''
# client = discord.Client()

load_conf()

bot = commands.Bot(command_prefix=COMMAND)


@bot.command(name='leaderboard', help='Prints the actual leaderboard', pass_context=True)
async def leaderboard(ctx):
    await ctx.send("Aqui deberia meter la tabla de puntuaciones")


@tasks.loop(hours=1)
async def update_leaderboard():
    channel = bot.get_channel(CHANNEL_ID)
    msg = await channel.send("leaderboard")
    leaderboard_message_id = msg.id


@bot.event
async def on_ready():
    # update_leaderboard.start()
    channel_liga = bot.get_channel(CHANNEL_ID)
    messages_liga = await channel_liga.history().flatten()
    # content = get_table()
    if messages_liga:
        for m in messages_liga:
            # print('{}\t{}\t{}\n'.format(m.id, m.content, m.author))
            await m.delete()
    # await update_table()

    guild = discord.utils.get(bot.guilds, name=GUILD)
    print('Bot is connected to: ', guild)


bot.run(TOKEN)

