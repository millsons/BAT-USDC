import Store, Buying_RSI, Settings, Selling
import json

def Recived(data):
    Store.StoreInfo("---------------------------WEBHOOK----------------------------------------------------------------------------------------------------")
    Store.StoreInfo(data)
    Store.StoreInfo("--------------------------------------------------------------------------------------------------------------------------------------")

    data = json.loads(data)
    if data["Type"] == "RSI" and data["Side"] == "Buy" and Settings.Cypto_Settings[data["Ticker"]]["canBuy"] == False:
        Buying_RSI.Buy_Setup(data["Price"], data["Ticker"])


    if data["Type"] == "RSI" and data["Side"] == "Sell" and Settings.Cypto_Settings[data["Ticker"]]["canBuy"] == False:
        Settings.Cypto_Settings[data["Ticker"]]["RSI_Sell"] = True
        Settings.Cypto_Settings[data["Ticker"]]["Cancel_Sell"] = False

    if data["Type"] == "RSI" and data["Side"] == "Stop":
        Settings.Cypto_Settings[data["Ticker"]]["RSI_Sell"] = False
        Settings.Cypto_Settings[data["Ticker"]]["Brought"] = False
        Settings.Cypto_Settings[data["Ticker"]]["canBuy"] = False
        Settings.Cypto_Settings[data["Ticker"]]["Cancel_Sell"] = True
        Buying_RSI.Cancel_Limit(data["Ticker"])


