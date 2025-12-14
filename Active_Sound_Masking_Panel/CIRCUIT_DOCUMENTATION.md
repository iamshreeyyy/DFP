# Active Sound Masking Panel - Complete Circuit Documentation

## 🔌 Circuit Schematic Overview

```
                    ACTIVE SOUND MASKING PANEL - CIRCUIT DIAGRAM
                                
    ┌─────────────┐         ┌─────────────┐         ┌─────────────┐
    │   INMP441   │  I2S    │             │  I2S    │   PCM5102   │
    │ MEMS  MIC   │◄────────┤    ESP32    ├────────►│    DAC      │
    │             │         │ DEVKIT-V1   │         │   MODULE    │
    └─────────────┘         │             │         └─────────────┘
          │                 │             │               │
          │ Sound Input     │             │               │ Analog Audio
          │                 └─────────────┘               │
          ▼                                               ▼
    ┌─────────────┐                                 ┌─────────────┐
    │ Acoustic    │                                 │   PAM8403   │
    │Environment  │                                 │ Class-D AMP │
    │             │◄────────────────────────────────┤             │
    └─────────────┘         Masking Sound          └─────────────┘
          ▲                                               │
          │                                               │ Amplified Audio
          │                                               ▼
          │                                         ┌─────────────┐
          └─────────────────────────────────────────┤  4Ω SPEAKER │
                          Sound Output              │    3-5W     │
                                                   └─────────────┘
```

## 📋 Complete Component List

### Core Components
| Component | Model/Type | Purpose | Specifications |
|-----------|------------|---------|----------------|
| **Microcontroller** | ESP32-WROOM-32 | Main processing unit | 240MHz dual-core, WiFi/BT, I2S support |
| **Microphone** | INMP441 | Ambient noise sensing | I2S MEMS, -26dBFS sensitivity, 61dB SNR |
| **DAC Module** | PCM5102A | Digital to analog conversion | 32-bit, 384kHz, 112dB SNR |
| **Amplifier** | PAM8403 | Audio power amplification | Class-D, 3W per channel, 90% efficiency |
| **Speaker** | Generic 4Ω | Sound output transducer | 4 ohm impedance, 3-5W power rating |

### Supporting Components
| Component | Quantity | Purpose | Notes |
|-----------|----------|---------|--------|
| **Bypass Capacitors** | 4-6 pcs | Power supply filtering | 100nF ceramic, 10µF electrolytic |
| **Pull-up Resistors** | 3 pcs | I2S signal integrity | 10kΩ, 1/4W |
| **Power Supply** | 1 pc | System power | 5V 2A minimum |
| **Connector Headers** | Various | Component connections | 2.54mm pitch |

## 🔌 Detailed Pin Mapping

### ESP32 to INMP441 Microphone
```
ESP32 Pin    │  INMP441 Pin  │  Signal      │  Wire Color  │  Function
─────────────┼───────────────┼──────────────┼──────────────┼─────────────────
3.3V         │  VDD          │  Power       │  Red         │  Supply voltage
GND          │  GND          │  Ground      │  Black       │  Power ground
GPIO26       │  SCK          │  I2S_SCLK    │  Green       │  Serial clock
GPIO25       │  WS           │  I2S_LRCLK   │  Blue        │  Left/Right clock
GPIO33       │  SD           │  I2S_DOUT    │  Purple      │  Serial data out
GND          │  L/R          │  Channel     │  Black       │  Left channel select
3.3V         │  CHIPEN       │  Enable      │  Red         │  Chip enable
```

### ESP32 to PCM5102 DAC
```
ESP32 Pin    │  PCM5102 Pin  │  Signal      │  Wire Color  │  Function
─────────────┼───────────────┼──────────────┼──────────────┼─────────────────
3.3V         │  VCC          │  Power       │  Red         │  Supply voltage
GND          │  GND          │  Ground      │  Black       │  Power ground
GPIO26       │  BCK          │  I2S_BCLK    │  Green       │  Bit clock
GPIO25       │  LCK          │  I2S_LRCK    │  Blue        │  Left/Right clock
GPIO22       │  DIN          │  I2S_DIN     │  Brown       │  Data input
3.3V         │  FLT          │  Filter      │  Red         │  Filter select
GND          │  SCL          │  Soft Mute   │  Black       │  Soft mute (GND=off)
```

### PCM5102 to PAM8403 Amplifier
```
PCM5102 Pin  │  PAM8403 Pin  │  Signal      │  Wire Color  │  Function
─────────────┼───────────────┼──────────────┼──────────────┼─────────────────
OUTL         │  INL          │  Audio Left  │  Magenta     │  Analog audio signal
OUTR         │  INR          │  Audio Right │  Cyan        │  Analog audio signal (optional)
GND          │  GND          │  Ground      │  Black       │  Audio ground
```

### PAM8403 to Speaker
```
PAM8403 Pin  │  Speaker      │  Signal      │  Wire Color  │  Function
─────────────┼───────────────┼──────────────┼──────────────┼─────────────────
OUTL+        │  Speaker +    │  Audio Pos   │  Red         │  Positive terminal
OUTL-        │  Speaker -    │  Audio Neg   │  Black       │  Negative terminal
```

## ⚡ Power Distribution

### Power Requirements
```
Component    │  Voltage  │  Current   │  Power    │  Notes
─────────────┼───────────┼────────────┼───────────┼──────────────────
ESP32        │  3.3V     │  240mA     │  0.8W     │  Peak during WiFi TX
INMP441      │  3.3V     │  200µA     │  0.7mW    │  Very low power
PCM5102      │  3.3V     │  50mA      │  0.16W    │  During operation
PAM8403      │  5V       │  1.5A      │  7.5W     │  At maximum output
Total System │  5V       │  2A        │  10W      │  Recommended supply
```

### Power Supply Connections
```
5V Power Supply
│
├── ESP32 Development Board (has onboard 3.3V regulator)
│   │
│   ├── 3.3V → INMP441 VDD
│   ├── 3.3V → PCM5102 VCC
│   └── GND → Common Ground
│
└── PAM8403 VDD (5V direct)
```

## 🔧 Assembly Instructions

### Step 1: Prepare Components
1. **ESP32 Development Board** - Ensure bootloader is functional
2. **INMP441 Module** - Check for proper I2S pin breakout
3. **PCM5102 Module** - Verify jumper settings for I2S mode
4. **PAM8403 Module** - Confirm power rating matches speaker
5. **Speaker** - Check impedance (4Ω) and power rating (3-5W)

### Step 2: Power Connections
```
1. Connect 5V power supply to ESP32 VIN and PAM8403 VDD
2. Connect all GND pins together (common ground)
3. ESP32 3.3V output connects to INMP441 and PCM5102 VDD
4. Add 100µF capacitor across 5V supply for filtering
5. Add 10µF capacitor across 3.3V for ESP32 stability
```

### Step 3: I2S Audio Connections
```
1. GPIO26 → INMP441 SCK and PCM5102 BCK (shared clock)
2. GPIO25 → INMP441 WS and PCM5102 LCK (shared word select)
3. GPIO33 → INMP441 SD (microphone data to ESP32)
4. GPIO22 → PCM5102 DIN (ESP32 data to DAC)
5. Add 10kΩ pull-up resistors on I2S lines for signal integrity
```

### Step 4: Audio Output Chain
```
1. PCM5102 OUTL → PAM8403 INL (left channel audio)
2. PCM5102 GND → PAM8403 GND (audio ground reference)
3. PAM8403 OUTL+ → Speaker positive terminal
4. PAM8403 OUTL- → Speaker negative terminal
5. Keep audio traces short to minimize interference
```

### Step 5: Configuration Settings
```
1. INMP441 L/R pin → GND (left channel mode)
2. INMP441 CHIPEN → 3.3V (enable chip)
3. PCM5102 FLT → 3.3V (filter enabled)
4. PCM5102 SCL → GND (soft mute disabled)
5. All unused PCM5102 pins can be left floating
```

## 🛡️ Safety Considerations

### Electrical Safety
- **Maximum power**: Keep total system power under 15W
- **Fuse protection**: Add 3A fuse on 5V supply line
- **Ground isolation**: Ensure proper grounding to prevent noise
- **Heat management**: PAM8403 may need heatsinking at high power

### Acoustic Safety  
- **Volume limiting**: Firmware enforces 48 dBA maximum
- **Gradual changes**: Gain adjustments are rate-limited
- **Fail-safe mode**: System defaults to minimum gain on error

### Component Protection
- **Reverse polarity**: Add protection diode on power input
- **Overvoltage**: Use TVS diodes on I2S lines if needed
- **ESD protection**: Handle components with anti-static precautions

## 📐 Mechanical Considerations

### Enclosure Requirements
- **Dimensions**: Minimum 100mm x 80mm x 40mm
- **Ventilation**: Slots for PAM8403 cooling
- **Microphone placement**: Clear acoustic path, away from speaker
- **Speaker mounting**: Secure mounting to prevent vibration
- **Access ports**: USB for programming, power jack

### Cable Management
- **I2S signals**: Keep traces under 10cm, use twisted pairs if possible
- **Power lines**: Use adequate wire gauge (18AWG for 5V, 22AWG for 3.3V)
- **Audio signals**: Shielded cable for analog audio connections
- **Speaker wires**: 16-18AWG for 3-5W speaker

## 🔬 Testing and Validation

### Functional Tests
1. **Power-on test**: Verify all voltage levels
2. **I2S communication**: Check for valid audio data transfer
3. **Microphone response**: Measure ambient noise detection
4. **DAC output**: Verify analog audio signal generation
5. **Amplifier function**: Test speaker output at various levels
6. **Control loop**: Validate adaptive gain behavior

### Performance Verification
1. **Frequency response**: Measure system bandwidth (20Hz-20kHz)
2. **SPL calibration**: Calibrate to target 38-44 dBA range
3. **Response time**: Verify <15 second settling time
4. **Stability test**: 24-hour continuous operation test
5. **EMI compliance**: Check for electromagnetic interference

---

**Note**: This circuit is designed for educational and research purposes. Ensure compliance with local regulations for acoustic devices in your intended application environment.
