import json
import Settings

global id
id = 0


def Add(CBID: str, Cypto: str, Paid: float, Size: float, Breakeven: float, OldPrice: float, TrailStop: float, TrailDistance: float, Strat: str):
    global id
    Trades["trade" + str(id)] = {
        "id": CBID,
        "Cypto" : Cypto,
        "Paid": Paid,
        "Size": Size,
        "Breakeven": Breakeven,
        "Old_Price": OldPrice,
        "Trail_Stop": TrailStop,
        "Trail_Distance": TrailDistance,
        "Sell_Order": False,
        "Sell_Order_ID": "",
        "Sell_Percentage": 0.3,
        "Strat" : Strat
    }
    print(Trades["trade" + str(id)])
    id = id + 1
    Save()


def Save():
    jsonD = json.dumps(Trades, indent=2, sort_keys=True)
    f = open("Trades.json", "w")
    f.write(jsonD)
    C = open("Id.txt", "w")
    C.write(str(id))
    f.close()


try:
    with open("Trades.json", "r") as json_file:
        Trades = json.load(json_file)
    with open('Id.txt') as f:
        for line in f:
            int_list = [int(i) for i in line.split()]
            id = int(int_list[0])
except:
    Trades = {
        "TradeTemp_" + Settings.Cypto_GBP: {
            "id": 0,
            "Cypto" : Settings.Cypto_GBP,
            "Paid": 0,
            "Size": 0,
            "Breakeven": 0,
            "Old_Price": 0,
            "Trail_Stop": 0,
            "Trail_Distance": 0,
            "Sell_Order": False,
            "Sell_Order_ID": "0",
            "Sell_Percentage": 0.5,
            "Strat": ""
        },

        "TradeTemp_" + Settings.Cypto_USDC: {
            "id": 0,
            "Cypto": Settings.Cypto_USDC,
            "Paid": 0,
            "Size": 0,
            "Breakeven": 0,
            "Old_Price": 0,
            "Trail_Stop": 0,
            "Trail_Distance": 0,
            "Sell_Order": False,
            "Sell_Order_ID": "0",
            "Sell_Percentage": 0.5,
            "Strat": ""
        },

        "TradeTemp_" + Settings.Cypto_EUR: {
            "id": 0,
            "Cypto": Settings.Cypto_EUR,
            "Paid": 0,
            "Size": 0,
            "Breakeven": 0,
            "Old_Price": 0,
            "Trail_Stop": 0,
            "Trail_Distance": 0,
            "Sell_Order": False,
            "Sell_Order_ID": "0",
            "Sell_Percentage": 0.5,
            "Strat": ""
        },

        "TradeTemp_" + Settings.Cypto_USDC2: {
            "id": 0,
            "Cypto": Settings.Cypto_USDC2,
            "Paid": 0,
            "Size": 0,
            "Breakeven": 0,
            "Old_Price": 0,
            "Trail_Stop": 0,
            "Trail_Distance": 0,
            "Sell_Order": False,
            "Sell_Order_ID": "0",
            "Sell_Percentage": 0.5,
            "Strat": ""
        }
    }
    Save()

