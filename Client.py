import datetime
import cbpro
#from Live import Selling, Settings, Position, Direction, Notif, Store
from flask import Flask, request, json

import Settings, Store, Notif, Direction, Position, Buying, Selling, Buying_RSI
import WebHook_Handler#
from sty import fg, bg


class myWebsocketClient(cbpro.WebsocketClient):
    public_client = cbpro.PublicClient()

    def __init__(self, url="wss://ws-feed.pro.coinbase.com", products=None, message_type="subscribe",
                 mongo_collection=None,
                 should_print=True, auth=False, api_key="", api_secret="", api_passphrase="", channels=None):
        super().__init__(url="wss://ws-feed.pro.coinbase.com", products=Settings.Cypto_Tickers, message_type="subscribe",
                         mongo_collection=None, should_print=True, auth=False, api_key="", api_secret="",
                         api_passphrase="", channels=Settings.Channel)

    def on_open(self):
        self.url = "wss://ws-feed.pro.coinbase.com/"
        name = datetime.datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")
        Store.Log = name


    def on_message(self, msg):
        public_client = cbpro.PublicClient()
        if 'price' in msg and 'type' in msg:
            if msg["product_id"] == Settings.Cypto_GBP:
                Store.StoreInfo(fg.blue + "---------------------------Defult LOG: " + msg["product_id"] + "----------------------------------------------------------------------------------------------------" + fg.rs)
            if msg["product_id"] == Settings.Cypto_USDC:
                Store.StoreInfo(fg.red + "---------------------------Defult LOG: " + msg["product_id"] + "----------------------------------------------------------------------------------------------------" + fg.rs)
            if msg["product_id"] == Settings.Cypto_USDC2:
                Store.StoreInfo(fg.green + "---------------------------Defult LOG: " + msg["product_id"] + "----------------------------------------------------------------------------------------------------" + fg.rs)
            Store.StoreInfo(str(datetime.datetime.now()))
            print("Pair", msg["product_id"],
                  "\t@ {:.6f}".format(float(msg["price"])), "\t",
                  msg["time"])
            Spread = round(float(msg["best_ask"]) - float(msg["best_bid"]), 4)
            Store.StoreInfo("Cur Price: " + msg["price"] + "Best Ask: " + msg["best_ask"] + " Best Bid: " + msg["best_bid"] + "  Spread: " + str(Spread))
            Direction.Direction(msg["price"], msg["product_id"])
            Position.GetPeosition(msg["product_id"])
            #Buying.Can_Buy(msg["price"], Spread)
            Buying_RSI.Check(msg["price"], Spread, msg["product_id"])
            Selling.RunAll(msg["price"], Spread, msg["product_id"])


    def on_close(self):
        Store.StoreInfo("-- Goodbye! --")
        Notif.Send("Application Closed")
        main()
        app.run()

def main():
    wsClient = myWebsocketClient()
    wsClient.start()

app = Flask(__name__)
def api():
    return "Hello World"

@app.route('/', methods=['POST'])
def api_gg_message():
    Mydata = json.dumps(request.json)
    WebHook_Handler.Recived(Mydata)
    return Mydata

if __name__ == '__main__':
      main()
      app.run()


# print(wsClient.url, wsClient.products)
