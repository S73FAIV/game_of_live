import time

import pygame

from ui.colors import BLACK, WHITE


class Notification:
    def __init__(self, text: str, duration: float = 3.0):
        self.text = text
        self.start_time = time.time()
        self.duration = duration

    @property
    def expired(self) -> bool:
        return (time.time() - self.start_time) > self.duration


class NotificationManager:
    """Handles short-lived on-screen notifications."""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.SysFont("arial", 18)
        self.active_notifications: list[Notification] = []

    def push(self, text: str, duration: float = 3.0) -> None:
        """Add a new notification to be displayed."""
        self.active_notifications.append(Notification(text, duration))

    def draw(self) -> None:
        """Render active notifications with fading and stacking."""
        now = time.time()
        self.active_notifications = [
            n for n in self.active_notifications if not n.expired
        ]
        if not self.active_notifications:
            return

        # Bottom-right stacking
        y_offset = self.screen.get_height() - 40
        for notification in reversed(self.active_notifications):
            age = now - notification.start_time
            alpha = 255
            if notification.duration - age < 0.5:
                alpha = int(255 * ((notification.duration - age) / 0.5))
            alpha = max(alpha, 0)

            text_surface = self.font.render(notification.text, True, WHITE)
            text_surface.set_alpha(alpha)
            bg_surface = pygame.Surface(
                (text_surface.get_width() + 20, text_surface.get_height() + 10)
            )
            bg_surface.fill(BLACK)
            bg_surface.set_alpha(int(alpha * 0.6))

            x = self.screen.get_width() - bg_surface.get_width() - 20
            self.screen.blit(bg_surface, (x, y_offset))
            self.screen.blit(text_surface, (x + 10, y_offset + 5))
            y_offset -= bg_surface.get_height() + 10
