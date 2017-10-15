import serial
from twilio.rest import Client
from flask import Flask, request
from pymongo import MongoClient
app = Flask(__name__)
@app.route("/", methods=['GET', 'POST'])

def main():

    client = MongoClient("mongodb://danklords:hackny2017@dankmemebank-shard-00-00-tbdbz.mongodb.net:27017,dankmemebank-shard-00-01-tbdbz.mongodb.net:27017,dankmemebank-shard-00-02-tbdbz.mongodb.net:27017/admin?replicaSet=DankMemeBank-shard-0&ssl=true")
    db = client.DankBank
    userList = db.users.find()
    number = []

    for user in userList:
        number.append(user['phone'])
    number = list(set(number))
    print(number)
    account_sid = "ACa742e26aac70bdb3d640b0ad8ce2f7fc"
    auth_token = "94fa41be0ad7cf7a2eb55e25fe662030"
    tw_client = Client(account_sid, auth_token)
    ser = serial.Serial("/dev/tty.usbmodemFA131", 9600)
    while True:
        arduinoData = ser.readline().strip()
        print(arduinoData)
        if b"nuke" in arduinoData:
            nuke(number, tw_client)
        else:
            print("hi?")


def nuke(numList, tw_client):
    for number in numList:
        message = tw_client.messages.create(number,from_="+19733106543",body = "Hope you enjoyed our DankBank product!\n", media_url="https://media.giphy.com/media/lgcUUCXgC8mEo/giphy.gif")
#    print(message.sid)
    print("working")


if __name__ == "__main__":
    main()
    app.run(debug=True)


