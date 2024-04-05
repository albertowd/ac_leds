"""
Aura API test module.
"""

import os
import sys

sys.path.append(os.getcwd())

from time import sleep
from ac_leds.aura.api import AuraAPI
from ac_leds.aura.bgr_color import BGRColor
from ac_leds.aura.device_color import AuraDeviceColor
from ac_leds.aura.keyboard import ROGFunctionKeys

if __name__ == "__main__":
    api = AuraAPI()
    try:
        print(api)
        if api.connect():
            print(api)
            api.get_devices()
            print(api)
            print(f"API Has Keyboard Device: {api.has_device_type('Keyboard')}")
            if api.has_device_type('Keyboard'):
                COUNT = 5
                while COUNT > 0:
                    RGB = int(255 / COUNT)
                    COLOR = BGRColor(RGB, RGB, RGB)
                    COLORS: [AuraDeviceColor] = [
                        AuraDeviceColor(color = COLOR, key_codes=[str(e.value) for e in ROGFunctionKeys]),
                        AuraDeviceColor(color = COLOR, device = "Mouse"),
                    ]
                    print(f"API Set Colors: {COLORS} => {api.set_colors(COLORS)}")
                    sleep(1)
                    COUNT -= 1
                #print(f"API Set Key Color: {set_key_color(True, 255, 'Keyboard', 3, 0)}")
    except Exception as e:
        print(e)
    print(f"API shutdown: {api.shutdown()}")
