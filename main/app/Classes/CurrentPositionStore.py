class CurrentPositionStore:

    def __init__(self):
        self.current_position_dict = {}

    def addCurrentPosition(self, current_position):
        self.current_position_dict[current_position.ticker] = current_position