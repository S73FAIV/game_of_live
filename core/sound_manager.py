"""Centralized sound management for the Game of Life."""

import pygame
import random
from pathlib import Path

class SoundManager:
    """Handles background music and sound effects for the Game of Life."""

    def __init__(self, base_path: str = "assets") -> None:
        pygame.mixer.init()

        # Paths
        self.music_path = Path(base_path) / "music" / "lofi-loop-hopeful-city-321581.mp3"
        self.sfx_birth_path = Path(base_path) / "sfx" / "cell_birth.wav"
        self.sfx_death_path = Path(base_path) / "sfx" / "cell_death.wav"

        # Load sound effects
        self.sfx_birth = pygame.mixer.Sound(self.sfx_birth_path)
        self.sfx_death = pygame.mixer.Sound(self.sfx_death_path)

        # Adjust default volumes
        pygame.mixer.music.set_volume(0.25)  # background music
        self.sfx_birth.set_volume(0.5)
        self.sfx_death.set_volume(0.4)

        # Simple limiter for effects (avoid overload)
        self.last_played = 0

    def play_music(self) -> None:
        """Start looping the background Lo-Fi track."""
        pygame.mixer.music.load(self.music_path)
        pygame.mixer.music.play(loops=-1, fade_ms=1000)

    def stop_music(self) -> None:
        """Fade out and stop the background music."""
        pygame.mixer.music.fadeout(1000)

    def play_birth(self) -> None:
        """Play a soft 'cell birth' sound with randomized pitch."""
        self._play_randomized(self.sfx_birth)

    def play_death(self) -> None:
        """Play a soft 'cell death' sound with randomized pitch."""
        self._play_randomized(self.sfx_death)

    def _play_randomized(self, sound: pygame.mixer.SoundType) -> None:
        """Play a sound effect with slight pitch/volume variations."""
        if random.random() < 0.05:  # only 5% of cell events trigger a sound
            # Create a new temporary channel to randomize volume
            channel = sound.play()
            if channel:
                channel.set_volume(random.uniform(0.3, 0.6))
