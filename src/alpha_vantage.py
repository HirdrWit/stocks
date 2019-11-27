import sys
import random
import requests
import time
from statistics import mean
import json
constants = {
    "range": 0,
    "samples": 500,
    "limit": 365
}


def verify_api_key(key):
    if len(key) < 1:
        sys.exit('No API key')


def get_stock_data(stocks, key):
    constants["range"] = len(stocks)
    random_500 = generate_random_500()
    percent_change_dictionary = {}
    for ran in random_500:
        stock = stocks[ran]
        json_data = request_stock_data(stock, key)
        if json_data == {'Note': 'Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute and 500 calls per day. Please visit https://www.alphavantage.co/premium/ if you would like to target a higher API call frequency.'}:
            print("too many calls, waiting 60 seconds")
            time.sleep(60)
            json_data = request_stock_data(stock, key)

        day = 0
        percent_change_list = []
        temp = []
        percent_change = 0
        try:
            print("Computing: " + stock)
            for val in json_data['Time Series (Daily)']:
                if day < constants["limit"]:
                    high = float(json_data['Time Series (Daily)'][val]['2. high'])
                    low = float(json_data['Time Series (Daily)'][val]['3. low'])
                    percent_change = ((high - low) / low) * 100
                    temp.append(percent_change)
                    if day % 5 == 0 and day > 0:
                        week_pc = mean(temp)
                        temp = []
                        percent_change_list.append(week_pc)
                    day += 1
            print("Results: " + str(mean(percent_change_list)))
            percent_change_dictionary.update({stock: mean(percent_change_list)})
        except KeyError as e:
            print("Could not do this stock. Hell-a lame. Error: " + str(e))

    print(sorted(percent_change_dictionary.items(), key=
    lambda kv: (kv[1], kv[0])))



def generate_random_500():
    ret = random.sample(range(constants["range"]), constants["samples"])
    return ret


def request_stock_data(s, k):
    URL = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&outputsize=full&apikey={}".format(s, k)
    r = requests.get(url=URL)
    data = r.json()
    return data
