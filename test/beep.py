import subprocess
import os

# Change this path if needed
BEEP_PATH = "/home/leptos/Desktop/LEPTOSIGHT/assets/system/beep.wav"

print("Testing beep...")

try:
    subprocess.Popen(["paplay", BEEP_PATH])
    print("Beep command sent!")
except Exception as e:
    print("Error:", e)
