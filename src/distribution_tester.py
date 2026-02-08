from distribution import Distrubution
import random
import time
class DistributionTester:
	def __init__(self, distribution: Distrubution):
		self.distribution = distribution
	
	def testWithRandomMasks(self):
		t0 = time.time()
		number_of_interest_variables = random.randint(1, self.distribution.number_of_variables)
		for _ in range(number_of_interest_variables):
			random_variable = random.randint(0, self.distribution.number_of_variables - 1)
			self.distribution.setInterestVariable(random_variable)

		number_of_conditioned_variables = 0
		for _ in range(random.randint(0, self.distribution.number_of_variables)):			
			random_variable = random.randint(0, self.distribution.number_of_variables - 1)
			if random_variable in self.distribution.getIndexesFromMask(self.distribution.interest_variables_mask):
				number_of_conditioned_variables += 1
				continue
			random_value = random.randint(0, 1)
			self.distribution.setConditionedVariable(random_variable, random_value)
		t1 = time.time()
		return (number_of_interest_variables, number_of_conditioned_variables, t1 - t0)