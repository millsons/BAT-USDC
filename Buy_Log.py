Buys = {
    "TradeTemp": {
        "id": 0,
        "Strat": "",
    }}
id =0

def Add(CBID: str, Strat: str):
    global id
    Buys["trade" + CBID] = {
        "id": CBID,
        "Strat": Strat,
    }
    id = id + 1