from distribution import Distrubution

class CSVDistributionLoader:
    def __init__(self):
        self.distrubution = None

    def binaryToDecimal(self, binary_str):
        return int(binary_str, 2)

    def parseLine(self, line):
        line = line.strip()
        if line.equals(""):
            return None, None
        parts = line.split(',')
        if len(parts) != 2:
            return None, None
        index, probability = parts[0].strip(), parts[1].strip()
        try:
            return self.binaryToDecimal(index), float(probability)
        except ValueError:
            return None, None

    def loadDistribution(self, file_path):
        with open(file_path, 'r') as file:
            first_line = file.readline()
            key, value = self.parseLine(first_line)
            first_line_mask = first_line.split(',')[0]
            number_of_variables = len(first_line_mask)
            amount_of_values = 2**len(number_of_variables)
            self.distrubution = Distrubution(amount_of_values)
            for line in file:
                key, value = self.parseLine(line)
                if key is not None and value is not None:
                    self.distrubution.insert(key, value)

    def getDistribution(self):
        return self.distrubution