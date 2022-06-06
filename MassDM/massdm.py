from telethon import TelegramClient, functions, errors
from telethon.sessions import StringSession

import threading
import asyncio
import time
from os import listdir
from os.path import isfile, join
import json
import logging
import csv

logging.basicConfig(filename='bot_log.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%DD/%MM/%YYYY %H:%M:%S',
                    level=logging.DEBUG)

logging.info("@ Starting script")

# logger = logging.getLogger('urbanGUI')

session_path = "./session/"
json_path = "./json/"
members_path = "./members/"

channels_limit = 50
message_sleep = 60

message_start = """Salut """
message_body = """ ça va depuis le temps? \nRegarde le groupe Telegram casino que j’ai trouvé c’est une dinguerie mdrr j’ai pris 3k en même pas 2h c’est de la folie je me sent obligé de le partager à tout mes contacts 😂 \nLeur Telegram : https://t.me/+DIYM_61OpSFlNGI5"""

admin_tom = {'username': 'astucescoinminer'}
admin_jeremy = {'username' : 'damienlexpert'}

async def sendMessage(channel, message, app_id, app_hash, session):

    async with TelegramClient(session_path + session, app_id, app_hash) as client:

        await client.connect()
        me = await client.get_me()

        logging.info("Working with", me.first_name)
        await client.send_message(channel, message, link_preview=True)


def getFilesList(path):
    files = [f for f in listdir(path) if isfile(join(path, f))]
    return files


def main():

    try:


        channels = []
        reader = csv.DictReader(open(members_path + 'members.csv'))
        for i, row in enumerate(reader):
            channels.append(row)

        existing_dicts = set()
        filtered_chanels = []
        for d in channels:
            if (d['user id']) not in existing_dicts and d['username'] != '':
                existing_dicts.add((d['user id']))
                filtered_chanels.append(d)


        for i, row in enumerate(filtered_chanels):
            if i % 10 == 0:
                filtered_chanels.insert(i, admin_tom)
                filtered_chanels.insert(i, admin_jeremy)
        # filtered_chanels = [filtered_chanels.insert(i, admin_tom)  for i, user in enumerate(filtered_chanels) if i % 10 == 0]
        # filtered_chanels = [filtered_chanels.insert(i, admin_jeremy)  for i, user in enumerate(filtered_chanels) if i % 10 == 0]

        # print(filtered_chanels)
        # raise Exception()

        jsons = getFilesList(json_path)

        accounts_used = []

        while True:

            if (not len(jsons)):
                jsons = accounts_used
                accounts_used = []

            for i, account in  enumerate(jsons):


                json_file = open(json_path + account)
                data = json.load(json_file)
                json_file.close()
                app_id = data['app_id']
                app_hash = data['app_hash']
                first_name = data['first_name']
                last_name = data['last_name']

                logging.info(f'@ Account : {app_id} - Name : {last_name} {first_name} ')

                for index, channel in enumerate(filtered_chanels):

                    username = channel['username']
                    logging.info(f'{index}) app id : {app_id} and channel {username} (channels size : {len(filtered_chanels)})')

                    time.sleep(message_sleep)
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    result = loop.run_until_complete(sendMessage(username, message_start + "@" + username + message_body , app_id, app_hash, data['session_file']))


                    if (index % channels_limit == 0 and index > 0) or (len(filtered_chanels) <= channels_limit): 
                        logging.info(f'@ Rotate account every {channels_limit} channels')
                        accounts_used.append(account)
                        jsons.remove(account)
                        del filtered_chanels[:index + 1]
                        break
                        

                if(not len(filtered_chanels)):
                    logging.info('@ All the channels are finish')
                    return
                

            

    except Exception as e:
        logging.info(e)



main()