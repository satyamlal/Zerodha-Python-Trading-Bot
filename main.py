import os
from kiteconnect import KiteConnect
import time, json, datetime, sys
import pandas as pd

try: 
    #Broker Details
    api_key = ""
    access_token = ""

    #strategy parameters
    trade_symbol = "NIFTY"  #NIFTY OR BANKNIFTY

    upper_range = 170
    lower_range = 150
    selection_time = datetime.time(9, 30)

    buy_level = 185
    sl_level = 155
    target_level = 215
    square_off_time = datetime.time(15, 15)

    qty_to_trade = 50

except:
    print("Wrong Input!!")
    sys.exit()


def get_login():
    global kite, api_key, access_token
    try:
        kite = KiteConnect(api_key = api_key)
        kite.set_access_token(access_token)
        kite.margins()
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)
        sys.exit


def get_strike(sysmbol_name):
    global lot_size
    while True:
        try:
            df = pd.DataFrame(kite.intruments())
            df = df[df["name"] == sysmbol_name]
            df = df[df["segment"] == "NFO-OPT"]
            df = df[df["expiry"] == sorted(list(df["expiry"].unique()))[0]]
            lot_size = float(list(df["lot_size"])[0])
            break
        except Exception as e:
            pass
    return [f"NFO: {i}" for i in list(df["tradingSymbols"])]


def place_trade(symbol, quantity, direction):
    try:
        order: kite.place_order(
            variety = kite.VARIETY_REGULAR,
            exchange = symbol[0:3],
            tradingsymbol = symbol[4:],
            transaction_type = kite.TRANSACTION_TYPE_BUY if direction == "BUY" else kite.TRANSACTION_TYPE_SELL,
            quantity = int(quantity),
            
        )
        return order
    except Exception as e:
        return f"{e}"
