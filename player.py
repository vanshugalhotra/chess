import os

class Player:
    
    def __init__(self, name, image, time=600):
        self.name = name
        self.image = os.path.join(f'assets/images/{image}')
        self.time = time # in seconds
        self.start_time = None
            