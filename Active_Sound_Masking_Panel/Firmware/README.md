Active Sound Masking – ESP32 Firmware

This firmware implements an adaptive sound-masking system.

Architecture:
I2S MEMS Microphone → ESP32 DSP → I2S DAC → Class-D Amplifier → Speaker

Files:

* main.py: Main control loop
* i2s_mic.py: Microphone input and RMS measurement
* dsp_control.py: Adaptive gain control (PI-like)
* pink_noise.py: Masking noise generation

Function:
The system continuously measures ambient noise, calculates RMS loudness,
and adjusts the masking noise level automatically to maintain speech privacy
without being intrusive.

Target masking level: 38–44 dBA (calibrated externally).
