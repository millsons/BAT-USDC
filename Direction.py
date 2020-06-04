from sty import bg

import Buying
import Selling
import Store, Settings

global PriceListAll
PriceListAll = []
global PriceListTwenty
PriceListTwenty = []
global PriceListTen
PriceListTen = []
global PriceListFive
PriceListFive = []
global PriceListThree
PriceListThree = []

global last
last = "Null"

global TwentyUp
TwentyUp = 0
global TwentyDown
TwentyDown = 0
global TenUp
TenUp = 0
global TenDown
TenDown = 0


def Direction(CurPrice, Cypto):
    global oldPrice
    global PriceListAll
    global PriceListTwenty
    global PriceListTen
    global PriceListFive
    global PriceListThree
    global last

    oldPrice = float(Settings.Cypto_Settings[Cypto]["Direction_Old"])
    if oldPrice == 0:
        oldPrice = CurPrice

    if float(CurPrice) > float(oldPrice):
        Settings.Cypto_Settings[Cypto]["Direction"] = "Up"
        """PriceListAll.append("Up")
        PriceListTwenty.append("Up")
        PriceListTen.append("Up")
        PriceListFive.append("Up")
        PriceListThree.append("Up")"""
        Store.StoreInfo("Direction: Up \t Current Price: " + str(CurPrice) + "\t Old Price: " + str(oldPrice))
        oldPrice = CurPrice

    elif float(CurPrice) < float(oldPrice):
        Settings.Cypto_Settings[Cypto]["Direction"] = "Down"
        """PriceListAll.append("Down")
        PriceListTwenty.append("Down")
        PriceListTen.append("Down")
        PriceListFive.append("Down")
        PriceListThree.append("Down")"""
        Store.StoreInfo("Direction: Down \t Current Price: " + CurPrice + "\t Old Price: " + str(oldPrice))
        oldPrice = CurPrice
    else:
        Settings.Cypto_Settings[Cypto]["Direction"] = "No Change"
    Settings.Cypto_Settings[Cypto]["Direction_Old"] = str(oldPrice)
    Settings.Save()


def CalInfo():
    global last
    Store.StoreInfo("Last direction: " + last)
    global PriceListAll
    global PriceListTwenty
    global PriceListTen
    global PriceListFive
    global PriceListThree

    AllUp = PercenCal(PriceListAll.count("Up"), len(PriceListAll))
    AllDown = PercenCal(PriceListAll.count("Down"), len(PriceListAll))

    global TwentyUp
    global TwentyDown
    TwentyUp = PercenCal(PriceListTwenty.count("Up"), len(PriceListTwenty))
    TwentyDown = PercenCal(PriceListTwenty.count("Down"), len(PriceListTwenty))
    if len(PriceListTwenty) == 21:
        PriceListTwenty.pop(0)

    global TenUp
    global TenDown
    TenUp = PercenCal(PriceListTen.count("Up"), len(PriceListTen))
    TenDown = PercenCal(PriceListTen.count("Down"), len(PriceListTen))  #
    if len(PriceListTen) == 11:
        PriceListTen.pop(0)

    FiveUp = PercenCal(PriceListFive.count("Up"), len(PriceListFive))
    FiveDown = PercenCal(PriceListFive.count("Down"), len(PriceListFive))
    if len(PriceListFive) == 6:
        PriceListFive.pop(0)

    ThreeUp = PercenCal(PriceListThree.count("Up"), len(PriceListThree))
    ThreeDown = PercenCal(PriceListThree.count("Down"), len(PriceListThree))
    if len(PriceListThree) == 4:
        PriceListThree.pop(0)

    Store.StoreInfo(
        str(len(PriceListThree)) + "\t" + str(len(PriceListFive)) + "\t" + str(len(PriceListTen)) + "\t" + str(
            len(PriceListTwenty)) + "\t" + str(len(PriceListAll)))
    Store.StoreInfo(str(ThreeUp) + "\t" + str(FiveUp) + "\t" + str(TenUp) + "\t" + str(TwentyUp) + "\t" + str(AllUp))
    Store.StoreInfo(
        str(ThreeDown) + "\t" + str(FiveDown) + "\t" + str(TenDown) + "\t" + str(TwentyDown) + "\t" + str(AllDown))


def PercenCal(Num, Total):
    return Num / Total * 100


def StopLoss(StopPer):
    if TwentyDown > 60 and TenDown > 50:
        if StopPer != 0.1:
            Selling.StopPercentageNS = 0.1
            Selling.DirectionAdjust = True
            Store.StoreInfo("Decresed Stop Percentage to: 0.1")

    elif TwentyUp > 60 and TenUp > 50:
        if StopPer != 0.5:
            Selling.StopPercentageNS = 0.5
            Selling.DirectionAdjust = True
            Store.StoreInfo("Increses Stop Percentage to: 0.5")

    elif StopPer != 0.3:
        Selling.StopPercentageNS = 0.3
        Selling.DirectionAdjust = True
        Store.StoreInfo("Reset Stop Percentage to: 0.3")


def BuyLoss():
    if TwentyDown > 60 and TenDown > 50:
        if Buying.StopPercentage != 0.5:
            Buying.StopPercentage = 0.5
            Buying.DirectionAdjust = True
            Store.StoreInfo("Increses Stop Percentage to: 0.5")

    elif TwentyUp > 60 and TenUp > 50:
        if Buying.StopPercentage != 0.1:
            Buying.StopPercentage = 0.1
            Buying.DirectionAdjust = True
            Store.StoreInfo("Decresed Stop Percentage to: 0.1")

    elif Buying.StopPercentage != 0.3:
        Buying.StopPercentage = 0.3
        Buying.DirectionAdjust = True
        Store.StoreInfo("Reset Stop Percentage to: 0.3")
