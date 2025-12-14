# dsp_control.py

# Adaptive gain control with safety limits

from config import TARGET_RMS, KP, GAIN_MIN, GAIN_MAX

def update_gain(measured_rms, current_gain):
    error = TARGET_RMS - measured_rms
    new_gain = current_gain + KP * error
    
    if new_gain < GAIN_MIN:
        new_gain = GAIN_MIN
    if new_gain > GAIN_MAX:
        new_gain = GAIN_MAX
    
    return new_gain
