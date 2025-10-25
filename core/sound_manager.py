"""Centralized sound management for the Game of Life."""

import random
from pathlib import Path

import pygame


class SoundManager:
    """Handles background music and sound effects for the Game of Life."""

    def __init__(self, base_path: str = "assets") -> None:
        """Initialize SoundManager with existing Sound-Files."""
        pygame.mixer.init()

        # Paths
        self.music_path = (
            Path(base_path) / "music" / "lofi-loop-hopeful-city-321581.mp3"
        )
        self.sfx_birth_path = Path(base_path) / "sfx" / "cell_birth.wav"
        self.sfx_death_path = Path(base_path) / "sfx" / "cell_death.wav"

        # Load sound effects
        self.sfx_birth = pygame.mixer.Sound(self.sfx_birth_path)
        self.sfx_death = pygame.mixer.Sound(self.sfx_death_path)

        # Adjust default volumes
        pygame.mixer.music.set_volume(0.25)  # background music
        self.sfx_birth.set_volume(0.5)
        self.sfx_death.set_volume(0.4)


    def play_music(self) -> None:
        """Start looping the background Lo-Fi track."""
        pygame.mixer.music.load(self.music_path)
        pygame.mixer.music.play(loops=-1, fade_ms=1000)

    def stop_music(self) -> None:
        """Fade out and stop the background music."""
        pygame.mixer.music.fadeout(1000)

    def _play_randomized(self, sound: pygame.mixer.SoundType) -> None:
        """Play a sound effect with slight randomization in volume."""
        channel = sound.play()
        if channel:
            channel.set_volume(random.uniform(0.3, 0.6))
        else:
            print("No channels available")

    def play_generation_batch(
        self, births: int, deaths: int, live_cells: int, total_cells: int
    ) -> None:
        """Play a few birth/death sounds, scaled by population density."""
        total_changes = births + deaths
        if total_changes == 0 or live_cells == 0:
            return

        # Scale playback density depending on population density
        density = live_cells / total_cells

        # Compute how many sounds to play this frame
        # Sparse grid → up to 5 sounds, dense grid → 1 sound
        max_sounds = int(5 * (1 - density)) + 1  # range: 1-6
        num_sounds = min(max_sounds, total_changes // 100 + 1)

        # Randomly mix births and deaths
        for _ in range(num_sounds):
            if random.random() < births / total_changes:
                self._play_randomized(self.sfx_birth)
            else:
                self._play_randomized(self.sfx_death)
