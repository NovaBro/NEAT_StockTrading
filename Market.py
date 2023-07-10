import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import neat, os
import gymnasium as gym

def standerdize(dataSet):
    standData = ((dataSet - dataSet.mean()) / (dataSet.std())) 
    return standData

#--Settings--

TSLAdata = pd.read_csv('./General/TSLA.csv')
TSLAdata = TSLAdata.iloc[662:1361]
TSLAdata = TSLAdata.loc[:, ["Open", "High", "Low", "Close", "Adj Close", "Volume"]]

APPLdata = pd.read_csv('./NEATStock/AAPL.csv')
APPLdata = APPLdata.loc[:, ["Open", "High", "Low", "Close", "Adj Close", "Volume"]]

AMZNdata = pd.read_csv('./NEATStock/AMZN.csv')
AMZNdata = AMZNdata.loc[:, ["Open", "High", "Low", "Close", "Adj Close", "Volume"]]


TSLA_adjClose = TSLAdata["Adj Close"].to_numpy()
APPL_adjClose = APPLdata["Adj Close"].to_numpy()
AMZN_adjClose = AMZNdata["Adj Close"].to_numpy()
dataSizes = 699
trainingLength = 199
dataSplitPoint = 600#200

TSLA_Stand = standerdize(TSLAdata)
APPL_Stand = standerdize(APPLdata)
AMZN_Stand = standerdize(AMZNdata)

dataLibrary = [TSLAdata, APPLdata, AMZNdata]
adjLibClose = [TSLA_adjClose, APPL_adjClose, AMZN_adjClose]
standLibrary = [TSLA_Stand, APPL_Stand, AMZN_Stand]

#normData = ((TSLAdata - TSLAdata.min()) / (TSLAdata.max() - TSLAdata.min()))#["Adj Close"] #Normalize
#standData = ((TSLAdata - TSLAdata.mean()) / (TSLAdata.std())) #["Adj Close"] #Standardize

#stockData = TSLAdata.iloc[0]
#print(stockData[0])

print(TSLAdata)
#print(APPLdata)
#print(AMZNdata)
#------------

def generateGraph(ax):
    #balanceFig = plt.figure()
    #balanceAX = balanceFig.add_subplot()
    ax.clear()
    ax.plot(xVal, yVal)
    #plt.show()

def updateBalanceGraph(newBalance):
    global xVal, yVal
    yVal[0:10] = yVal[1:12]
    yVal[10] = newBalance

def buy(balance, ownedShares, buyAmount, stockPrice):
    if (stockPrice * buyAmount > balance or buyAmount == 0):
        return (balance), (ownedShares), 0
    else:
        ownedShares += buyAmount
        balance -= stockPrice * buyAmount
        return balance, ownedShares, 1

def sell(balance, ownedShares, sellAmount, stockPrice):
    if (sellAmount > ownedShares or sellAmount == 0):
        return (balance), (ownedShares), 0
    else:
        ownedShares -= sellAmount
        balance += stockPrice * sellAmount
        return balance, ownedShares, 1

def buyButton(buyAmount, stockPrice, ax, canvas):
    buy(buyAmount, stockPrice)
    #updateBalanceGraph(balance)
    generateGraph(ax)
    canvas.draw()
    #print("New Balance: ", balance, "\nOwned Shares: ", ownedShares)

def sellButton(buyAmount, stockPrice, ax, canvas):
    sell(buyAmount, stockPrice)
    #updateBalanceGraph(balance)
    generateGraph(ax)
    canvas.draw()
    #print("New Balance: ", balance, "\nOwned Shares: ", ownedShares)

def buyAndHold(balance, ownedShares, start, stop):
    avgWealth = np.zeros(len(dataLibrary))
    for d in range(len(adjLibClose)):
        amount = int(balance / adjLibClose[d][start])
        newBalance, newSharesOwned, valid = buy(balance, ownedShares, amount, adjLibClose[d][start])
        newBalance, newSharesOwned, valid = sell(newBalance, newSharesOwned, newSharesOwned, adjLibClose[d][stop])
        #print("Start Price: ", d[start], " stop price: ", d[stop])
        #print("New Balance: ", newBalance + newSharesOwned * d[-1])
        avgWealth[d] = newBalance + newSharesOwned * adjLibClose[d][-1]
    return avgWealth #/len(adjLibClose)

#print("Average Buy and Hold Balance: ", buyAndHold(1000, 0, 0, 500))

def TSLAbuyAndHold(balance, ownedShares, start, stop):
    avgWealth = 0
    amount = int(balance / TSLA_adjClose[start])
    newBalance, newSharesOwned, valid = buy(balance, ownedShares, amount, TSLA_adjClose[start])
    newBalance, newSharesOwned, valid = sell(newBalance, newSharesOwned, newSharesOwned, TSLA_adjClose[stop])
    #print("Start Price: ", TSLA_adjClose[start], " stop price: ", TSLA_adjClose[stop])
    #print("New Balance: ", newBalance + newSharesOwned * TSLA_adjClose[-1])
    avgWealth += newBalance + newSharesOwned * TSLA_adjClose[-1]
    return avgWealth

def marketDriver():
    balance = 1000
    ownedShares = int(balance / TSLA_adjClose[55])
    #buyAndHold(1000, ownedShares, 0)
    newPrice = TSLA_adjClose[999]
    newBalance = newPrice * ownedShares
    print("New price: ", f'{newPrice:.2f}')
    print(TSLA_adjClose[0])
    print("Buy and Hold Value: ", newBalance)
    #The value to beat for buy and hold: 16044.453348
    fig = plt.figure()
    ax = fig.subplots()
    ax.plot(TSLA_adjClose)
    #ax.plot(adjClose[500:865])
    #ax.plot(adjClose[865:1230])
    ax.axvline(x=500)
    ax.axvline(x=999)
    plt.show()
    return

#marketDriver()