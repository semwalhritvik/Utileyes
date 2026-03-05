import numpy as np
import sounddevice as sd

class SpatialSonar:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        
        # Audio state variables
        self.current_frequency = 200.0
        self.current_pan = 0.0
        self.phase = 0.0
        
        # Output stream
        self.stream = None

    def start(self):
        """Starts the audio output stream."""
        if self.stream is None:
            self.stream = sd.OutputStream(
                samplerate=self.sample_rate,
                channels=2,
                callback=self.audio_callback
            )
            self.stream.start()

    def stop(self):
        """Stops the audio output stream."""
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            self.stream = None

    def audio_callback(self, outdata, frames, time, status):
        """Callback to generate the sine wave continuously."""
        if status:
            pass
            
        t = (self.phase + np.arange(frames)) / self.sample_rate
        
        wave = np.sin(2 * np.pi * self.current_frequency * t)
        
        self.phase = (self.phase + frames) % self.sample_rate
        
        left_amplitude = (1 - self.current_pan) / 2.0
        right_amplitude = (1 + self.current_pan) / 2.0
        
        outdata[:, 0] = wave * left_amplitude
        outdata[:, 1] = wave * right_amplitude

    def update_target(self, target_pan, target_area):
        """
        Instantly updates parameters for zero-latency tracking.
        """
        area_clamped = max(0.0, min(1.0, target_area))
        self.current_frequency = 200.0 + (area_clamped * 600.0)
        self.current_pan = max(-1.0, min(1.0, target_pan))
