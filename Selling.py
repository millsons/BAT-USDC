import decimal

import cbpro
from itertools import islice
from sty import fg, bg
import Settings, Direction, Position, Notif, Store, Trades

auth_client = cbpro.AuthenticatedClient(Settings.Key,
                                        Settings.Secret,
                                        Settings.Pass)



# Both of these are changeable at the start

# at what point does the trail stop get put on the order book?

# what is the starting stoploss percentage?
global StopPercentageNS
global DirectionAdjust
DirectionAdjust = False



TradeList = Trades.Trades
Cypto_Settings = Settings.Cypto_Settings


def RunAll(Curprice, Spread, Cypto):
    global TrailStop
    global LimitOrderTime
    LimitOrderTime = float(Cypto_Settings[Cypto]["LimitOrder"])
    RSI_Sell = Cypto_Settings[Cypto]["RSI_Sell"]
    Store.StoreInfo("RIS_Sell = " + str(RSI_Sell))
    i = 0
    Count = len(TradeList) - 1
    Store.StoreInfo("------------------------------Brought Log---------------------------------------")
    Store.StoreInfo("{:<12} {:<20} {:<6} {:<40} {:<8}".format("Size", 'Breakeven',
                                              'Sell_Order', 'Sell_Order_ID', 'Strat'))
    if(Count > 0):
        for trade in TradeList:
            if trade != "TradeTemp_" + Cypto and TradeList[trade]['Cypto'] == Cypto:

                Size = TradeList[trade]['Size']
                Breakeven = TradeList[trade]['Breakeven']
                basePrice = TradeList[trade]['Old_Price']
                TrailStop = TradeList[trade]['Trail_Stop']
                TrailDistance = TradeList[trade]['Trail_Distance']
                SellOrder = TradeList[trade]['Sell_Order']
                SellOrderId = TradeList[trade]['Sell_Order_ID']
                StopPercentageTL = TradeList[trade]['Sell_Percentage']
                Strat = TradeList[trade]['Strat']
                if(float(Size) > 0):
                    Store.StoreInfo ("{:<12} {:<20} {:<6} {:<40} {:<8}".format(TradeList[trade]['Size'], TradeList[trade]['Breakeven'], str(TradeList[trade]['Sell_Order']), TradeList[trade]['Sell_Order_ID'], TradeList[trade]['Strat']))
                if float(Size) > 0 and Strat == "RSI" and RSI_Sell == True or float(Size) > 0 and Strat == "Follow":
                    Check(trade, Curprice, Spread, Size, Breakeven, basePrice, TrailStop, TrailDistance, SellOrder, SellOrderId, StopPercentageTL, Cypto)

                if Settings.Cypto_Settings[Cypto]["Cancel_Sell"] == True and SellOrder == True and float(Size) > 0:
                    auth_client.cancel_order(OrderId)
                    TradeList[trade]['Sell_Order'] = False
                    TradeList[trade]['Sell_Order_ID'] = ""
                    Settings.Cypto_Settings[Cypto]["Cancel_Sell"] = False
                    Settings.Save()


                # This is the function of the trailing stop loss
def Check(id, curPrice, Spread, Size, Breakeven, basePrice, TrailStop, TrailDistance, SellOrder, SellorderID, StopPercentage, Cypto):
    Store.StoreInfo("------------------------------SELLING LOG" + str(TradeList[id]["id"]) + "---------------------------------------")
    Store.StoreInfo("Price: " + str(curPrice) + "\t Spread: " + str(Spread))
    Store.StoreInfo("Stop Percentage: " + str(StopPercentage))
    Store.StoreInfo("Base Price: " + str(basePrice))
    global DirectionAdjust
    global OrderId
    global StopPercentageNS
    global idNum
    idNum = id

    StopPercentageNS = 0


    #Direction.StopLoss(StopPercentage)
    """if DirectionAdjust == True:
        AdjustStop(id, basePrice, Breakeven, TrailStop)
        DirectionAdjust = False
        Store.StoreInfo("AdjustStop Called, Baseprice: " + str(basePrice))
        TradeList[id]['Sell_Percentage'] = StopPercentageNS"""



    # finds the distance between the current price and the set stop loss
    TrailDistance = float(curPrice) - float(TrailStop)
    TradeList[id]['Trail_Distance'] = str(TrailDistance)
    TrailDistance = round(decimal.Decimal(TrailDistance), 6)

    if TrailDistance > 1:
        toprintD = "Trail Distance: " + fg.green + str(TrailDistance) + fg.rs
    else:
        toprintD = "Trail Distance: " + fg.red + str(TrailDistance) + fg.rs

    if TrailStop >= Breakeven:
        toprintB = "Trail Stop: " + fg.green + str(TrailStop) + fg.rs
    else:
        toprintB = "Trail Stop: " + fg.red + str(TrailStop) + fg.rs


    Store.StoreInfo("Selling: " + toprintD + "\t" + toprintB)
    Store.StoreInfo("Breakeven: " + str(Breakeven))
    Store.StoreInfo(Breakeven + float(Cypto_Settings[Cypto]["MarketSell_Plus"]) + (Spread / 2))
    # check to see if there has been a price incresse between the last high price that reset the stop loss and the current last sold price.
    if float(curPrice) > float(basePrice):
        AdjustStop(id,curPrice, Breakeven, TrailStop)

    if float(curPrice) > float(Breakeven) + float(Cypto_Settings[Cypto]["Condition_1"]) and float(TrailStop) < float(Breakeven):
        TradeList[id]['Trail_Stop'] = float(Breakeven) + float(Cypto_Settings[Cypto]["TrailStop_Plus"])
        Store.StoreInfo("New Trail set at breakeven: " + str(TradeList[id]['Trail_Stop']))
        TradeList[id]['Old_Price'] = curPrice

    # checks to see if the distance between the current price and the stop loss is below 1, if so put a sell order on the market, to make sure we sell at that price
    if LimitOrderTime > TrailDistance > 0 and SellOrder == False and TrailStop > Breakeven + (Spread/2) and TrailStop > 0:
        Store.StoreInfo("****************SELL INFO - Limit Order****************")
        try:
            SellPrice = float(curPrice) + float(Cypto_Settings[Cypto]["SellPrice_Plus"])
            SellPrice = round(SellPrice, Cypto_Settings[Cypto]["Round"])
            Sell = auth_client.sell(price=SellPrice,  # USD
                                    size=Size,  # BTC
                                    order_type='limit',
                                    product_id=Cypto)

            OrderId = Sell.get('id')
            TradeList[id]['Sell_Order'] = True
            TradeList[id]['Sell_Order_ID'] = OrderId
            Notif.Send("Placed Sell Limit Order: " + str(SellPrice))
            Store.StoreInfo("Sell Price: " + str(SellPrice) + "Order Id: " + str(OrderId) + "Amount: " + str(Size))
        except Exception as e:
            print(e)
            Notif.Send("ERROR: Tried to place a limit sell, but failed")
            Store.StoreInfo("ERROR: Tried to place a limit sell, but failed")
            Store.StoreInfo(e)


    if SellOrder == True and Settings.Cypto_Settings[Cypto]["Direction"] == "Up" and TrailDistance < LimitOrderTime and TrailStop > Breakeven + (Spread/2) and TrailStop > 0:
        Store.StoreInfo("****************SELL INFO - Change Limit Order****************")
        try:
            auth_client.cancel_order(SellorderID)
            SellPrice = float(curPrice) + float(Cypto_Settings[Cypto]["SellPrice_Plus"])
            SellPrice = round(SellPrice, Cypto_Settings[Cypto]["Round"])
            Sell = auth_client.sell(price=SellPrice,  # USD
                                    size=Size,  # BTC
                                    order_type='limit',
                                    product_id=Cypto)

            OrderId = Sell.get('id')
            TradeList[id]['Sell_Order_ID'] = OrderId
            TradeList[id]['Sell_Order'] = True
            Notif.Send("Moved Sell Limit Order To: " + str(SellPrice))
            Store.StoreInfo("Sell Price: " + str(SellPrice) + "Order Id: " + str(OrderId) + "Amount: " + str(Size))
        except Exception as e:
            print(e)
            Notif.Send("ERROR: Tried to change a limit sell, but failed")
            Store.StoreInfo("ERROR: Tried to change a limit sell, but failed")
            Store.StoreInfo(e)

    # checks to see if the distance between the current price and stop loss is above one and that a sell order has been created. if so it will remove the sell order to allow the stop loss to adjust to anymore possible incresess
    if TrailDistance > LimitOrderTime and SellOrder == True and TrailStop > 0:
        Store.StoreInfo("****************SELL INFO - Removed Limit Order****************")
        try:
            auth_client.cancel_order(SellorderID)
            TradeList[id]['Sell_Order'] = False
            TradeList[id]['Sell_Order_ID'] = ""
            Notif.Send("Removed Sell Limit Order")
        except Exception as e:
            print(e)
            Notif.Send("ERROR: Tried to remove a limit sell, but failed")
            Store.StoreInfo("ERROR: Tried to remove a limit sell, but failed")
            Store.StoreInfo(e)

    if float(TrailDistance) < 0 and TrailStop > Breakeven + float(Cypto_Settings[Cypto]["MarketSell_Plus"]) + (Spread/2) and Settings.Cypto_Settings[Cypto]["Market_Useable"] == True:
        Store.StoreInfo("****************SELL INFO - Market Order****************")
        try:
            if SellOrder == True:
                auth_client.cancel_order(SellorderID)

            Sell = auth_client.place_market_order(product_id=Cypto,
                                           side='sell',
                                           size=Size)

            Store.StoreInfo("Amount: " + str(Size))
            TradeList[id]['Sell_Order_ID'] = Sell.get('id')
            TradeList[id]['Sell_Order'] = True

        except Exception as e:
            print(e)
            Notif.Send("ERROR: Tried to sell, but failed")
            Store.StoreInfo("ERROR: Market sell, but failed")
            Store.StoreInfo(e)
    elif float(TrailDistance) < 0 and TrailStop > Breakeven + float(Cypto_Settings[Cypto]["MarketSell_Plus"]) + (Spread/2) and Settings.Cypto_Settings[Cypto]["Market_Useable"] == False:
        Store.StoreInfo("****************SELL INFO - Market Limit Order****************")

        try:
            auth_client.cancel_order(SellorderID)
            SellPrice = float(curPrice)
            SellPrice = round(SellPrice, Cypto_Settings[Cypto]["Round"])
            Sell = auth_client.sell(price=SellPrice,  # USD
                                    size=Size,  # BTC
                                    order_type='limit',
                                    product_id=Cypto)

            TradeList[id]['Sell_Order_ID'] = Sell.get('id')
            TradeList[id]['Sell_Order'] = True
            OrderId = Sell.get('id')
            Store.StoreInfo("Sell Price: " + str(SellPrice) + "Order Id: " + str(OrderId) + "Amount: " + str(Size))
        except Exception as e:
            print(e)
            Notif.Send("ERROR: Tried to change a limit sell, but failed")
            Store.StoreInfo("ERROR: Tried to change a limit sell, but failed")
            Store.StoreInfo(e)
    Trades.Save()
    Settings.Save()


def AdjustStop(id, curPrice, Breakeven, TrailStop):
    global basePrice
    StopPercentage = TradeList[id]['Sell_Percentage']
    PTrailstopInc = StopPercentage / 100 * float(curPrice)
    PTrailStop = float(curPrice) - float(PTrailstopInc)
    Store.StoreInfo("Stop percentage: " + str(StopPercentage) +"\t PTrail: " + str(PTrailStop))
    Settings.Save()

    if TrailStop >= Breakeven and PTrailStop >= TrailStop:

        TrailstopInc = StopPercentage / 100 * float(curPrice)
        TrailStop = float(curPrice) - float(TrailstopInc)
        TradeList[id]['Trail_Stop'] = TrailStop
        basePrice = curPrice
        TradeList[id]['Old_Price'] = basePrice
        Store.StoreInfo("Trail higher than break even, Trail went to: " + str(TrailStop))
        Store.StoreInfo("baseprice is now: " + str(basePrice))

    elif TrailStop >= Breakeven and PTrailStop < TrailStop:
        TrailStop = Breakeven
        TradeList[id]['Trail_Stop'] = TrailStop
        Store.StoreInfo("Trail was higher than break even, stopped from going lower Trail went to: " + str(TrailStop))


    else:
        TrailstopInc = StopPercentage / 100 * float(curPrice)
        TrailStop = float(curPrice) - float(TrailstopInc)
        TradeList[id]['Trail_Stop'] = TrailStop
        basePrice = curPrice
        TradeList[id]['Old_Price'] = basePrice
        Store.StoreInfo("Price incresed but no gone above breakeven, Trail went to: " + str(TrailStop))
        Store.StoreInfo("baseprice is now: " + str(basePrice))

    Trades.Save()

def Cancel_Limit():
    global OrderId
    global SellOrder
    global trade
    global idNum
    if TradeList[idNum]['Sell_Order'] == True:
        auth_client.cancel_order(OrderId)
        TradeList[id]['Sell_Order_ID'] = ""
        TradeList[idNum]['Sell_Order'] = False



