"""A simple animated popup for achievements or tutorial messages."""

import time

import pygame


class Popup:
    def __init__(self, surface: pygame.Surface, title: str, message: str):
        self.surface = surface
        self.title = title
        self.message = message
        self.start_time = time.time()
        self.duration = 3.0  # seconds
        self.finished = False

        self.font_title = pygame.font.SysFont(None, 36)
        self.font_msg = pygame.font.SysFont(None, 24)

    def update(self):
        if time.time() - self.start_time > self.duration:
            self.finished = True

    def draw(self):
        elapsed = time.time() - self.start_time
        alpha = max(0, 255 - int((elapsed / self.duration) * 255))

        # Popup rectangle
        popup_rect = pygame.Rect(50, 50, 300, 120)
        popup_surf = pygame.Surface(popup_rect.size, pygame.SRCALPHA)
        popup_surf.fill((50, 50, 50, alpha))

        # Text
        title_surf = self.font_title.render(self.title, True, (255, 255, 255))
        msg_surf = self.font_msg.render(self.message, True, (200, 200, 200))

        popup_surf.blit(title_surf, (10, 10))
        popup_surf.blit(msg_surf, (10, 60))

        self.surface.blit(popup_surf, popup_rect.topleft)
