from distribution import Distrubution

class CSVDistributionLoader:
    def __init__(self):
        self.distrubution = None

    def loadDistribution(self, file_path: str):
        with open(file_path, 'r') as file:
            # First line is used to determine the number of variables and initialize the distribution
            first_line = file.readline()
            first_key, first_value = self.__parseLine(first_line)
            first_line_mask = first_line.split(',')[0]
            # The number of variables is determined by the length of the binary string in the first line
            number_of_variables = len(first_line_mask)
            amount_of_values = 2**number_of_variables
            self.distrubution = Distrubution(amount_of_values)
            if first_key is None or first_value is None:
                raise ValueError("El formato del archivo CSV es incorrecto.")
            self.distrubution.insert(first_key, first_value)
            # Parse the rest of the lines in the file
            for line in file:
                key, value = self.__parseLine(line)
                if key is not None and value is not None:
                    self.distrubution.insert(key, value)

    def getDistribution(self):
        return self.distrubution
    
    def __binaryToDecimal(self, binary_str: str):
        return int(binary_str, 2)

    def __parseLine(self, line: str):
        line = line.strip()
        if line == "":
            return None, None
        # Split the line by comma and check if it has exactly two parts (index and probability)
        parts = line.split(',')
        if len(parts) != 2:
            return None, None
        index, probability = parts[0].strip(), parts[1].strip()
        try:
            return self.__binaryToDecimal(index), float(probability)
        except ValueError:
            return None, None