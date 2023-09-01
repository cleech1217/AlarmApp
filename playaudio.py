import pygame
import os
import ctypes

class AudioVolumeController:
    def __init__(self):
        self.default_volume = 1
        self.get_default_volume()  # Call the method to initialize default_volume
    
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

    def desired_volume(self,percent):
        desired_volume_percent = percent
        max_volume = 0xFFFF
        desired_volume_value = int((desired_volume_percent / 100) * max_volume)
        ctypes.windll.winmm.waveOutSetVolume(None, desired_volume_value)

# Initialize pygame
pygame.init()

# Specify the audio file path
audio_file_path = "c:/Users/Cliff/linux/AlarmProject/alarm.mp3"

# Set the environment variable to play audio through pygame
os.environ['SDL_AUDIODRIVER'] = 'dsp'

# Initialize the mixer module
pygame.mixer.init()

# Create an instance of the AudioVolumeController class
audio_controller = AudioVolumeController()
# Set the volume to maximum
audio_controller.desired_volume(40)
# Restore the volume to the previous level

# Load the audio file
audio = pygame.mixer.Sound(audio_file_path)

# Play the audio
audio.play()

# Wait for the audio to finish playing
while pygame.mixer.get_busy():
    pygame.time.Clock().tick(10)

# Quit pygame
pygame.quit()

#audio_file_path = "file:///c:/Users/Cliff/linux/AlarmProject/alarm.mp3"