# bot token
# ODA4NzY0OTgyMTk5NTgyNzMx.YCLTFQ.2xtXRG3pEGPe9eWMlicwfjXGkFo
# cargar librerias

import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
import statsLoL
import os
from time import sleep

load_dotenv()

TOKEN = 'ODA4NzY0OTgyMTk5NTgyNzMx.YCLTFQ.2xtXRG3pEGPe9eWMlicwfjXGkFo'
GUILD = 'TILT SQUAD'

# client = discord.Client()
bot = commands.Bot(command_prefix='+')

leaderboard_message_id = 808828682181279794


async def update_table():
    return


@bot.command(name='leaderboard', help='Prints the actual leaderboard', pass_context=True)
async def leaderboard(ctx):
    await ctx.send("Aqui deberia meter la tabla de puntuaciones")


@tasks.loop(hours=1)
async def update_leaderboard():
    channel = bot.get_channel(808638690678407228)
    msg = await channel.send("leaderboard")
    leaderboard_message_id = msg.id


@bot.event
async def on_ready():
    # update_leaderboard.start()
    channel_liga = bot.get_channel(808638690678407228)
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

