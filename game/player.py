import os
import time
import threading

class Player:
    
    def __init__(self, name, image, initial_time=600):
        self.name = name
        self.image = os.path.join(f'assets/images/{image}')
        self.time = initial_time # in seconds
        
        self.timer_thread = None
        self.running = False
            
    def start_timer(self):
        self.running = True
        self.timer_thread = threading.Thread(target=self.update_timer, daemon=True)
        self.timer_thread.start()
        
    def stop_timer(self):
        self.running = False
        if self.timer_thread is not None:
            # self.timer_thread.join()
            pass
            
    def update_timer(self):
        while self.running and self.time > 0:
            time.sleep(1)
            self.time -= 1
            
            if self.time <= 0:
                self.running = False