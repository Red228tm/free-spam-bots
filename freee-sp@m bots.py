import discord  
import asyncio   
from discord.ext import commands 
import json 
import aiohttp

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

async def send(userid, token):
    payload = {
        "content": f"freee-dm bots"
    }
    u = 'https://discord.com/api/v9/users/@me/channels'
    d = {
        "recipients": [f"{userid}"]
    }

    header = {
        "authorization": f"Bot {token}"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url=u, json=d, headers=header) as r:
                jss = await r.json()
                for _ in range(100):
                    url = f'https://discord.com/api/v9/channels/{jss["id"]}/messages'
                    async with session.post(url, data=payload, headers=header) as r:
                        pass
    except Exception as e:
        print(f'[ - ] Error: {e}')


@client.command()
@commands.cooldown(1, 120, commands.BucketType.user)
async def spam(ctx, user:discord.Member=None):
    if user is None:
        await ctx.author.send(embed=discord.Embed(title='Укажи пользователя для спама в лс!'))
    else:
        try:
            await user.send('кайф')
        except discord.Forbidden:
            await ctx.send('Пользователь закрыл лс, не могу делать спам!')
            return
        await ctx.author.send(embed=discord.Embed(title=f'Спам пользователю {user} запущен'))
        with open('tokens.txt', 'r') as f:
            tokens = f.readlines()
        tasks = [asyncio.create_task(send(userid=str(user.id), token=token.rstrip())) for token in tokens]
        await asyncio.gather(*tasks)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(embed=discord.Embed(title=f'{ctx.author}, Пожалуйста, повтори попытку через {round(error.retry_after, 2)} секунд'))
    elif isinstance(error, commands.CommandInvokeError):
        original = error.original
        if isinstance(original, discord.errors.HTTPException) and original.code == 429:
            await asyncio.sleep(original.retry_after)
            await ctx.reinvoke()
        else:
            raise error

client.run('сюда токен')