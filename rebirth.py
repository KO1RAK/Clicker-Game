# rebirth.py
class Rebirth:
    def __init__(self, multiplier=1, count=0):
        self.multiplier = multiplier
        self.count = count

    def apply_rebirth(self):
        self.multiplier *= 2
        self.count += 1

    def get_multiplier(self):
        return self.multiplier

    def get_count(self):
        return self.count
