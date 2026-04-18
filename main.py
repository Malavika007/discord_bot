import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random
import asyncio

from groq import Groq
load_dotenv()

token = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8',mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

key = os.getenv('API_KEY')
groq_client = Groq(api_key=key)

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
    await ctx.send("Alright you have 10 tries to guess the number im thinking of. Go on")

    chance = 10
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
    

@bot.command()

async def ask(ctx,*,question):
    await ctx.send("Thinking...")

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role":"system","content":"you are a friendly discord bot",},
                {"role":"user","content":question}
            ]
        )

        reply = response.choices[0].message.content
        await ctx.send(reply[:2000])
        
    except Exception as e:
        await ctx.send("error")
        print(e)


bot.run(token, log_handler=handler, log_level=logging.DEBUG)
