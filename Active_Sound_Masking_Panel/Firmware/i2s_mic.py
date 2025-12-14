# i2s_mic.py

# Handles I2S microphone input and RMS calculation

from machine import I2S, Pin
from config import *
import array
import math

mic = I2S(
    I2S_MIC_ID,
    sck=Pin(MIC_SCK_PIN),
    ws=Pin(MIC_WS_PIN),
    sd=Pin(MIC_SD_PIN),
    mode=I2S.RX,
    bits=BITS_PER_SAMPLE,
    format=I2S.MONO,
    rate=SAMPLE_RATE,
    ibuf=BUFFER_SIZE
)

buffer = array.array("h", [0] * NOISE_BUFFER_SIZE)

def read_mic_rms():
    mic.readinto(buffer)
    s = 0
    for x in buffer:
        s += x * x
    return math.sqrt(s / len(buffer))
