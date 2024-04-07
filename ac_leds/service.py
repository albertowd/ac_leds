"""
Fuck
"""
import os
import sys

sys.path.append(os.getcwd())

from ac_leds.ac.udp_telemetry import UDPTelemetry
from ac_leds.gauges.gears import Gears
from ac_leds.gauges.rev_bar import RevBar
from ac_leds.open_rgb.api import OpenRGBAPI

if __name__ == "__main__":
    api = OpenRGBAPI()
    gauges = [Gears(), RevBar()]
    telemetry = UDPTelemetry()

    print('Waiting for an Assetto Corsa sessin to be opened...')
    tries = 1
    try:
        while not telemetry.is_connected():
            print(f'Trying to connect ({tries})...')
            telemetry.connect()
            tries += 1
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
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        api.disconnect()

    telemetry.disconnect()
