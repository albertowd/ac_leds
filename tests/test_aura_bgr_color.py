"""
Aura BGRColor test module.
"""

import os
import sys

sys.path.append(os.getcwd())

from ac_leds.aura.bgr_color import BGRColor

if __name__ == "__main__":
    print(f"BGRColor: {BGRColor(0xAA, 0xBB, 0xCC)}")
