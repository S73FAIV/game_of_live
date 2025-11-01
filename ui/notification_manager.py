import time

import pygame

from ui.colors import BLACK, WHITE, GRAY, LIGHTGRAY


class NotificationType:
    """Defines available notification categories."""

    TUTORIAL = "tutorial"
    ACHIEVEMENT = "achievement"
    RULE = "rule"


class Notification:
    """Represents a self-contained notification with type-specific styling."""

    def __init__(
        self,
        text: str,
        ntype: str = NotificationType.TUTORIAL,
        duration: float = 3.0,
        icon_sprite: pygame.Surface | None = None
    ) -> None:
        self.text = text
        self.ntype = ntype
        self.start_time = time.time()
        self.duration = duration

        self.bg_color = WHITE
        self.text_color = BLACK
        self.border_color = BLACK
        self.shadow_color = (0, 0, 0)
        self.accent_color = (255, 255, 255)
        self.position = "bottom-right"
        self.icon_surface: pygame.Surface | None = None
        self.icon_tint = (0, 0, 0)

        self._init_visuals(icon_sprite)

    def _init_visuals(self, icon_sprite: pygame.Surface | None) -> None:
        """Assign visual attributes based on type."""
        icon_size = (24, 24)

        match self.ntype:
            case NotificationType.TUTORIAL:
                self.position = "top-center"
                self.icon_tint = (255, 235, 150)  # yellow tint
                if icon_sprite:
                    # user-supplied sprite for tutorial (e.g. character)
                    self.icon_surface = pygame.transform.smoothscale(
                        icon_sprite, icon_size
                    )
                else:
                    # default speech-bubble icon
                    self.icon_surface = pygame.Surface(icon_size, pygame.SRCALPHA)
                    pygame.draw.rect(self.icon_surface, self.icon_tint, (4, 4, 16, 14))
                    pygame.draw.polygon(
                        self.icon_surface, self.icon_tint, [(6, 18), (10, 14), (14, 18)]
                    )

            case NotificationType.ACHIEVEMENT:
                self.position = "bottom-right"
                self.icon_tint = (120, 200, 120)  # green tint
                self.icon_surface = pygame.Surface(icon_size, pygame.SRCALPHA)
                pygame.draw.circle(
                    self.icon_surface, self.icon_tint, (12, 12), 10, width=0
                )
                pygame.draw.circle(
                    self.icon_surface, BLACK, (12, 12), 10, width=2
                )
                pygame.draw.line(
                    self.icon_surface, BLACK, (8, 12), (11, 15), 2
                )
                pygame.draw.line(
                    self.icon_surface, BLACK, (11, 15), (16, 8), 2
                )

            case NotificationType.RULE:
                self.position = "bottom-right"
                self.icon_tint = (120, 160, 230)  # blue tint
                self.icon_surface = pygame.Surface(icon_size, pygame.SRCALPHA)
                pygame.draw.rect(self.icon_surface, self.icon_tint, (4, 4, 16, 16))
                pygame.draw.rect(self.icon_surface, BLACK, (4, 4, 16, 16), width=2)
                pygame.draw.line(
                    self.icon_surface, BLACK, (4, 4), (20, 20), 2
                )

    @property
    def expired(self) -> bool:
        return (time.time() - self.start_time) > self.duration


class NotificationManager:
    """Handles creation, rendering, and lifecycle of all active notifications."""

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font = pygame.font.SysFont("arial", 18)
        self.active_notifications: list[Notification] = []

    def push(
        self,
        text: str,
        ntype: str = NotificationType.TUTORIAL,
        duration: float = 3.0,
        icon_sprite: pygame.Surface | None = None,
    ) -> None:
        """Add a new notification to the queue."""
        self.active_notifications.append(Notification(text, ntype, duration, icon_sprite))

    def draw(self) -> None:
        """Render and manage fading notifications on screen."""
        now = time.time()
        self.active_notifications = [
            n for n in self.active_notifications if not n.expired
        ]
        if not self.active_notifications:
            return

        # group notifications by position for layout stacking
        positions = {
            "top-left": [],
            "top-center": [],
            "top-right": [],
            "bottom-left": [],
            "bottom-right": [],
        }
        for n in self.active_notifications:
            positions[n.position].append(n)

        for pos, group in positions.items():
            if not group:
                continue
            self._draw_group(group, pos, now)

    def _draw_group(self, group: list[Notification], pos: str, now: float) -> None:
        """Render a stacked group of notifications for a given corner."""
        # determine stacking origin
        padding = 10
        screen_w, screen_h = self.screen.get_width(), self.screen.get_height()

        if "top" in pos:
            y_offset = padding
            y_dir = 1
        else:
            y_offset = screen_h - padding
            y_dir = -1

        for notification in reversed(group):
            age = now - notification.start_time
            alpha = 255
            if notification.duration - age < 0.5:
                alpha = int(255 * ((notification.duration - age) / 0.5))
            alpha = max(alpha, 0)

            # text surface
            text_surface = self.font.render(
                notification.text, True, notification.text_color
            )
            text_surface.set_alpha(alpha)

            # compute background size with icon spacing
            icon_w = 0
            if notification.icon_surface:
                icon_w = notification.icon_surface.get_width() + 16
            bg_w = text_surface.get_width() + icon_w + 40
            bg_h = text_surface.get_height() + 20

            # base + shadow
            bg_surface = pygame.Surface((bg_w, bg_h))
            bg_surface.fill(notification.bg_color)
            pygame.draw.rect(bg_surface, notification.border_color, bg_surface.get_rect(), 3)

            shadow_offset = 5
            shadow = pygame.Surface((bg_w, bg_h))
            shadow.fill(notification.shadow_color)
            shadow.set_alpha(int(alpha * 0.3))

            # compute x position
            if "left" in pos:
                x = 20
            elif "center" in pos:
                x = (screen_w - bg_surface.get_width()) // 2
            else:
                x = screen_w - bg_surface.get_width() - 20

            # compute y position (stack vertically)
            if "top" in pos:
                y = y_offset
                y_offset += bg_surface.get_height() + 10
            else:
                y_offset -= bg_surface.get_height() + 10
                y = y_offset

                        # blit
            self.screen.blit(shadow, (x + shadow_offset, y + shadow_offset))
            self.screen.blit(bg_surface, (x, y))
            if notification.icon_surface:
                icon = notification.icon_surface.copy()
                icon.set_alpha(alpha)
                self.screen.blit(icon, (x + 12, y + (bg_h - icon.get_height()) // 2))
                self.screen.blit(text_surface, (x + 12 + icon_w, y + 8))
            else:
                self.screen.blit(text_surface, (x + 20, y + 8))
