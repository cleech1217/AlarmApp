from playsound import playsound
import ctypes

class AudioVolumeController:
    def __init__(self):
        self.default_volume = 0
    
    def get_default_volume(self):
        # Get the default audio output device volume
        default_device = ctypes.c_int()
        ctypes.windll.winmm.waveOutGetVolume(None, ctypes.byref(default_device))
        self.default_volume = default_device.value
        
    def set_max_volume(self):
        # Set both left and right channels to maximum volume (0xFFFF)
        max_volume = 0xFFFF
        ctypes.windll.winmm.waveOutSetVolume(None, max_volume)
    
    def restore_volume(self):
        # Restore the previous audio output device volume
        ctypes.windll.winmm.waveOutSetVolume(None, self.default_volume)