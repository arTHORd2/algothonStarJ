#!/usr/bin/env python

# RENAME THIS FILE WITH YOUR TEAM NAME.

import numpy as np

nInst = 100
currentPos = np.zeros(nInst)

# Dummy algorithm to demonstrate function format.
def getMyPosition(prcSoFar):
    global currentPos
    (nins,nt) = prcSoFar.shape
    rpos = np.array([int(x) for x in 1000 * np.random.randn(nins)])
    currentPos += rpos
    print("Return type is: " + str(type(currentPos)))
    print(currentPos)
    # The algorithm must return a vector of integers, indicating the position of each stock.
    # Position = number of shares, and can be positve or negative depending on long/short position.

    
    
    #     Determine volatility of price based on average % change each day?

    # Volatility index -> class into categories

    # Set a certain value of %rise/fall tolerance depending on which category of risk

    # If profit/loss% exceeds certain amount, then sell/buy

    # If position = 0, buy/short if running average indicates %rise/fall - commission rate

    # If position /=0, buy/sell if running average indicates %fall/rise - commission rate
    
    # PSEUDOCODE
    # currentTradedPerStock = {}
    
    # bigSpikeThreshold = 0 (% of long term threshold)
    # shortTermTimeRange = 5 days
    # "stockTradingVolumeBasedOnShortTermChange = $X / shortTermPriceIncrease"
    
    # Check our current days holdings
    # for each stock we have:
        # check if it's now above $10k
        # if it is, sell so that it isn't above $10k


    #write something that stops algo from buying if position is already at 10k
    
    # calculating short term threshold
    # for each stock:
        # calculate 5 day average price (including magnitude)
            # on day N-1, calculate average from day N-5 to day N-1
            # on day N, calculate average from N-4 to day N
            # comapre difference in changes between these two averages
            # (N[0] - (N[-5]) )/ 5
        # Determine short term volatility figure based on 5 days
        # Class volatility figures into categories
        # Depending on the volatility figure we had before, set % change threshold 

    #calculating long term threshold
    #for each stock:
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

    
            
            
            

    return currentPos
