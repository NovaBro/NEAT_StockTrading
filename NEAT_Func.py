import numpy as np
import neat, pickle, sys
from Market import *
import gymnasium as gym
import matplotlib.pyplot as plt
import visualize as vz
#np.set_printoptions(threshold=sys.maxsize)
np.set_printoptions(suppress=True)

config_file = "NEATStock/config.INI"
outputAction = np.zeros((dataSizes, 6))
wealthHist = np.zeros((dataSizes, len(dataLibrary)))
randStart = 0
validCount = 0
balanceCONSTANT = 10000

def findAmount(balance, percentage:float, price:float):
    #depricated
    availableFunds = balance * percentage
    return int(availableFunds / price)

def eval_genomes(genomes, config):
    global outputAction, randStart, dataSplitPoint
    randStart = np.random.randint(0, (dataSplitPoint - trainingLength))
    for genome_id, genome in genomes:
        totalWealths = 0
        for d in range(len(dataLibrary)):
            genData = standLibrary[d].to_numpy()
            ownedShares = 0
            balance = balanceCONSTANT
            genome.fitness = balance
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            

            for i in range(trainingLength):
                dayData = genData[i + randStart]
                input = np.zeros(7)
                input[0:6] = dayData
                input[6] = balance / balanceCONSTANT
                output = net.activate(input)
                action = int(np.argmax(output[0:3]))
                price = adjLibClose[d][i + randStart]
                amount = int(output[3] * 20)

                if action == 0:
                    balance, ownedShares, valid = buy(balance, ownedShares, amount, price)
                elif action == 1:
                    balance, ownedShares, valid = sell(balance, ownedShares, amount, price)

            totalWealths += balance + ownedShares * adjLibClose[d][-1]

        genome.fitness = totalWealths / len(dataLibrary)

chosenStartingPoint = 0
def winnerRerun(genome, config):
    global outputAction, wealthHist, chosenStartingPoint, dataSplitPoint
    
    totalWealths = np.zeros((len(dataLibrary)))
    randStart = np.random.randint(0, (dataSplitPoint - trainingLength))
    chosenStartingPoint = randStart
    for d in range(len(dataLibrary)):
        genData = standLibrary[d].to_numpy()
        ownedShares = 0
        balance = balanceCONSTANT
        genome.fitness = balance
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        
        for i in range(trainingLength):
            dayData = genData[i + randStart]
            input = np.zeros(7)
            input[0:6] = dayData
            input[6] = balance / balanceCONSTANT
            output = net.activate(input)
            action = int(np.argmax(output[0:3]))
            price = adjLibClose[d][i + randStart]
            amount = int(output[3] * 20)

            if action == 0:
                balance, ownedShares, valid = buy(balance, ownedShares, amount, price)
            elif action == 1:
                balance, ownedShares, valid = sell(balance, ownedShares, amount, price)
            netWealth = balance + ownedShares * adjLibClose[d][i]

            wealthHist[i + randStart][d] = netWealth # + wealthHist[i + randStart][d]
        totalWealths += balance + ownedShares * adjLibClose[d][-1]

    wealthHist = wealthHist # / len(dataLibrary)
    #genome.fitness = totalWealths / len(dataLibrary) #balance + ownedShares * adjLibClose[d][-1]

testWealthHist = np.zeros((dataSizes))
def winnerTest(genome, config):
    global testWealthHist, dataSplitPoint, validCount
    genData = TSLA_Stand.to_numpy()
    ownedShares = 0
    balance = balanceCONSTANT
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    actIndex = 0

    for i in range(dataSizes - dataSplitPoint):
        dayData = genData[i + dataSplitPoint]
        input = np.zeros(7)
        input[0:6] = dayData
        input[6] = balance / balanceCONSTANT
        output = net.activate(input)
        action = int(np.argmax(output[0:3]))
        price = TSLA_adjClose[i + dataSplitPoint]
        valid = 0
        amount = int(output[3] * 20)
        if action == 0:
            balance, ownedShares, valid = buy(balance, ownedShares, amount, price)
        elif action == 1:
            balance, ownedShares, valid = sell(balance, ownedShares, amount, price)

        netWealth = balance + ownedShares * TSLA_adjClose[i + dataSplitPoint]
        if valid:
            validCount += 1

        if (valid or True): 

            outputAction[actIndex][0] = action
            outputAction[actIndex][1] = amount
            outputAction[actIndex][2] = balance
            outputAction[actIndex][3] = ownedShares
            outputAction[actIndex][4] = netWealth
            outputAction[actIndex][5] = i + dataSplitPoint
            actIndex += 1

        
        testWealthHist[i + dataSplitPoint] = netWealth

    return balance + ownedShares * TSLA_adjClose[-1]

def main():
    global config_file, outputAction, config, validCount
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1000))

    # Run generations.
    winner = p.run(eval_genomes, 30)
    vz.plot_stats(stats)
    vz.plot_species(stats)
    vz.draw_net(config, winner)

    winnerRerun(winner, config)
    finalTestBalance = winnerTest(winner, config)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))
    
    
    #fileOpen = open("NEATStock/outputAction.txt", "w")
    #fileOpen.write("Action,Amount,Balance,Owned,Wealth,Day")
    #fileOpen.close()
    #np.savetxt("NEATStock/outputAction.txt", outputAction, fmt="%f")
    df = pd.DataFrame(data=outputAction, columns=["Action","Amount","Balance","Owned","Wealth","Day"])
    df.to_csv("NEATStock/outputAction.txt")
    #Action, Amount of Stock, Balance, Stock owned, net wealth, day
    fig, ax = plt.subplots(2, 1)
    fig.set_figheight(4)
    fig.set_figwidth(12)
    line1 = ax[0].plot(wealthHist[:,0], label = "Net Wealth", color = "black")
    line2 = ax[0].plot(wealthHist[:,1], label = "Net Wealth", color = "red")
    line3 = ax[0].plot(wealthHist[:,2], label = "Net Wealth", color = "orange")
    line4 = ax[0].plot(testWealthHist, label = "Net Wealth", color = "blue")
    line5 = ax[1].plot(adjLibClose[0], label = "TSLA", color = "black")
    line6 = ax[1].plot(adjLibClose[1], label = "APPLE", color = "red")
    line7 = ax[1].plot(adjLibClose[2], label = "AMZN", color = "orange")
    #averageAll = (adjLibClose[0] + adjLibClose[1] + adjLibClose[2]) / 3
    #line2 = ax[1][0].plot(averageAll, label = "AMZN", color = "purple")
    #ax1.legend(loc = "upper right")
    print("Final Wealth: ", wealthHist[chosenStartingPoint + trainingLength - 1,:])
    buyHoldValue1 = buyAndHold(balanceCONSTANT, 0, chosenStartingPoint, trainingLength)
    print("Buy and Hold Balance: ", buyHoldValue1)
    print("Percentage Change ReRun: ", (wealthHist[chosenStartingPoint + trainingLength - 1,:] / buyHoldValue1 )* 100 - 100, "%")
    buyHoldValue2 = TSLAbuyAndHold(balanceCONSTANT, 0, dataSplitPoint, -1)
    print("TSLA Buy and Hold Balance: ", buyHoldValue2)
    print("TSLA Winner result: ", finalTestBalance)
    print("TSLA Percentage Increase ReRun: ", finalTestBalance / buyHoldValue2 * 100 - 100, "%")
    print("Number of Valid Actions Done: ", validCount)
    plt.show()

main()