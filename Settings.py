import json

import Settings
Cypto_Tickers = ["BAT-USDC", "ETH-GBP", "DNT-USDC"]
Cypto_USDC = "BAT-USDC"
Cypto_GBP = "ETH-GBP"
Cypto_EUR = "OMG-EUR"
Cypto_USDC2 = "DNT-USDC"
Channel = ["ticker"]

# Sell side percentages
TwentyUpS = 60
TwentyDownS = 40
TenUpS = 70
TenDownS = 20

Key = "e1cba97f78a63299e3ee44e329d15858"
Secret = "KhOOeDU+EpoA0+xoB+RkxwTmzSzQrw780pzq3fqiYLURiBpVL/H2K/qtv6pI1dvmAYT1LhiSWSbyFa8q81hupg=="
Pass = "xue75slzmbn"

GBP_Account_ID = "d4d6a284-7ee4-45a4-9365-667a0efe4855"

Base_Buy_Percentage = 10
Base_Sell_Percentage = 10





def Save():
    jsonD = json.dumps(Cypto_Settings, indent=2, sort_keys=True)
    f = open("Settings.json", "w")
    f.write(jsonD)
    f.close()


try:
    with open("Settings.json", "r") as json_file:
        Cypto_Settings = json.load(json_file)
except:
    Cypto_Settings = {
        # ETH
        Settings.Cypto_GBP: {
            "RSI_Sell": False,
            "LimitOrder": 0.5,
            "Cypto": Settings.Cypto_GBP,
            "Condition_1": 0.2,
            "TrailStop_Plus": 0.1,
            "SellPrice_Plus": 0.3,
            "MarketSell_Plus": 0.5,
            "Round": 2,
            "Account_Num": "d4d6a284-7ee4-45a4-9365-667a0efe4855",
            "Cancel_Sell": False,

            "canBuy": False,
            "BuyOrder": False,
            "Brought": False,
            "Breakeven": 0,
            "BasePrice": 0,
            "trailStop": 0,
            "Base_Buy_Percentage": 50,
            "Round_Bool": False,
            "Can_Market": True,
            "ID" : "",

            "Direction": "",
            "Direction_Old": 0,
            "Market_Useable": True,
        },

        # BAT
        Settings.Cypto_USDC: {
            "RSI_Sell": False,
            "LimitOrder": "0.0005",
            "Cypto": Settings.Cypto_USDC,
            "Condition_1": "0.00002",
            "TrailStop_Plus": "0.0001",
            "SellPrice_Plus": "0.0003",
            "MarketSell_Plus": "0.0005",
            "Round": 6,
            "Account_Num": "454b39a5-f2e5-400d-baa6-d281bad0bb9c",
            "Cancel_Sell": False,

            "canBuy": False,
            "BuyOrder": False,
            "Brought": False,
            "Breakeven": 0,
            "BasePrice": 0,
            "trailStop": 0,
            "Base_Buy_Percentage": 50,
            "Round_Bool": True,
            "Can_Market": True,
            "Market_Useable": True,
            "ID": "",

            "Direction": "",
            "Direction_Old": 0,

        },
        # Not assigned
        Settings.Cypto_EUR: {
            "RSI_Sell": False,
            "LimitOrder": "0.005",
            "Cypto": Settings.Cypto_EUR,
            "Condition_1": "0.002",
            "TrailStop_Plus": "0.001",
            "SellPrice_Plus": "0.003",
            "MarketSell_Plus": "0.005",
            "Round": 4,
            "Account_Num": "5e0fa8df-6fb2-427e-b9b0-b918d1803771",
            "Cancel_Sell": False,

            "canBuy": False,
            "BuyOrder": False,
            "Brought": False,
            "Breakeven": 0,
            "BasePrice": 0,
            "trailStop": 0,
            "Base_Buy_Percentage": 50,
            "Round_Bool": False,
            "Can_Market": True,
            "Market_Useable": True,
            "ID": "",

            "Direction": "",
            "Direction_Old": 0,
        },

        # DNT
        Settings.Cypto_USDC2: {
            "RSI_Sell": False,
            "LimitOrder": 0.0005,
            "Cypto": Settings.Cypto_USDC,
            "Condition_1": "0.00002",
            "TrailStop_Plus": "0.00001",
            "SellPrice_Plus": "0.00003",
            "MarketSell_Plus": "0.00005",
            "Round": 6,
            "Account_Num": "454b39a5-f2e5-400d-baa6-d281bad0bb9c",
            "Cancel_Sell": False,

            "canBuy": False,
            "BuyOrder": False,
            "Brought": False,
            "Breakeven": 0,
            "BasePrice": 0,
            "trailStop": 0,
            "Base_Buy_Percentage": 50,
            "Round_Bool": True,
            "Can_Market": True,
            "Market_Useable": False,
            "ID": "",

            "Direction": "",
            "Direction_Old": 0,

        },

    }

Save()


