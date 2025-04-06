import pygame
import pygame.font
from pygame.locals import *

class ConnectionPopup:
    def __init__(self, screen, width=350, height=280):
        self.screen = screen
        self.width = width
        self.height = height
        self.x = (screen.get_width() - width) // 2
        self.y = (screen.get_height() - height) // 2
        self.active = False
        
        # Text fields
        self.ip_text = ""
        self.username_text = ""
        self.active_field = "ip"  # 'ip' or 'username'
        
        # Fonts
        self.title_font = pygame.font.SysFont('Arial', 26, bold=True)
        self.font = pygame.font.SysFont('Arial', 20)
        self.small_font = pygame.font.SysFont('Arial', 16)
        
        # Colors
        self.bg_color = (245, 245, 245)
        self.border_color = (200, 200, 200)
        self.text_color = (60, 60, 60)
        self.input_color = (255, 255, 255)
        self.input_border_active = (80, 150, 220)
        self.input_border_inactive = (180, 180, 180)
        self.button_color = (80, 150, 220)
        self.button_hover_color = (100, 170, 240)
        self.error_color = (220, 80, 80)
        self.success_color = (80, 180, 80)
        self.label_color = (100, 100, 100)
        
        # Create popup surface
        self.popup_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Input rectangles
        self.ip_rect = pygame.Rect(25, 80, 300, 32)
        self.username_rect = pygame.Rect(25, 140, 300, 32)
        
        # Buttons
        self.connect_rect = pygame.Rect(70, 190, 120, 36)
        self.cancel_rect = pygame.Rect(210, 190, 70, 36)
        
        # Messages
        self.error_message = ""
        self.success_message = ""
        
    def draw(self):
        if not self.active:
            return
            
        # Draw semi-transparent overlay
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Darker overlay for better contrast
        self.screen.blit(overlay, (0, 0))
        
        # Draw popup background with shadow effect
        pygame.draw.rect(self.popup_surface, (0, 0, 0, 30), (5, 5, self.width, self.height), border_radius=8)
        pygame.draw.rect(self.popup_surface, self.bg_color, (0, 0, self.width, self.height), border_radius=8)
        pygame.draw.rect(self.popup_surface, self.border_color, (0, 0, self.width, self.height), 1, border_radius=8)
        
        # Draw title
        title = self.title_font.render("Connect to Game Server", True, self.text_color)
        self.popup_surface.blit(title, (self.width//2 - title.get_width()//2, 20))
        
        # Draw IP input field
        pygame.draw.rect(self.popup_surface, 
                        self.input_border_active if self.active_field == "ip" else self.input_border_inactive, 
                        self.ip_rect, 2, border_radius=4)
        pygame.draw.rect(self.popup_surface, self.input_color, 
                        (self.ip_rect.x+2, self.ip_rect.y+2, self.ip_rect.width-4, self.ip_rect.height-4), 
                        border_radius=4)
        
        # Draw IP label
        ip_label = self.small_font.render("Server IP:", True, self.label_color)
        self.popup_surface.blit(ip_label, (25, 60))
        
        # Draw IP text
        ip_surface = self.font.render(self.ip_text, True, self.text_color)
        self.popup_surface.blit(ip_surface, (self.ip_rect.x + 8, self.ip_rect.y + 6))
        
        # Draw cursor if active
        if self.active_field == "ip":
            cursor_x = self.ip_rect.x + 8 + self.font.size(self.ip_text[:len(self.ip_text)])[0]
            pygame.draw.line(self.popup_surface, self.text_color, 
                           (cursor_x, self.ip_rect.y + 6), 
                           (cursor_x, self.ip_rect.y + 26), 2)
        
        # Draw username input field
        pygame.draw.rect(self.popup_surface, 
                        self.input_border_active if self.active_field == "username" else self.input_border_inactive, 
                        self.username_rect, 2, border_radius=4)
        pygame.draw.rect(self.popup_surface, self.input_color, 
                        (self.username_rect.x+2, self.username_rect.y+2, self.username_rect.width-4, self.username_rect.height-4), 
                        border_radius=4)
        
        # Draw username label
        user_label = self.small_font.render("Your Name:", True, self.label_color)
        self.popup_surface.blit(user_label, (25, 120))
        
        # Draw username text
        username_surface = self.font.render(self.username_text, True, self.text_color)
        self.popup_surface.blit(username_surface, (self.username_rect.x + 8, self.username_rect.y + 6))
        
        # Draw cursor if active
        if self.active_field == "username":
            cursor_x = self.username_rect.x + 8 + self.font.size(self.username_text[:len(self.username_text)])[0]
            pygame.draw.line(self.popup_surface, self.text_color, 
                           (cursor_x, self.username_rect.y + 6), 
                           (cursor_x, self.username_rect.y + 26), 2)
        
        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        adjusted_mouse_pos = (mouse_pos[0] - self.x, mouse_pos[1] - self.y)
        
        # Connect button
        connect_color = self.button_hover_color if self.connect_rect.collidepoint(adjusted_mouse_pos) else self.button_color
        pygame.draw.rect(self.popup_surface, connect_color, self.connect_rect, border_radius=4)
        pygame.draw.rect(self.popup_surface, (0, 0, 0, 20), self.connect_rect, 1, border_radius=4)
        connect_text = self.font.render("Connect", True, (255, 255, 255))
        self.popup_surface.blit(connect_text, 
                               (self.connect_rect.x + self.connect_rect.width//2 - connect_text.get_width()//2,
                                self.connect_rect.y + self.connect_rect.height//2 - connect_text.get_height()//2))
        
        # Cancel button
        cancel_color = self.button_hover_color if self.cancel_rect.collidepoint(adjusted_mouse_pos) else (220, 220, 220)
        pygame.draw.rect(self.popup_surface, cancel_color, self.cancel_rect, border_radius=4)
        pygame.draw.rect(self.popup_surface, (0, 0, 0, 20), self.cancel_rect, 1, border_radius=4)
        cancel_text = self.font.render("Cancel", True, self.text_color)
        self.popup_surface.blit(cancel_text, 
                               (self.cancel_rect.x + self.cancel_rect.width//2 - cancel_text.get_width()//2,
                                self.cancel_rect.y + self.cancel_rect.height//2 - cancel_text.get_height()//2))
        
        # Draw error/success message
        if self.error_message:
            error_text = self.small_font.render(self.error_message, True, self.error_color)
            self.popup_surface.blit(error_text, (self.width//2 - error_text.get_width()//2, 240))
        elif self.success_message:
            success_text = self.small_font.render(self.success_message, True, self.success_color)
            self.popup_surface.blit(success_text, (self.width//2 - success_text.get_width()//2, 240))
        
        # Blit the popup surface to the screen
        self.screen.blit(self.popup_surface, (self.x, self.y))
        
    def handle_event(self, event):
        if not self.active:
            return None
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Adjust mouse position relative to popup
            mouse_pos = (event.pos[0] - self.x, event.pos[1] - self.y)
            
            # Check which field was clicked
            if self.ip_rect.collidepoint(mouse_pos):
                self.active_field = "ip"
            elif self.username_rect.collidepoint(mouse_pos):
                self.active_field = "username"
            else:
                self.active_field = None
                
            # Check buttons
            if self.connect_rect.collidepoint(mouse_pos):
                if not self.username_text.strip():
                    self.set_error("Please enter your name")
                    return None
                return {
                    'ip': self.ip_text if self.ip_text.strip() != "" else "192.168.1.43",
                    'username': self.username_text.strip()
                }
                
            if self.cancel_rect.collidepoint(mouse_pos):
                return "cancel"
                
        if event.type == pygame.KEYDOWN and self.active_field:
            current_text = self.ip_text if self.active_field == "ip" else self.username_text
            
            if event.key == pygame.K_RETURN:
                if not self.username_text.strip():
                    self.set_error("Please enter your name")
                    return None
                return {
                    'ip': self.ip_text if self.ip_text.strip() != "" else "192.168.1.43",
                    'username': self.username_text.strip()
                }
            elif event.key == pygame.K_BACKSPACE:
                if self.active_field == "ip":
                    self.ip_text = current_text[:-1]
                else:
                    self.username_text = current_text[:-1]
            elif event.key == pygame.K_TAB:
                self.active_field = "username" if self.active_field == "ip" else "ip"
            else:
                # Field-specific validation
                if self.active_field == "ip":
                    if event.unicode in '0123456789.':
                        self.ip_text += event.unicode
                else:  # username
                    if len(self.username_text) < 20:  # Limit username length
                        self.username_text += event.unicode
                    
        return None

    def show(self, default_ip="", default_username=""):
        self.active = True
        self.ip_text = default_ip
        self.username_text = default_username
        self.active_field = "ip"
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