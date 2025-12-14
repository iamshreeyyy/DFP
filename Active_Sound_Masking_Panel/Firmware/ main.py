# main.py

# Active Sound Masking – ESP32 (MicroPython)

# Architecture: I2S Mic → ESP32 DSP → I2S DAC → Class-D Amp → Speaker

from i2s_mic import read_mic_rms
from dsp_control import update_gain
from pink_noise import generate_pink_noise
from machine import I2S, Pin
from config import *
import time

# I2S DAC configuration
dac = I2S(
    I2S_DAC_ID,
    sck=Pin(DAC_SCK_PIN),
    ws=Pin(DAC_WS_PIN),
    sd=Pin(DAC_SD_PIN),
    mode=I2S.TX,
    bits=BITS_PER_SAMPLE,
    format=I2S.MONO,
    rate=SAMPLE_RATE,
    ibuf=BUFFER_SIZE
)

gain = INITIAL_GAIN  # initial masking gain

while True:
    # Read ambient noise RMS
    ambient_rms = read_mic_rms()
    
    # Update gain using PI-like control
    gain = update_gain(ambient_rms, gain)
    
    # Generate masking noise
    noise = generate_pink_noise(NOISE_BUFFER_SIZE, gain)
    
    # Output to DAC → Amplifier → Speaker
    dac.write(noise)
    
    time.sleep_ms(UPDATE_INTERVAL_MS)
