"""Manages tutorial progression and onboarding messages."""

class TutorialManager:
    """Manages tracking of tutorial-messages."""
    def __init__(self) -> None:
        """Initialize the tutorial manager and connect it to the event_bus."""
        self.shown = set()
        # self.event_bus = EventBus()
        # self.event_bus.subscribe(GameEvent.GENERATION_COMPLETED, self.on_generation)
        # self.event_bus.subscribe(GameEvent.GAME_STARTED, self.on_game_start)

    def on_game_start(self, data: dict) -> None:
        if "start_tip" not in self.shown:
            self.shown.add("start_tip")
            # self.event_bus.emit(GameEvent.TUTORIAL_POPUP, {
            #     "title": "Welcome!",
            #     "message": "Press 'Start' to begin the simulation."
            # })

    def on_generation(self, data: dict) -> None:
        if "progress_tip" not in self.shown and data.get("generation", 0) > 10:
            self.shown.add("progress_tip")
            # self.event_bus.emit(GameEvent.TUTORIAL_POPUP, {
            #     "title": "Nice Progress!",
            #     "message": "You've advanced 10 generations! Try pausing and editing the grid."
            # })
