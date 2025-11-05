"""Handles unlocking and tracking of achievements."""

import numpy as np
import pygame

from core.models.achievement import Achievement
from core.services.notification_service import NotificationService
from ui.icons import ACHIEVEMENT_ICON_PATH
from ui.notification_manager import NotificationType


class AchievementManager:
    """Recognizes classic Game of Life patterns and awards achievements."""

    def __init__(self, notifier: NotificationService) -> None:
        self.unlocked: set[str] = set()
        self.achievements: dict[str, Achievement] = {}
        self.notify = notifier

        self.icon_sprite = pygame.image.load(ACHIEVEMENT_ICON_PATH).convert_alpha()
        self.icon_sprite = pygame.transform.smoothscale(self.icon_sprite, (32, 32))
        self._register_achievements()

    def _register_achievements(self) -> None:
        self.achievements["block"] = Achievement(
            title="Still-Live: BLOCK",
            description="Well, this one does nothing... (except survive)",
            pattern=np.array([[1, 1], [1, 1]]),
        )
        tub = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
        self.achievements["tub"] = Achievement(
            title="Still-Live: TUB",
            description="Looks more like a star to me, but I wasn't asked...",
            pattern=tub,
        )
        beehive = np.array([[0, 1, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0]])
        self.achievements["beehive"] = Achievement(
            title="Still-Live: BEEHIVE",
            description="Can you hear them humming?!",
            pattern=beehive,
            variants=[np.rot90(beehive)],
        )
        loaf = np.array([[0, 1, 1, 0], [1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 0]])
        self.achievements["loaf"] = Achievement(
            title="Still-Live: LOAF",
            description="I think, they never saw real bread...",
            pattern=loaf,
            variants=[
                np.rot90(loaf),
                np.rot90(np.rot90(loaf)),
                np.rot90(np.rot90(np.rot90(loaf))),
            ],
        )
        boat = np.array([[1, 1, 0], [1, 0, 1], [0, 1, 0]])
        self.achievements["boat"] = Achievement(
            title="Still-Live: BOAT",
            description="Maybe you see it if you squint reeealy hard?",
            pattern=boat,
            variants=[
                np.rot90(boat),
                np.rot90(np.rot90(boat)),
                np.rot90(np.rot90(np.rot90(boat))),
            ],
        )
        # TODO: add more oscillators
        blinker = np.array([[1, 1, 1]])
        self.achievements["blinker"] = Achievement(
            title="Oscillator: BLINKER",
            description="At least it does something!",
            pattern=blinker,
            variants=[np.rot90(blinker)],
        )
        # TODO: add more spaceships
        glider = np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]])
        self.achievements["glider"] = Achievement(
            title="Spaceship: GLIDER",
            description="Now, that's what I call some moves!",
            pattern=glider,
            variants=[
                np.rot90(glider),
                np.rot90(np.rot90(glider)),
                np.rot90(np.rot90(np.rot90(glider))),
            ],
        )

    def update(self, grid: np.ndarray, births: np.ndarray, deaths: np.ndarray) -> None:
        """Check for all registered achievements in the current grid."""
        for key, achievement in self.achievements.items():
            if key in self.unlocked:
                continue
            if self._contains_pattern(grid, achievement):
                self._unlock(key, achievement)

    def _contains_pattern(self, grid: np.ndarray, achievement: Achievement) -> bool:
        """Return True if the grid contains the given pattern anywhere."""
        patterns = [achievement.pattern]
        if achievement.variants:
            patterns += achievement.variants

        for pattern in patterns:
            ph, pw = pattern.shape
            gh, gw = grid.shape

            # simple sliding-window check using correlation
            # match means all live cells of pattern match live cells in grid
            for y in range(gh - ph + 1):
                for x in range(gw - pw + 1):
                    sub = grid[y : y + ph, x : x + pw]
                    if np.array_equal(sub, pattern):
                        return True
        return False

    def _unlock(self, key: str, achievement: Achievement) -> None:
        """Record achievement and show notification."""
        self.unlocked.add(key)
        text = f"Achievement unlocked: {achievement.title} discovered!"
        self.notify(NotificationType.ACHIEVEMENT, text, 6, self.icon_sprite)
        print(f"Unlocked achievement: {achievement.title}")
