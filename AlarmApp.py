import socket
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import json
import os
from playsound import playsound
import threading

is_playing = False

def get_current_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    return int(volume.GetMasterVolumeLevelScalar() * 100)

def set_volume(volume_level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(volume_level, None)

def set_volume1(left_volume, right_volume):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    
    # Set the left and right channel volumes
    volume.SetChannelVolumeLevelScalar(0, left_volume, None)  # 0 for left channel
    volume.SetChannelVolumeLevelScalar(1, right_volume, None)  # 1 for right channel

def play_alarm():
    try:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        audio_file_path = os.path.join(script_directory, "alarm.mp3")

        # Play the audio file using playsound
        while True:
            playsound(audio_file_path)

            print("Alarm is playing...")
    except Exception as e:
        print(f"Error playing alarm: {str(e)}")


# Create a socket to listen on port 49152
host = socket.gethostbyname(socket.gethostname())  # Your PC's local IP address
port = 49152  # Define the port to listen on
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)

# Start a thread to play the alarm in a loop
alarm_thread = threading.Thread(target=play_alarm)

print("Listening for connections on port 49152...")

while True:
    conn, addr = server_socket.accept()
    print(f"Connection from {addr}")
    
    data = conn.recv(1024).decode()
    if data == "ACTIVATE_ALARM" and not is_playing:
        # Get and save the current volume
        current_volume = get_current_volume()
        if current_volume is not None:
            # Set the volume to max (1.0 represents 100%)
            set_volume1(0.2,0.20)
            # Play the alarm
            alarm_thread.start()
            is_playing = True
            print("Alarm started playing.")
            is_playing = True
            # Send a reply indicating the alarm is active
            conn.send(json.dumps({"status": "ALARM_ACTIVE"}).encode())
        else:
            # Send a reply indicating an error
            conn.send(json.dumps({"status": "ERROR"}).encode())
    elif data == "DEACTIVATE_ALARM" and is_playing:
        is_playing = False
        alarm_thread.join()  # Stop the alarm thread
        print("Alarm stopped.")
        # Set the volume back to the saved volume
        if current_volume is not None:
            set_volume1(current_volume / 100.0,current_volume / 100.0)  # Convert back to scalar
            # Send a reply indicating the alarm is deactivated
            conn.send(json.dumps({"status": "ALARM_DEACTIVATED"}).encode())
        else:
            # Send a reply indicating an error
            conn.send(json.dumps({"status": "ERROR"}).encode())
    else:
        # Send a reply indicating an unknown command
        conn.send(json.dumps({"status": "UNKNOWN_COMMAND"}).encode())

    conn.close()