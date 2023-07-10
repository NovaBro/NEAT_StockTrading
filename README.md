![avg_fitness](https://github.com/NovaBro/NEAT_StockTrading/assets/57100555/41d776d2-7eeb-4031-a8cd-577acf1115b0)# NEAT_StockTrading
This project was an attempt at using the Neural Evolutions of Augmented Topologies (NEAT) algorithm to develop a neural network (NN) that could trade stocks better than the "buy and hold" strategy.

There is alot of things going on and potential problems in this project which I will do my best to explain.

Overiew of set up:
So the hope is that from reading pricing and volume data, the NN would devlop a strategy to make returns better than simply buying and holding a stock. The data used for training comes from Yahoo Finance using data for Apple, Tesla, and Amazon. The data is standardized before training the NN, and cleaned it. I have split the data into two parts, one fore training and one for testing. 

Concerns, Thoughts, and Struggles:
There are many parameters to making the enviroment for the NN to evolve in that I think have no sttraight answers. For one, do I randomize the training start point? For example, when I test the fitness of multiple geneomes, do I give the same starting point in a stock period or do I randomize the starting point for each generation? Randomization potentially prevents the NN from over fitting the data and be more generalizable. However, from viewing the average fitness graphs, randomizations makes it hard to optimize and improve the NN. Another crucial component it the config file of the NEAT enviroment. What is the optimal mutation rate? How high should I allow the reporduction rate? And so on. Having high mutation and reproductions rates will potentially allow for more improvments and complex strategies, but those are hard to evolve. Having low rates will potentially overfit the data but be easier to see results and improvments.
Another probelm I seem to have with this NN is that it often settles on the solution of buy and holding. I cannot tell weather this means that it is impossible to determine future stock movement with previous price movements (which I think is unlikely), or the best strategy is buy and hold (which I think is also unlikely), or simply I do not have a good enviroment to develop a complex NN than can make good strategies. 

RESULTS:

This is the average fitness when randomized strarting points are off:

![avg_fitness](https://github.com/NovaBro/NEAT_StockTrading/assets/57100555/4292f0f8-bbac-4fd6-93b7-0c9ce473701b)

Here is the Training and testing performance with this method. The top graph is the NN and the bottom graph are the stock price movements.
Black is TSLA, APPL is red, AMZN is orange. In the top graph, blue is the testing performance. The others are the the training results.
![Figure_1](https://github.com/NovaBro/NEAT_StockTrading/assets/57100555/638c8760-2097-4f8b-9e17-bd976138e906)

Same images but when randomization is on:

![avg_fitness](https://github.com/NovaBro/NEAT_StockTrading/assets/57100555/b1a7eac0-e15f-43fe-902c-daea792bd00c)

![Figure_2](https://github.com/NovaBro/NEAT_StockTrading/assets/57100555/e0f9f6b5-b44e-492d-9413-50313c421630)


