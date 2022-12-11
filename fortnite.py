try:
    import asyncio
    import sys
    import os
    import time
    import datetime
    import json
    from functools import partial
    import random as rand

    from colorama import Fore, Back, Style, init
    init(autoreset=True)

    import fortnitepy
    from fortnitepy.ext import commands
    import FortniteAPIAsync
    import aiohttp
    import requests

except ModuleNotFoundError as e:
    print(e)
    print(Fore.RED + ' • ' + Fore.RESET + 'Failed to import 1 or more modules. Run "INSTALL PACKAGES.bat')
    exit()

os.system('cls||clear')

intro = Fore.LIGHTCYAN_EX + """ • SchuhFN is made by Schuh weiß nicht
 • For support, questions, etc join https://discord.gg/AtJ2xgzjQY
 • Don't forget to follow me on Instagram and Twitter (@kilianbtw)
 """

print(intro)

def lenPartyMembers():
    members = client.party.members
    return len(members)

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

def lenFriends():
    friends = client.friends
    return len(friends)

def getNewSkins():
    r = requests.get('https://fortnite-api.com/v2/cosmetics/br/new')

    response = r.json()

    cids = []

    for cid in [item for item in response if item.split('/')[-1].upper().startswith('CID_')]:
        cids.append(cid.split('/')[-1].split('.')[0])
    
    return cids

def getNewEmotes():
    r = requests.get('https://fortnite-api.com/v2/cosmetics/br/new')

    response = r.json()

    eids = []

    for cid in [item for item in response if item.split('/')[-1].upper().startswith('EID_')]:
        eids.append(cid.split('/')[-1].split('.')[0])
    
    return eids

def get_device_auth_details():
    if os.path.isfile('auths.json'):
        with open('auths.json', 'r') as fp:
            return json.load(fp)
    else:
        with open('auths.json', 'w+') as fp:
            json.dump({}, fp)
    return {}

def store_device_auth_details(email, details):
    existing = get_device_auth_details()
    existing[email] = details

    with open('auths.json', 'w') as fp:
        json.dump(existing, fp)

with open('config.json') as f:
    try:
        data = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print(Fore.RED + ' [ERROR] ' + Fore.RESET + "There was an error in one of the bot's files! (config.json). If you have problems trying to fix it, join the discord support server for help - https://discord.gg/AtJ2xgzjQY")
        print(Fore.LIGHTRED_EX + f'\n {e}')
        exit(1)

with open('info.json') as f:
    try:
        info = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print(Fore.RED + ' [ERROR] ' + Fore.RESET + "There was an error in one of the bot's files! (info.json) If you have problems trying to fix it, join the discord support server for help - https://discord.gg/AtJ2xgzjQY")
        print(Fore.LIGHTRED_EX + f'\n {e}')
        exit(1)

def is_admin():
    async def predicate(ctx):
        return ctx.author.id in info['FullAccess']
    return commands.check(predicate)


device_auth_details = get_device_auth_details().get(data['email'], {})

prefix = (data['prefix'])

fortnite_api = FortniteAPIAsync.APIClient()

client = commands.Bot(
    command_prefix=prefix,
    case_insensitive=True,
    auth=fortnitepy.AdvancedAuth(
        email=data['email'],
        password=data['password'],
        prompt_authorization_code=True,
        delete_existing_device_auths=True,
        **device_auth_details
    ),
    status=data['status'],
    platform=fortnitepy.Platform(data['platform']),
)


@client.event
async def event_device_auth_generate(details, email):
    store_device_auth_details(email, details)

@client.event
async def event_ready():
    os.system('cls||clear')
    print(intro)
    print(Fore.LIGHTCYAN_EX + ' • ' + Fore.RESET + 'Client ready as ' + Fore.LIGHTCYAN_EX + f'{client.user.display_name}')
    
    member = client.party.me

    await member.edit_and_keep(
        partial(
            fortnitepy.ClientPartyMember.set_outfit,
            asset=data['cid']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_backpack,
            asset=data['bid']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_pickaxe,
            asset=data['pid']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_banner,
            icon=data['banner'],
            color=data['banner_color'],
            season_level=data['level']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_battlepass_info,
            has_purchased=True,
            level=data['bp_tier']
        )
    )

    client.set_avatar(fortnitepy.Avatar(asset=data['avatar'], background_colors=['#ffffff', '#2E8B57', '#7FFF00']))
    

@client.event
async def event_party_invite(invite):
    if data['joinoninvite'].lower() == 'true':
        try:
            await invite.accept()
            print(Fore.LIGHTCYAN_EX + ' • ' + Fore.RESET + 'Accepted party invite from' + Fore.LIGHTCYAN_EX + f'{invite.sender.display_name}')
        except Exception:
            pass
    elif data['joinoninvite'].lower() == 'false':
        if invite.sender.id in info['FullAccess']:
            await invite.accept()
            print(Fore.LIGHTCYAN_EX + ' • ' + Fore.RESET + 'Accepted party invite from ' + Fore.LIGHTCYAN_EX + f'{invite.sender.display_name}')
        else:
            print(Fore.LIGHTCYAN_EX + ' • ' + Fore.RESET + 'Never accepted party invite from ' + Fore.LIGHTCYAN_EX + f'{invite.sender.display_name}')


@client.event
async def event_friend_request(request):
    if data['friendaccept'].lower() == 'true':
        try:
            await request.accept()
            print(f' • Accepted friend request from {request.display_name}' + Fore.LIGHTBLACK_EX + f' ({lenFriends()})')
        except Exception:
            pass
    elif data['friendaccept'].lower() == 'false':
        if request.id in info['FullAccess']:
            try:
                await request.accept()
                print(Fore.LIGHTCYAN_EX + ' • ' + Fore.RESET + 'Accepted friend request from ' + Fore.LIGHTCYAN_EX + f'{request.display_name}' + Fore.LIGHTBLACK_EX + f' ({lenFriends()})')
            except Exception:
                pass
        else:
            print(f' • Never accepted friend request from {request.display_name}')


@client.event
async def event_party_member_join(member: fortnitepy.PartyMember) -> None:
    if client.user.display_name != member.display_name:
        try:
            print(Fore.LIGHTYELLOW_EX + f' • {member.display_name}' + Fore.RESET + ' has joined the lobby.' + Fore.LIGHTBLACK_EX + f' ({lenPartyMembers()})')
        except fortnitepy.HTTPException:
            pass
        try:
            await client.party.set_playlist(playlist=data['playlist'])
        except fortnitepy.Forbidden:
            pass
        await client.party.send(data['JoinMessage'])


@client.event
async def event_party_member_confirm(confirmation):
    if confirmation.user.id in client.blocked_users:
        await confirmation.reject()
    else:
        await confirmation.confirm()


@client.event
async def event_party_member_leave(member):
    if client.user.display_name != member.display_name:
        try:
            print(Fore.LIGHTYELLOW_EX + f' • {member.display_name}' + Fore.RESET + ' has left the lobby.' + Fore.LIGHTBLACK_EX + f' ({lenPartyMembers()})')
        except fortnitepy.HTTPException:
            pass


@client.event
async def event_party_message(message):
    if message.author.id in info['FullAccess']:
        name = Fore.LIGHTCYAN_EX + f'{message.author.display_name}'
    else:
        name = Fore.RESET + f'{message.author.display_name}'
    print(Fore.GREEN + ' • [Party] ' + f'{name}' + Fore.RESET + f': {message.content}')


@client.event
async def event_friend_message(message):
    if message.author.id in info['FullAccess']:
        name = Fore.LIGHTMAGENTA_EX + f'{message.author.display_name}'
    else:
        name = Fore.RESET + f'{message.author.display_name}'
    print(Fore.LIGHTMAGENTA_EX + ' • [Whisper] ' + f'{name}' + Fore.RESET + f': {message.content}')

    if message.content.upper().startswith('CID_'):
        await client.party.me.set_outfit(asset=message.content.upper())
        await message.reply(f'Skin set to: {message.content}')
    elif message.content.upper().startswith('BID_'):
        await client.party.me.set_backpack(asset=message.content.upper())
        await message.reply(f'Backpack set to: {message.content}')
    elif message.content.upper().startswith('EID_'):
        await client.party.me.set_emote(asset=message.content.upper())
        await message.reply(f'Emote set to: {message.content}')
    elif message.content.upper().startswith('PID_'):
        await client.party.me.set_pickaxe(asset=message.content.upper())
        await message.reply(f'Pickaxe set to: {message.content}')
    elif message.content.startswith('Playlist_'):
        try:
            await client.party.set_playlist(playlist=message.content)
            await message.reply(f'Playlist set to: {message.content}')
        except fortnitepy.Forbidden:
            await message.reply(f"I can not set gamemode because I am not party leader.")
    elif message.content.lower().startswith('prefix'):
        await message.reply(f'Current prefix: !')


@client.event
async def event_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'That is not a command. Try !help')
    elif isinstance(error, IndexError):
        pass
    elif isinstance(error, fortnitepy.HTTPException):
        pass
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("You don't have access to this command!")
    elif isinstance(error, TimeoutError):
        await ctx.send("You took too long to respond!")
    else:
        print(error)


@client.command()
async def skin(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No skin was given, try: {prefix}skin (skin name)')
    elif content.upper().startswith('CID_'):
        await client.party.me.set_outfit(asset=content.upper())
        await ctx.send(f'Skin set to: {content}')
    else:
        try:
            cosmetic = await fortnite_api.cosmetics.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaCharacter"
            )
            await client.party.me.set_outfit(asset=cosmetic.id)
            await ctx.send(f'Skin set to: {cosmetic.name}')
        except FortniteAPIAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a skin named: {content}')


@client.command()
async def backpack(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No backpack was given, try: {prefix}backpack (backpack name)')
    elif content.lower() == 'none':
        await client.party.me.clear_backpack()
        await ctx.send('Backpack set to: None')
    elif content.upper().startswith('BID_'):
        await client.party.me.set_backpack(asset=content.upper())
        await ctx.send(f'Backpack set to: {content}')
    else:
        try:
            cosmetic = await fortnite_api.cosmetics.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaBackpack"
            )
            await client.party.me.set_backpack(asset=cosmetic.id)
            await ctx.send(f'Backpack set to: {cosmetic.name}')
        except FortniteAPIAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a backpack named: {content}')


@client.command()
async def emote(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No emote was given, try: {prefix}emote (emote name)')
    elif content.lower() == 'floss':
        await client.party.me.clear_emote()
        await client.party.me.set_emote(asset='EID_Floss')
        await ctx.send(f'Emote set to: Floss')
    elif content.lower() == 'none':
        await client.party.me.clear_emote()
        await ctx.send(f'Emote set to: None')
    elif content.upper().startswith('EID_'):
        await client.party.me.clear_emote()
        await client.party.me.set_emote(asset=content.upper())
        await ctx.send(f'Emote set to: {content}')
    else:
        try:
            cosmetic = await fortnite_api.cosmetics.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaDance"
            )
            await client.party.me.clear_emote()
            await client.party.me.set_emote(asset=cosmetic.id)
            await ctx.send(f'Emote set to: {cosmetic.name}')
        except FortniteAPIAsync.exceptions.NotFound:
            await ctx.send(f'Could not find an emote named: {content}')


@client.command()
async def pickaxe(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No pickaxe was given, try: {prefix}pickaxe (pickaxe name)')
    elif content.upper().startswith('Pickaxe_'):
        await client.party.me.set_pickaxe(asset=content.upper())
        await ctx.send(f'Pickaxe set to: {content}')
    else:
        try:
            cosmetic = await fortnite_api.cosmetics.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaPickaxe"
            )
            await client.party.me.set_pickaxe(asset=cosmetic.id)
            await ctx.send(f'Pickaxe set to: {cosmetic.name}')
        except FortniteAPIAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a pickaxe named: {content}')


@client.command()
async def random(ctx, content = None):

    skins = await fortnite_api.cosmetics.get_cosmetics(
        lang="en",
        backendType="AthenaCharacter"
    )

    skin = rand.choice(skins)

    backpacks = await fortnite_api.cosmetics.get_cosmetics(
        lang="en",
        backendType="AthenaBackpack"
    )

    backpack = rand.choice(backpacks)

    emotes = await fortnite_api.cosmetics.get_cosmetics(
        lang="en",
        backendType="AthenaDance"
    )

    emote = rand.choice(emotes)

    pickaxes = await fortnite_api.cosmetics.get_cosmetics(
        lang="en",
        backendType="AthenaPickaxe"
    )

    pickaxe = rand.choice(pickaxes)

    
    if content is None:
        me = client.party.me
        await me.set_outfit(asset=skin.id)
        await me.set_backpack(asset=backpack.id)
        await me.set_pickaxe(asset=pickaxe.id)

        await ctx.send(f'Loadout randomly set to: {skin.name}, {backpack.name}, {pickaxe.name}')
    else:
        if content.lower() == 'skin':
            await client.party.me.set_outfit(asset=skin.id)
            await ctx.send(f'Skin randomly set to: {skin.name}')

        elif content.lower() == 'backpack':
            await client.party.me.set_backpack(asset=backpack.id)
            await ctx.send(f'Backpack randomly set to: {backpack.name}')

        elif content.lower() == 'emote':
            await client.party.me.set_emote(asset=emote.id)
            await ctx.send(f'Emote randomly set to: {emote.name}')

        elif content.lower() == 'pickaxe':
            await client.party.me.set_pickaxe(asset=pickaxe.id)
            await ctx.send(f'Pickaxe randomly set to: {pickaxe.name}')

        else:
            await ctx.send(f"I don't know that, try: {prefix}random (skin, backpack, emote, pickaxe - og, exclusive, unreleased")



@client.command()
async def point(ctx, *, content = None):
    if content is None:
        await client.party.me.clear_emote()
        await client.party.me.set_emote(asset='EID_IceKing')
        await ctx.send(f'Pointing with: {client.party.me.pickaxe}')
    
    else:
        if content.upper().startswith('Pickaxe_'):
            await client.party.me.set_pickaxe(asset=content.upper())
            await client.party.me.clear_emote()
            asyncio.sleep(0.25)
            await client.party.me.set_emote(asset='EID_IceKing')
            await ctx.send(f'Pointing with: {content}')
        else:
            try:
                cosmetic = await fortnite_api.cosmetics.get_cosmetic(
                    lang="en",
                    searchLang="en",
                    matchMethod="contains",
                    name=content,
                    backendType="AthenaPickaxe"
                )
                await client.party.me.set_pickaxe(asset=cosmetic.id)
                await client.party.me.clear_emote()
                await client.party.me.set_emote(asset='EID_IceKing')
                await ctx.send(f'Pointing with: {cosmetic.name}')
            except FortniteAPIAsync.exceptions.NotFound:
                await ctx.send(f'Could not find a pickaxe named: {content}')



@client.command()
async def checkeredrenegade(ctx):
    variants = client.party.me.create_variants(material=2)

    await client.party.me.set_outfit(
        asset='CID_028_Athena_Commando_F',
        variants=variants
    )

    await ctx.send('Skin set to: Checkered Renegade')



@client.command()
async def pinkghoul(ctx):
    variants = client.party.me.create_variants(material=3)

    await client.party.me.set_outfit(
        asset='CID_029_Athena_Commando_F_Halloween',
        variants=variants
    )

    await ctx.send('Skin set to: Pink Ghoul Trooper')



@client.command()
async def purpleskull(ctx):
    variants = client.party.me.create_variants(clothing_color=1)

    await client.party.me.set_outfit(
        asset='CID_030_Athena_Commando_M_Halloween',
        variants = variants
    )

    await ctx.send('Skin set to: Purple Skull Trooper')



@client.command()
async def purpleportal(ctx):
    variants = client.party.me.create_variants(
        item='AthenaBackpack',
        particle_config='Particle',
        particle=1
    )

    await client.party.me.set_backpack(
        asset='BID_105_GhostPortal',
        variants=variants
    )

    await ctx.send('Backpack set to: Purple Ghost Portal')


@client.command()
async def gift(ctx):
    await client.party.me.set_emote(
        asset='EID_nevergonna'
    )
    
    await ctx.send(f"Nice try but i can't gift anything.")
    await asyncio.sleep(10)
    await client.party.me.clear_emote()


@client.command()
async def rareskins(ctx):
    previous_skin = client.party.me.outfit
    variants = client.party.me.create_variants(material=1)

    await client.party.me.set_outfit(
        asset='CID_028_Athena_Commando_F',
        variants=variants
    )
    await ctx.send(f'Skin set to: Renegade Raider')

    await asyncio.sleep(2.25)
    await client.party.me.set_outfit(
        asset='cid_017_athena_commando_m',
    )
    await ctx.send(f'Skin set to: Aerial Assault Trooper')

    await asyncio.sleep(2.25)
    variants = client.party.me.create_variants(material=3)
    await client.party.me.set_outfit(
        asset='CID_029_Athena_Commando_F_Halloween',
        variants=variants
    )
    await ctx.send('Skin set to: Pink Ghoul Trooper')

    await asyncio.sleep(2.25)
    variants = client.party.me.create_variants(clothing_color=1)

    await client.party.me.set_outfit(
        asset='CID_030_Athena_Commando_M_Halloween',
        variants = variants
    )
    await ctx.send('Skin set to: Purple Skull Trooper')

    await asyncio.sleep(2.25)
    await client.party.me.set_outfit(asset=previous_skin)
    
    await ctx.send(f'Done!')


@client.command()
async def reset(ctx):
    member = client.party.me

    await member.edit_and_keep(
        partial(
            fortnitepy.ClientPartyMember.set_outfit,
            asset=data['cid']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_backpack,
            asset=data['bid']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_pickaxe,
            asset=data['pid']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_banner,
            icon=data['banner'],
            color=data['banner_color'],
            season_level=data['level']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_battlepass_info,
            has_purchased=True,
            level=data['bp_tier']
        )
    )
    await ctx.send(f'Reset loadout to Config!')


@client.command()
async def olddefaults(ctx):
    previous_skin = client.party.me.outfit
    
    await ctx.send(f'Show old defaults..')
    await client.party.me.set_outfit(asset='cid_001_athena_commando_f_default')
    await asyncio.sleep(1.25)
    await client.party.me.set_outfit(asset='cid_002_athena_commando_f_default')
    await asyncio.sleep(1.25)
    await client.party.me.set_outfit(asset='cid_003_athena_commando_f_default')
    await asyncio.sleep(1.25)
    await client.party.me.set_outfit(asset='cid_004_athena_commando_f_default')
    await asyncio.sleep(1.25)
    await client.party.me.set_outfit(asset='cid_005_athena_commando_m_default')
    await asyncio.sleep(1.25)
    await client.party.me.set_outfit(asset='cid_006_athena_commando_m_default')
    await asyncio.sleep(1.25)
    await client.party.me.set_outfit(asset='cid_007_athena_commando_m_default')
    await asyncio.sleep(1.25)
    await client.party.me.set_outfit(asset='cid_008_athena_commando_m_default')
    await asyncio.sleep(2.25)
    await ctx.send(f'Done!')
    await client.party.me.set_outfit(asset=previous_skin)



@client.command()
async def goldpeely(ctx):
    variants = client.party.me.create_variants(progressive=4)

    await client.party.me.set_outfit(
        asset='CID_701_Athena_Commando_M_BananaAgent',
        variants=variants,
        enlightenment=(2, 350)
    )

    await ctx.send('Skin set to: Golden Peely')



@client.command()
async def hatlessrecon(ctx):
    variants = client.party.me.create_variants(parts=2)

    await client.party.me.set_outfit(
        asset='CID_022_Athena_Commando_F',
        variants=variants
    )

    await ctx.send('Skin set to: Hatless Recon Expert')



@client.command()
async def hologram(ctx):
    await client.party.me.set_outfit(
        asset='CID_VIP_Athena_Commando_M_GalileoGondola_SG'
    )
    
    await ctx.send("Skin set to: Hologram")


@client.command()
async def new(ctx: fortnitepy.ext.commands.Context, cosmetic_type: str = 'skin') -> None:
    cosmetic_types = {'skin': {'id': 'cid_', 'function': client.party.me.set_outfit},
                      'backpack': {'id': 'bid_', 'function': client.party.me.set_backpack},
                      'emotes': {'id': 'eid_', 'function': client.party.me.set_emote}, }

    if cosmetic_type not in cosmetic_types:
        return await ctx.send('Invalid cosmetic type, valid types include: skin, backpack & emotes.')

    new_cosmetics = await fortnite_api.cosmetics.get_new_cosmetics()

    for new_cosmetic in [new_id for new_id in new_cosmetics if
                         new_id.id.lower().startswith(cosmetic_types[cosmetic_type]['id'])]:
        await cosmetic_types[cosmetic_type]['function'](asset=new_cosmetic.id)

        await ctx.send(f"{cosmetic_type}s set to {new_cosmetic.name}.")

        await asyncio.sleep(3)

    await ctx.send(f'Done with all new {cosmetic_type}s.')



@client.command()
async def ready(ctx):
    await client.party.me.set_ready(fortnitepy.ReadyState.READY)
    await ctx.send('Ready!')



@client.command()
async def unready(ctx):
    await client.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
    await ctx.send('Unready!')



@client.command()
async def sitin(ctx):
    await client.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
    await ctx.send('Sitting in')


@client.command()
async def sitout(ctx):
    await client.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
    await ctx.send('Sitting out')



@client.command()
async def tier(ctx, tier = None):
    if tier is None:
        await ctx.send(f'No tier was given. try: {prefix}tier (tier number)') 
    else:
        await client.party.me.set_battlepass_info(
            has_purchased=True,
            level=tier
        )

        await ctx.send(f'Battle Pass tier set to: {tier}')



@client.command()
async def level(ctx, level = None):
    if level is None:
        await ctx.send(f'No level was given. try: {prefix}level (number)')
    else:
        await client.party.me.set_banner(season_level=level)
        await ctx.send(f'Level set to: {level}')



@client.command()
async def banner(ctx, args1 = None, args2 = None):
    if (args1 is not None) and (args2 is None):
        if args1.startswith('defaultcolor'):
            await client.party.me.set_banner(
                color = args1
            )
            
            await ctx.send(f'Banner color set to: {args1}')

        elif args1.isnumeric() == True:
            await client.party.me.set_banner(
                color = 'defaultcolor' + args1
            )

            await ctx.send(f'Banner color set to: defaultcolor{args1}')

        else:
            await client.party.me.set_banner(
                icon = args1
            )

            await ctx.send(f'Banner Icon set to: {args1}')

    elif (args1 is not None) and (args2 is not None):
        if args2.startswith('defaultcolor'):
            await client.party.me.set_banner(
                icon = args1,
                color = args2
            )

            await ctx.send(f'Banner icon set to: {args1} -- Banner color set to: {args2}')
        
        elif args2.isnumeric() == True:
            await client.party.me.set_banner(
                icon = args1,
                color = 'defaultcolor' + args2
            )

            await ctx.send(f'Banner icon set to: {args1} -- Banner color set to: defaultcolor{args2}')

        else:
            await ctx.send(f'Not proper format. try: {prefix}banner (Banner ID) (Banner Color ID)')


copied_player = ""



@client.command()
async def stop(ctx):
    global copied_player
    if copied_player != "":
        copied_player = ""
        await ctx.send(f'Stopped copying all users.')
        return
    else:
        try:
            await client.party.me.clear_emote()
        except RuntimeWarning:
            pass



@client.command()
@is_admin()
async def copy(ctx: fortnitepy.ext.commands.Context, *, epic_username=None) -> None:
    global copied_player

    if epic_username is None:
        user = await client.fetch_user(ctx.author.display_name)
        member = client.party.get_member(user.id)

    elif 'stop' in epic_username:
        copied_player = ""
        await ctx.send(f'Stopped copying all users.')
        await client.party.me.clear_emote()
        return

    elif epic_username is not None:
        try:
            user = await client.fetch_user(epic_username)
            member = client.party.get_member(user.id)
        except AttributeError:
            await ctx.send("Could not get that user.")
            return
    try:
        copied_player = member
        await client.party.me.edit_and_keep(
            partial(fortnitepy.ClientPartyMember.set_outfit, asset=member.outfit, variants=member.outfit_variants),
            partial(fortnitepy.ClientPartyMember.set_pickaxe, asset=member.pickaxe, variants=member.pickaxe_variants))
        await ctx.send(f"Now copying: {member.display_name}")
    except AttributeError:
        await ctx.send("Could not get that user.")


@client.event()
async def event_party_member_outfit_change(member, before, after):
    if member == copied_player:
        await client.party.me.edit_and_keep(
            partial(
                fortnitepy.ClientPartyMember.set_outfit,
                asset=after,
                variants=member.outfit_variants
            )
        )

@client.event()
async def event_party_member_outfit_variants_change(member, before, after):
    if member == copied_player:
        await client.party.me.edit_and_keep(
            partial(
                fortnitepy.ClientPartyMember.set_outfit,
                variants=member.outfit_variants
            )
        )

@client.event()
async def event_party_member_backpack_change(member, before, after):
    if member == copied_player:
        if after is None:
            await client.party.me.clear_backpack()
        else:
            await client.party.me.edit_and_keep(
                partial(
                    fortnitepy.ClientPartyMember.set_backpack,
                    asset=after,
                    variants=member.backpack_variants
                )
            )

@client.event()
async def event_party_member_backpack_variants_change(member, before, after):
    if member == copied_player:
        await client.party.me.edit_and_keep(
            partial(
                fortnitepy.ClientPartyMember.set_backpack,
                variants=member.backpack_variants
            )
        )

@client.event()
async def event_party_member_emote_change(member, before, after):
    if member == copied_player:
        if after is None:
            await client.party.me.clear_emote()
        else:
            await client.party.me.edit_and_keep(
                partial(
                    fortnitepy.ClientPartyMember.set_emote,
                    asset=after
                )
            )

@client.event()
async def event_party_member_pickaxe_change(member, before, after):
    if member == copied_player:
        await client.party.me.edit_and_keep(
            partial(
                fortnitepy.ClientPartyMember.set_pickaxe,
                asset=after,
                variants=member.pickaxe_variants
            )
        )

@client.event()
async def event_party_member_pickaxe_variants_change(member, before, after):
    if member == copied_player:
        await client.party.me.edit_and_keep(
            partial(
                fortnitepy.ClientPartyMember.set_pickaxe,
                variants=member.pickaxe_variants
            )
        )

@client.event()
async def event_party_member_banner_change(member, before, after):
    if member == copied_player:
        await client.party.me.edit_and_keep(
            partial(
                fortnitepy.ClientPartyMember.set_banner,
                icon=member.banner[0],
                color=member.banner[1],
                season_level=member.banner[2]
            )
        )

@client.event()
async def event_party_member_battlepass_info_change(member, before, after):
    if member == copied_player:
        await client.party.me.edit_and_keep(
            partial(
                fortnitepy.ClientPartyMember.set_battlepass_info,
                has_purchased=member.battlepass_info[0],
                level=member.battlepass_info[1]
            )
        )

async def set_and_update_party_prop(schema_key: str, new_value: str):
    prop = {schema_key: client.party.me.meta.set_prop(schema_key, new_value)}
    await client.party.patch(updated=prop)


@client.command()
@is_admin()
async def hide(ctx, *, user = None):
    if client.party.me.leader:
        if user != "all":
            try:
                if user is None:
                    user = await client.fetch_profile(ctx.message.author.id)
                    member = client.party.members.get(user.id)
                else:
                    user = await client.fetch_profile(user)
                    member = client.party.members.get(user.id)

                raw_squad_assignments = client.party.meta.get_prop('Default:RawSquadAssignments_j')["RawSquadAssignments"]

                for m in raw_squad_assignments:
                    if m['memberId'] == member.id:
                        raw_squad_assignments.remove(m)

                await set_and_update_party_prop(
                    'Default:RawSquadAssignments_j',
                    {
                        'RawSquadAssignments': raw_squad_assignments
                    }
                )

                await ctx.send(f"Hid {member.display_name}")
            except AttributeError:
                await ctx.send("I could not find that user.")
            except fortnitepy.HTTPException:
                await ctx.send("I am not party leader.")
        else:
            try:
                await set_and_update_party_prop(
                    'Default:RawSquadAssignments_j',
                    {
                        'RawSquadAssignments': [
                            {
                                'memberId': client.user.id,
                                'absoluteMemberIdx': 1
                            }
                        ]
                    }
                )

                await ctx.send("Hid everyone in the party.")
            except fortnitepy.HTTPException:
                await ctx.send("I am not party leader.")
    else:
        await ctx.send("I need party leader to do this!")


@client.command()
@is_admin()
async def unhide(ctx):
    if client.party.me.leader:
        user = await client.fetch_profile(ctx.message.author.id)
        member = client.party.members.get(user.id)

        await member.promote()

        await ctx.send("Unhid all players.")

    else:
        await ctx.send("I am not party leader.")


@client.command()
@is_admin()
async def say(ctx, *, message = None):
    if message is not None:
        await client.party.send(message)
        await ctx.send(f'Sent "{message}" to party chat')
    else:
        await ctx.send(f'No message was given. try: {prefix}say (message)')



@client.command()
@is_admin()
async def whisper(ctx, member = None, *, message = None):
    if (member is not None) and (message is not None):
        try:
            user = await client.fetch_profile(member)
            friend = client.get_friend(user.id)

            if friend.is_online():
                await friend.send(message)
                await ctx.send("Message sent.")
            else:
                await ctx.send("That friend is offline.")
        except AttributeError:
            await ctx.send("I couldn't find that friend.")
        except fortnitepy.HTTPException:
            await ctx.send("Something went wrong sending the message.")
    else:
        await ctx.send(f"Command missing one or more arguments. try: {prefix}whisper (friend) (message)")



@client.command()
@is_admin()
async def match(ctx, players = None):
    time = datetime.utcnow()
    if players is not None:
        if 'auto' in players.lower():
            if client.party.me.in_match():
                left = client.party.me.match_players_left
            else:
                left = 100
            await client.party.me.set_in_match(players_left=left, started_at=time)

            await asyncio.sleep(rand.randint(20, 30))

            while client.party.me.match_players_left > 5 and client.party.me.in_match():
                await client.party.me.set_in_match(players_left=client.party.me.match_players_left - rand.randint(3, 5), started_at=time),

                await asyncio.sleep(rand.randint(8, 18))

            while (client.party.me.match_players_left <= 5) and (client.party.me.match_players_left > 3):
                await client.party.me.set_in_match(players_left=client.party.me.match_players_left - rand.randint(1, 2), started_at=time)

                await asyncio.sleep(rand.randint(12, 20))

            while (client.party.me.match_players_left <= 3) and (client.party.me.match_players_left > 1):
                await client.party.me.set_in_match(players_left=client.party.me.match_players_left - 1, started_at=time)

                await asyncio.sleep(rand.randint(12, 20))

            await asyncio.sleep(6)
            await client.party.me.clear_in_match()

        elif 'leave' in players.lower():
            await client.party.me.clear_in_match()

        else:
            try:
                await client.party.me.set_in_match(players_left=int(players), started_at=time)
            except ValueError:
                await ctx.send(f"Invalid usage. try: {prefix}match (0-255)")
                pass

    else:
        await ctx.send(f'Incorrect usage. try: {prefix}match (auto, #, leave)')



@client.command()
@is_admin()
async def status(ctx, *, status = None):
    if status is not None:
        await client.set_status(status)
        await ctx.send(f'Set status to: {status}')
        print(Fore.LIGHTCYAN_EX + ' • ' + Fore.RESET + 'Changed status to: ' + Fore.LIGHTBLACK_EX + f'{status}')
    else:
        await ctx.send(f'No status was given. try: {prefix}status (status message)')



@client.command()
@is_admin()
async def leave(ctx):
    await client.party.me.leave()
    await ctx.send('Left party.')



@client.command()
@is_admin()
async def kick(ctx, *, member = None):
    if member is not None:
        if member.lower() == 'all':
            members = client.party.members

            for m in members:
                try:
                    member = await client.get_user(m)
                    await member.kick()
                except fortnitepy.Forbidden:
                    await ctx.send("I am not party leader.")

            await ctx.send("Kicked everyone in the party")

        else:
            try:
                user = await client.fetch_profile(member)
                member = client.party.members.get(user.id)
                friend = client.get_friend(user.id)

                if member is None:
                    await ctx.send("Couldn't find that user. Are you sure they're in the party?")

                await member.kick()
                await ctx.send(f'Kicked: {member.display_name}')
                await friend.send("Improve your behavior or we feel compelled to exclude you permanently")
            except fortnitepy.Forbidden:
                await ctx.send("I can't kick that user because I am not party leader")
            except AttributeError:
                await ctx.send("Couldn't find that user.")
    else:
        await ctx.send(f'No member was given. try: {prefix}kick (user)')



@client.command()
@is_admin()
async def promote(ctx, *, member = None):
    if member is None:
        user = await client.fetch_profile(ctx.message.author.id)
        member = client.party.members.get(user.id)
    if member is not None:
        user = await client.fetch_profile(member.display_name)
        member = client.party.members.get(user.id)
    try:
        await member.promote()
        await ctx.send(f"Promoted: {member.display_name}")
    except fortnitepy.Forbidden:
        await ctx.send("Client is not party leader")
    except fortnitepy.PartyError:
        await ctx.send("That person is already party leader")
    except fortnitepy.HTTPException:
        await ctx.send("Something went wrong trying to promote that member")
    except AttributeError:
        await ctx.send("I could not find that user")



@client.command()
@is_admin()
async def privacy(ctx, setting = None):
    if setting is not None:
        try:
            if setting.lower() == 'public':
                await client.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                await ctx.send(f"Party Privacy set to: Public")
            elif setting.lower() == 'friends':
                await client.party.set_privacy(fortnitepy.PartyPrivacy.FRIENDS)
                await ctx.send(f"Party Privacy set to: Friends Only")
            elif setting.lower() == 'private':
                await client.party.set_privacy(fortnitepy.PartyPrivacy.PRIVATE)
                await ctx.send(f"Party Privacy set to: Private")
            else:
                await ctx.send("That is not a valid privacy setting. Try: Public, Friends, or Private")
        except fortnitepy.Forbidden:
            await ctx.send("I can not set the party privacy because I am not party leader.")
    else:
        await ctx.send(f"No privacy setting was given. try: {prefix}privacy (Public, Friends, Private)")



@client.command()
@is_admin()
async def join(ctx, *, member = None):
    try:
        if member is None:
            user = await client.fetch_profile(ctx.message.author.id)
            friend = client.get_friend(user.id)
        elif member is not None:
            user = await client.fetch_profile(member)
            friend = client.get_friend(user.id)

        await friend.join_party()
        await ctx.send(f"Joined {friend.display_name}'s party.")
    except fortnitepy.Forbidden:
        await ctx.send("I can not join that party because it is private.")
    except fortnitepy.PartyError:
        await ctx.send("That user is already in the party.")
    except fortnitepy.HTTPException:
        await ctx.send("Something went wrong joining the party")
    except AttributeError:
        await ctx.send("I can not join that party. Are you sure I have them friended?")
        


@client.command()
@is_admin()
async def invite(ctx, *, member=None):
    if member == 'all':
        friend = client.friends
        invited = []

        try:
            for friend in friend:
                if friend.is_online():
                    invited.append(friend.display_name)
                    await friend.invite()

            await ctx.send(f"Invited {len(invited)} friends to the party.")

        except Exception:
            pass

    else:
        try:
            if member is None:
                user = await client.fetch_profile(ctx.message.author.id)
                friend = client.get_friend(user.id)
            if member is not None:
                user = await client.fetch_profile(member)
                friend = client.get_friend(user.id)

            await friend.invite()
            await ctx.send(f"Invited {friend.display_name} to the party.")
        except fortnitepy.PartyError:
            await ctx.send("That user is already in the party.")
        except fortnitepy.HTTPException:
            await ctx.send("Something went wrong inviting that user.")
        except AttributeError:
            await ctx.send("I can not invite that user. Are you sure I have them friended?")
        except Exception:
            pass



@client.command()
@is_admin()
async def add(ctx, *, member = None):
    if member is not None:
        try:
            user = await client.fetch_profile(member)
            friends = client.friends

            if user.id in friends:
                await ctx.send(f"I already have {user.display_name} as a friend")
            else:
                await client.add_friend(user.id)
                await ctx.send(f'Sent a friend request to {user.display_name}')
                print(Fore.LIGHTCYAN_EX + ' • ' + Fore.RESET + 'Sent a friend request to: ' + Fore.LIGHTBLACK_EX + f'{user.display_name}')

        except fortnitepy.HTTPException:
            await ctx.send("There was a problem trying to add this friend.")
        except AttributeError:
            await ctx.send("I can't find a player with that name.")
    else:
        await ctx.send(f"No user was given. try: {prefix}add (user)")



@client.command()
@is_admin()
async def remove(ctx, *, friend = None):
    if friend is not None:
        if friend.lower() == 'all':
            await ctx.send("Are you sure you want to remove ALL of the client's friends? (yes/no)")
            response = await client.wait_for('friend_message', timeout=15)
            content = response.content.lower()

            if 'yes' in content.lower():
                await ctx.send("Admin password?")
                res1 = await client.wait_for('friend_message', timeout=15)
                content1 = res1.content.lower()

                if content1.lower() == data['AdminPassword']:
                    try:
                        await client.remove_all_friends()
                        await ctx.send(f'Successfully removed all friends.')
                        print(Fore.LIGHTCYAN_EX + ' • ' + Fore.RESET + "Removed all of the client's friends")
                    except fortnitepy.HTTPException:
                        await ctx.send("There was an error trying to remove all friends")
                else:
                    ctx.send("That password is not correct. Kept all of the client's friends")
            elif 'no' in content.lower():
                await ctx.send('Kept all friends.')
            else:
                await ctx.send('That is not a valid response. Kept all friends.')

        else:
            try:
                user = await client.fetch_profile(friend)
                friends = client.friends

                if user.id in friends:
                    await client.remove_or_decline_friend(user.id)
                    await ctx.send(f'Successfully removed {user.display_name} as a friend.')
                    print(Fore.LIGHTCYAN_EX + ' • ' + Fore.RESET + 'Removed ' + Fore.LIGHTBLACK_EX + f'{user.display_name}' + Fore.RESET + ' as a friend.')
                else:
                    await ctx.send(f"I don't have {user.display_name} added as a friend.")
            except fortnitepy.HTTPException:
                await ctx.send("There was an error trying to remove that friend.")
            except AttributeError:
                await ctx.send("I can't find a player with that name.")
    else:
        await ctx.send(f"No user was given. try: {prefix}remove (friend)")


@client.command()
@is_admin()
async def block(ctx, *, user = None):
    if user is not None:
        try:
            user = await client.fetch_profile(user)
            friends = client.friends

            if user.id in friends:
                try:
                    await user.block()
                    await ctx.send(f"Blocked {user.display_name}")
                except fortnitepy.HTTPException:
                    await ctx.send("Something went wrong trying to block that user.")

            elif user.id in client.blocked_users:
                await ctx.send(f"I already have {user.display_name} blocked.")
        except AttributeError:
            await ctx.send("I can't find a player with that name.")
    else:
        await ctx.send(f"No user was given. try: {prefix}block (friend)")



@client.command()
@is_admin()
async def blocked(ctx):

    blockedusers = []

    for b in client.blocked_users:
        user = client.get_blocked_user(b)
        blockedusers.append(user.display_name)
    
    await ctx.send(f'Client has {len(blockedusers)} users blocked:')
    for x in blockedusers:
        if x is not None:
            await ctx.send(x)



@client.command()
@is_admin()
async def unblock(ctx, *, user = None):
    if user is not None:
        try:
            member = await client.fetch_profile(user)
            blocked = client.blocked_users
            if member.id in blocked:
                try:
                    await client.unblock_user(member.id)
                    await ctx.send(f'Successfully unblocked {member.display_name}')
                except fortnitepy.HTTPException:
                    await ctx.send('Something went wrong trying to unblock that user.')
            else:
                await ctx.send('That user is not blocked')
        except AttributeError:
            await ctx.send("I can't find a player with that name.")
    else:
        await ctx.send(f'No user was given. try: {prefix}unblock (blocked user)')
    


@client.command()
async def friends(ctx: fortnitepy.ext.commands.Context) -> None:
    onlineFriends = []
    offlineFriends = []

    try:
        for friend in client.friends:
            if friend.is_online():
                onlineFriends.append(friend.display_name)
            else:
                offlineFriends.append(friend.display_name)

        await ctx.send(f"Bot has {lenFriends()} Friends and {len(onlineFriends)} are Online!")

        if ctx.author.id in info['FullAccess']:
            print(Fore.LIGHTCYAN_EX + ' • ' + Fore.RESET + "Friends List: " + Fore.GREEN + f'{len(onlineFriends)} Online ' + Fore.RESET + "/" + Fore.LIGHTBLACK_EX + f' {len(offlineFriends)} Offline ' + Fore.RESET + "/" + Fore.LIGHTWHITE_EX + f' {len(onlineFriends) + len(offlineFriends)} Total')

            for x in onlineFriends:
                if x is not None:
                    print(Fore.GREEN + " • " + x)
            for x in offlineFriends:
                if x is not None:
                    print(Fore.LIGHTBLACK_EX + " • " + x)
    except Exception:
        pass

    else:
        pass



@is_admin()
@client.command(aliases=['cc'],)
async def crown(ctx: fortnitepy.ext.commands.Context, amount = None):
    meta = client.party.me.meta
    data = (meta.get_prop('Default:AthenaCosmeticLoadout_j'))['AthenaCosmeticLoadout']

    if amount is not None:
        try:
            data['cosmeticStats'][1]['statValue'] = int(amount)
        except KeyError:
            data['cosmeticStats'] = [{"statName": "TotalVictoryCrowns", "statValue": int(amount)},
                                     {"statName": "TotalRoyalRoyales", "statValue": int(amount)},
                                     {"statName": "HasCrown", "statValue": 0}]

        final = {'AthenaCosmeticLoadout': data}
        key = 'Default:AthenaCosmeticLoadout_j'
        prop = {key: meta.set_prop(key, final)}

        await client.party.me.patch(updated=prop)

        await asyncio.sleep(0.2)
        await ctx.send(f'Set {int(amount)} Crown')
        await client.party.me.clear_emote()
        await client.party.me.set_emote('EID_Coronet')

    else:
        await ctx.send(f"No amount was given. try: {prefix}crown (crown amount)")



@client.command()
@is_admin()
async def members(ctx):
    pmembers = client.party.members
    partyMembers = []
    
    for m in pmembers:
        member = client.get_user(m)
        partyMembers.append(member.display_name)
    
    await ctx.send(f"There are {len(partyMembers)} members in {client.user.display_name}'s party:")
    for x in partyMembers:
        if x is not None:
            await ctx.send(x)



@client.command()
@is_admin()
async def id(ctx, *, user = None):
    if user is not None:
        user = await client.fetch_profile(user)
    
    elif user is None:
        user = await client.fetch_profile(ctx.message.author.id)

    try:
        await ctx.send(f"{user}'s Epic ID is: {user.id}")
        print(Fore.LIGHTCYAN_EX + ' • ' + Fore.RESET + f"{user}'s Epic ID is: " + Fore.LIGHTBLACK_EX + f'{user.id}')
    except AttributeError:
        await ctx.send("I couldn't find an Epic account with that name.")



@client.command()
@is_admin()
async def user(ctx, *, user = None):
    if user is not None:
        user = await client.fetch_profile(user)

        try:
            await ctx.send(f"The ID: {user.id} belongs to: {user.display_name}")
            print(Fore.LIGHTCYAN_EX + ' • ' + Fore.RESET + f'The ID: {user.id} belongs to: ' + Fore.LIGHTBLACK_EX + f'{user.display_name}')
        except AttributeError:
            await ctx.send(f"I couldn't find a user that matches that ID")
    else:
        await ctx.send(f'No ID was given. try: {prefix}user (ID)')



@client.command()
async def admin(ctx, setting = None, *, user = None):
    if (setting is None) and (user is None):
        await ctx.send(f"Missing one or more arguments. try: {prefix}admin (add, remove, list) (user)")
    elif (setting is not None) and (user is None):

        user = await client.fetch_profile(ctx.message.author.id)

        if setting.lower() == 'add':
            if user.id in info['FullAccess']:
                await ctx.send("You are already an admin")

            else:
                await ctx.send("Password?")
                response = await client.wait_for('friend_message', timeout=20)
                content = response.content.lower()
                if content == data['AdminPassword']:
                    info['FullAccess'].append(user.id)
                    with open('info.json', 'w') as f:
                        json.dump(info, f, indent=4)
                        await ctx.send(f"Correct. Added {user.display_name} as an admin.")
                        print(Fore.LIGHTCYAN_EX + " • " + Fore.LIGHTCYAN_EX + user.display_name + Fore.RESET + " was added as an admin.")
                else:
                    await ctx.send("Incorrect Password.")

        elif setting.lower() == 'remove':
            if user.id not in info['FullAccess']:
                await ctx.send("You are not an admin.")
            else:
                await ctx.send("Are you sure you want to remove yourself as an admin?")
                response = await client.wait_for('friend_message', timeout=20)
                content = response.content.lower()
                if (content.lower() == 'yes') or (content.lower() == 'y'):
                    info['FullAccess'].remove(user.id)
                    with open('info.json', 'w') as f:
                        json.dump(info, f, indent=4)
                        await ctx.send("You were removed as an admin.")
                        print(Fore.BLUE + " • " + Fore.LIGHTBLUE_EX + user.display_name + Fore.RESET + " was removed as an admin.")
                elif (content.lower() == 'no') or (content.lower() == 'n'):
                    await ctx.send("You were kept as admin.")
                else:
                    await ctx.send("Not a correct reponse. Cancelling command.")
                
        elif setting == 'list':
            if user.id in info['FullAccess']:
                admins = []

                for admin in info['FullAccess']:
                    user = await client.fetch_profile(admin)
                    admins.append(user.display_name)

                await ctx.send(f"The bot has {len(admins)} admins:")

                for admin in admins:
                    await ctx.send(admin)

            else:
                await ctx.send("You don't have permission to this command.")

        else:
            await ctx.send(f"That is not a valid setting. try: {prefix}admin (add, remove, list) (user)")
            
    elif (setting is not None) and (user is not None):
        user = await client.fetch_profile(user)

        if setting.lower() == 'add':
            if ctx.message.author.id in info['FullAccess']:
                if user.id not in info['FullAccess']:
                    info['FullAccess'].append(user.id)
                    with open('info.json', 'w') as f:
                        json.dump(info, f, indent=4)
                        await ctx.send(f"Correct. Added {user.display_name} as an admin.")
                        print(Fore.LIGHTCYAN_EX + " • " + Fore.LIGHTCYAN_EX + user.display_name + Fore.RESET + " was added as an admin.")
                else:
                    await ctx.send("That user is already an admin.")
            else:
                await ctx.send("You don't have access to add other people as admins. Try just: !admin add")
        elif setting.lower() == 'remove':
            if ctx.message.author.id in info['FullAccess']:
                if user.id in info['FullAccess']:
                    await ctx.send("Password?")
                    response = await client.wait_for('friend_message', timeout=20)
                    content = response.content.lower()
                    if content == data['AdminPassword']:
                        info['FullAccess'].remove(user.id)
                        with open('info.json', 'w') as f:
                            json.dump(info, f, indent=4)
                            await ctx.send(f"{user.display_name} was removed as an admin.")
                            print(Fore.BLUE + " • " + Fore.LIGHTBLUE_EX + user.display_name + Fore.RESET + " was removed as an admin.")
                    else:
                        await ctx.send("Incorrect Password.")
                else:
                    await ctx.send("That person is not an admin.")
            else:
                await ctx.send("You don't have permission to remove players as an admin.")
        else:
            await ctx.send(f"Not a valid setting. try: {prefix}admin (add, remove) (user)")


if (data['email'] and data['password']) and (data['email'] != "" and data['password'] != ""):
    try:
        client.run()
    except fortnitepy.errors.AuthException as e:
        print(Fore.RED + ' • [ERROR] ' + Fore.RESET + f'{e}')
    except ModuleNotFoundError:
        print(e)
        print(Fore.RED + f' • ' + Fore.RESET + 'Failed to import 1 or more modules. Run "INSTALL PACKAGES.bat')
        exit()
else:
    print(Fore.RED + ' • [ERROR] ' + Fore.RESET + 'Can not log in, as no accounts credentials were provided.')
    
