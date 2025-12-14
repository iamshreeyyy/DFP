#!/usr/bin/env python3
"""
Active Sound Masking Panel - Circuit Diagram Generator
Creates detailed schematic and wiring diagrams
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle
import matplotlib
matplotlib.use('Agg')

def create_schematic_diagram():
    """Create detailed system schematic diagram"""
    print("🔧 Generating circuit schematic diagram...")
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    
    # Component positions
    esp32_pos = (2, 6)
    mic_pos = (0.5, 8.5)
    dac_pos = (4.5, 8.5)
    amp_pos = (7, 6)
    speaker_pos = (9, 6)
    power_pos = (1, 3)
    
    # Draw ESP32 (main controller)
    esp32 = FancyBboxPatch((esp32_pos[0]-0.8, esp32_pos[1]-1.2), 1.6, 2.4,
                          boxstyle="round,pad=0.1", facecolor='lightblue', 
                          edgecolor='black', linewidth=2)
    ax.add_patch(esp32)
    ax.text(esp32_pos[0], esp32_pos[1], 'ESP32\nDevelopment\nBoard', 
            ha='center', va='center', fontweight='bold', fontsize=10)
    
    # Draw INMP441 Microphone
    mic = FancyBboxPatch((mic_pos[0]-0.6, mic_pos[1]-0.6), 1.2, 1.2,
                        boxstyle="round,pad=0.1", facecolor='lightgreen',
                        edgecolor='black', linewidth=2)
    ax.add_patch(mic)
    ax.text(mic_pos[0], mic_pos[1], 'INMP441\nI2S MEMS\nMicrophone', 
            ha='center', va='center', fontweight='bold', fontsize=8)
    
    # Draw PCM5102 DAC
    dac = FancyBboxPatch((dac_pos[0]-0.6, dac_pos[1]-0.6), 1.2, 1.2,
                        boxstyle="round,pad=0.1", facecolor='lightyellow',
                        edgecolor='black', linewidth=2)
    ax.add_patch(dac)
    ax.text(dac_pos[0], dac_pos[1], 'PCM5102\nI2S DAC\nModule', 
            ha='center', va='center', fontweight='bold', fontsize=8)
    
    # Draw PAM8403 Amplifier
    amp = FancyBboxPatch((amp_pos[0]-0.7, amp_pos[1]-0.8), 1.4, 1.6,
                        boxstyle="round,pad=0.1", facecolor='lightcoral',
                        edgecolor='black', linewidth=2)
    ax.add_patch(amp)
    ax.text(amp_pos[0], amp_pos[1], 'PAM8403\nClass-D\nAmplifier', 
            ha='center', va='center', fontweight='bold', fontsize=9)
    
    # Draw Speaker
    speaker_circle = Circle(speaker_pos, 0.8, facecolor='lightpink', 
                           edgecolor='black', linewidth=2)
    ax.add_patch(speaker_circle)
    ax.text(speaker_pos[0], speaker_pos[1], '4Ω Speaker\n3-5W', 
            ha='center', va='center', fontweight='bold', fontsize=9)
    
    # Draw Power Supply
    power = Rectangle((power_pos[0]-0.5, power_pos[1]-0.5), 1, 1,
                     facecolor='orange', edgecolor='black', linewidth=2)
    ax.add_patch(power)
    ax.text(power_pos[0], power_pos[1], '5V\nPower', 
            ha='center', va='center', fontweight='bold', fontsize=9)
    
    # Connection lines and labels
    connections = [
        # Microphone to ESP32 (I2S)
        ((mic_pos[0]+0.6, mic_pos[1]), (esp32_pos[0]-0.8, esp32_pos[1]+0.8), 'I2S Bus\n(SCK, WS, SD)', 'green'),
        # ESP32 to DAC (I2S)
        ((esp32_pos[0]+0.8, esp32_pos[1]+0.8), (dac_pos[0]-0.6, dac_pos[1]), 'I2S Bus\n(BCK, LRCK, DIN)', 'blue'),
        # DAC to Amplifier (Analog)
        ((dac_pos[0]+0.6, dac_pos[1]), (amp_pos[0]-0.7, amp_pos[1]+0.4), 'Analog Audio\n(OUTL)', 'purple'),
        # Amplifier to Speaker
        ((amp_pos[0]+0.7, amp_pos[1]), (speaker_pos[0]-0.8, speaker_pos[1]), 'Amplified\nAudio', 'red'),
        # Power connections
        ((power_pos[0]+0.5, power_pos[1]), (esp32_pos[0], esp32_pos[1]-1.2), '5V/3.3V', 'orange'),
    ]
    
    for start, end, label, color in connections:
        ax.annotate('', xy=end, xytext=start,
                   arrowprops=dict(arrowstyle='->', color=color, lw=2))
        # Add label at midpoint
        mid_x, mid_y = (start[0] + end[0])/2, (start[1] + end[1])/2
        ax.text(mid_x, mid_y+0.2, label, ha='center', va='bottom', 
               fontsize=7, color=color, fontweight='bold',
               bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
    
    # Add title and specifications
    ax.text(5, 11, 'Active Sound Masking Panel - System Schematic', 
           ha='center', va='center', fontsize=16, fontweight='bold')
    
    # Add pin mapping details
    pin_details = [
        "ESP32 Pin Mapping:",
        "• GPIO26 → I2S SCK (Mic & DAC)",
        "• GPIO25 → I2S WS/LRCK (Mic & DAC)",
        "• GPIO33 → I2S SD (Microphone Input)",
        "• GPIO22 → I2S DIN (DAC Output)",
        "",
        "Power Requirements:",
        "• ESP32: 3.3V (from onboard regulator)",
        "• INMP441: 3.3V (200mA max)",
        "• PCM5102: 3.3V (50mA typical)",
        "• PAM8403: 5V (2A max at full power)"
    ]
    
    for i, detail in enumerate(pin_details):
        ax.text(0.5, 1.8-i*0.15, detail, ha='left', va='top', fontsize=8,
               fontfamily='monospace')
    
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(0, 12)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('circuit_schematic.png', dpi=300, bbox_inches='tight')
    print("✅ Circuit schematic saved: circuit_schematic.png")

def create_wiring_diagram():
    """Create detailed wiring/breadboard diagram"""
    print("🔌 Generating wiring diagram...")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 10))
    
    # Left side - Component layout
    ax1.set_title('Component Layout & Connections', fontsize=14, fontweight='bold')
    
    # Draw breadboard representation
    breadboard = Rectangle((1, 1), 8, 6, facecolor='lightgray', 
                          edgecolor='black', linewidth=2)
    ax1.add_patch(breadboard)
    
    # Component positions on breadboard
    components = [
        {'name': 'ESP32', 'pos': (2, 4), 'size': (1.5, 1), 'color': 'lightblue'},
        {'name': 'INMP441', 'pos': (1.2, 6), 'size': (0.8, 0.6), 'color': 'lightgreen'},
        {'name': 'PCM5102', 'pos': (4, 6), 'size': (0.8, 0.6), 'color': 'lightyellow'},
        {'name': 'PAM8403', 'pos': (6.5, 4), 'size': (1.2, 1), 'color': 'lightcoral'},
        {'name': 'Speaker', 'pos': (8.5, 4), 'size': (0.8, 0.8), 'color': 'lightpink'},
    ]
    
    for comp in components:
        rect = Rectangle(comp['pos'], comp['size'][0], comp['size'][1],
                        facecolor=comp['color'], edgecolor='black', linewidth=1.5)
        ax1.add_patch(rect)
        ax1.text(comp['pos'][0] + comp['size'][0]/2, 
                comp['pos'][1] + comp['size'][1]/2,
                comp['name'], ha='center', va='center', fontweight='bold', fontsize=8)
    
    # Wire connections with colors
    wires = [
        # Power wires (red for +, black for -)
        {'start': (2.75, 4), 'end': (1.6, 6), 'color': 'red', 'label': '3.3V'},
        {'start': (2.75, 4), 'end': (4.4, 6), 'color': 'red', 'label': '3.3V'},
        {'start': (2.75, 4), 'end': (7.1, 4), 'color': 'orange', 'label': '5V'},
        
        # I2S connections (different colors for different signals)
        {'start': (2.5, 4.5), 'end': (1.4, 6.3), 'color': 'green', 'label': 'SCK'},
        {'start': (2.7, 4.5), 'end': (1.6, 6.3), 'color': 'blue', 'label': 'WS'},
        {'start': (2.9, 4.5), 'end': (1.8, 6.3), 'color': 'purple', 'label': 'SD'},
        
        # DAC connections
        {'start': (3.2, 4.5), 'end': (4.2, 6), 'color': 'green', 'label': 'BCK'},
        {'start': (3.4, 4.5), 'end': (4.4, 6), 'color': 'blue', 'label': 'LRCK'},
        {'start': (3.6, 4.5), 'end': (4.6, 6), 'color': 'brown', 'label': 'DIN'},
        
        # Audio output
        {'start': (4.8, 6.3), 'end': (6.5, 4.5), 'color': 'magenta', 'label': 'AUDIO'},
        {'start': (7.7, 4.5), 'end': (8.5, 4.4), 'color': 'red', 'label': 'SPK+'},
        {'start': (7.7, 4.3), 'end': (8.5, 4.2), 'color': 'black', 'label': 'SPK-'},
    ]
    
    for wire in wires:
        ax1.plot([wire['start'][0], wire['end'][0]], 
                [wire['start'][1], wire['end'][1]], 
                color=wire['color'], linewidth=2)
        # Add wire label
        mid_x = (wire['start'][0] + wire['end'][0]) / 2
        mid_y = (wire['start'][1] + wire['end'][1]) / 2
        ax1.text(mid_x, mid_y, wire['label'], fontsize=6, 
                bbox=dict(boxstyle="round,pad=0.1", facecolor='white', alpha=0.7))
    
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 8)
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.3)
    
    # Right side - Pin mapping table
    ax2.set_title('Detailed Pin Mapping & Connections', fontsize=14, fontweight='bold')
    
    # Create connection table
    table_data = [
        ['Component', 'Pin', 'ESP32 GPIO', 'Wire Color', 'Function'],
        ['', '', '', '', ''],
        ['INMP441 Mic', 'VDD', '3.3V', 'Red', 'Power Supply'],
        ['', 'GND', 'GND', 'Black', 'Ground'],
        ['', 'SCK', 'GPIO26', 'Green', 'I2S Clock'],
        ['', 'WS', 'GPIO25', 'Blue', 'Word Select'],
        ['', 'SD', 'GPIO33', 'Purple', 'Serial Data'],
        ['', 'L/R', 'GND', 'Black', 'Left Channel'],
        ['', 'CHIPEN', '3.3V', 'Red', 'Chip Enable'],
        ['', '', '', '', ''],
        ['PCM5102 DAC', 'VDD', '3.3V', 'Red', 'Power Supply'],
        ['', 'GND', 'GND', 'Black', 'Ground'],
        ['', 'BCK', 'GPIO26', 'Green', 'Bit Clock'],
        ['', 'LRCK', 'GPIO25', 'Blue', 'LR Clock'],
        ['', 'DIN', 'GPIO22', 'Brown', 'Data Input'],
        ['', 'OUTL', 'PAM8403 INL', 'Magenta', 'Audio Output'],
        ['', '', '', '', ''],
        ['PAM8403 Amp', 'VDD', '5V', 'Orange', 'Power Supply'],
        ['', 'GND', 'GND', 'Black', 'Ground'],
        ['', 'INL', 'PCM5102 OUTL', 'Magenta', 'Audio Input'],
        ['', 'OUTL+', 'Speaker +', 'Red', 'Speaker Positive'],
        ['', 'OUTL-', 'Speaker -', 'Black', 'Speaker Negative'],
    ]
    
    # Draw table
    cell_height = 0.3
    cell_width = 1.5
    start_y = 7
    
    for row_idx, row in enumerate(table_data):
        y_pos = start_y - row_idx * cell_height
        
        # Header row styling
        if row_idx == 0:
            bg_color = 'lightblue'
            text_weight = 'bold'
        elif row[0] == '':  # Empty separator rows
            bg_color = 'white'
            text_weight = 'normal'
        else:
            bg_color = 'lightgray' if row_idx % 2 == 0 else 'white'
            text_weight = 'normal'
        
        for col_idx, cell in enumerate(row):
            x_pos = col_idx * cell_width
            
            # Draw cell background
            rect = Rectangle((x_pos, y_pos), cell_width, cell_height,
                           facecolor=bg_color, edgecolor='black', linewidth=0.5)
            ax2.add_patch(rect)
            
            # Add text
            ax2.text(x_pos + cell_width/2, y_pos + cell_height/2, cell,
                    ha='center', va='center', fontsize=8, fontweight=text_weight)
    
    ax2.set_xlim(0, 7.5)
    ax2.set_ylim(0, 8)
    ax2.axis('off')
    
    plt.tight_layout()
    plt.savefig('wiring_diagram.png', dpi=300, bbox_inches='tight')
    print("✅ Wiring diagram saved: wiring_diagram.png")

def create_pcb_layout():
    """Create suggested PCB layout diagram"""
    print("🛠️ Generating PCB layout suggestion...")
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # PCB outline
    pcb = Rectangle((0.5, 0.5), 9, 6, facecolor='darkgreen', 
                   edgecolor='black', linewidth=3)
    ax.add_patch(pcb)
    
    ax.text(5, 7, 'Suggested PCB Layout (80mm x 60mm)', 
           ha='center', va='center', fontsize=14, fontweight='bold')
    
    # Component footprints
    footprints = [
        {'name': 'ESP32-WROOM-32', 'pos': (2, 3), 'size': (1.8, 2.4), 'color': 'lightblue'},
        {'name': 'INMP441', 'pos': (0.8, 5.2), 'size': (0.8, 0.6), 'color': 'lightgreen'},
        {'name': 'PCM5102A', 'pos': (4.5, 5.2), 'size': (1.2, 0.8), 'color': 'lightyellow'},
        {'name': 'PAM8403', 'pos': (6.5, 3), 'size': (1.5, 1.2), 'color': 'lightcoral'},
        {'name': 'Power Jack', 'pos': (0.7, 1), 'size': (0.6, 0.8), 'color': 'orange'},
        {'name': 'Speaker Conn', 'pos': (8.3, 3.2), 'size': (0.8, 0.6), 'color': 'lightpink'},
    ]
    
    for fp in footprints:
        rect = Rectangle(fp['pos'], fp['size'][0], fp['size'][1],
                        facecolor=fp['color'], edgecolor='black', linewidth=1)
        ax.add_patch(rect)
        ax.text(fp['pos'][0] + fp['size'][0]/2, 
               fp['pos'][1] + fp['size'][1]/2,
               fp['name'], ha='center', va='center', fontweight='bold', fontsize=7)
    
    # PCB traces (simplified)
    traces = [
        # Power traces (thicker, red)
        {'path': [(1, 1.4), (2.9, 1.4), (2.9, 3)], 'width': 3, 'color': 'red'},
        {'path': [(1.3, 1.8), (6.5, 1.8), (6.5, 3)], 'width': 3, 'color': 'red'},
        
        # I2S traces (thinner, various colors)
        {'path': [(1.6, 5.5), (2.2, 5.5), (2.2, 5.4)], 'width': 1, 'color': 'green'},
        {'path': [(4.5, 5.6), (3.8, 5.6), (3.8, 5.4)], 'width': 1, 'color': 'blue'},
        
        # Audio traces
        {'path': [(5.7, 5.6), (6.5, 5.6), (6.5, 4.2)], 'width': 2, 'color': 'purple'},
        {'path': [(8, 3.5), (8.3, 3.5)], 'width': 2, 'color': 'purple'},
    ]
    
    for trace in traces:
        path = trace['path']
        for i in range(len(path)-1):
            ax.plot([path[i][0], path[i+1][0]], [path[i][1], path[i+1][1]],
                   color=trace['color'], linewidth=trace['width'], alpha=0.7)
    
    # Add mounting holes
    mounting_holes = [(1, 6), (8.5, 6), (1, 1), (8.5, 1)]
    for hole in mounting_holes:
        circle = Circle(hole, 0.1, facecolor='white', edgecolor='black', linewidth=2)
        ax.add_patch(circle)
    
    # Add design notes
    notes = [
        "Design Notes:",
        "• Ground plane recommended",
        "• Keep analog traces short", 
        "• Separate power domains",
        "• EMI shielding for sensitive areas",
        "• Proper bypass capacitors needed"
    ]
    
    for i, note in enumerate(notes):
        ax.text(0.5, 2.5-i*0.2, note, fontsize=8, 
               fontweight='bold' if i == 0 else 'normal')
    
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7.5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('pcb_layout.png', dpi=300, bbox_inches='tight')
    print("✅ PCB layout saved: pcb_layout.png")

def create_system_block_diagram():
    """Create detailed system block diagram with signal flow"""
    print("📊 Generating system block diagram...")
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    
    # Define blocks with signal flow
    blocks = [
        {'name': 'Acoustic\nEnvironment', 'pos': (1, 8), 'size': (1.5, 1), 'color': 'lightcyan'},
        {'name': 'INMP441\nMEMS Mic', 'pos': (4, 8), 'size': (1.5, 1), 'color': 'lightgreen'},
        {'name': 'I2S Interface\n(RX)', 'pos': (7, 8), 'size': (1.5, 1), 'color': 'lightblue'},
        {'name': 'ESP32\nDSP Core', 'pos': (7, 5), 'size': (2, 1.5), 'color': 'yellow'},
        {'name': 'RMS\nCalculation', 'pos': (4, 5), 'size': (1.5, 1), 'color': 'lightyellow'},
        {'name': 'PI Control\nAlgorithm', 'pos': (4, 3), 'size': (1.5, 1), 'color': 'lightcoral'},
        {'name': 'Pink Noise\nGenerator', 'pos': (7, 2), 'size': (1.5, 1), 'color': 'lightpink'},
        {'name': 'I2S Interface\n(TX)', 'pos': (10, 5), 'size': (1.5, 1), 'color': 'lightblue'},
        {'name': 'PCM5102\nDAC', 'pos': (10, 8), 'size': (1.5, 1), 'color': 'lightyellow'},
        {'name': 'PAM8403\nAmplifier', 'pos': (1, 5), 'size': (1.5, 1), 'color': 'lightcoral'},
        {'name': 'Speaker\n4Ω 3-5W', 'pos': (1, 2), 'size': (1.5, 1), 'color': 'lightpink'},
    ]
    
    # Draw blocks
    for block in blocks:
        rect = FancyBboxPatch(block['pos'], block['size'][0], block['size'][1],
                             boxstyle="round,pad=0.1", facecolor=block['color'],
                             edgecolor='black', linewidth=2)
        ax.add_patch(rect)
        ax.text(block['pos'][0] + block['size'][0]/2, 
               block['pos'][1] + block['size'][1]/2,
               block['name'], ha='center', va='center', fontweight='bold', fontsize=9)
    
    # Signal flow arrows with labels
    arrows = [
        # Forward path
        {'start': (2.5, 8.5), 'end': (4, 8.5), 'label': 'Sound Waves', 'color': 'blue'},
        {'start': (5.5, 8.5), 'end': (7, 8.5), 'label': 'I2S Digital\nAudio', 'color': 'green'},
        {'start': (7.75, 8), 'end': (7.75, 6.5), 'label': 'Digital\nSamples', 'color': 'purple'},
        {'start': (7, 5.75), 'end': (5.5, 5.75), 'label': 'Raw Audio\nData', 'color': 'orange'},
        {'start': (4.75, 5), 'end': (4.75, 4), 'label': 'RMS\nValue', 'color': 'red'},
        
        # Control path
        {'start': (4.75, 3), 'end': (7, 2.5), 'label': 'Gain\nControl', 'color': 'magenta'},
        {'start': (8.5, 2.5), 'end': (8.5, 5), 'label': 'Masking\nNoise', 'color': 'brown'},
        
        # Output path
        {'start': (9, 5.5), 'end': (10, 5.5), 'label': 'I2S Digital\nOut', 'color': 'green'},
        {'start': (10.75, 6), 'end': (10.75, 8), 'label': 'Digital\nAudio', 'color': 'purple'},
        {'start': (10, 8.5), 'end': (2.5, 6), 'label': 'Analog\nAudio', 'color': 'red'},
        {'start': (1.75, 5), 'end': (1.75, 3), 'label': 'Amplified\nAudio', 'color': 'red'},
        {'start': (1.75, 2), 'end': (1.75, 8), 'label': 'Masking\nSound', 'color': 'cyan'},
    ]
    
    for arrow in arrows:
        ax.annotate('', xy=arrow['end'], xytext=arrow['start'],
                   arrowprops=dict(arrowstyle='->', color=arrow['color'], lw=2))
        # Add label
        mid_x = (arrow['start'][0] + arrow['end'][0]) / 2
        mid_y = (arrow['start'][1] + arrow['end'][1]) / 2
        ax.text(mid_x+0.2, mid_y+0.2, arrow['label'], fontsize=7, 
               color=arrow['color'], fontweight='bold',
               bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
    
    # Add system specifications
    ax.text(7, 0.5, 'System Specifications:\n• Sample Rate: 16 kHz\n• Resolution: 16-bit\n• Update Rate: 50 Hz\n• Target SPL: 38-44 dBA\n• Safety Limit: 48 dBA',
           ha='center', va='center', fontsize=10,
           bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow', alpha=0.8))
    
    ax.set_title('Active Sound Masking Panel - Detailed System Block Diagram', 
                fontsize=16, fontweight='bold', pad=20)
    
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('system_block_diagram.png', dpi=300, bbox_inches='tight')
    print("✅ System block diagram saved: system_block_diagram.png")

if __name__ == "__main__":
    print("🔧 Generating complete circuit documentation...")
    create_schematic_diagram()
    create_wiring_diagram()
    create_pcb_layout()
    create_system_block_diagram()
    
    print(f"\n📁 Generated Circuit Documentation:")
    print(f"   • circuit_schematic.png - Main system schematic")
    print(f"   • wiring_diagram.png - Detailed pin connections")
    print(f"   • pcb_layout.png - Suggested PCB layout")
    print(f"   • system_block_diagram.png - Signal flow diagram")
    print(f"\n🎯 Complete circuit documentation ready!")
