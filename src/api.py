import json
from bottle import Bottle, get, post, request, response

from .mongo import Db
from .configuration import Configuration
from .sentiment import Sentiment

app = Bottle()
db = Db(Configuration.DATABASE, chat_col=Configuration.CHAT, user_col=Configuration.USERS, room_col=Configuration.ROOMS)
sentiment = Sentiment()


@app.post('/user/create')
def create_user():
    data = request.json
    print(data)
    if not data or not data.get('name'):
        response.status = 400
        return json.dumps({'error': f'invalid data: {data}'})
    return json.dumps({'user_id': str(db.create_user(data['name']))})


@app.post("/chat/create")
def create_conversation():
    data = request.json
    if not data or not data.get('names') or len(data.get('names')) < 2:
        response.status = 400
        return json.dumps({'error': f'invalid data: {data}'})
    return json.dumps({'chat_id': str(db.create_conversation(data['names']))})


@app.post("/chat/<chat_id>/addmessage")
def add_message(chat_id):
    data = request.json
    if not data or not data.get('user') or not data.get('text'):
        response.status = 400
        return json.dumps({'error': f'invalid data: {data}'})
    result = db.add_message(user_name=data['user'], chat_id=chat_id, message=data['text'])
    if not result:
        response.status = 400
        return json.dumps({'error': 'user does not exist'})
    return json.dumps({'message_id': str(result)})


@app.get("/chat/<chat_id>/list")
def list_chat(chat_id):
    return json.dumps({'chat': [{**m, 'datetime': str(m['datetime']), '_id': str(m['_id']), 'idUser': str(m['idUser']), 'idChat': str(m['idChat'])} for m in db.get_messages(chat_id)]})


@app.get("/chat/<chat_id>/sentiment")
def sentiment_chat(chat_id):
    return json.dumps({
        'sentiment_analysis': [{
            '_id': str(m['_id']),
            'userName': m['userName'],
            'sentiment': sentiment.classify(m['text'])
        } for m in db.get_messages(chat_id)]
    })

