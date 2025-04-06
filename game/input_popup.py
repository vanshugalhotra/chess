import pygame
import pygame.font
from pygame.locals import *

class IPInputPopup:
    def __init__(self, screen, width=400, height=250):
        self.screen = screen
        self.width = width
        self.height = height
        self.x = (screen.get_width() - width) // 2
        self.y = (screen.get_height() - height) // 2
        self.active = False
        self.ip_text = ""
        self.font = pygame.font.SysFont('Arial', 24)
        self.small_font = pygame.font.SysFont('Arial', 18)
        self.input_active = True
        self.error_message = ""
        self.success_message = ""
        
        # Colors
        self.bg_color = (240, 240, 240)
        self.border_color = (100, 100, 100)
        self.text_color = (50, 50, 50)
        self.input_color = (255, 255, 255)
        self.input_border_active = (70, 130, 180)
        self.input_border_inactive = (150, 150, 150)
        self.button_color = (70, 130, 180)
        self.button_hover_color = (100, 160, 210)
        self.error_color = (200, 50, 50)
        self.success_color = (50, 150, 50)
        
        # Create a semi-transparent surface
        self.popup_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Input rect
        self.input_rect = pygame.Rect(self.x + 50, self.y + 100, 300, 32)
        
        # Buttons
        self.connect_rect = pygame.Rect(self.x + 100, self.y + 150, 100, 40)
        self.cancel_rect = pygame.Rect(self.x + 220, self.y + 150, 100, 40)
        
    def draw(self):
        if not self.active:
            return
            
        # Draw semi-transparent overlay
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        # Draw popup background
        pygame.draw.rect(self.popup_surface, self.bg_color, (0, 0, self.width, self.height), border_radius=10)
        pygame.draw.rect(self.popup_surface, self.border_color, (0, 0, self.width, self.height), 2, border_radius=10)
        
        # Draw title
        title = self.font.render("Connect to Server", True, self.text_color)
        self.popup_surface.blit(title, (self.width//2 - title.get_width()//2, 20))
        
        # Draw input label
        label = self.small_font.render("Server IP Address:", True, self.text_color)
        self.popup_surface.blit(label, (50, 70))
        
        # Draw input box
        input_border_color = self.input_border_active if self.input_active else self.input_border_inactive
        pygame.draw.rect(self.popup_surface, input_border_color, (50, 100, 300, 32), 2, border_radius=5)
        pygame.draw.rect(self.popup_surface, self.input_color, (52, 102, 296, 28), border_radius=5)
        
        # Draw input text
        ip_surface = self.font.render(self.ip_text, True, self.text_color)
        self.popup_surface.blit(ip_surface, (60, 105))
        
        # Draw cursor if active
        if self.input_active:
            cursor_x = 60 + self.font.size(self.ip_text[:len(self.ip_text)])[0]
            pygame.draw.line(self.popup_surface, self.text_color, (cursor_x, 105), (cursor_x, 125), 2)
        
        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        
        # Connect button
        connect_color = self.button_hover_color if self.connect_rect.collidepoint(mouse_pos) else self.button_color
        pygame.draw.rect(self.popup_surface, connect_color, (100, 150, 100, 40), border_radius=5)
        connect_text = self.font.render("Connect", True, (255, 255, 255))
        self.popup_surface.blit(connect_text, (150 - connect_text.get_width()//2, 160))
        
        # Cancel button
        cancel_color = self.button_hover_color if self.cancel_rect.collidepoint(mouse_pos) else self.button_color
        pygame.draw.rect(self.popup_surface, cancel_color, (220, 150, 100, 40), border_radius=5)
        cancel_text = self.font.render("Cancel", True, (255, 255, 255))
        self.popup_surface.blit(cancel_text, (270 - cancel_text.get_width()//2, 160))
        
        # Draw error/success message
        if self.error_message:
            error_text = self.small_font.render(self.error_message, True, self.error_color)
            self.popup_surface.blit(error_text, (self.width//2 - error_text.get_width()//2, 200))
        elif self.success_message:
            success_text = self.small_font.render(self.success_message, True, self.success_color)
            self.popup_surface.blit(success_text, (self.width//2 - success_text.get_width()//2, 200))
        
        # Blit the popup surface to the screen
        self.screen.blit(self.popup_surface, (self.x, self.y))
        
    def handle_event(self, event):
        if not self.active:
            return None
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                self.input_active = True
            else:
                self.input_active = False
                
            if self.connect_rect.collidepoint(event.pos):
                return self.ip_text if self.ip_text.strip() != "" else "192.168.1.43"
                
            if self.cancel_rect.collidepoint(event.pos):
                return "cancel"
                
        if event.type == pygame.KEYDOWN and self.input_active:
            if event.key == pygame.K_RETURN:
                return self.ip_text if self.ip_text.strip() != "" else "192.168.1.43"
            elif event.key == pygame.K_BACKSPACE:
                self.ip_text = self.ip_text[:-1]
            else:
                # Only allow valid IP characters
                if event.unicode in '0123456789.':
                    self.ip_text += event.unicode
                    
        return None

    def show(self):
        self.active = True
        self.ip_text = ""
        self.error_message = ""
        self.success_message = ""
        
    def hide(self):
        self.active = False
        
    def set_error(self, message):
        self.error_message = message
        self.success_message = ""
        
    def set_success(self, message):
        self.success_message = message
        self.error_message = ""