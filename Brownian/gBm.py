import random
import math
import matplotlib.pyplot as plt

class gBm:
    def __init__(self, amount, price=10.0, life=252, drift=.10, volatility=.4):
        self.totalGain = None
        self.prevLogReturn = None
        self.returns = []
        self.price = price
        self.lifeSpan = life
        self.values = [self.price]

        self.lifeDrift = drift
        #10%
        self.dailyDrift = self.lifeDrift / self.lifeSpan
        #0.04%

        self.lifeVolatility = volatility
        #40%
        self.dailyVolatility = self.lifeVolatility / math.sqrt(self.lifeSpan)
        #2.52%

        self.mean = self.dailyDrift - self.dailyVolatility**2 / 2
        #0.01%

        self.totalGain = None

        
        self.update(amount)

    def update(self, amount):
        for x in xrange(amount):
            self.run()

    def run(self):
        randomAmount = random.gauss(0,1)
        percentReturn = self.mean + (randomAmount * self.dailyVolatility)
        logReturn = math.exp(percentReturn)
        if self.prevLogReturn == None:
            self.totalGain = (logReturn - 1)
        else:
            self.totalGain += (self.prevLogReturn + 1) * (logReturn - 1)
        self.prevLogReturn = self.totalGain
        end = logReturn * self.values[-1]
        self.values.append(end)
        self.returns.append(logReturn)

    def show(self):
        plt.plot(self.values)
        plt.ylabel('Price')
        plt.xlabel('Time')
        plt.show()
