# Active Sound Masking Panel - Setup Guide

This guide will help you set up and deploy the Active Sound Masking Panel firmware to your ESP32.

## Hardware Requirements

- ESP32 development board
- I2S MEMS microphone (e.g., INMP441)
- PCM5102 DAC module
- PAM8403 amplifier module
- Speaker (4-8 ohms, 3-5W)
- Jumper wires and breadboard/PCB

## Software Requirements

### 1. Install Python Dependencies

```bash
# Install required Python packages
pip3 install esptool mpremote

# Optional: Install development dependencies for simulation
pip3 install -r requirements.txt
```

### 2. Hardware Connections

Follow the pin mapping in `hardware/Pin_Mapping.txt`:

**I2S MEMS Microphone → ESP32:**
- VDD → 3.3V
- GND → GND  
- SCK → GPIO26
- WS → GPIO25
- SD → GPIO33
- L/R → GND

**ESP32 → PCM5102 DAC:**
- GPIO26 → BCK
- GPIO25 → LRCK
- GPIO22 → DIN
- 3.3V → VDD
- GND → GND

**PCM5102 → PAM8403 Amplifier:**
- OUTL → INL
- GND → GND

**PAM8403 → Speaker:**
- OUTL+ → Speaker +
- OUTL- → Speaker -

### 3. Firmware Deployment

#### Option 1: Automatic Deployment (Recommended)
```bash
cd /path/to/Active_Sound_Masking_Panel
./deploy.sh
```

Follow the menu options:
1. Flash MicroPython firmware
2. Deploy Python files
3. Full deployment (recommended for first setup)

#### Option 2: Manual Deployment

1. **Flash MicroPython firmware:**
```bash
# Download MicroPython firmware
wget https://micropython.org/resources/firmware/esp32-20231005-v1.21.0.bin

# Erase and flash ESP32
esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 esp32-20231005-v1.21.0.bin
```

2. **Deploy Python files:**
```bash
cd Firmware
mpremote connect /dev/ttyUSB0 cp config.py :
mpremote connect /dev/ttyUSB0 cp i2s_mic.py :
mpremote connect /dev/ttyUSB0 cp dsp_control.py :
mpremote connect /dev/ttyUSB0 cp pink_noise.py :
mpremote connect /dev/ttyUSB0 cp " main.py" :main.py
```

### 4. Testing and Calibration

1. **Power on the ESP32** and allow 15 seconds for auto-calibration
2. **Measure SPL** at 1 meter distance using a sound level meter
3. **Verify** masking level is between 38-44 dBA
4. **Adjust configuration** in `config.py` if needed:
   - `TARGET_RMS`: Adjust for different ambient noise levels
   - `KP`: Adjust response speed (lower = slower response)
   - `GAIN_MIN/MAX`: Set safety limits for output level

### 5. Configuration Options

Edit `Firmware/config.py` to adjust system parameters:

```python
# Acoustic Parameters
TARGET_RMS = 300        # Target ambient noise level
KP = 0.0006            # Control loop gain
GAIN_MIN = 0.05        # Minimum masking level
GAIN_MAX = 0.8         # Maximum masking level

# Hardware Configuration  
SAMPLE_RATE = 16000    # Audio sample rate
UPDATE_INTERVAL_MS = 20 # Main loop update rate
```

## Troubleshooting

### Common Issues:

1. **No sound output:**
   - Check DAC wiring and power connections
   - Verify ESP32 GPIO pins match configuration
   - Test DAC module separately

2. **Distorted audio:**
   - Lower `GAIN_MAX` in config.py
   - Check amplifier power supply
   - Verify speaker impedance (4-8 ohms recommended)

3. **System not responding to noise changes:**
   - Check microphone wiring and power
   - Adjust `KP` (proportional gain) in config.py
   - Monitor serial output for debugging

4. **Deployment fails:**
   - Check USB cable and port permissions
   - Try different baud rate: `--baud 115200`
   - Press ESP32 boot button during flashing

### Serial Monitoring:
```bash
mpremote connect /dev/ttyUSB0
# Press Ctrl+D to soft reset and see output
```

## Performance Specifications

- **Target SPL:** 38-44 dBA
- **Convergence time:** ≤15 seconds  
- **Spatial variation:** ±2 dB
- **Maximum output:** 48 dBA (safety limit)
- **Update rate:** 50 Hz (20ms intervals)
- **Frequency response:** Optimized for speech masking

## Safety Notes

- Always verify output levels with a calibrated sound meter
- Never exceed 48 dBA output to prevent hearing damage
- Use appropriate power supplies (ESP32: 5V, Amplifier: 5V)
- Ensure proper grounding of all audio components
