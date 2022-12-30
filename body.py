import disnake
from disnake.ext import tasks, commands
import json

global bufer

bufer = [0, False] ## 0 - привязан к серверу? | 1 - айди привязаного сервера |

with open('TOKEN_HERE.txt', 'r+') as token_file:
    token = token_file.read()


intents = disnake.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

def ExportData(bufer):
    
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

@bot.event ## works when it ready
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try: ## проверяю на наличие файлика и обьявляю переменные
        importData()
        global bufer
        bufer = importData()
        print(f'Loading succesful. {importData()}')
    except:
        print('No saves found')

@bot.event
async def on_guild_join(guild):
    bufer[0] = guild.id

class Loggin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.accses = False

    @commands.Cog.listener()
    async def on_message(self, message):
        
        if (message.author == bot.user): ## проверка чтобы не было цикла
            return
        
        print(bufer, self.accses)

        if ((bufer[0] == message.author.guild.id) and (bufer[1])):
            self.accses = True
            checker(self)
        else:
            self.accses = False

    @commands.command()
    async def link(self, ctx):
        if ((not(bufer[1])) and (not(bufer[0] == ctx.author.guild.id))):
            bufer[1] = True
    
    def checker(self):
        if self.accses:

            @commands.command()
            async def debug(self, ctx):
                await ctx.reply(f'{self.accses} {self.bufer[1]}, {self.bufer[0]}')


            @commands.command()
            async def hello(self, ctx, *, member: disnake.Member = None):

                    """Says hello"""
                    member = member or ctx.author
                    await ctx.send(f'Hello {member.name}~')


bot.add_cog(Loggin(bot))
bot.run(token)