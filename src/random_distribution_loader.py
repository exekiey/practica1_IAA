from distribution import Distribution
import random

class RandomDistributionLoader:
    def __init__(self):
        self.distrubution = None
    
    def loadDistribution(self, amount_of_variables):
        if (amount_of_variables < 1):
            raise ValueError("El número de variables de la distribución debe ser al menos 1.")
        amount_of_values = 2**amount_of_variables
        self.distrubution = Distribution(amount_of_values)
        # Generate random values and normalize them before inserting into the distribution
        values = [random.random() for _ in range(amount_of_values)]
        total_sum = sum(values)
        for index, value in enumerate(values):
            self.distrubution.insert(index, value / total_sum)

    def getDistribution(self):
        return self.distrubution
