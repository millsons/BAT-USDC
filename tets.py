import decimal

curPrice = 0.006212
TrailStop = 0.00627113

TrailDistance = float(curPrice) - float(TrailStop)
TrailDistance = decimal.Decimal(TrailDistance)
print(str(round(TrailDistance, 6)))

