import numpy as np
import sounddevice as sd

class SpatialSonar:
    def __init__(self, sample_rate=44100, frame_width=640):
        self.sample_rate = sample_rate
        self.frame_width = frame_width

    def play_feedback(self, x_center, normalized_area):
        """
        Generates and plays a short stereo sine wave based on object location.
        
        :param x_center: X-coordinate of the bounding box.
        :param normalized_area: Float from 0.0 to 1.0 representing proximity.
        """
        # 1. Map normalized_area to frequency (200 Hz to 800 Hz)
        # Small area (far distance) = low hum (200 Hz)
        # Large area (close distance) = high pitch beep (800 Hz)
        normalized_area = max(0.0, min(1.0, normalized_area))
        frequency = 200 + (normalized_area * 600)
        
        # 2. Normalize x_center to range [-1.0, 1.0]
        # x_center = 0 -> -1.0 (full left)
        # x_center = frame_width -> 1.0 (full right)
        pan = (x_center / self.frame_width) * 2 - 1.0
        pan = max(-1.0, min(1.0, pan))
        
        # 3. Generate a 0.1 second sine wave
        duration = 0.1
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        wave = np.sin(frequency * t * 2 * np.pi)
        
        # 4. Apply stereo panning
        # When pan = -1.0, left is max volume
        # When pan = 1.0, right is max volume
        left_amplitude = (1 - pan) / 2.0
        right_amplitude = (1 + pan) / 2.0
        
        # Combine into a stereo numpy array (2 columns)
        stereo_wave = np.column_stack((wave * left_amplitude, wave * right_amplitude))
        
        # 5. Play using sounddevice (non-blocking)
        sd.play(stereo_wave, self.sample_rate)
        # Do not use sd.wait() here to keep it non-blocking
