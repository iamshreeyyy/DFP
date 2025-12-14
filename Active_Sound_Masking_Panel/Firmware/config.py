# MicroPython Configuration for Active Sound Masking Panel

# This file contains configuration constants that can be adjusted
# based on your specific hardware setup and acoustic requirements

# I2S Configuration
I2S_MIC_ID = 0
I2S_DAC_ID = 1
SAMPLE_RATE = 16000
BITS_PER_SAMPLE = 16
BUFFER_SIZE = 4000

# Pin Assignments (ESP32)
# Microphone
MIC_SCK_PIN = 26
MIC_WS_PIN = 25
MIC_SD_PIN = 33

# DAC Output
DAC_SCK_PIN = 26
DAC_WS_PIN = 25
DAC_SD_PIN = 22

# DSP Parameters
TARGET_RMS = 300        # Target ambient noise level
KP = 0.0006            # Proportional gain for control loop
GAIN_MIN = 0.05        # Minimum masking gain (safety)
GAIN_MAX = 0.8         # Maximum masking gain (safety)
INITIAL_GAIN = 0.3     # Starting masking level

# Timing
UPDATE_INTERVAL_MS = 20    # Main loop update rate
NOISE_BUFFER_SIZE = 512    # Samples per noise generation cycle

# Acoustic Calibration
# Adjust these values based on your specific hardware and room acoustics
# Target SPL: 38-44 dBA
SPL_CALIBRATION_OFFSET = 0  # dB adjustment for microphone calibration
MAX_SPL_LIMIT = 48          # Maximum allowed output level (dBA)
