import os

class Player:
    
    def __init__(self, name, image, time=6000):
        self.name = name
        self.image = os.path.join(f'assets/images/{image}')
        self.time = time # in seconds