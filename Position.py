import cbpro
from itertools import islice
import Selling, Settings, Notif, Buying, Store, Trades, Buying_RSI
import datetime

auth_client = cbpro.AuthenticatedClient(Settings.Key,
                                        Settings.Secret,
                                        Settings.Pass)

global First
First = True

global LOID
LOID = ""

def GetPeosition(Cypto):
    global CurPos
    global First
    global LOID
    global LastStat
    try:
        recent_fills = islice(auth_client.get_fills(product_id=Cypto), 5)
        all_fills = list(recent_fills)

        CBID = all_fills[0].get('order_id')
        LOID = Trades.Trades["TradeTemp_" + Cypto]["id"]
        print(LOID)

        if(LOID != CBID):
            LOID = CBID
            Trades.Trades["TradeTemp_" + Cypto]["id"] = LOID
            Position = all_fills[0].get('side')

            if Position == "buy":

                type = auth_client.get_order(all_fills[0].get('order_id')).get('type')
                size = all_fills[0].get('size')
                price = all_fills[0].get('price')
                Store.StoreInfo("Size: " + size)
                Store.StoreInfo("Type: " + type)
                PaidEXfee = float(size) * float(price)
                Store.StoreInfo("Paidexfee: " + str(PaidEXfee))
                Percentage = 0.5
                Store.StoreInfo(str(Percentage))

                Store.StoreInfo("Breakeven percentage cal: " + str(Percentage))
                fees = Percentage / 100 * PaidEXfee
                Store.StoreInfo("Fee: " + str(fees))
                global PaidFees
                PaidFees = PaidEXfee + fees
                Store.StoreInfo("paid fee: " + str(PaidFees))


                global Breakeven
                Breakeven = float(PaidFees) / float(size)
                Store.StoreInfo("Breakeven: " + str(Breakeven))
                TrailstopInc = 0.3 / 100 * float(Breakeven)

                global basePrice
                basePrice = Breakeven
                Store.StoreInfo("Base Price: " + str(basePrice))
                global TrailStop
                TrailStop = Breakeven - TrailstopInc
                Store.StoreInfo("TrailStop: " + str(TrailStop))

                TrailDistance = float(price) - float(TrailStop)
                LastStat = "RSI"
                Trades.Add(CBID, Cypto, all_fills[0].get('price'), all_fills[0].get('size'), Breakeven, basePrice, TrailStop, TrailDistance, "RSI")
                Notif.Send("Brought at: " + all_fills[0].get('price'))
                Store.StoreInfo("///////////////////////////////////////////////")
                Store.StoreInfo("Brought: " + all_fills[0].get('price'))
                Store.StoreInfo("///////////////////////////////////////////////")
                Settings.Cypto_Settings[Cypto]["BuyOrder"]= False
                Settings.Cypto_Settings[Cypto]["canBuy"] = False
                Settings.Cypto_Settings[Cypto]["Brought"] = True
                Buying.Get_Buys()



            if Position == "sell":
                for trade in Trades.Trades:
                    if all_fills[0].get('order_id') == Trades.Trades[trade]['Sell_Order_ID']:
                        Store.StoreInfo(all_fills[0].get('order_id') + "\t " + Trades.Trades[trade]['Sell_Order_ID'])
                        Trades.Trades[trade]['Size'] = 0
                        Trades.Trades[trade]["Sell_Order"] = False
                        Notif.Send("Sold at: " + all_fills[0].get('price'))
                        Store.StoreInfo("///////////////////////////////////////////////")
                        Store.StoreInfo("Sold: " + all_fills[0].get('price'))
                        Store.StoreInfo("///////////////////////////////////////////////")
                        Settings.Cypto_Settings[Cypto]["Base_Buy_Percentage"] = 50.0
                        #Buying.Get_Buys()
                        Trades.Save()
        Settings.Save()

    except Exception as e:
        Store.StoreInfo(e)


for trade in Trades.Trades:
    if float(Trades.Trades[trade]["Size"]) > 0:
     Store.StoreInfo(str(Trades.Trades[trade]))