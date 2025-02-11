import pygame, tkinter.messagebox
import tkinter as tk

pygame.font.init()
vector = pygame.math.Vector2

class HPBar():
    def __init__(self, x, y):
        self.bar_width_max = 200
        self.size = self.width, self.height = self.bar_width_max, 20
        self.pos = vector((x, y))

    def _display_text(self, screen, mx, current):
        font = pygame.font.SysFont('Comic Sans MS', 20)
        hp_text = font.render("HP:", False, (255, 255, 255))
        hp_value = font.render("%s/%s" % (current, mx), False, (255, 255, 255))
        screen.blit(hp_text, pygame.Rect((self.pos.x, self.pos.y), hp_text.get_size()))
        screen.blit(hp_value, pygame.Rect((self.pos.x + 40, self.pos.y + 30), hp_value.get_size()))

    def _display_outer_rect(self, screen):
        pygame.draw.rect(screen, (255, 255, 255),
        pygame.Rect(self.pos.x + 40, self.pos.y, self.bar_width_max, self.height), width = 2, border_radius = 3)

    def _display_inner_rect(self, screen):
        pygame.draw.rect(screen, (128, 255, 40),
        pygame.Rect(self.pos.x + 40, self.pos.y, self.width, self.height), border_radius = 3)
    
    def display(self, screen, mx, current):
        self.width = self.bar_width_max * (current / mx)
        self._display_text(screen, mx, current)
        self._display_inner_rect(screen)
        self._display_outer_rect(screen)

class Score():
    def __init__(self, x, y):
        self.pos = vector((x, y))
    
    def display(self, screen, score):
        font = pygame.font.SysFont('Comic Sans MS', 40)
        text = font.render(str(score), False, (255, 255, 255))
        rect = text.get_rect(center = (self.pos.x, self.pos.y))
        screen.blit(text, rect)

class Button():
    def __init__(self, screen, x, y, text, fill = (150, 0, 24), outline = (255, 160, 122), text_color = (255, 160, 122), highlighted = False):
        self.screen = screen
        self.size = self.width, self.height = 300, 60
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x - self.width / 2, self.y, self.width, self.height)
        self.text = text
        self.highlighted = highlighted
        self.fill = fill
        self.h_fill = (fill[0] + 100, fill[1] + 100, fill[2] + 100)
        self.outline = outline
        self.text_color = text_color
    
    def _draw_rect(self):
        if self.highlighted:
            pygame.draw.rect(self.screen, self.h_fill, self.rect, border_radius = 10)
        else:
            pygame.draw.rect(self.screen, self.fill, self.rect, border_radius = 10)
        pygame.draw.rect(self.screen, self.outline, self.rect, width = 4, border_radius = 10)

    def _draw_text(self):
        font = pygame.font.SysFont('Comic Sans MS', 30)
        text = font.render(self.text, False, self.text_color)
        self.screen.blit(text, text.get_rect(center = (self.x, self.y + self.height / 2)))

    def draw(self):
        self._draw_rect()
        self._draw_text()

def alert(message, title = "Alert"):
    root = tk.Tk()
    root.overrideredirect(1)
    root.withdraw()
    alert = tkinter.messagebox.showinfo(title, message, icon = 'warning')
    root.destroy()

def confirm(title, message):
    root = tk.Tk()
    root.overrideredirect(1)
    root.withdraw()
    alert = tkinter.messagebox.askquestion(title, message, icon = 'warning')
    root.destroy()
    if alert == 'yes':
        return True