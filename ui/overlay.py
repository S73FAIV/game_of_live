"""Overlay system for displaying achievements or rules over the grid."""

import pygame

from core.services.achievement_manager import AchievementManager
from core.services.rule_manager import RuleManager
from ui.colors import (
    ACHIEVEMENT_COLOUR,
    BLACK,
    GRAY,
    RULE_COLOUR,
    WHITE,
)
from ui.icons import ACHIEVEMENT_ICON_PATH, RULE_ICON_PATH
from ui.utils import tint_surface


class Overlay:
    """Base overlay covering the grid area."""

    def __init__(self, surface: pygame.Surface, width: int, height: int) -> None:
        self.surface = surface
        self.width = width
        self.height = height
        self.visible = False
        self.font = pygame.font.SysFont("Arial", 22, bold=True)
        self.desc_font = pygame.font.SysFont("Arial", 18, bold=True)

    def draw(self) -> None:
        """Draw a semi-transparent layer (base)."""
        overlay_surface = pygame.Surface((self.width, self.height))
        overlay_surface.set_alpha(230)
        overlay_surface.fill(WHITE)
        self.surface.blit(overlay_surface, (0, 0))
        pygame.draw.rect(self.surface, BLACK, (0, 0, self.width, self.height), 3)

    def set_visible(self, visible: bool) -> None:
        self.visible = visible


class AchievementsOverlay(Overlay):
    """Overlay showing unlocked achievements."""

    def __init__(
        self,
        achievements: AchievementManager,
        surface: pygame.Surface,
        width: int,
        height: int,
    ) -> None:
        super().__init__(surface, width, height)
        self.achievements = achievements
        self.icon = pygame.image.load(ACHIEVEMENT_ICON_PATH).convert_alpha()
        self.tint = ACHIEVEMENT_COLOUR
        self.icon = pygame.transform.smoothscale(self.icon, (32, 32))
        self.icon = tint_surface(self.icon, self.tint)

    def draw(self) -> None:
        super().draw()
        # header
        header_rect = pygame.Rect(0, 0, self.width, 100)
        pygame.draw.rect(self.surface, WHITE, header_rect)
        pygame.draw.rect(self.surface, BLACK, header_rect, 6)

        # icon + title
        self.surface.blit(self.icon, (40, 34))
        title = self.font.render("Unlocked Achievements", True, BLACK)
        self.surface.blit(title, (100, 40))

        # check if any achievements exist
        if not self.achievements.unlocked:
            placeholder = self.font.render("None yet...", True, GRAY)
            self.surface.blit(
                placeholder,
                (
                    self.width // 2 - placeholder.get_width() // 2,
                    self.height // 2 - placeholder.get_height() // 2,
                ),
            )
            return  # stop drawing further

        # entries
        y_base = 140
        for i, key in enumerate(self.achievements.unlocked or ["None yet..."]):
            ach = self.achievements.achievements.get(key)
            if not ach:
                continue

            y = y_base + i * 60  # extra spacing for description line

            # coloured square accent (as before)
            pygame.draw.rect(self.surface, self.tint, (80, y + 8, 20, 20))

            # title (same position as before)
            title_surf = self.font.render(ach.title, True, BLACK)
            self.surface.blit(title_surf, (120, y))

            # description line below title
            desc_surf = self.desc_font.render(ach.description, True, GRAY)
            self.surface.blit(desc_surf, (120, y + 28))


class RulesOverlay(Overlay):
    """Overlay showing unlocked rules."""

    def __init__(
        self, rules: RuleManager, surface: pygame.Surface, width: int, height: int
    ) -> None:
        super().__init__(surface, width, height)
        self.rules = rules
        self.icon = pygame.image.load(RULE_ICON_PATH).convert_alpha()
        self.tint = RULE_COLOUR
        self.icon = pygame.transform.smoothscale(self.icon, (32, 32))
        self.icon = tint_surface(self.icon, self.tint)

    def draw(self) -> None:
        super().draw()
        # header
        header_rect = pygame.Rect(0, 0, self.width, 100)
        pygame.draw.rect(self.surface, WHITE, header_rect)
        pygame.draw.rect(self.surface, BLACK, header_rect, 6)

        # Icon + Heading
        self.surface.blit(self.icon, (40, 34))
        title = self.font.render("Discovered Rules", True, BLACK)
        self.surface.blit(title, (100, 40))

        # no rules yet
        if not self.rules.unlocked:
            placeholder = self.font.render("No rules discovered.", True, GRAY)
            self.surface.blit(
                placeholder,
                (
                    self.width // 2 - placeholder.get_width() // 2,
                    self.height // 2 - placeholder.get_height() // 2,
                ),
            )
            return

        # list entries
        y_base = 140
        for i, key in enumerate(self.rules.unlocked):
            rule = self.rules.rules.get(key)
            if not rule:
                continue

            y = y_base + i * 60
            pygame.draw.rect(self.surface, self.tint, (80, y + 8, 20, 20))
            title_surf = self.font.render(rule.title, True, BLACK)
            self.surface.blit(title_surf, (120, y))
            desc_surf = self.desc_font.render(rule.description, True, GRAY)
            self.surface.blit(desc_surf, (120, y + 28))
