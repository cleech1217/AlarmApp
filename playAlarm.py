import threading
import time
from playsound import playsound
import logging
import os

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

def do_something():
    global is_playing
    
    try:
        while not stop_event.is_set():
            logger.info("Try playing audio: " + AUDIO_FILE_PATH)
            playsound(AUDIO_FILE_PATH)
            logger.info("Playing audio: " + AUDIO_FILE_PATH)
            time.sleep(5)
    except Exception as e:
        logger.error(e)
    finally:
        logger.info("Playback complete.")
        is_playing = False

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
        is_playing = False
    else:
        logger.info("Thread is not running.")