import random, discord
from save import save
from newjson import dict

TOKEN = ' '

client = discord.Client(intents = discord.Intents(message_content = True, messages = True, members = True))

@client.event
async def on_ready():
    print('We have logged in')

class VARS:
    def __init__(self):
        self.catch = False
        self.catchcount = 0

    def pokepick(self):
        self.pokenum = random.randint(1,905)
        self.pokemon = dict[self.pokenum]['name']
        self.pic = dict[self.pokenum]['pic']        

vars = VARS()

@client.event
async def on_message(message):
    channel = message.channel
    user = message.author.id
    name = message.author
    catchprob = random.randint(1,3)
    currentsave = save
    keytrue = currentsave.get(user)

    if message.content == 'pwalk':
        if vars.catch == False:
            num = random.randint(1, 3)
            if num == 1:
                vars.catch = True
                vars.pokepick()
                print(f'{name}: A pokemon has appeared')
                await channel.send(content = 'A pokemon has appeared')
                await channel.send(content = str(vars.pic))
                await channel.send(content = f'{vars.pokemon} has appeared')

            else:
                print(f'{name}: is walking...')
                await channel.send(content = f'{name} is walking...')
        else:
            await channel.send(content = 'You cant run away')
            return

    elif message.content == 'pcatch':
        print(str(catchprob))
        if vars.catch == True:
            if catchprob == 1 and vars.catchcount <= 3:
                vars.catch = False
                vars.catchcount = 0
                await channel.send(content = 'Ding')
                await channel.send(content = 'Ding')
                await channel.send(content = 'Ding')
                await channel.send(content = f'{name} has caught {vars.pokemon}')

                print(str(currentsave))

                if keytrue == None:
                    pokelist = [vars.pokenum]
                    currentpokemon = {}
                    print(str(pokelist))
                    currentpokemon['pokemon'] = pokelist
                    currentsave[user] = currentpokemon
                else:
                    currentpokemon = currentsave.get(user)
                    pokelist = currentpokemon['pokemon']
                    print(str(pokelist))
                    pokelist.append(vars.pokenum)
                    print(str(pokelist))
                    currentpokemon.update({'pokemon': pokelist})
                    currentsave.update({user:currentpokemon})
                    print(str(currentpokemon))
                    print(str(currentsave))
                    print(str(pokelist))

                with open('save.py', 'w') as i:
                    i.write('save = ' + str(currentsave))
                    i.close()

            elif vars.catchcount <= 3:
                vars.catchcount += 1
                await channel.send(content = 'Ding')
                await channel.send(content = 'Ding')
                await channel.send(content = 'Ding')
                await channel.send(content = f'{vars.pokemon} has escaped!')
            elif vars.catchcount > 3:
                await channel.send(content = f'{vars.pokemon} has run away!')
                vars.catch = False
                vars.catchcount = 0
        if vars.catch == False:
            await channel.send(content = 'No pokemon to catch')
        
    elif message.content == 'pstor':
        if vars.catch == True:
            await channel.send(content = 'Cant open storage, in a battle')

        else:
            await channel.send(content = f'{name}\'s pokemon:')
            for x in currentsave[user]['pokemon']:
                await channel.send(content = str(x) + " " + str(dict[x]['name']))

    elif message.content == 'prun':
        if vars.catch == True:
            canrun = random.randint(1,2)
            if canrun == 1:
                await channel.send(content = 'You have fled')
                vars.catchcount = 0
                vars.catch = False
            else:
                await channel.send(content = 'You cannot run')
        
    elif message.content == 'phelp':
        await channel.send('Commands:')
        await channel.send('phelp: For help')
        await channel.send('pwalk: To walk around')
        await channel.send('pcatch: To catch an encountered pokemon')
        await channel.send('prun: To attempt to escape the pokemon')
        await channel.send('pstor: To look at your captured pokemon')
        await channel.send('psummon (number): Summon your pokemon')
        await channel.send('psearch (number): To look up a pokemon')
        await channel.send('prelease (number): To release a pokemon')

    content = message.content 
    content = content.split(" ")
    if content[0] == 'psummon':
        for j in currentsave[user]['pokemon']:
            if int(content[1]) == j:
                await channel.send(content = str(name) + '\'s ' + str(dict[int(content[1])]['name']))
                await channel.send(content = str(dict[int(content[1])]['pic']))

    elif content[0] == 'psearch':
        await channel.send(content = str(dict[int(content[1])]['name']))
        await channel.send(content = str(dict[int(content[1])]['pic']))

    elif content[0] == 'prelease':
            currentpokemon = currentsave.get(user)
            pokelist = currentpokemon['pokemon']

            if len(pokelist) == 1:
                await channel.send(content = 'You cannot release your last pokemon!')
            
            else:
                pokelist.remove(int(content[1]))
                currentpokemon.update({'pokemon': pokelist})
                currentsave.update({user:currentpokemon})

                with open('save.py', 'w') as i:
                    i.write('save = ' + str(currentsave))
                    i.close()
                await channel.send(content = str(name) + '\'s ' + str(dict[int(content[1])]['name']) + ' has been released!')
                await channel.send(content = str(dict[int(content[1])]['name']) + ' will miss you!')

client.run(TOKEN)