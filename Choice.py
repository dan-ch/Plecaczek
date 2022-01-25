class Choice:
    binary_array: []
    weight: float
    totalValue: float
    affinity: float

    def __init__(self):
        super().__init__()
        self.binary_array = []
        self.weight = 0
        self.totalValue = 0
        self.affinity = 0


    def __str__(self):
        return f'''
         Tablica: {self.binary_array}
         Weight: {self.weight}
         Value: {self.totalValue}
         Affinity: {self.affinity}
         '''






