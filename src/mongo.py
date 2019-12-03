#!/usr/bin/python3

import datetime
from pymongo import MongoClient
import getpass
import json
import os
import ssl
from dotenv import load_dotenv
from bson.objectid import ObjectId


def get_ids(chat_list, key):
    ''' Translate numbers to ObjectsId in origal collection'''

    return [ObjectId() for _ in range(max([d[key] for d in chat_list]) + 1)]

class Db:
    ''' initialize mongo client and its collections which are chats, users, rooms'''
    def __init__(self, database, chat_col, user_col, room_col):
        load_dotenv()
        url = os.getenv('MONGO_PASSWORD_KEY')
        self.db = MongoClient(url, ssl_cert_reqs=ssl.CERT_NONE)[database]
        self.chats = self.db[chat_col]
        self.users = self.db[user_col]
        self.rooms = self.db[room_col]

    def create_chat_collection(self):
        '''Fills the database collections with their initial values extracted from the input file'''
        with open('./input/chats.json') as f:
            chats_json = json.load(f)
            user_id_list = get_ids(chats_json, 'idUser')
            chat_id_list = get_ids(chats_json, 'idChat')
            chats = []
            for c in chats_json:
                c.pop('idMessage')
                user_id_int = c.pop('idUser')
                c['idUser'] = user_id_list[user_id_int]
                chat_id_int = c.pop('idChat')
                c['idChat'] = chat_id_list[chat_id_int]
                chats.append(c)
            if not self.chats.count_documents({}):
                self.chats.insert_many(chats)
                users = list({v['_id']: v for v in [{'_id': d['idUser'], 'name': d['userName']}
                                                    for d in chats_json]}.values())
                self.users.insert_many(users)
                rooms = {}
                for element in [{'_id': d['idChat'], 'participant': d['idUser']}for d in chats_json]:
                    if rooms.get(element['_id']):
                        if element['participant'] not in rooms.get(element['_id']):
                            rooms[element['_id']].append(element['participant'])
                        else:
                            rooms[element['_id']] = [element['participant']]
                        
                rooms = [{'_id':k, 'participants': v} for k, v in rooms.items()]
                self.rooms.insert_many(rooms)

        
    def create_user(self, user_name):
        '''Inserts a new user into the Users collection using the provided name'''
        if not self.users.find_one({'name': user_name}):
            return self.users.insert_one({'name': user_name}).inserted_id
        return None

    def create_conversation(self, user_names):
        '''Inserts new conversation in rooms'''
        users = []
        for n in user_names:
            u = self.users.find_one({'name': n})
            if not u:
                users.append(self.create_user(n))
                u = self.users.find_one({'name': n})
            else:
                users.append(u)
        if not self.rooms.find_one({
            '$and': [{'participants': {'$elemMatch': u}} for u in users]
        }):
            return self.rooms.insert_one({'participants': [u['_id'] for u in users]}).inserted_id
        return None

    def add_message(self, user_name, chat_id, message):
        ''' Adds a new message in chat collection''' 
        user = self.users.find_one({'name': user_name})
        if user:
            return self.chats.insert_one({
                'idUser': user['_id'],
                'userName': user_name,
                'idChat': ObjectId(chat_id),
                'datetime': datetime.datetime.utcnow(),
                'text': message
            }).inserted_id

    def get_messages(self, chat_id):
        ''' Returns messages from chat collection''' 
        return [m for m in self.chats.find({'idChat': ObjectId(chat_id)})]




