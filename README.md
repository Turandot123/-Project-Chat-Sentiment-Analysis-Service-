# Project-Chat-Sentiment-Analysis-Service

A.Introduction 

The proyect developed creates an API which works in local. It takes the messages from a slack chat and makes modifications to the initial messages by adding users, messages, chats and also analyses user sentiment per chat. I have not been able to complete all the points asked in the class (only L1 to L2)

*** I would like to test the API in postman and also make it public but not sure if I will have time for now ****

B.Execution 

I have used Mongo Atlas to work with the initial set of chats and developed the API in the files under src folder. 

In input folder there is a copy of the initial chats in json.

Main.py executes and runs the entire code (use python3 main.py from console).

Also included a requirements.txt

Regarding the API:

a) creates new users and records them in the data base - with bottle function POST

b) creates new chats - with bottle function POST

c) adds a user message to a chat - with bottle function POST

d) gets a chat content users, messages and date time - with bottle function GET

e) gets chats sentiment analyses sentiment per user within a chat - with bottle function GET


C.How to test results

Since I did not have enough time I have learnt to test my results in the terminal directly using ipython which I found extremelly useful

How I tested: 

Write iptython in console
Execute python3 main.py
Import requests
Import json


1.1. An example type in console:

# Create a user 
respuesta=requests.post('http://localhost:8080/user/create', data=json.dumps({'name':'< insert a name>'}), headers={'Content-Type':'application/json'})

respuesta.json() --> generates a new user (new user Id registered to data base)

# Create a chat 
respuesta = requests.post('http://localhost:8080/chat/create', data=json.dumps({'names': ['< insert name> ', '< insert name >']}), headers={'Content-Type':'application/json'})

respuesta.json() --> generates a new chat (new chat Id registered to data base)

# Adds messages to a chat from a given user
respuesta = requests.post('http://localhost:8080/chat/< insert chat ID >/addmessage', data=json.dumps({'user': '< insert user name >', 'text': '< insert message >'}), headers={'Content-Type':'application/json'})

respuesta.json() --> generates a message Id (message generated and recorded in data base)

# Get list of messages from a chat 

respuesta = requests.get('http://localhost:8080/chat/< insert chat ID>/list')

respuesta.json() --> to get all details about a chat including messages per user and time

# Get sentiment from a given chat 

respuesta = requests.get('http://localhost:8080/chat/< insert chat ID >/sentiment')

respuesta.json()--> to get sentiment analysis in the specific chat ID per user