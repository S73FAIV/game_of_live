"""Handles unlocking and tracking of achievements."""

class AchievementManager:
    """Manages tracking of achievments."""

    def __init__(self) -> None:
        """Initialize the achievemnt manager and connect it to the event_bus."""
        self.unlocked = set()

    def on_pattern_detected(self, data: dict) -> None:
        """Handle logic, what happens, when a pattern is detected."""
        pattern = data.get("pattern")
        if pattern and pattern not in self.unlocked:
            self.unlocked.add(pattern)
            print(f"🏆 Achievement unlocked: Found {pattern}!")

