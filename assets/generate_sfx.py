"""Generate minimalistic lo-fi sound effects for cell birth and death with pitch sweep."""

import numpy as np
from scipy.io import wavfile

SAMPLE_RATE = 44100  # Hz

def make_lofi_sweep(start_freq=440, end_freq=440, duration_ms=100, volume=0.5, decay=0.95):
    """Generate a short lo-fi sound with a linear pitch sweep."""
    n_samples = int(SAMPLE_RATE * (duration_ms / 1000.0))
    t = np.linspace(0, duration_ms / 1000.0, n_samples, False)

    # Linear frequency sweep
    freqs = np.linspace(start_freq, end_freq, n_samples)
    tone = np.sin(2 * np.pi * freqs * t)

    # Gentle noise overlay
    noise = np.random.uniform(-0.3, 0.3, n_samples)
    signal = (tone * np.linspace(1, 0, n_samples)) + noise * 0.1

    # Apply decay and volume
    signal *= decay
    signal *= volume

    # Convert to int16
    audio = np.int16(signal / np.max(np.abs(signal)) * 32767)
    return audio

def generate_sounds():
    """Generate and export cell birth and death sounds with pitch sweeps."""
    # Cell birth → ascending tone
    birth = make_lofi_sweep(start_freq=400, end_freq=520, duration_ms=120, volume=0.5)
    wavfile.write("sfx/cell_birth.wav", SAMPLE_RATE, birth)

    # Cell death → descending tone
    death = make_lofi_sweep(start_freq=300, end_freq=150, duration_ms=100, volume=0.5)
    wavfile.write("sfx/cell_death.wav", SAMPLE_RATE, death)

    print("✅ Sound effects generated in assets/sfx/")

if __name__ == "__main__":
    generate_sounds()
