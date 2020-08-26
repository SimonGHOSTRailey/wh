import discord
import asyncio
from discord.ext import commands
import os

bot = commands.Bot(command_prefix = '$')
bot.remove_command('help')

@bot.event
async def on_ready():
  print('Бот подключился!')
  await bot.change_presence(activity= discord.Activity(name= 'пространственно-временной континуум', type= discord.ActivityType.playing), status= discord.Status.online)

@bot.command()
@commands.cooldown(3, 300, commands.BucketType.user)
async def report(ctx, member:discord.Member=None, *, arg=None):
    message = ctx.message
    channel = ctx.guild.get_channel (716392845006864444)    
    if member == None:
        await ctx.send(embed=discord.Embed(description='Укажите пользователя!', color=discord.Color.red()))
    elif arg == None:
        await ctx.send(embed=discord.Embed(description='Укажите причину жалобы!', color=discord.Color.red()))
    else:
        emb = discord.Embed(title=f'Жалоба на пользователя {member.id}', color=discord.Color.blue())
        emb.add_field(name='ID автора жалобы:', value=f'*{ctx.message.author.id}*')
        emb.add_field(name='Причина:', value='*' +arg + '*')
        emb.add_field(name='ID жалобы:', value=f'{message.id}')
        await channel.send(embed=emb)
        await ctx.author.send('✅ Ваша жалоба успешно отправлена!')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send(embed=discord.Embed(description='Неверный аргумент команды!\nОбычно это происходит, когда вы неверно указали юзера.', color=discord.Color.red()))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        
        def TimeExpand(time):
            if time//60 > 0:
                return str(time//60)+' мин. '+str(time%60)+' сек.'
            elif time > 0:
                return str(time)+' сек.'
            else:
                return f"0.1 сек."
        
        cool_notify = discord.Embed(
                title='⏳ Пожалуйста подождите!',
                description = f"Осталось {TimeExpand(int(error.retry_after))}"
            )
        await ctx.send(embed=cool_notify)

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    if member == None: #проверка указан ли пользователь
        member = ctx.author
    embed =discord.Embed(title = f'Аватар пользователя {member.name}')
    embed.set_image(url = f'{member.avatar_url}')
    await ctx.send(embed = embed)

@bot.command(aliases = ['b'])
@commands.has_permissions(ban_members = True)
async def ban (ctx, member: discord.Member, *, reason = None):
    await member.ban(reason = reason)
    await ctx.send(f'{member.mention} был забанен администратором {ctx.author.mention} по причине: *{reason}*')

token = os.environ.get('BOT_TOKEN')

bot.run(str(token))