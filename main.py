import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random
import asyncio

load_dotenv()

token = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8',mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents = intents)

@bot.event
async def on_ready():
    print(f"we are ready to go in, {bot.user.name}")


@bot.event 
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "hehe" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} - dont use that word! ")
    
    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f"hello {ctx.author.mention}!")

@bot.command()
async def guess(ctx):
    await ctx.send("Alright you have 5 tries to guess the number im thinking of. Go on")

    chance = 5
    answer = random.randint(1,100)
    print(answer)

    def is_valid(m):
        return m.author == ctx.author and m.channel == ctx.channel

    while chance > 0:
        try:
            guess = await bot.wait_for('message',check=is_valid, timeout=20)
        except asyncio.TimeoutError:
            return await ctx.send(f"sorry you took too long to respond! the answer was {answer}")  

        if guess.content.isdigit():

            user_guess = int(guess.content)

            if user_guess == answer:
                await ctx.send("correct")
                break
            elif user_guess > answer:
                await ctx.send("wronggg too high")
            else:
                await ctx.send("wronggg too low")
        else:
            await ctx.send("booo send a number dumbass")
        
        chance -= 1

    await ctx.send(f"it was {answer} btw")
    



bot.run(token, log_handler=handler, log_level=logging.DEBUG)
