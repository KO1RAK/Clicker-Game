class Rebirth:
    def __init__(self, count=0, multiplier=1):
        self.count = count
        self.multiplier = multiplier

    def apply_rebirth(self):
        self.count += 1
        self.multiplier = 1 + self.count  # linear growth

    def get_multiplier(self):
        return self.multiplier

    def get_count(self):
        return self.count