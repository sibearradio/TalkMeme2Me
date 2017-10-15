# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
import random
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient

from PIL import Image
import pytesseract
import requests
from io import BytesIO

import re

client = MongoClient("mongodb://danklords:hackny2017@dankmemebank-shard-00-00-tbdbz.mongodb.net:27017,dankmemebank-shard-00-01-tbdbz.mongodb.net:27017,dankmemebank-shard-00-02-tbdbz.mongodb.net:27017/admin?replicaSet=DankMemeBank-shard-0&ssl=true")
db=client.DankBank
app = Flask(__name__)
@app.route("/", methods=['GET', 'POST'])



def hello_world():
    def ocr(url):

        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        text = pytesseract.image_to_string(img, lang = 'eng')
        re.sub('[^A-Za-z0-9]+', '', text)

        return "Text Recognition Feature 'Alpha':\n" + text 

    """Respond and greet the caller by name."""
    # Try adding your own number to this list!
    db_len = db.DankBank.count()
    r = random.randint(1,db_len)
    db2 = client.users
    message = request.values.get('Body',None)
    count = db.DankBank.find().limit(-1).skip(r).next();
    from_number = request.values.get('From', None)
    query = {"url":count['url']}
    duplicates = db.users.find(query)
    if(duplicates != []):
        r = random.randint(1,db_len)        
    if(message=="Balance" or message == "balance"):
        query = {"phone":from_number}
        string = ""
        balance = db.users.find(query)
        amount = db.users.find(query).count()
        resps=MessagingResponse()
        for meme in balance:
            string = string + "\n" + str(meme['url'])
        msg= resps.message("Here are all your links!:" + string +"\n"+ "Total Balance: " + str(amount) +  " Dank Memes")
        return str(resps)
        
    else:        
        img_url = count['url']
        print(count['url'])
        ocr = ocr(img_url)
        # print(ocr)
        resp = MessagingResponse()
        msg = resp.message("One dank meme coming right up!" + "Description: "  + count['description']  + "\n"+ocr + " \n"+ str(count['url']) )
        print(count['url'])
    
        message = request.values.get('Body',None)
        from_number = request.values.get('From', None)
        db.users.insert({"phone" : from_number , "url": count['url']})
        return str(resp)
if __name__ == "__main__":
    app.run(debug=True)