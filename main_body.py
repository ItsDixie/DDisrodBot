import disnake
from disnake import SyncWebhook
from disnake.ext import tasks, commands
import random
from  graphic_engine import Map
from utils import rand, cardValue, randToCard
from parsing import workAI, giveQuot

import json
import time


##--переменные---##
bufer = [0, False, 0, False] ## буфер в 0 индексе лежит привязанный канал, в индексе 1 лежит есть ли закрытые каналы (тру фалсе), в индексе 2 лежит айди сервера к которому привязан, в индексе 3 состояние автомода
bjstats = {} ## для лидеров в блекджеке
warned = {} ## для варнов

# service variables #
global slash_inter, button_inter

slash_inter: disnake.AppCmdInter
button_inter = disnake.MessageInteraction

cursewords = ["блять", "ебать", "залупа", "сука", "хуй", "пиздец", "еба", "ахуеть", "пидор", "бля", "сучка", "выебу", "eбал"]
mup = Map(10, 16) ## инициализация мапа

rephook = SyncWebhook.from_url("webhook url here")
# service variables #

##--переменные---##




########################################################
########### РАБОТА С ФАЙЛАМИ ###########################
########################################################

##--сохранение--##
def exportData(bufer, warned, bjstats):
    data = {'bufer': bufer,
            'warned': warned,
            'bjstats': bjstats}
    with open('value.json', 'w') as save:
        json.dump(data, save)
##--сохранение--##

##--загрузка--##
def importData():
    with open('value.json', 'r') as save:
        data = json.load(save)
        bufer = data['bufer']
        warned = data['warned']
        bjstats = data['bjstats']
    return bufer, warned, bjstats
##--загрузка--##

##--очистка--##
def flushs():
    data = {'bufer': [0, False, 0, False],
            'warned': {},
            'bjstats': {}}
    with open('value.json', 'w') as save:
        json.dump(data, save)


##--очистка--##

########################################################
########### РАБОТА С ФАЙЛАМИ ###########################
########################################################




intents = disnake.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='>', intents=intents, help_command=None)




##------------on_ready-----------------##

@bot.event ## works when it ready
async def on_ready():
    print(f'We have logged in as {bot.user}')

    try: ## проверяю на наличие файлика и обьявляю переменные
        importData()
        global bufer, warned, bjstats
        bufer, warned, bjstats = importData()
        print(f'Loading succesful. {importData()}')
    except:
        print('No saves found')
        
##-------------------------------------##





##---------COMMANDS----------------------------##



##------------HELP--------------##

@bot.slash_command(description='Описание возможностей бота.') ## help command
async def help(slash_inter): 
    emb = disnake.Embed(title="Информация о командах", color=random.randint(1, 16777216))
    if(slash_inter.author.guild_permissions.administrator): #check if user is admin so he will more accses
        emb.add_field(name = f"`help` : ", value="Вызовет это меню", inline=False)
        emb.add_field(name = f"`report` : ", value="Отправить разработчику ваш найденный недочет. Опишите как можно подробнее.", inline=False)
        emb.add_field(name = f"`link` : ", value="Привязка лог чата/привязывает тот канал в котором было отправлено сообщение", inline=False)
        emb.add_field(name = f"`lock` : ", value="Закрытие канала/закрывает тот канал в котором было отправлено сообщение", inline=False)
        emb.add_field(name = f"`unlock` : ", value="Открытие канала/открывает тот канал в котором было отправлено сообщение", inline=False)
        emb.add_field(name = f"`embed` : ", value="Отправит сообщение класса embed/принимает параметры title|description|color", inline=False)
        emb.add_field(name = f"`debug` : ", value="Отправит сообщение который покажет все текущие сохраненные переменные", inline=False)
        emb.add_field(name = f"`map` : ", value="Создает красивую ACSII карту", inline=False)
        emb.add_field(name = f"`coinflip` : ", value="Бросить монетку! Как в старые добрые :)", inline=False)
        emb.add_field(name = f"`clear` : ", value="Очищает чат в которым была вызвана команда/принимает параметры amount", inline=False)
        emb.add_field(name = f"`warn` : ", value="Выдает варн указаному пользователю/принимает параметр @user", inline=False)
        emb.add_field(name = f"`warns` : ", value="Показывает сколько варнов у пользователя/принимает параметр @user", inline=False)
        emb.add_field(name = f"`unwarn` : ", value="Удаляет варны у пользователя/принимает параметр @user", inline=False)
        emb.add_field(name = f"`automod` : ", value="Переключения статуса автомодерации/принимает параметр 1 это включить, любые другие !ЧИСЛА! - выключить (Работает только на привязаном сервере)", inline=False)
        emb.add_field(name = f"`save` : ", value="Запускает цикл сохранения данных в файл.", inline=False)
        emb.add_field(name = f"`flush` : ", value="Очищает файл с данными", inline=False)
        emb.add_field(name = f"`load` : ", value="Загружает данные из файла (вызывается при старте бота)", inline=False)
        emb.add_field(name = f"`bj` : ", value="Блэкджек! Принимает start/stats/stats @user , развлекайтесь!", inline=False)
        emb.add_field(name = f"`quote` : ", value="Цитата из интернета", inline=False)
    else:  #check if user is not admin so he will get basic accses
        emb.add_field(name = f"`help` : ", value="Вызовет это меню", inline=False)
        emb.add_field(name = f"`report` : ", value="Отправить разработчику ваш найденный недочет. Опишите как можно подробнее.", inline=False)
        emb.add_field(name = f"`map` : ", value="Создает красивую ACSII карту/не принимает параметры.", inline=False)
        emb.add_field(name = f"`coinflip` : ", value="Бросить монетку! Как в старые добрые :)", inline=False)
        emb.add_field(name = f"`avatar` : ", value="Получить аватар пользователя/принимает параметр @user ", inline=False)
        emb.add_field(name = f"`bj` : ", value="Блэкджек! Принимает start/stats/stats @user , развлекайтесь!", inline=False)
        emb.add_field(name = f"`quote` : ", value="Цитата из интернета", inline=False)
    await slash_inter.send(embed = emb, ephemeral=True)

##------------HELP--------------##







##------------black jack--------##

@bot.command()
async def bj(ctx, arg, user=None):
    if( arg == 'start'):
        await ctx.reply('Начинаю игру в блекджек!')
        start = True ## начало цикла
        usercards = [randToCard(), randToCard()] ## карты игрока

        while start: ## цикл пока игра запущена для набора игроком карт
            
            if(cardValue(usercards) > 21): ## если карт игрока больше 21
                await ctx.channel.send(f'У тебя перебор! {usercards}, {cardValue(usercards)}, ты проиграл!')
                break
            elif(cardValue(usercards) == 21): ## если карты игрока равны 21
                await ctx.channel.send(f'Красивая победа! У тебя 21!')

                if ctx.author.mention in bjstats: ## СЛОВАРЬ НА РАССТРЕЛ (или список лидеров в блекджеке)
                    bjstats[f'{ctx.author.mention}'] = int(bjstats[f'{ctx.author.mention}']) + 1
                else: 
                    bjstats[f'{ctx.author.mention}'] = '1'
                
                break

            await ctx.channel.send(f'{ctx.author} у тебя {usercards} или {cardValue(usercards)}, еще?') ## набор карт И ОЧЕНЬ СЛОЖНАЯ СКОПИРОВАННАЯ ПРОВЕРКА СООБЩЕНИЯ
            res = await bot.wait_for('message', check=lambda x: x.channel.id == ctx.channel.id and ctx.author.id == x.author.id and x.content.lower() == "да" or x.content.lower() == "нет", timeout=None)

            if (res.content.lower() == 'да'): ## беру беру беруберуберу
                usercards.append(randToCard())

            elif (res.content.lower() == 'нет'): ## Я ОТКАЗЫВАЮСЬ
                await ctx.channel.send('Окей, моя очередь.')
                start = False
                await botCards(ctx, usercards)
        
    if (arg == 'stats' and user != None):
        if user in bjstats:
            await ctx.channel.send(f'{user} has {bjstats[user]} wins in blackjack')
        else:
            await ctx.channel.send(f'{user} dont have any win, rip bozo')
    
    if (arg == 'stats' and user == None):
        await ctx.channel.send(bjstats)
        await ctx.channel.send(f'Ребята которые смогли обыграть казино')

@bj.error
async def error(ctx, error):
    await ctx.channel.send(f"Somethin went wrong, please check how to use '>bj' command. Error: {error}")


async def botCards(ctx, usercards): ## КАЗИНО НЕ ПРОИГРЫВАЕТ СВОЛОЧИ     
    botcards = [randToCard(), randToCard()]
    
    while cardValue(usercards) > cardValue(botcards): ## БЕРУ БЕРУ БЕРУБЕРУБЕРУ
        botcards.append(randToCard())

    if(cardValue(botcards) > 21): ## ААААААА КАЗИНО ПРОИГРАЛО
            await ctx.channel.send(f'У меня перебор! {botcards}, {cardValue(botcards)}, победа за тобой...')

            if str(ctx.author.mention) in bjstats: ## СЛОВАРЬ НА РАССТРЕЛ (или список лидеров в блекджеке)
                bjstats[f'{ctx.author.mention}'] = int(bjstats[f'{ctx.author.mention}']) + 1
            else: 
                bjstats[f'{ctx.author.mention}'] = '1'

    elif(cardValue(botcards) > cardValue(usercards)): ## ХАХАХАХАХАХАХАХХА
        await ctx.channel.send(f'Ты проиграл! У меня {botcards} или {cardValue(botcards)}')
    else: ## НИЧЬЯ
        await ctx.channel.send(f'Ничья! У меня {botcards}, а у тебя {usercards}')
        
        

     
##------------black jack--------##





@bot.slash_command(description='Пожаловаться на ошибку. Пожалуйста опишите как можно точнее.') ## defenies commands idk cogs
async def report(slash_inter, text:str):
    rephook.send(f"{slash_inter.author} пожаловался на проблему! '{text}'")
    await slash_inter.send("Succesful send report!")
    
    


@bot.slash_command(description="Привязывает бота к серверу где будут выполнятся команды") ## link command
async def link(slash_inter):
    if (slash_inter.author.guild_permissions.administrator):
        bufer[0] = slash_inter.channel.id
        bufer[2] = slash_inter.author.guild.id
        print(f"Succesful linked to '{bufer[0]}' channel, {bufer[2]} server")
        await slash_inter.send(f"Succesful linked to '{bufer[0]}' channel, {bufer[2]} server")
    else:
        await slash_inter.send("you don't have permission to use this command", ephemeral=True)

@bot.slash_command(description='Закрыть чат где вызывали команду') ## lock command 
async def lock(slash_inter):
    everyone = slash_inter.author.guild.default_role

    if (slash_inter.author.guild_permissions.administrator):
        await slash_inter.channel.set_permissions(everyone, send_messages = False)
        bufer[1] = True
        print(f"LOCKED {slash_inter.channel} CHAT")
        await slash_inter.send(f"Warning everyone. Chat has been locked, please wait or ask admins.")
    elif (bufer[1]):
        await slash_inter.send("Chat locked already =~=", ephemeral=True)
    else:
        await slash_inter.send("you don't have permission to use this command", ephemeral=True)

@bot.slash_command(description='Открыть чат где вызвали команду') ## unlock command
async def unlock(slash_inter):
    everyone = slash_inter.author.guild.default_role

    if (slash_inter.author.guild_permissions.administrator) and (bufer[1]):
        await slash_inter.channel.set_permissions(everyone, send_messages = True)

        print(f"unLOCKED {slash_inter.channel} CHAT")
        await slash_inter.send(f"Warning everyone. Chat has been unlocked.")
        bufer[1] = False

    elif (not slash_inter.author.guild_permissions.administrator):
        await slash_inter.send("you don't have permission to use this command", ephemeral=True)

    elif (slash_inter.author.guild_permissions.administrator) and (not bufer[1]): 
        await slash_inter.send("Channel is unlocked already O-o'", ephemeral=True)

@bot.slash_command(description='Инструмент для вывода всех переменных') ## tool for debugging values
async def debug(slash_inter):
    if (slash_inter.author.guild_permissions.administrator):
        await slash_inter.send(f"{bufer} is bufer value, {warned} is warned users, {bjstats} is winners in blackjack; no more value", ephemeral=True)
        print(f"{bufer} is bufer value, {warned} is warned users, {bjstats} is winners in blackjack; no more value")
    else:
        print(f"{slash_inter.author} tried to use debug comand")

@bot.slash_command(description='Инструмент для создание сообщения класса embed') ## for cool embed messages exmp: title|description|0
async def embed(slash_inter, *, content: str):
    if (slash_inter.author.guild_permissions.administrator):
        title, description, color = content.split('|')
        embed = disnake.Embed(title=title, description=description, color=int(color, 0))
        await slash_inter.send(embed=embed)
    else:
        print(f"{slash_inter.author} tried to use embed comand")


@bot.slash_command(description='Инструмент для создания ASCCI карты') ## generates cool maps, uses map class, graphic_engine.py and utils.py
async def map(slash_inter):
    emb = disnake.Embed(title="Map", color=random.randint(32052, 32768))
    mup.generateForest(int(40))
    mup.generateLake(int(10))
    mup.generateRiver(int(10))
    mup.generateMountains(int(10))
    await mup.print(slash_inter, emb)

@bot.slash_command(description='Бросить монетку!') ## uses utils function rand check it
async def coinflip(slash_inter):
    if rand(50):
        await slash_inter.send('Выпал орёл!')
    else:
        await slash_inter.send('Выпала решка!')


@bot.slash_command(description='Работа c системой авто-модерации') ## для чистки плохих слов
async def automod(slash_inter, mode: int):
    if (slash_inter.author.guild_permissions.administrator):
        if mode == 1:
            bufer[3] = True
            await slash_inter.send("Automod enabled")
        else:
            bufer[3] = False
            await slash_inter.send("Automod disabled")
    else:
        print(f"{slash_inter.author} tried to use automod command")

@bot.slash_command(description='Запуск цикла сохранений') ## запускает цикл сохранения переменных в файл 290
async def save(slash_inter):
    if (slash_inter.author.guild_permissions.administrator):
        save.start(bufer, warned, bjstats)
        time.sleep(2)
        await slash_inter.send(f'Succesful started saving all data', ephemeral=True)
        print(f'Succesful started saving all data')
    else:
        print(f"{slash_inter.author} tried to use save comand")


@bot.slash_command(description='Очистка сохранения') ## очистка ФАЙЛА, не переменных
async def flush(slash_inter):
    if (slash_inter.author.guild_permissions.administrator):
        await slash_inter.send(f'Succesful delete all data from file', ephemeral=True)
        print(f'Succesful delete all data from file')
        flushs()
    else:
        print(f"{slash_inter.author} tried to use flushs comand")

@bot.slash_command(description='Загрузка данных из сохранения') ## загрузка из ФАЙЛА 
async def load(slash_inter):
    if (slash_inter.author.guild_permissions.administrator):
        global bufer, warned, bjstats
        bufer, warned, bjstats = importData()
        print(f'Loading succesful. {importData()}')
        await slash_inter.send(f'Loaded data from the file', ephemeral=True)
    else:
        print(f"{slash_inter.author} tried to use load comand")

@bot.slash_command(description='Получить аватар пользователя') ## аватарка чек
async def avatar(slash_inter, member : disnake.Member=None):
    try:
        userAvatar = member.avatar
        await slash_inter.send(userAvatar, ephemeral=True)
    except Exception:
        await slash_inter.send('Something went wrong :(', ephemeral=True)

@bot.slash_command(description='Создать картинку по запросу')
async def generate(slash_inter, prompt: str, * , delay=80):
    delay = int(delay)
    await slash_inter.send(f"Started generating an image '{prompt}', please wait {delay+10} seconds. If you don't see the result try add more time.", ephemeral=True)

    await workAI(prompt, delay)

    with open('result.png', 'rb') as f:
        picture = disnake.File(f)
        await slash_inter.edit_original_response(f'Here is your result {slash_inter.author.mention}', file=picture)
        
    
@bot.slash_command(description='Получить случайную цитату')
async def quote(slash_inter):
    emb = disnake.Embed(title="Цитата", color=random.randint(32052, 32768))
    emb.add_field(name = f"Цитата c сайта https://citaty.info/", value=f"{giveQuot()}", inline=False)
    await slash_inter.send(embed = emb)




#----------------------------------------------#
@bot.slash_command(description='Очистка чата') ## clear chat from shit
async def clear(slash_inter, amount: int):
    if (slash_inter.author.guild_permissions.administrator):
        amount = int(amount)
        await slash_inter.channel.purge(limit=amount)
        await slash_inter.send(f"Cleared {amount} messages.")
    else: 
        await slash_inter.send("you don't have permission to use this command", ephemeral=True)
#----------------------------------------------#




#------------warns-----------------------------#
@bot.slash_command(description='Выдать предупреждение пользователю') ## warns user for shitting
async def warn(slash_inter, member:disnake.Member):
    if (slash_inter.author.guild_permissions.administrator):
        user = member.mention
        if user in warned:
            warned[f'{user}'] = int(warned[f'{user}']) + 1
        else: 
            warned[f'{user}'] = '1'
        await slash_inter.send(f"Warned {user}.")   
    else:
         await slash_inter.send("you don't have permission to use this command", ephemeral = True)

@bot.slash_command(description='Узнать количество предупреждений у пользователя') ## send amoun of warns
async def warns(slash_inter, member:disnake.Member):
    if (slash_inter.author.guild_permissions.administrator):
        user = member.mention
        if user in warned:
            await slash_inter.send(f'{user} has {warned[user]} warns')
        else:
            await slash_inter.send(f'{user} has not warns. Cool!')
    else:
         await slash_inter.send("you don't have permission to use this command", ephemeral = True)

@bot.slash_command(description='Удалить все предупреждения у пользователя') ## remove warn from user
async def unwarn(slash_inter, member:disnake.Member):
    if (slash_inter.author.guild_permissions.administrator):
        user = member.mention
        if user in warned:
            warned.pop(f'{user}')
            await slash_inter.send(f"You're forgiven {user}. For now") 
        else: 
            await slash_inter.send(f"{user} dont have warns. Cool!")  
    else:
         await slash_inter.send("you don't have permission to use this command", ephemeral = True)
#------------warns-----------------------------#




##---------END OF COMMANDS---------------------##





##-----------on_message---------------##

@bot.event ## messages from users
async def on_message(message):
    try:
        msg_content = message.content.lower()
        if (message.author == bot.user): ## проверка чтобы не было цикла
            return
    
        elif any(word in msg_content for word in cursewords) and (bufer[3]) and (bufer[2] == message.author.guild.id): ## чистка чата от плохих слов емае
            await message.delete()
            print(f"{message.author} writed in {message.channel} Server {message.guild}. Content bad message {message.content}")

        elif (message.content.startswith('>')):
            await message.channel.send('Бот использует теперь только слеш команды. (исключение >bj)')

        elif (bufer[0] > 0 and bufer[2] == message.author.guild.id): ## logs in admin chat that linked by >link comand
            channel = bot.get_channel(bufer[0])

            if(message.content == ""): ## checking for image
                print(f"{message.author} probably sent video or image in {message.channel}. Server {message.guild}")
                await channel.send(f"```{message.author} probably sent video or image```")

            else: ## simple message or image with text
                await channel.send(f"```{message.author} writed in {message.channel}.``` \n > Content {message.content}")
        
        else: ## вывод в консоль сообщений от людей
            print(f"{message.author} writed in {message.channel} Server {message.guild}. Content {message.content}")  
        
        await bot.process_commands(message)
    except Exception: 
        pass
##----------end_on_message-----------##





##--------------TASKS--------------------------##

@tasks.loop(minutes=1.0) ## цикл сохранения переменных в файл линия 180
async def save(bufer, warned, bjstats):
    try:
        exportData(bufer, warned, bjstats)
        #print(f'Saved {bufer} and {warned} valuables')
    except Exception:
        pass

##-----------END_TASKS-------------------------##




bot.run('token here')


        
