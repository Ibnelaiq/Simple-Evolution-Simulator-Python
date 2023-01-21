class ConnectionString:
    # 1 = Positive or -1 = Negative
    type = 0
    # to 100%
    strength = 0

    def __init__(self,type,strength):
        self.type = type
        self.strength = (strength / 100)

    def get_strength(self):
        return self.strength

    def calculateInput(self,input):
        # Input in 1 to 0 range
        return input * self.strength
