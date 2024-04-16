'''
Main service script
'''
import os
import sys

sys.path.append(os.getcwd())

import time

from ac_leds.ac.udp_telemetry import UDPTelemetry
from ac_leds.gauges.gears import Gears
from ac_leds.gauges.pedals import Pedals
from ac_leds.gauges.rev_bar import RevBar
from ac_leds.gauges.steer import Steer
from ac_leds.open_rgb.api import OpenRGBAPI

if __name__ == '__main__':
    api = OpenRGBAPI()
    gauges = [Gears(), Pedals(), RevBar(), Steer()]
    telemetry = UDPTelemetry()
    tries = 1

    print('Waiting for an Assetto Corsa sessin to be opened...')
    try:
        while not telemetry.is_connected():
            print(f'Trying to connect ({tries})...')
            telemetry.connect()
            tries += 1
            time.sleep(1)
        telemetry.start_listening()
    except Exception as e:
        print(e)

    try:
        if api.connect() and api.is_ready():
            while True:
                car_info = telemetry.get_lastest_car_info()
                if car_info is not None:
                    for gauge in gauges:
                        gauge.update(car_info)
                    for gauge in gauges:
                        for color, zones in gauge.get_colors():
                            api.set_color(color, zones)
                    api.show()
                    time.sleep(0.1)
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        pass

    try:
        if api.is_connected():
            api.disconnect()
    except Exception as e:
        print(e)

    try:
        if telemetry.is_connected():
            telemetry.disconnect()
    except Exception as e:
        print(e)
