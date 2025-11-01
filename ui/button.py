"""UI Button component for the sidebar (neo-brutalistic design)."""

import pygame

from ui.colors import WHITE, BLACK, GRAY



class Button:
    """Simple rectangular button with text or icon, self-contained."""

    def __init__(
        self,
        rect: pygame.Rect,
        label: str = "",
        icon_path: str | None = None,
        font_size: int = 16,
    ) -> None:
        self.rect = rect
        self.label = label
        self.icon = None
        self.icon_surface = None
        self.font = pygame.font.SysFont("Arial", font_size, bold=True)

        if icon_path:
            self.icon_surface = pygame.image.load(icon_path).convert_alpha()
            self.icon_surface = pygame.transform.smoothscale(
                self.icon_surface, (rect.height - 8, rect.height - 8)
            )

        self.hovered = False
        self.active = False

    def draw(self, surface: pygame.Surface) -> None:
        """Render the button with brutalist styling."""
        bg = WHITE if not self.hovered else GRAY
        pygame.draw.rect(surface, bg, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, width=3)

        # Render label or icon
        if self.icon_surface:
            icon_rect = self.icon_surface.get_rect(center=self.rect.center)
            surface.blit(self.icon_surface, icon_rect)
        elif self.label:
            text = self.font.render(self.label, True, BLACK)
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Return True if button is clicked."""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.active = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.active = False
        return False
