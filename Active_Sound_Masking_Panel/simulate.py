#!/usr/bin/env python3
"""
Active Sound Masking Panel - Simulation Script
Simulates the DSP algorithms without requiring ESP32 hardware
"""

import numpy as np
import matplotlib.pyplot as plt
import time

# Simulation parameters
SAMPLE_RATE = 16000
SIMULATION_TIME = 30  # seconds
TARGET_RMS = 300
KP = 0.0006
GAIN_MIN = 0.05
GAIN_MAX = 0.8

def simulate_ambient_noise(t, base_level=250):
    """Simulate varying ambient noise levels"""
    # Base noise + periodic variations + random fluctuations
    noise_level = base_level + 100 * np.sin(0.1 * t) + 50 * np.random.randn()
    
    # Add speech events (sudden increases)
    if 10 < t < 12 or 20 < t < 22:
        noise_level += 200  # Speech event
    
    return max(50, noise_level)  # Minimum noise floor

def update_gain_sim(measured_rms, current_gain):
    """Simulate the DSP gain control algorithm"""
    error = TARGET_RMS - measured_rms
    new_gain = current_gain + KP * error
    
    # Apply safety limits
    if new_gain < GAIN_MIN:
        new_gain = GAIN_MIN
    if new_gain > GAIN_MAX:
        new_gain = GAIN_MAX
    
    return new_gain

def generate_pink_noise_sim(n, gain):
    """Simulate pink noise generation"""
    # Simple approximation of pink noise
    white = np.random.randn(n)
    # Apply 1/f filtering (simplified)
    pink = np.convolve(white, [1, -0.5, 0.25], mode='same')
    return gain * pink

def run_simulation():
    """Run the complete system simulation"""
    print("Active Sound Masking Panel - Simulation")
    print("======================================")
    
    # Time arrays
    dt = 0.02  # 20ms update rate
    time_points = np.arange(0, SIMULATION_TIME, dt)
    
    # Initialize arrays for logging
    ambient_rms_log = []
    gain_log = []
    masking_level_log = []
    
    # Initial conditions
    gain = 0.3
    
    print(f"Simulating {SIMULATION_TIME} seconds of operation...")
    
    for t in time_points:
        # Simulate ambient noise measurement
        ambient_rms = simulate_ambient_noise(t)
        
        # Update masking gain
        gain = update_gain_sim(ambient_rms, gain)
        
        # Generate masking noise (calculate RMS level)
        noise_buffer = generate_pink_noise_sim(512, gain)
        masking_rms = np.sqrt(np.mean(noise_buffer**2)) * 1000  # Scale for display
        
        # Log data
        ambient_rms_log.append(ambient_rms)
        gain_log.append(gain)
        masking_level_log.append(masking_rms)
        
        # Print status every 2 seconds
        if int(t) % 2 == 0 and abs(t - int(t)) < dt:
            print(f"t={t:4.1f}s: Ambient={ambient_rms:6.1f}, Gain={gain:5.3f}, Masking={masking_rms:6.1f}")
    
    # Plot results
    plot_simulation_results(time_points, ambient_rms_log, gain_log, masking_level_log)

def plot_simulation_results(time_points, ambient_rms, gain, masking_level):
    """Plot the simulation results"""
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))
    
    # Ambient noise level
    ax1.plot(time_points, ambient_rms, 'b-', label='Ambient RMS')
    ax1.axhline(y=TARGET_RMS, color='r', linestyle='--', label='Target RMS')
    ax1.set_ylabel('RMS Level')
    ax1.set_title('Ambient Noise Measurement')
    ax1.legend()
    ax1.grid(True)
    
    # Control gain
    ax2.plot(time_points, gain, 'g-', label='Masking Gain')
    ax2.axhline(y=GAIN_MIN, color='r', linestyle=':', label='Min Gain')
    ax2.axhline(y=GAIN_MAX, color='r', linestyle=':', label='Max Gain')
    ax2.set_ylabel('Gain')
    ax2.set_title('Adaptive Gain Control')
    ax2.legend()
    ax2.grid(True)
    
    # Masking output level
    ax3.plot(time_points, masking_level, 'm-', label='Masking Level')
    ax3.set_ylabel('Output Level')
    ax3.set_xlabel('Time (seconds)')
    ax3.set_title('Masking Noise Output')
    ax3.legend()
    ax3.grid(True)
    
    plt.tight_layout()
    plt.savefig('simulation_results.png', dpi=300, bbox_inches='tight')
    print("\nSimulation complete! Results saved to 'simulation_results.png'")
    plt.show()

def analyze_performance():
    """Analyze system performance metrics"""
    print("\nPerformance Analysis:")
    print("====================")
    
    # Simulate step response
    print("Testing step response...")
    
    gain = 0.3
    step_times = []
    step_gains = []
    
    # Sudden increase in ambient noise
    for i in range(100):  # 2 seconds at 20ms intervals
        if i < 10:
            ambient_rms = 200  # Low noise
        else:
            ambient_rms = 500  # High noise (step input)
        
        gain = update_gain_sim(ambient_rms, gain)
        step_times.append(i * 0.02)
        step_gains.append(gain)
    
    # Calculate settling time (95% of final value)
    final_gain = step_gains[-1]
    initial_gain = step_gains[9]  # Just before step
    target_gain = initial_gain + 0.95 * (final_gain - initial_gain)
    
    settling_time = None
    for i, g in enumerate(step_gains[10:], 10):
        if g >= target_gain:
            settling_time = i * 0.02
            break
    
    print(f"Step response settling time: {settling_time:.2f} seconds")
    print(f"Initial gain: {initial_gain:.3f}")
    print(f"Final gain: {final_gain:.3f}")
    
    # Plot step response
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(step_times[:10] + step_times[10:], [200]*10 + [500]*90, 'b-', label='Ambient Noise')
    plt.ylabel('Ambient RMS')
    plt.title('Step Response Test')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(2, 1, 2)
    plt.plot(step_times, step_gains, 'g-', label='Gain Response')
    if settling_time:
        plt.axvline(x=settling_time, color='r', linestyle='--', label=f'95% Settling: {settling_time:.2f}s')
    plt.ylabel('Gain')
    plt.xlabel('Time (seconds)')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('step_response.png', dpi=300, bbox_inches='tight')
    print("Step response plot saved to 'step_response.png'")
    plt.show()

if __name__ == "__main__":
    try:
        run_simulation()
        analyze_performance()
    except ImportError as e:
        print("Error: Missing dependencies. Install with:")
        print("pip3 install numpy matplotlib")
        print(f"Details: {e}")
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user.")
