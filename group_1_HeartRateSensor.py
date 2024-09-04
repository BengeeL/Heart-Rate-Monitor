# GROUP 1

# Benjamin 
# Paige
# Harpreet
# Gwen 

import random

class HeartRateSensor:
    def __init__(self, base_rate=80, min_fluctuation=0, max_fluctuation=30):
        self.base_rate = base_rate
        self.min_fluctuation = min_fluctuation
        self.max_fluctuation = max_fluctuation
        self.counter = 0
    
    def _change_value(self):
        value = random.random()
        return (value * (self.max_fluctuation - self.min_fluctuation)) + self.min_fluctuation

    @property
    def get_heart_rate(self):
        change_value = self._change_value()
        self.counter += 1

        if self.counter % self.base_rate > self.base_rate / 2:
            return self.base_rate + change_value
        else:
            return self.base_rate - change_value