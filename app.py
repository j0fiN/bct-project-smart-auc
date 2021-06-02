from flask import Flask, request, render_template, redirect, url_for
import os
from dotenv import load_dotenv
import pendulum as pen
from ds import *
import json
import requests as req
load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'abcd1234'
MY_KEY = rsakeys()

def get_block():
    res = req.get("https://web3api.j0fin.repl.co/api/latest")
    return res.json()

def generate_keys():
    pub_key = list()
    for i in range(4):
        strs = str(rsakeys()[1])[:6] + "..."
        pub_key.append(strs)
    return pub_key


def hash(string):
    import hashlib
    encoded=string.encode()
    result = hashlib.sha256(encoded)
    return result.hexdigest()

def get_current_datetime():
    return [
        pen.now().to_day_datetime_string(),
        pen.now().subtract(minutes=2).to_day_datetime_string(),
        pen.now().subtract(minutes=4).to_day_datetime_string(),
        pen.now().subtract(minutes=6).to_day_datetime_string(),
    ]

def details():
    return [{
        "s": 1,
        "name": "Ming vase",
        "des": "A Ming vase from the Yongle dynasty, when the porcelain reached its most refined form.", 
        "hash": "652...",
        "audience": "600",
        "bidders": "20",
        "auctioneer": "Anish Giri"
    }, {
        "s": 2,
        "name": "The Starry Night Painting",
        "des": "The Starry Night is an oil on canvas painting by Dutch Post-Impressionist painter Vincent van Gogh. Painted in June 1889.", 
        "hash": "07d...",
        "audience": "400",
        "bidders": "10",
        "auctioneer": "Jagdeesh Singh"
    }, {
        "s": 3,
        "name": "1990 Porsche Cabriolet",
        "des": "The Porsche 964 is the company's internal name for the Porsche 911 manufactured and sold between 1989 and 1994.", 
        "hash": "d02...",
        "audience": "600",
        "bidders": "20",
        "auctioneer": "Levy Rosman"
    }, {
        "s": 4,
        "name": "Audemars Piguet Watch",
        "des": "Inspired by the Black Panther's cutting-edge suit, the sandblasted titanium case presents a textured look with satin-brushed and polished titanium inserts.", 
        "hash": "fe7...",
        "audience": "1800",
        "bidders": "50",
        "auctioneer": "Sanjay Raina"
    }
    ]
def create_bidder_and_save():

    BIDDER_DATA = [
            {
                "date": pen.now().to_day_datetime_string(),
                "bid": "1.6cr",
                "bidder": "Samay Ritish",
                "public_key": str(rsakeys()[1])[:6] + "...",
                "calls": 2
            },
            {
                "date": pen.now().subtract(minutes=2).to_day_datetime_string(),
                "bid": "1.4cr",
                "bidder": "Sneha Rahul",
                "public_key": str(rsakeys()[1])[:6] + "...",
                "calls": 1
            },
            {
                "date": pen.now().subtract(minutes=4).to_day_datetime_string(),
                "bid": "1.3cr",
                "bidder": "Robert Hess",
                "public_key": str(rsakeys()[1])[:6] + "...",
                "calls": 2
            },
            {
                "date": pen.now().subtract(minutes=6).to_day_datetime_string(),
                "bid": "1.2cr",
                "bidder": "Varun Aditya",
                "public_key": str(rsakeys()[1])[:6] + "...",
                "calls": 1
            }
        ]
    with open('data.json', 'w') as f:
        json.dump({"data":BIDDER_DATA}, f, indent=4)

def add_bidder_data(bid):
    BIDDER_DATA = [
            {
                "date": pen.now().to_day_datetime_string(),
                "bid": "1.6cr",
                "bidder": "Samay Ritish",
                "public_key": str(rsakeys()[1])[:6] + "...",
                "calls": 2
            },
            {
                "date": pen.now().subtract(minutes=2).to_day_datetime_string(),
                "bid": "1.4cr",
                "bidder": "Sneha Rahul",
                "public_key": str(rsakeys()[1])[:6] + "...",
                "calls": 1
            },
            {
                "date": pen.now().subtract(minutes=4).to_day_datetime_string(),
                "bid": "1.3cr",
                "bidder": "Robert Hess",
                "public_key": str(rsakeys()[1])[:6] + "...",
                "calls": 2
            },
            {
                "date": pen.now().subtract(minutes=6).to_day_datetime_string(),
                "bid": "1.2cr",
                "bidder": "Varun Aditya",
                "public_key": str(rsakeys()[1])[:6] + "...",
                "calls": 1
            }
        ]
    BIDDER_DATA.insert(0,
                    {
                        "date": pen.now().subtract(minutes=6).to_day_datetime_string(),
                        "bid": bid,
                        "bidder": "Jofin Archbald",
                        "public_key": str(rsakeys()[1])[:6] + "...",
                        "calls": 1
                    })
    BIDDER_DATA.pop()
    with open('data.json', 'w') as f:
        json.dump({"data":BIDDER_DATA}, f, indent=4)

def bidder():
    with open('data.json', 'r') as f:
        return json.load(f)['data']

@app.get('/')
def home():
    create_bidder_and_save()
    return render_template('index.html', list = [hash("Ming vase"), 
                                                hash("Starry Night Painting"), 
                                                hash("1990 Porsche Cabriolet"), 
                                                hash("Audemars Piguet Watch")])

@app.get('/auctions/<index>')
def auction(index):
    if int(index) <= 3:
        return render_template('user_page.html',
                                index=index, 
                                details=details()[int(index)], 
                                date=get_current_datetime(),
                                pubkey=generate_keys(),
                                data=bidder())
    else:
        return render_template('user_page.html',
                                index=index,
                                details=details()[0], 
                                date=get_current_datetime(),
                                pubkey=generate_keys(),
                                data=bidder())


@app.get('/new/<a>/<price>')
def new_bidder(a, price):
    add_bidder_data(price + "cr")
    print(a, price)
    return "Done"


@app.get('/transaction/<index>')
def transaction(index):
    if int(index) <= 3:
        return render_template('trans.html', 
                                block=get_block(),
                                details=details()[int(index)])
    else:
        return render_template('trans.html', 
                                block=get_block(),
                                details=details()[0])


if __name__ == "__main__":
    app.run(debug=True)