import threading
import time
from playsound import playsound
import logging
import os
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Thread control
is_playing = False
stop_event = threading.Event()
audio_thread = None

# Constants
SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
AUDIO_FILE_PATH = os.path.join(SCRIPT_DIRECTORY, "alarm.mp3")
current_volume = 0
MAX_VOLUME = 0.4

def do_something():
    global is_playing
    current_volume = get_current_volume()
    try:
        while not stop_event.is_set():

            set_volume(MAX_VOLUME,MAX_VOLUME) # Set volume to maximum
            playsound(AUDIO_FILE_PATH) #play the alarm file
            is_playing = True #set playing flag

    except Exception as e:
        logger.error(e)
    finally:

        set_volume(current_volume/100,current_volume/100) #Revert volume to previous value

        is_playing = False #set playing flag

def start_thread():
    global audio_thread, is_playing

    if is_playing:
        logger.info("Thread is already running.")
        return
    is_playing = True
    audio_thread = threading.Thread(target=do_something)
    audio_thread.start()
    logger.info("Thread started.")

def stop_thread():
    global audio_thread, is_playing
    if audio_thread and audio_thread.is_alive():
        stop_event.set()
        audio_thread.join()
        logger.info("Thread stopped.")
        stop_event.clear()
        is_playing = False #set playing flag
    else:
        logger.info("Thread is not running.")

def get_current_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    logger.info("Getting current volume: ")
    return int(volume.GetMasterVolumeLevelScalar() * 100)

def set_volume(left_volume, right_volume):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    
    # Set the left and right channel volumes
    volume.SetChannelVolumeLevelScalar(0, left_volume, None)  # 0 for left channel
    volume.SetChannelVolumeLevelScalar(1, right_volume, None)  # 1 for right channel