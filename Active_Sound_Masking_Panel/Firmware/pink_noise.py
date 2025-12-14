# pink_noise.py

# Simple pink-noise-like generator for masking

import array
import math
import time

def generate_pink_noise(n, gain):
    buf = array.array("h", [0] * n)
    t = time.ticks_ms()
    for i in range(n):
        white = math.sin((t + i) * 0.01)
        buf[i] = int(32767 * gain * white)
    return buf
