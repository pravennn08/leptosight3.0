import subprocess
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BEEP_PATH = os.path.join(BASE_DIR, "assets", "system", "beep.wav")


def beep(self):
    try:
        subprocess.Popen(["paplay", BEEP_PATH])
    except Exception as e:
        print("Beep error:", e)
