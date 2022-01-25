class Point:
    iteration: int
    value: float

    def __init__(self, iteration: int, value: float):
        super().__init__()
        self.value = value
        self.iteration = iteration
