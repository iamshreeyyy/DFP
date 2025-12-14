#!/bin/bash

# Active Sound Masking Panel - Deployment Script
# This script helps deploy the MicroPython firmware to ESP32

echo "Active Sound Masking Panel - ESP32 Deployment"
echo "============================================="

# Check if esptool is installed
if ! command -v esptool.py &> /dev/null; then
    echo "Installing esptool..."
    pip3 install esptool
fi

# Check if mpremote is installed
if ! command -v mpremote &> /dev/null; then
    echo "Installing mpremote..."
    pip3 install mpremote
fi

# Function to flash MicroPython firmware
flash_micropython() {
    echo "Downloading MicroPython firmware for ESP32..."
    MICROPYTHON_URL="https://micropython.org/resources/firmware/esp32-20231005-v1.21.0.bin"
    
    if [ ! -f "esp32-micropython.bin" ]; then
        wget $MICROPYTHON_URL -O esp32-micropython.bin
    fi
    
    echo "Erasing ESP32 flash..."
    esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
    
    echo "Flashing MicroPython firmware..."
    esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 esp32-micropython.bin
    
    echo "MicroPython firmware flashed successfully!"
}

# Function to deploy Python files
deploy_files() {
    echo "Deploying Python files to ESP32..."
    
    # Copy all Python files to ESP32
    mpremote connect /dev/ttyUSB0 cp config.py :
    mpremote connect /dev/ttyUSB0 cp i2s_mic.py :
    mpremote connect /dev/ttyUSB0 cp dsp_control.py :
    mpremote connect /dev/ttyUSB0 cp pink_noise.py :
    mpremote connect /dev/ttyUSB0 cp " main.py" :main.py
    
    echo "Files deployed successfully!"
}

# Function to test the system
test_system() {
    echo "Testing system..."
    mpremote connect /dev/ttyUSB0 exec "import main"
}

# Main menu
echo "Select an option:"
echo "1. Flash MicroPython firmware"
echo "2. Deploy Python files only"
echo "3. Full deployment (firmware + files)"
echo "4. Test system"
read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        flash_micropython
        ;;
    2)
        deploy_files
        ;;
    3)
        flash_micropython
        sleep 3
        deploy_files
        ;;
    4)
        test_system
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo "Deployment completed!"
