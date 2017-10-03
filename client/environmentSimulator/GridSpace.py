class GridSpace:
    def __init__(self, _obstacle: bool=False, _value: float=0):
        self.obstacle = _obstacle  # obstacle present in this space
        self.objective_value = _value  # whatever information we are surveying
