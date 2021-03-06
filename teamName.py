#!/usr/bin/env python

# RENAME THIS FILE WITH YOUR TEAM NAME.

import numpy as np
nInst = 100
currentPos = []
currentTradedPerStock = []
for i in range(0, nInst):
            currentTradedPerStock.append({"numberOfStockOnHand" : 0, "priceBroughtAt" : 0})
# index = instrument
# [
#     {
#         priceBoughtAt: 23.1,
#         numberOfStockOnHand: 1
#     }

# ]

commissionRate = 0.5
shortTermTimeRange = 10
init = False

# Changeable coefficients
coefficient = 0.2 # Higher means higher tolerance for short-term movement
coefficient2Selling = 0.05 # Lower means you sell more
coefficientBuying = 0.1 # Lower means we buy more
longTermCoefficient = 0.2 # Lower means you will action long-term trades
negativeFactor = -0.23

# Dummy algorithm to demonstrate function format.
def getMyPosition(prcSoFar):
    global currentPos
    global init
    currentPos = []
    # nt is number of elements in a list
    # nins is the number of lists
    (nins,nt) = prcSoFar.shape

    for x in range(0, nInst):
        soh = currentTradedPerStock[x]["numberOfStockOnHand"]
        currentPos.append(soh)

    # currentPos = np.array([currentTradedPerStock[x]["numberOfStockOnHand"] for x in range(0, nInst)])
    # rpos = np.array([int(x) for x in 1000 * np.random.randn(nins)])
    # currentPos += rpos
    # print("Return type is: " + str(type(currentPos)))
    # print(currentPos)
    # The algorithm must return a vector of integers, indicating the position of each stock.
    # Position = number of shares, and can be positve or negative depending on long/short position.

    #     Determine volatility of price based on average % change each day?

    # Volatility index -> class into categories

    # Set a certain value of %rise/fall tolerance depending on which category of risk

    # If profit/loss% exceeds certain amount, then sell/buy

    # If position = 0, buy/short if running average indicates %rise/fall - commission rate

    # If position /=0, buy/sell if running average indicates %fall/rise - commission rate
    
    # PSEUDOCODE

    stocksThatExceed10k = checkCurrentHoldingsExceed10k(prcSoFar, nt)
    # {stock index : position}
    
    # calculating short term threshold
    for instrumentIndex in range(0, nInst):
        # print("=====")
        currentlyHeldStock = currentTradedPerStock[instrumentIndex]

        # skip stock if at 10k
        if instrumentIndex in stocksThatExceed10k.keys():
            currentlyHeldStock["numberOfStockOnHand"] = stocksThatExceed10k[instrumentIndex]
            continue

        position = getPosition_LongTermThreshhold(prcSoFar, instrumentIndex, nt)
        # print("Long term position is: ", position)
        if not position:
            position = getPosition_ShortTermVolatility(prcSoFar, instrumentIndex, nt)
            # print("Short term position is: ", position)
        
        currentPos[instrumentIndex] = negativeFactor * float(position)
          
    for x in range(0, nInst):
        currentTradedPerStock[x]["numberOfStockOnHand"] = currentPos[x]
        currentTradedPerStock[x]["priceBroughtAt"] = prcSoFar[x][nt - 1]
    return np.array(currentPos)

def checkCurrentHoldingsExceed10k(prcSoFar, nt):
    # Check our current days holdings
    # for each stock we have:
        # check if it's now above $10k
        # if it is, sell so that it isn't above $10k
    stocksToSell = {}

    for curStock in range(0, nInst):
        stockPrice = prcSoFar[curStock][nt - 1]
        originalVolume = currentTradedPerStock[curStock]["numberOfStockOnHand"]

        if ((stockPrice * originalVolume) > 10000):
            # need to sell if exceed 10k
            curVolume = originalVolume

            # find how many we can keep
            while ((stockPrice * curVolume) > 10000):
                curVolume -= 1

            stocksToSell[curStock] = curVolume

    return stocksToSell

def getPosition_ShortTermVolatility(prcSoFar, curStockIndex, nt):

    newPosition = 0

    if (nt < shortTermTimeRange):
        averageSoFar = sum([x for x in prcSoFar[curStockIndex][0:(nt - 1)]]) / nt
        return averageSoFar

    startIndex = nt - (shortTermTimeRange - 1) - 1 # index 5 days ago
    endIndex = nt - 1 # today index
    prevIndex = endIndex - 1 # previous day index

    shortTermAverage = sum([x for x in prcSoFar[curStockIndex][startIndex:endIndex]]) / shortTermTimeRange
    priceChange = prcSoFar[curStockIndex][endIndex] - prcSoFar[curStockIndex][endIndex - 1]

    volatility = (priceChange / shortTermAverage) * 100
    stockPrice = prcSoFar[curStockIndex][endIndex]

    if (volatility - commissionRate > (coefficient * shortTermAverage)):
        # only positive, and bigger
        # sell a certain amount of the difference between price and coefficient * shortTermAverage
        # irregardless of amount of stock we have on hand.
        movementInPosition = (stockPrice - (coefficient * shortTermAverage)) * coefficientBuying
        newPosition = currentTradedPerStock[curStockIndex]["numberOfStockOnHand"] + movementInPosition

    elif (volatility - commissionRate < -(coefficient * shortTermAverage)):
        # buy a certain amount
        movementInPosition = (stockPrice - (coefficient * shortTermAverage)) * coefficient2Selling
        newPosition = currentTradedPerStock[curStockIndex]["numberOfStockOnHand"] - movementInPosition

    return newPosition

    # calculate 5 or less day average price (including magnitude)
    # on day N-1, calculate average from day N-5 to day N-1
            # on day N, calculate average from N-4 to day N
            # comapre difference in changes between these two averages
            # (N[0] - (N[-5]))/ 5
        # Determine short term volatility figure based on 5 days
        # Class volatility figures into categories
        # Depending on the volatility figure we had before, set % change threshold

def getPosition_LongTermThreshhold(prcSoFar, curStockIndex, nt):
    newPos = 0

    sumList = []

    for x in range(0, nt):
        sumList.append(prcSoFar[curStockIndex][x])
    averageSoFar = sum(sumList) / nt

    curStockPrice = prcSoFar[curStockIndex][nt - 1]
    curMonetaryPosition = currentTradedPerStock[curStockIndex]["numberOfStockOnHand"] * curStockPrice
    # print("Current stock price is: ", curStockPrice)
    # print("Our current monetary position for this stock is: ", curMonetaryPosition)
    if (curStockPrice > (1+longTermCoefficient) * averageSoFar ):
        newPos = curMonetaryPosition + (((1-longTermCoefficient * averageSoFar) - curStockPrice)/ curStockPrice) * 10000

    elif  (curStockPrice < (1-longTermCoefficient) * averageSoFar):
        newPos = curMonetaryPosition - ((curStockPrice - (1+longTermCoefficient * averageSoFar))/ curStockPrice) * 10000

    else:
        newPos = False
    return newPos
#calculating long term threshold
        # calculate running average price (average of prices up to present day)

        # check absolute profit/loss threshold 
        # if total profit/loss > bigSpikeThreshold, then sell/buy to take profit/stop loss
        # if total price increase > bigSpikeThreshold: 
            # sell (because we think it's about to go down)
        # if abs(total price decrease) > abs(bigTroughThreshold):
            # buy/sell (test different approaches with sample prices)

        # if total profit/loss < threshold, then
            # if price change compared to running average is above % change threshold
                # if price change > 0, exit position because of short term rise
                # if price change < 0, enter position because of short term fall?