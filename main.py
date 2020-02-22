import requests
import time
import config
import datetime

def get_binance(pair):
    url = "https://api.binance.com/api/v3/depth?symbol=" + pair + "&limit=5"

    try:
        r = requests.get(url)
    except Exception as e:
        print("Хуета на бинансе")
        return None
    else:
        dict = r.json()
        return [dict["asks"][0][0], dict["bids"][0][0]]


def get_poloniex(pair):
    url = "https://poloniex.com/public?command=returnOrderBook&currencyPair=" + pair + "&depth=1"
    try:
        r = requests.get(url)
    except Exception as e:
        print("Хуета на poloniex")
        return None
    else:
        dict = r.json()
        return [dict["asks"][0][0], dict["bids"][0][0]]


def analitic(list_poloniex, list_binance, key):
    if not (list_poloniex[0] or list_poloniex[1] or list_binance[0] or list_binance[1]):
        return None
    asks_pol = float(list_poloniex[0])
    bids_pol = float(list_poloniex[1])

    asks_bin = float(list_binance[0])
    bids_bin = float(list_binance[1])
    response = ""
    bin_to_pol = (bids_bin/asks_pol-1)*100
    pol_to_bin = (bids_pol/asks_bin-1)*100
    if bin_to_pol > 0.01:
        write_to_file("POLONIEX", "BINANCE", key, str(bin_to_pol))
        return "Можно купить " + key + " на POLONIEX и продать на BINANCE\nРазница:" + str(bin_to_pol) + "%\n\n"
    elif pol_to_bin > 0.01:
        write_to_file("BINANCE", "POLONIEX", key, str(pol_to_bin))
        return "Можно купить " + key + " на BINANCE и продать на POLONIEX\nРазница:" + str(pol_to_bin) + "%\n\n"
    else:
        return None


def write_to_file(where_buy, where_sell, pair, percent):
    with open(config.OUTPUT_FILENAME, "a") as fileobj:
        datet = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        string = datet + "," + where_buy + "," + where_sell + "," + pair + "," + percent + "\n"
        fileobj.write(string)

while(True):
    for key in config.PAIRS_POLONIEX.keys():
        re = analitic(get_poloniex(config.PAIRS_POLONIEX[key]), get_binance(config.PAIRS_BINANCE[key]), key)
        print(re)
    time.sleep(0.1)
