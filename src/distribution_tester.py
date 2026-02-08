from distribution import Distribution
import random
import time
class DistributionTester:
	def __init__(self, distribution: Distribution):
		self.distribution = distribution
	
	def testWithRandomMasks(self):
		number_of_interest_variables = random.randint(1, self.distribution.number_of_variables)
		for _ in range(number_of_interest_variables):
			random_variable = random.randint(0, self.distribution.number_of_variables - 1)
			self.distribution.setInterestVariable(random_variable)

		number_of_conditioned_variables = 0
		for _ in range(random.randint(0, self.distribution.number_of_variables)):			
			random_variable = random.randint(0, self.distribution.number_of_variables - 1)
			if random_variable in self.distribution.getIndexesFromMask(self.distribution.interest_variables_mask):
				continue
			random_value = random.randint(0, 1)
			number_of_conditioned_variables += 1
			self.distribution.setConditionedVariable(random_variable, random_value)
		t0 = time.time()
		conditioned_distribution = self.distribution.buildConditionDistribution()
		t1 = time.time()
		return (number_of_interest_variables, number_of_conditioned_variables, t1 - t0)