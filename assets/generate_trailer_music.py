import numpy as np
import soundfile as sf


def linear_env(length, sr, attack, release):
    total = int(length * sr)
    env = np.ones(total)
    a = int(attack * sr)
    r = int(release * sr)
    if a > 0:
        env[:a] = np.linspace(0, 1, a)
    if r > 0:
        env[-r:] = np.linspace(1, 0, r)
    return env

def sine(freq, length, sr):
    t = np.arange(int(length*sr)) / sr
    return np.sin(2*np.pi*freq*t)

def modulated_sine(freq, length, sr, mod_freq, mod_depth):
    t = np.arange(int(length*sr)) / sr
    mod = 1.0 + mod_depth * np.sin(2*np.pi*mod_freq*t)
    return np.sin(2*np.pi*freq*t) * mod

def normalize(sig):
    m = np.max(np.abs(sig))
    return sig if m == 0 else sig / m

def noise_hit(sr, decay_ms):
    n = int(decay_ms/1000*sr)
    noise = np.random.randn(n)
    env = np.exp(-np.linspace(0, 8, n))
    hit = noise * env
    # simple low-pass: moving average
    hit = np.convolve(hit, np.ones(50)/50, mode='same')
    return hit

def melodic_event(freq, length, sr):
    t = np.arange(int(length*sr)) / sr
    drift = 1 + 0.01*np.sin(2*np.pi*0.1*t)
    sig = np.sin(2*np.pi*freq*t) * drift
    env = np.linspace(0,1,int(0.3*sr))
    env = np.concatenate([env, np.ones(len(sig)-len(env))])
    return sig * env


# parameters
sr = 48000
length = 90.0            # 90 seconds
base_freq = 65.41        # C2 (drone base)
layer_shift = 2**(3/12)  # +3 semitones
mod_freq = 0.15          # slow drift
mod_depth = 0.05         # subtle
attack = 2.0
release = 2.0

# layers
layer1 = modulated_sine(base_freq, length, sr, mod_freq, mod_depth)
layer2 = modulated_sine(base_freq*layer_shift, length, sr, mod_freq*0.8, mod_depth*0.8)

# envelope
env = linear_env(length, sr, attack, release)
layer1 *= env
layer2 *= env

# mix
mix = normalize(layer1 + 0.5*layer2)

sf.write("drone.wav", mix, sr)
