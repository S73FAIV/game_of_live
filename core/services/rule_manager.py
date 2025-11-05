"""Handles unlocking and tracking of Conway's Game of Life rules."""

import numpy as np
import pygame

from core.models.rule import Rule
from core.services.notification_service import NotificationService
from ui.icons import RULE_ICON_PATH
from ui.notification_manager import NotificationType


class RuleManager:
    """Detects and unlocks Conway's fundamental rules when first observed."""

    def __init__(self, notifier: NotificationService) -> None:
        self.unlocked: set[str] = set()
        self.rules: dict[str, Rule] = {}
        self.icon_sprite = pygame.image.load(RULE_ICON_PATH).convert_alpha()
        self.icon_sprite = pygame.transform.smoothscale(self.icon_sprite, (32, 32))
        self.notify = notifier
        self._register_rules()

    def _register_rules(self) -> None:
        self.rules["underpopulation"] = Rule(
            title="Underpopulation",
            description="Any live cell with fewer than two live neighbours dies, as if by underpopulation.",
            notification="A lonely cell has died from isolation.",
        )
        self.rules["survival"] = Rule(
            title="Survival",
            description="Any live cell with two or three live neighbours lives on to the next generation.",
            notification="Some cells have stabilized and survived.",
        )
        self.rules["overpopulation"] = Rule(
            title="Overpopulation",
            description="Any live cell with more than three live neighbours dies, as if by overpopulation.",
            notification="A crowded area has collapsed from overpopulation.",
        )
        self.rules["reproduction"] = Rule(
            title="Reproduction",
            description="Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.",
            notification="New life has emerged from perfect balance.",
        )

    def update(self, new_grid: np.ndarray, old_grid: np.ndarray) -> None:
        """Evaluate which Life rules are expressed between two consecutive grids."""
        # Compute neighbor counts for the old generation
        neighbors = sum(
            np.roll(np.roll(old_grid, i, 0), j, 1)
            for i in (-1, 0, 1)
            for j in (-1, 0, 1)
            if (i != 0 or j != 0)
        )

        was_alive = old_grid == 1
        is_alive = new_grid == 1

        # Identify cell transitions
        births = (~was_alive) & is_alive
        deaths = was_alive & (~is_alive)

        # Rule 1 - Underpopulation: alive → dead, < 2 neighbors
        if np.any(deaths & (neighbors < 2)) and "underpopulation" not in self.unlocked:
            self._unlock("underpopulation")

        # Rule 2 - Survival: alive → alive, 2 or 3 neighbors
        if (
            np.any(is_alive & was_alive & ((neighbors == 2) | (neighbors == 3)))
            and "survival" not in self.unlocked
        ):
            self._unlock("survival")

        # Rule 3 - Overpopulation: alive → dead, > 3 neighbors
        if np.any(deaths & (neighbors > 3)) and "overpopulation" not in self.unlocked:
            self._unlock("overpopulation")

        # Rule 4 - Reproduction: dead → alive, exactly 3 neighbors
        if np.any(births & (neighbors == 3)) and "reproduction" not in self.unlocked:
            self._unlock("reproduction")

    def _unlock(self, key: str) -> None:
        """Mark rule as unlocked and notify."""
        self.unlocked.add(key)
        rule = self.rules[key]
        message = f"{rule.title}: {rule.notification}"
        self.notify(NotificationType.RULE, message, 6, self.icon_sprite)
        print(message)
