import math

class Distribution:
    def __init__(self, data_or_size):
        if isinstance(data_or_size, int):
            self.data = [0.0] * data_or_size
        elif isinstance(data_or_size, list):
            self.data = data_or_size
        else:
            raise TypeError("El constructor de Distrubution debe recibir un entero o una lista.")
        # Calculate the number of variables based on the length of the data list
        self.number_of_variables = int(math.log2(len(self.data)))
        # Initialize masks for conditioned variables, conditioned values, and interest values
        self.conditioned_variables_mask = [0] * self.number_of_variables
        self.conditioned_values_mask = [0] * self.number_of_variables
        self.interest_variables_mask = [0] * self.number_of_variables
    
    def insert(self, key: int, value: float):
        # Check if the key is within the valid range and if the value is a valid probability
        if key < 0 or key >= len(self.data):
            raise IndexError("Índice de clave fuera de rango.")
        elif value < 0 or value > 1:
            raise ValueError("El valor de probabilidad debe estar entre 0 y 1.")
        self.data[key] = value

    def showDistribution(self):
        # Header, showing variable names in the format Xn where n is the variable index
        header: str = " ".join(f"X{self.number_of_variables - i}" for i in range(self.number_of_variables))
        print(f"{header} Probabilidad")
        # Each row corresponds to a combination of variable values
        for index, probability in enumerate(self.data):
            # Convert the index to a binary string, padded with zeros to match the number of variables
            binary: str = format(index, f"0{self.number_of_variables}b")
            # Join the bits with spaces for better readability
            row: str = " " + "  ".join(bit for bit in binary)
            print(f"{row}     {probability:.2f}")

    def showConditionedVariablesMask(self):
        # Reverse the mask for display, so the order matches the variable order in the distribution table
        formatted_mask: list[int] = self.conditioned_variables_mask[::-1]  
        string_mask: str = "".join(str(value) for value in formatted_mask)
        print("Máscara de variables condicionadas: ", string_mask)

    def showConditionedValuesMask(self):
        # Reverse the mask for display, so the order matches the variable order in the distribution table
        formatted_mask: list[int] = self.conditioned_values_mask[::-1]
        string_mask: str = "".join(str(value) for value in formatted_mask)
        print("Máscara de valores condicionados: ", string_mask)

    def showInterestValuesMask(self):
        # Reverse the mask for display, so the order matches the variable order in the distribution table
        formatted_mask: list[int] = self.interest_variables_mask[::-1]
        string_mask: str = "".join(str(value) for value in formatted_mask)
        print("Máscara de variables de interés: ", string_mask)

    def setConditionedVariable(self, variable_index: int, value: int):
        # Check if the variable index is within the valid range and if the value is boolean
        if variable_index < 0 or variable_index >= self.number_of_variables:
            raise IndexError("Índice de variable condicionada fuera de rango.")
        if value not in (0, 1):
            raise ValueError("El valor de la variable condicionada debe ser 0 o 1.")
        # Check if the variable is already marked as an interest variable
        if variable_index in self.getIndexesFromMask(self.interest_variables_mask):
            raise ValueError("Una variable no puede ser de interés y condicionada al mismo tiempo.")
        
        self.conditioned_variables_mask[variable_index] = 1
        self.conditioned_values_mask[variable_index] = value

    def setInterestVariable(self, variable_index: int):
        # Check if the variable index is within the valid range
        if variable_index < 0 or variable_index >= self.number_of_variables:
            raise IndexError("Índice de variable de interés fuera de rango.")
        # Check if the variable is already marked as a conditioned variable
        if variable_index in self.getIndexesFromMask(self.conditioned_variables_mask):
            raise ValueError("Una variable no puede ser de interés y condicionada al mismo tiempo.")
        self.interest_variables_mask[variable_index] = 1

    def resetMasks(self):
        self.conditioned_variables_mask = [0] * self.number_of_variables
        self.conditioned_values_mask = [0] * self.number_of_variables
        self.interest_variables_mask = [0] * self.number_of_variables
        
    def buildConditionDistribution(self):
        conditioned_indexes: list[int] = self.getIndexesFromMask(self.conditioned_variables_mask)
        valid_indexes: list[int] = self.__getValidIndexes(conditioned_indexes)
        interest_indexes: list[int] = self.getIndexesFromMask(self.interest_variables_mask)

        new_distribution_size: int = 2 ** len(interest_indexes)
        conditioned_distribution: Distribution = Distribution(new_distribution_size)
        interest_index_translator = {}

        for new_index, current_shift in enumerate(interest_indexes):
            interest_index_translator[current_shift] = new_index
        for conditioned_row in range(new_distribution_size):
            current_index_mask = []
            for current_shift in range(len(interest_indexes)):
                current_interest_bit = (conditioned_row >> current_shift) & 1
                current_index_mask.append(current_interest_bit)
            # Will store the indexes of the valid rows that have been used
            used_indexes = []
            for current_valid_index in valid_indexes:
                if self.__checkValidInterestRow(interest_indexes, current_valid_index, current_index_mask, interest_index_translator):
                    conditioned_distribution.data[conditioned_row] += self.data[current_valid_index]
                    used_indexes.append(current_valid_index)
            # Remove used indexes (rows) from valid indexes (rows) to optimize the next iterations
            for used_index in used_indexes:
                valid_indexes.remove(used_index)

        conditioned_distribution.__normalize()
        return conditioned_distribution

    def __normalize(self):
        sumatory = 0
        for current_probability in self.data:
            sumatory += current_probability
        if sumatory == 0:
            raise ValueError("Distribución no se puede normalizar: suma de probabilidades es cero.")
        
        normalized_probability = []
        for current_probability in self.data:
          normalized_probability.append(current_probability / sumatory)
        self.data = normalized_probability

    def getIndexesFromMask(self, mask: list):
        indexes: list = []
        for i in range(self.number_of_variables):
            if mask[i] == 1:
                indexes.append(i)
        return indexes
    
    def __checkValidInterestRow(self, interest_indexes: list, current_row: int, values_mask: list, index_translator: dict):
      for current_interest_index in interest_indexes:
        current_row_interest_bit = (current_row >> current_interest_index) & 1
        if current_row_interest_bit != values_mask[index_translator[current_interest_index]]:
          return False
      return True
    
    def __checkValidConditionedRow(self, conditioned_indexes: list, current_row: int):
      for current_conditioned_index in conditioned_indexes:
        current_row_conditioned_bit = (current_row >> current_conditioned_index) & 1
        if current_row_conditioned_bit != self.conditioned_values_mask[current_conditioned_index]:
          return False
      return True

    def __getValidIndexes(self, conditioned_indexes: list):
        valid_indexes: list = []
        for current_row in range(len(self.data)):
            if self.__checkValidConditionedRow(conditioned_indexes, current_row):
                valid_indexes.append(current_row)
        return valid_indexes

