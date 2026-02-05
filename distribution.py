class Distrubution:
    def __init__(self, amount_of_values):
        self.data = [float()] * amount_of_values
    
    def insert(self, key, value):
        self.data[key] = value