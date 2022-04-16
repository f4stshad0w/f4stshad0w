import json, config
from flask import Flask, request, jsonify, render_template
from binance.client import Client
from binance.enums import *

import json
from types import SimpleNamespace

import requests


app = Flask(__name__)

client = Client(config.TEST_API_KEY, config.TEST_API_SECRET, tld='com')

# private method: it sends message through telegram bot
def __telegramMessage(m):
    # telegram bot "algotrading123456bot" token 
    TOKEN = "5361138079:AAHO1suifkTV3DsgzD41xtaOakcVOi9PMJg"
    # To find chat_id => https://api.telegram.org/bot{TOKEN}/getUpdates https://api.telegram.org/bot5361138079:AAHO1suifkTV3DsgzD41xtaOakcVOi9PMJg/getUpdates
    #chat_id = "114698014" #personal chat
    chat_id = "-1001738112635" #group chat
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={m}"
    r = requests.get(url)
    #print(r.json())

def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print(f"sending order {order_type} - {side} {quantity} {symbol}")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return order

@app.route('/ciao')
def hello_world():
    try: 
        pippo = client.get_account()
        text = (format(pippo["balances"][0]))
        objectJSON = json.loads(json.dumps(pippo), object_hook=lambda d: SimpleNamespace(**d))
        #testo = ("{}".format(objectJSON))
        __telegramMessage(text) #__telegramMessage(objectJSON.accountType)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False
 
    return objectJSON.accountType
    #return 'Hello, World!'


@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    #print(request.data)
    data = json.loads(request.data)
    
    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        return {
            "code": "error",
            "message": "Nice try, invalid passphrase"
        }

    side = data['strategy']['order_action'].upper()
    quantity = data['strategy']['order_contracts']
    order_response = order(side, quantity, "DOGEUSD")

    if order_response:
        return {
            "code": "success",
            "message": "order executed"
        }
    else:
        print("order failed")

        return {
            "code": "error",
            "message": "order failed"
        }