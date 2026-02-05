import math

class Distrubution:
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
        header = " ".join(f"X{self.number_of_variables - i}" for i in range(self.number_of_variables))
        print(f"{header} Probabilidad")
        # Each row corresponds to a combination of variable values
        for index, probability in enumerate(self.data):
            # Convert the index to a binary string, padded with zeros to match the number of variables
            binary = format(index, f"0{self.number_of_variables}b")
            # Join the bits with spaces for better readability
            row = " " + "  ".join(bit for bit in binary)
            print(f"{row}     {probability:.2f}")

    def showConditionedVariablesMask(self):
        # Reverse the mask for display, so the order matches the variable order in the distribution table
        formatted_mask = self.conditioned_variables_mask[::-1]  
        string_mask = "".join(str(value) for value in formatted_mask)
        print("Máscara de variables condicionadas: ", string_mask)

    def showConditionedValuesMask(self):
        # Reverse the mask for display, so the order matches the variable order in the distribution table
        formatted_mask = self.conditioned_values_mask[::-1]
        string_mask = "".join(str(value) for value in formatted_mask)
        print("Máscara de valores condicionados: ", string_mask)

    def showInterestValuesMask(self):
        # Reverse the mask for display, so the order matches the variable order in the distribution table
        formatted_mask = self.interest_variables_mask[::-1]
        string_mask = "".join(str(value) for value in formatted_mask)
        print("Máscara de variables de interés: ", string_mask)

    def setConditionedVariable(self, variable_index: int, value: int):
        # Check if the variable index is within the valid range and if the value is boolean
        if variable_index < 0 or variable_index >= self.number_of_variables:
            raise IndexError("Índice de variable condicionada fuera de rango.")
        elif value not in (0, 1):
            raise ValueError("El valor de la variable condicionada debe ser 0 o 1.")
        self.conditioned_variables_mask[variable_index] = 1
        self.conditioned_values_mask[variable_index] = value

    def setInterestVariable(self, variable_index: int):
        # Check if the variable index is within the valid range
        if variable_index < 0 or variable_index >= self.number_of_variables:
            raise IndexError("Índice de variable de interés fuera de rango.")
        self.interest_variables_mask[variable_index] = 1

    def resetMasks(self):
        self.conditioned_variables_mask = [0] * self.number_of_variables
        self.conditioned_values_mask = [0] * self.number_of_variables
        self.interest_variables_mask = [0] * self.number_of_variables