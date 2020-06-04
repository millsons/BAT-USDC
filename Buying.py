import math

import cbpro
from itertools import islice
from sty import fg, bg

import Buy_Log
import Settings, Direction, Position, Notif, Store, Store, Trades

auth_client = cbpro.AuthenticatedClient(Settings.Key,
                                        Settings.Secret,
                                        Settings.Pass)

# Both of these are changeable at the start
# at what point does the trail stop get put on the order book?


global LimitOrderTime
LimitOrderTime = 0.5
# what is the starting stoploss percentage?
global StopPercentage
StopPercentage = 0.3

global DirectionAdjust
DirectionAdjust = False

global CanBuy
CanBuy = False

global SellOrder
SellOrder = False
global size
size = True
global Market
size = True

def Get_Buys():
    Store.StoreInfo("Start New Buying")
    recent_fills = islice(auth_client.get_fills(product_id="ETH-GBP"), 5)
    all_fills = list(recent_fills)
    global price
    price = all_fills[0].get('price')
    #price = 167.78

    basepricePer = 0.2 / 100 * float(price)

    global Breakeven
    Breakeven = float(price) - float(basepricePer);
    Store.StoreInfo("Buying Breakeven: " + str(Breakeven))

Get_Buys()
def Get_Cypto():
    global GBP
    global Market
    global Limit
    GBP = auth_client.get_account(Settings.GBP_Account_ID).get('balance')
    GBP = float(Settings.Base_Buy_Percentage)/100 * float(GBP)
    GBP = round(GBP, 2)
    if float(GBP) < 10.0:
        Market = False
        Limit = True
    else:
        Market = True
        Limit = False

    return GBP








def Can_Buy(curPrice, Spread):
    Store.StoreInfo("------------------------------BUYING LOG---------------------------------------")
    global CanBuy
    global Breakeven
    global DirectionAdjust
    if float(curPrice) < float(Breakeven) - (Spread / 2):
        Store.StoreInfo("Condition 1 Set, Less than Breakeven")

    """if Direction.TwentyUp > 60 and Direction.TenUp > 65:
        Store.StoreInfo("Condition 2 Set, Directions")"""

    if len(Direction.PriceListTwenty) >= 20:
        Store.StoreInfo("Condition 3 Set, 20 Trades Stored")

    if float(curPrice) < float(Breakeven) - (Spread / 2) and CanBuy == False and len(Direction.PriceListTwenty) >= 20:
        global basePrice

        global TrailStop
        basePrice = curPrice
        TrailStop = Breakeven
        Store.StoreInfo("############################STARTED BUYING##########################")
        Store.StoreInfo("Trailstop: " + str(TrailStop))
        Store.StoreInfo("Stop Percentage: " + str(StopPercentage))
        CanBuy = True
    # elif CanBuy == True and Direction.TwentyUp < 40 and Direction.TenUp < 45:
    #     CanBuy = False
    #     Store.StoreInfo("############################STOPPED BUYING##########################")
    #     Cancel_Limit()

    if CanBuy == True:
        Check(curPrice, Spread)




def Check(curPrice, spread):
    Store.StoreInfo("Price: " + str(curPrice))
    global basePrice
    global TrailStop
    global SellOrder
    global OrderId
    global size
    global DirectionAdjust

    Direction.BuyLoss()
    if DirectionAdjust == True:
        AdjustStop(basePrice)
        DirectionAdjust = False


    if float(curPrice) < float(basePrice):
        AdjustStop(curPrice)

    # finds the distance between the current price and the set stop loss
    TrailDistance = float(TrailStop) - float(curPrice)
    Store.StoreInfo("Trail Distance: " + str(TrailDistance))

    if TrailDistance > 1:
        toprintD = "Trail Distance: " + fg.green + str(TrailDistance) + fg.rs
    else:
        toprintD = "Trail Distance: " + fg.red + str(TrailDistance) + fg.rs

    if TrailStop <= Breakeven:
        toprintB = "Trail Stop: " + fg.green + str(TrailStop) + fg.rs
    else:
        toprintB = "Trail Stop: " + fg.red + str(TrailStop) + fg.rs

    Store.StoreInfo("Buying: " + toprintD + "\t" + toprintB)
    Store.StoreInfo("Breakeven: " + str(Breakeven))

    # check to see if there has been a price incresse between the last high price that reset the stop loss and the current last sold price.

    # checks to see if the distance between the current price and the stop loss is below 1, if so put a sell order on the market, to make sure we sell at that price
    if TrailDistance < LimitOrderTime and SellOrder == False and TrailDistance > 0:
        Store.StoreInfo("****************BUY INFO - Limit Order****************")
        try:
            SellPrice = float(curPrice) - spread - 0.20
            SellPrice = round(SellPrice, 2)

            BuySize = float(Get_Cypto()) / float(SellPrice)
            BuySize = round(BuySize, 5)
            Store.StoreInfo("Buy Size: " + str(BuySize))
            Sell = auth_client.buy(price=SellPrice,
                                   size=BuySize,
                                   order_type='limit',
                                   product_id=Settings.Cypto)
            global OrderId
            OrderId = Sell.get('id')


            SellOrder = True
            Notif.Send("Placed Limit order: " + str(SellPrice))
            Store.StoreInfo("Buy Price: " + str(SellPrice) + "Amount: " + str(BuySize) + "Ode Id: " + str(OrderId))
            Buy_Log.Add(OrderId, "Follow")
        except Exception as e:
            Notif.Send("ERROR: Tried to place a limit buy, but failed")
            Store.StoreInfo("ERROR: Tried to place a limit buy, but failed")
            Store.StoreInfo(str(e))

    if SellOrder == True and Direction.last == "Down" and TrailDistance < LimitOrderTime and TrailDistance > 0:
        Store.StoreInfo("****************Buy INFO - Change Limit Order****************")
        try:
            auth_client.cancel_order(OrderId)
            SellPrice = float(curPrice) - spread - 0.20
            SellPrice = round(SellPrice, 5)

            BuySize = float(Get_Cypto()) / float(SellPrice)
            BuySize = round(BuySize, 5)
            Store.StoreInfo("Buy Size: " + str(BuySize))
            Sell = auth_client.buy(price=SellPrice,
                                   size=BuySize,
                                   order_type='limit',
                                   product_id=Settings.Cypto)
            OrderId = Sell.get('id')
            Notif.Send("Moved Limit Order To: " + str(SellPrice))
            Store.StoreInfo("Buy Price: " + str(SellPrice) + "Order Id: " + str(OrderId) + "Amount: " + str(BuySize))
            Buy_Log.Add(OrderId, "Follow")
        except Exception as e:
            Notif.Send("ERROR: Tried to change a limit buy, but failed")
            Store.StoreInfo("ERROR: Tried to change a limit buy, but failed")
            Store.StoreInfo(str(e))
    # checks to see if the distance between the current price and stop loss is above one and that a sell order has been created. if so it will remove the sell order to allow the stop loss to adjust to anymore possible incresess
    if TrailDistance > LimitOrderTime and SellOrder == True and TrailDistance > 0:
        Store.StoreInfo("****************BUY INFO - Removed Limit Order****************")
        try:
            auth_client.cancel_order(OrderId)

            SellOrder = False

            Notif.Send("Removed Limit Order")
            Store.StoreInfo("Removed Limit Order")

        except Exception as e:
            Notif.Send("ERROR: Tried to remove a limit buy, but failed")
            Store.StoreInfo("ERROR: Tried to remove a limit buy, but failed")
            Store.StoreInfo(str(e))

    if TrailDistance < 0 and Market == True:
        Store.StoreInfo("****************BUY INFO - Market Order****************")
        try:
            if SellOrder:
                auth_client.cancel_order(OrderId)
                Store.StoreInfo("removed Limit Order")

            GBP = Get_Cypto()
            if(GBP < 10):
                GBP = 10
            Store.StoreInfo("Spening: £" + str(GBP))
            auth_client.place_market_order(product_id=Settings.Cypto,
                                                  side='buy',
                                                  funds=GBP)

            Store.StoreInfo("Amount: " + str(GBP))
            SellOrder = False
            Buy_Log.Add(OrderId, "Follow")

        except Exception as e:
            Notif.Send("ERROR: Tried to buy, but failed")
            Store.StoreInfo("ERROR: Market buy, but failed")
            Store.StoreInfo(str(e))
    elif TrailDistance < 0 and Limit == True:
        try:
            if SellOrder:
                auth_client.cancel_order(OrderId)
                Store.StoreInfo("removed Limit Order")

            SellPrice = float(curPrice)
            SellPrice = round(SellPrice, 5)

            BuySize = float(Get_Cypto()) / float(SellPrice)
            BuySize = round(BuySize, 5)
            Store.StoreInfo("Buy Size: " + str(BuySize))
            Sell = auth_client.buy(price=SellPrice,
                                   size=BuySize,
                                   order_type='limit',
                                   product_id=Settings.Cypto)
            OrderId = Sell.get('id')
            Notif.Send("Market Limit Order: " + str(SellPrice))
            Store.StoreInfo("Buy Price: " + str(SellPrice) + "Order Id: " + str(OrderId) + "Amount: " + str(BuySize))
            Buy_Log.Add(OrderId, "Follow")
        except Exception as e:
            Notif.Send("ERROR: Tried to limit market buy, but failed")
            Store.StoreInfo("ERROR: limit market buy, but failed")
            Store.StoreInfo(str(e))

def AdjustStop(curPrice):
    global TrailStop
    global basePrice
    TrailstopInc = float(StopPercentage) / 100 * float(curPrice)
    TrailStop = float(curPrice) + float(TrailstopInc)
    Store.StoreInfo("New Trail: " + str(TrailStop))
    basePrice = curPrice
    Settings.Base_Buy_Percentage = Settings.Base_Buy_Percentage + 1


def Cancel_Limit():
    global OrderId
    global SellOrder
    try:
        if SellOrder == True:
            auth_client.cancel_order(OrderId)
            SellOrder = False

    except Exception as e:
        print(e)
        Notif.Send("ERROR: Tried to remove a limit buy, but failed")
        Store.StoreInfo("ERROR: Tried to remove a limit buy, but failed")
        Store.StoreInfo(e)