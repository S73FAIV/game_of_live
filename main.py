"""Entry point for Conway's Game of Life.

Initializes Pygame, creates the MVC components, and starts the main event loop.
"""

import pygame

from core.game_controller import GameController
from core.game_model import GameState
from core.meta_controller import MetaController
from core.view import GameView
from ui.notification_manager import NotificationType
from utils.settings import FPS


def main() -> None:
    """Run the main loop of Conway's Game of Life.

    This function initializes the game environment, sets up the model-view-
    controller structure, and continuously updates and renders the simulation
    until the user quits.

    Steps:
        1. Initialize Pygame and create core objects.
        2. Process user input via the controller.
        3. Update the simulation state.
        4. Redraw the current frame via the view.
        5. Limit the frame rate to `FPS` from settings.

    Exits cleanly when the Pygame window is closed.
    """
    pygame.init()
    state = GameState()
    view = GameView(state)

    # Implementation of NotificationService interface
    def notifier(
        ntype: NotificationType,
        message: str,
        duration: float = 3.0,
        item_sprite: pygame.SurfaceType | None = None,
    ) -> None:
        # view.notification_manager.push(message, ntype, duration, item_sprite)
        pass

    meta = MetaController(state, notifier)
    # create access to the meta-data for the view
    view.add_meta_system(meta)

    controller = GameController(state, view)

    clock = pygame.time.Clock()
    running = True

    while running:
        # 1. Handle input
        running = controller.handle_events()

        # 2. Update game state (if simulation is running)
        state.update()

        # 3. Check Meta-Progression (Achievements, Tutorial, etc.)
        # meta.update() -> moved as subscriber of state

        # 4. Render
        view.draw()

        # 5. Cap frame rate
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
