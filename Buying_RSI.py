import decimal
import math

import cbpro
from itertools import islice
from sty import fg, bg

import Settings, Direction, Position, Notif, Store, Store, Trades

auth_client = cbpro.AuthenticatedClient(Settings.Key,
                                        Settings.Secret,
                                        Settings.Pass)

# Both of these are changeable at the start
# at what point does the trail stop get put on the order book?


global LimitOrderTime
# what is the starting stoploss percentage?
global StopPercentage
StopPercentage = 0.2

global DirectionAdjust
DirectionAdjust = False

global CanBuy

global SellOrder

global size
size = True
global Market
Market = False


def Get_Cypto(Cypto):
    global GBP
    global Market
    global Limit
    GBP_Base = auth_client.get_account(Settings.Cypto_Settings[Cypto]["Account_Num"]).get('balance')
    Store.StoreInfo(GBP_Base)
    GBP = float(Settings.Cypto_Settings[Cypto]["Base_Buy_Percentage"]) / 100 * float(GBP_Base)
    Store.StoreInfo(GBP)
    GBP = round(GBP, Settings.Cypto_Settings[Cypto]["Round"])
    Store.StoreInfo(GBP)

    if float(GBP) < 10 and float(GBP_Base) >= 10:
        Settings.Cypto_Settings[Cypto]["Can_Market"] = True
        return 10.0
    elif float(GBP_Base) < 1:
        Settings.Cypto_Settings[Cypto]["Can_Market"] = False
        Settings.Cypto_Settings[Cypto]["canBuy"] = False
        return 0
    elif float(GBP) > 10:
        Settings.Cypto_Settings[Cypto]["Can_Market"] = True
        return GBP
    else:
        Settings.Cypto_Settings[Cypto]["Can_Market"] = False
        return GBP


def Buy_Setup(curPrice, Cypto):
    global CanBuy
    global Breakeven
    global DirectionAdjust
    global basePrice
    global TrailStop

    Store.StoreInfo("----------------------------------------Buying Info - SETUP------------------------------")
    basepricePer = 0.1 / 100 * float(curPrice)
    Breakeven = float(curPrice) + float(basepricePer);

    Store.StoreInfo("Buying Breakeven: " + str(Breakeven))
    basePrice = curPrice
    TrailStop = Breakeven

    Store.StoreInfo("############################STARTED BUYING##########################")
    Store.StoreInfo("Trailstop: " + str(TrailStop))
    Store.StoreInfo("Stop Percentage: " + str(StopPercentage))
    Settings.Cypto_Settings[Cypto]["canBuy"] = True
    Settings.Cypto_Settings[Cypto]["Breakeven"] = str(Breakeven)
    Settings.Cypto_Settings[Cypto]["BasePrice"] = str(basePrice)
    Settings.Cypto_Settings[Cypto]["trailStop"] = str(TrailStop)


def Check(curPrice, spread, Cypto):
    Store.StoreInfo("------------------------------BUYING LOG---------------------------------------")
    Store.StoreInfo("{:<15} {:<15} {:<15} {:<15} {:<15}".format("Can_buy", "Buy_Order", "Brought", "can_Market", "ID"))
    Store.StoreInfo("{:<15} {:<15} {:<15} {:<15} {:<15}".format(str(Settings.Cypto_Settings[Cypto]["canBuy"]), str(Settings.Cypto_Settings[Cypto]["BuyOrder"]), str(Settings.Cypto_Settings[Cypto]["Brought"]),str(Settings.Cypto_Settings[Cypto]["Can_Market"]),Settings.Cypto_Settings[Cypto]["ID"]))
    global CanBuy
    global SellOrder
    global LimitOrderTime
    LimitOrderTime = float(Settings.Cypto_Settings[Cypto]["LimitOrder"])
    SellOrder = Settings.Cypto_Settings[Cypto]["BuyOrder"]
    if Settings.Cypto_Settings[Cypto]["canBuy"] == True and Settings.Cypto_Settings[Cypto]["Brought"] == False:
        Store.StoreInfo("---------------------------------------- BUYING - RSI------------------------------------")
        Store.StoreInfo("Price: " + str(curPrice))
        global basePrice
        global TrailStop

        global OrderId
        global size
        global DirectionAdjust
        OrderId = Settings.Cypto_Settings[Cypto]["ID"]

        basePrice = float(Settings.Cypto_Settings[Cypto]["BasePrice"])
        TrailStop = float(Settings.Cypto_Settings[Cypto]["trailStop"])
        Breakeven = float(Settings.Cypto_Settings[Cypto]["Breakeven"])

        if float(curPrice) < float(basePrice):
            AdjustStop(curPrice, Cypto)

        # finds the distance between the current price and the set stop loss
        TrailDistance = float(TrailStop) - float(curPrice)
        TrailDistance = round(decimal.Decimal(TrailDistance), 6)
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
        Store.StoreInfo(str(Settings.Cypto_Settings[Cypto]["Base_Buy_Percentage"]))

        # check to see if there has been a price incresse between the last high price that reset the stop loss and the current last sold price.

        # checks to see if the distance between the current price and the stop loss is below 1, if so put a sell order on the market, to make sure we sell at that price
        if TrailDistance < LimitOrderTime and SellOrder == False and TrailDistance > 0:
            Store.StoreInfo("****************BUY INFO - Limit Order****************")

            SellPrice = float(curPrice) - spread - float(Settings.Cypto_Settings[Cypto]["Condition_1"])
            SellPrice = round(SellPrice, Settings.Cypto_Settings[Cypto]["Round"])

            BuySize = float(Get_Cypto(Cypto)) / float(SellPrice)
            if BuySize != 0:
                if Settings.Cypto_Settings[Cypto]["Round_Bool"] == True:
                    BuySize = int(BuySize)
                    Store.StoreInfo("inted")
                else:
                    BuySize = round(float(BuySize), Settings.Cypto_Settings[Cypto]["Round"])
                    Store.StoreInfo("Rounded")
                Store.StoreInfo("Buy Size: " + str(BuySize))
                try:
                    Sell = auth_client.buy(price=SellPrice,
                                           size=BuySize,
                                           order_type='limit',
                                           product_id=Cypto)
                    OrderId = Sell.get('id')
                    SellOrder = True
                    Settings.Cypto_Settings[Cypto]["BuyOrder"] = True
                    Settings.Cypto_Settings[Cypto]["ID"] = OrderId
                    Notif.Send("Placed Limit order: " + str(SellPrice))
                    Store.StoreInfo("Buy Price: " + str(SellPrice) + "Amount: " + str(BuySize) + "Ode Id: " + str(OrderId))
                except Exception as e:
                    Notif.Send("ERROR: Tried to place a limit buy, but failed")
                    Store.StoreInfo("ERROR: Tried to place a limit buy, but failed")
                    Store.StoreInfo(str(e))
            else:
                Store.StoreInfo("Buy size was less than 1")

        if SellOrder == True and Settings.Cypto_Settings[Cypto]["Direction"] == "Down" and TrailDistance < LimitOrderTime and TrailDistance > 0:
            Store.StoreInfo("****************Buy INFO - Change Limit Order****************")
            try:
                auth_client.cancel_order(OrderId)
                Store.StoreInfo(curPrice)
                SellPrice = float(curPrice) - spread - float(Settings.Cypto_Settings[Cypto]["Condition_1"])
                SellPrice = round(SellPrice, Settings.Cypto_Settings[Cypto]["Round"])

                BuySize = float(Get_Cypto(Cypto)) / float(SellPrice)
                if Settings.Cypto_Settings[Cypto]["Round_Bool"] == True:
                    BuySize = int(BuySize)
                else:
                    BuySize = round(float(BuySize), Settings.Cypto_Settings[Cypto]["Round"])
                Store.StoreInfo("Buy Size: " + str(BuySize))
                Sell = auth_client.buy(price=SellPrice,
                                       size=BuySize,
                                       order_type='limit',
                                       product_id=Cypto)
                OrderId = Sell.get('id')
                Settings.Cypto_Settings[Cypto]["ID"] = OrderId
                Notif.Send("Moved Limit Order To: " + str(SellPrice))
                Store.StoreInfo(
                    "Buy Price: " + str(SellPrice) + "Order Id: " + str(OrderId) + "Amount: " + str(BuySize))
            except Exception as e:
                Notif.Send("ERROR: Tried to change a limit buy, but failed")
                Store.StoreInfo("ERROR: Tried to change a limit buy, but failed")
                Store.StoreInfo(str(e))
        # checks to see if the distance between the current price and stop loss is above one and that a sell order has been created. if so it will remove the sell order to allow the stop loss to adjust to anymore possible incresess
        if TrailDistance > LimitOrderTime and SellOrder == True and TrailDistance > 0:
            Store.StoreInfo("****************BUY INFO - Removed Limit Order****************")
            try:
                auth_client.cancel_order(OrderId)

                Settings.Cypto_Settings[Cypto]["BuyOrder"] = False
                SellOrder = False
                Notif.Send("Removed Limit Order")
                Store.StoreInfo("Removed Limit Order")
                Settings.Cypto_Settings[Cypto]["ID"] = ""

            except Exception as e:
                Notif.Send("ERROR: Tried to remove a limit buy, but failed")
                Store.StoreInfo("ERROR: Tried to remove a limit buy, but failed")
                Store.StoreInfo(str(e))

        if TrailDistance < 0 and Settings.Cypto_Settings[Cypto]["Can_Market"] == True and Settings.Cypto_Settings[Cypto]["Market_Useable"] == True:
            Store.StoreInfo("****************BUY INFO - Market Order****************")
            if SellOrder and Settings.Cypto_Settings[Cypto]["Can_Market"]:
                auth_client.cancel_order(OrderId)
                Store.StoreInfo("removed Limit Order")
                Settings.Cypto_Settings[Cypto]["BuyOrder"] = False
                SellOrder = False
                Settings.Cypto_Settings[Cypto]["ID"] = ""

            GBP = Get_Cypto(Cypto)
            Store.StoreInfo("Spening: £" + str(GBP))
            Sell = auth_client.place_market_order(product_id=Cypto,
                                                  side='buy',
                                                  funds=GBP)

            OrderId = Sell.get('id')
            Store.StoreInfo("Amount: " + str(GBP) + "\t Order Id: " + OrderId)
            Settings.Cypto_Settings[Cypto]["BuyOrder"] = False
            Settings.Cypto_Settings[Cypto]["canBuy"] = False
            Settings.Cypto_Settings[Cypto]["ID"] = OrderId
            Store.StoreInfo(
            "Order Id: " + str(OrderId))
        elif TrailDistance < 0 and Settings.Cypto_Settings[Cypto]["Can_Market"] == False or Settings.Cypto_Settings[Cypto]["Market_Useable"] == False:
            Store.StoreInfo("****************BUY INFO - Market Order - Limited****************")

            if SellOrder == True:
                auth_client.cancel_order(OrderId)
                Store.StoreInfo("removed Limit Order")
                Settings.Cypto_Settings[Cypto]["BuyOrder"] = False
                SellOrder = False
                Settings.Cypto_Settings[Cypto]["ID"] = ""

            SellPrice = float(curPrice)

            BuySize = float(Get_Cypto(Cypto)) / float(SellPrice)
            Store.StoreInfo("Buy Size: " + str(BuySize))
            if BuySize != 0:
                if Settings.Cypto_Settings[Cypto]["Round_Bool"] == True:
                    BuySize = int(BuySize)
                else:
                    BuySize = round(float(BuySize), Settings.Cypto_Settings[Cypto]["Round"])

                try:
                    Sell = auth_client.buy(price=SellPrice,
                                           size=BuySize,
                                           order_type='limit',
                                           product_id=Cypto)
                    OrderId = Sell.get('id')

                    Notif.Send("Placed Limit order: " + str(SellPrice))
                    Store.StoreInfo("Buy Price: " + str(SellPrice) + "Amount: " + str(BuySize) + "Ode Id: " + str(OrderId))
                    Settings.Cypto_Settings[Cypto]["BuyOrder"] = False
                    Settings.Cypto_Settings[Cypto]["canBuy"] = False
                    Settings.Cypto_Settings[Cypto]["ID"] = OrderId
                except Exception as e:
                    Notif.Send("ERROR: Tried to place a limit buy, but failed")
                    Store.StoreInfo("ERROR: Tried to place a limit buy, but failed")
                    Store.StoreInfo(str(e))
            else:
                Store.StoreInfo("Buy size was less than 1")
    Settings.Save()


def AdjustStop(curPrice, Cypto):
    global TrailStop
    global basePrice
    TrailstopInc = float(StopPercentage) / 100 * float(curPrice)
    TrailStop = float(curPrice) + float(TrailstopInc)
    Store.StoreInfo("New Trail: " + str(TrailStop))
    basePrice = curPrice
    Settings.Cypto_Settings[Cypto]["Base_Buy_Percentage"] = Settings.Cypto_Settings[Cypto]["Base_Buy_Percentage"] + 1
    Settings.Cypto_Settings[Cypto]["trailStop"] = str(TrailStop)
    Settings.Cypto_Settings[Cypto]["BasePrice"] = str(basePrice)
    Settings.Save()


def Cancel_Limit(Cypto):
    global OrderId
    global SellOrder
    try:
        if Settings.Cypto_Settings[Cypto]["BuyOrder"] == True:
            auth_client.cancel_order(OrderId)
            Settings.Cypto_Settings[Cypto]["BuyOrder"] = False
            Settings.Save()

    except Exception as e:
        print(e)
        Notif.Send("ERROR: Tried to remove a limit buy, but failed")
        Store.StoreInfo("ERROR: Tried to remove a limit buy, but failed")
        Store.StoreInfo(e)
