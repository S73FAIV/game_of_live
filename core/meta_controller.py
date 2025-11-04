"""Controller Orchestrating persistance and Meta-Systems."""
import numpy as np

from core.game_model import GameState, UpdateType
from core.services.achievement_manager import AchievementManager
from core.services.notification_service import NotificationService
from core.services.rule_manager import RuleManager
from core.services.tutorial_manager import TutorialManager


class MetaController:
    achievements: AchievementManager
    tutorial: TutorialManager
    state: GameState
    notifier: NotificationService
    old_grid: np.ndarray

    def __init__(self, state: GameState, notifier:  NotificationService) -> None:
        self.state = state
        self.state.subscribe(self.update)
        self.notifier = notifier
        self.rules = RuleManager(notifier)
        self.achievements = AchievementManager(notifier)
        self.tutorial = TutorialManager(notifier)
        self.old_grid = self.state.grid.copy()

    def update(self, update_type: UpdateType) -> None:
        """Forward state to the Meta-Progression-Systems so they can update achievements, tutorials and others."""
        grid = self.state.grid.copy()
        # Don't do anything, if the grid hasn't changed
        if np.array_equal(self.old_grid, grid):
            return

        # Get the relevant state
        births = self.state.births.copy()
        deaths = self.state.deaths.copy()
        # Tell the managers to check!
        if update_type == UpdateType.STEP:
            self.rules.update(grid, self.old_grid)
            self.achievements.update(grid, births, deaths)
            self.tutorial.update(
                grid,
                births,
                deaths,
                from_step=(update_type == UpdateType.STEP),
                old_grid=self.old_grid,
            )
        elif update_type == UpdateType.CELL_TOGGLE:
            self.tutorial.update(
                grid,
                births,
                deaths,
                from_step=(update_type == UpdateType.STEP),
                old_grid=self.old_grid,
            )

        # remember the grid
        self.old_grid = grid
