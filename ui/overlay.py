"""Overlay system for displaying achievements or rules over the grid."""

import pygame
from ui.colors import WHITE, BLACK, GRAY


class Overlay:
    """Base overlay covering the grid area."""

    def __init__(self, surface: pygame.Surface, width: int, height: int) -> None:
        self.surface = surface
        self.width = width
        self.height = height
        self.visible = False

    def draw(self) -> None:
        """Draw a semi-transparent layer (base)."""
        overlay_surface = pygame.Surface((self.width, self.height))
        overlay_surface.set_alpha(230)
        overlay_surface.fill(WHITE)
        self.surface.blit(overlay_surface, (0, 0))

    def set_visible(self, visible: bool) -> None:
        self.visible = visible


class AchievementsOverlay(Overlay):
    """Overlay showing unlocked achievements."""

    def __init__(self, surface: pygame.Surface, width: int, height: int) -> None:
        super().__init__(surface, width, height)
        self.font = pygame.font.SysFont("Arial", 22, bold=True)
        self.items = []  # will later hold achievement data

    def draw(self) -> None:
        super().draw()
        text = self.font.render("Unlocked Achievements", True, BLACK)
        self.surface.blit(text, (self.width // 2 - text.get_width() // 2, 40))
        # placeholder items
        for i, label in enumerate(self.items or ["None yet..."]):
            txt = self.font.render(label, True, GRAY)
            self.surface.blit(txt, (100, 100 + i * 40))


class RulesOverlay(Overlay):
    """Overlay showing unlocked rules."""

    def __init__(self, surface: pygame.Surface, width: int, height: int) -> None:
        super().__init__(surface, width, height)
        self.font = pygame.font.SysFont("Arial", 22, bold=True)
        self.items = []  # will later hold rule data

    def draw(self) -> None:
        super().draw()
        text = self.font.render("Discovered Rules", True, BLACK)
        self.surface.blit(text, (self.width // 2 - text.get_width() // 2, 40))
        # placeholder items
        for i, label in enumerate(self.items or ["No rules discovered."]):
            txt = self.font.render(label, True, GRAY)
            self.surface.blit(txt, (100, 100 + i * 40))
