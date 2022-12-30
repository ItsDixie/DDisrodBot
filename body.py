import disnake
from disnake.ext import tasks, commands
import json

with open('TOKEN_HERE.txt', 'r+') as token_file:
    token = token_file.read()



global bufer, acs

bufer = [0, False] ## 0 - привязан к серверу? | 1 - айди привязаного сервера |
acs = False ##accses


intents = disnake.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

############################################
def exportData(bufer):
    
    data = {
            'bufer': bufer 
                            }
    
    with open('value.json', 'w') as save:
        json.dump(data, save)

def LoadData():
    with open('value.json', 'r') as save:
        data = json.load(save)
        bufer = data['bufer']
    return bufer
##################################################

@bot.event ## works when it ready
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try: ## проверяю на наличие файлика и обьявляю переменные
        LoadData()
        global bufer
        bufer = LoadData()
        print(f'Loading succesful. {LoadData()}')
    except:
        print('No saves found')

@bot.event
async def on_guild_join(guild):
    bufer[0] = guild.id
    bufer[1] = True
    print(f'I have joined on server! {guild} Hope all working!')
    save.start(bufer)

##################################################

@bot.event
async def on_message(message):
        if (message.author == bot.user): ## проверка чтобы не было цикла
            return

        if ((bufer[0] == message.author.guild.id)):
            global acs
            acs = True  
        else:
            acs = False
            
        print(acs)
        await bot.process_commands(message)


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command()
    async def debug(self, ctx):
        if acs:
            await ctx.reply(f'{acs} {bufer[1]}, {bufer[0]}')


    @commands.command()
    async def hello(self, ctx, *, member: disnake.Member = None):
        member = member or ctx.author
        if acs:
            await ctx.send(f'Hello {member.name}~')



#------------tasks------------------#

@tasks.loop(minutes=1.0) ## цикл сохранения переменных в файл линия 180
async def save(bufer):
    try:
        exportData(bufer)
    except Exception:
        pass

#------------tasks------------------#


bot.add_cog(AdminCommands(bot))
bot.run(token)