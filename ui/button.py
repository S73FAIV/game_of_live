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
        toggleable: bool = False,
        accent_color: tuple[int, int, int] = (0, 0, 0),
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
        self.enabled = True
        self.toggleable = toggleable
        self.toggled = False
        self.accent_color = accent_color

    def draw(self, surface: pygame.Surface) -> None:
        """Render the button with brutalist styling."""
        if not self.enabled:
            bg = (220, 220, 220)  # dimmed background
            border_color = (150, 150, 150)  # softer border
            text_color = (120, 120, 120)
            shadow_color = (180, 180, 180)
        else:
            bg = WHITE if not self.hovered else GRAY
            border_color = BLACK
            text_color = BLACK
            shadow_color = (40, 40, 40)

        # Highlight toggled buttons with accent shadow
        if self.toggleable and self.toggled:
            shadow_color = self.accent_color

        # Draw shadow (offset rectangle)
        shadow_offset = 4
        shadow_rect = self.rect.move(shadow_offset, shadow_offset)
        pygame.draw.rect(surface, shadow_color, shadow_rect)

        pygame.draw.rect(surface, bg, self.rect)
        pygame.draw.rect(surface, border_color, self.rect, width=3)

        # Render label or icon
        if self.icon_surface:
            icon = self.icon_surface.copy()
            if not self.enabled:
                # desaturate icon
                icon.fill((180, 180, 180, 100), special_flags=pygame.BLEND_RGBA_MULT)
            icon_rect = icon.get_rect(center=self.rect.center)
            surface.blit(icon, icon_rect)
        elif self.label:
            text = self.font.render(self.label, True, text_color)
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Return True if button is clicked."""
        if not self.enabled:
            return False
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.toggleable:
                    self.toggled = not self.toggled
                self.active = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.active = False
        return False
