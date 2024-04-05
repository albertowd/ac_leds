"""
AC UDP Telemetry test module.
"""

import os
import sys

sys.path.append(os.getcwd())

from ac_leds.ac.udp_telemetry import UDPTelemetry

if __name__ == "__main__":
    telemetry = UDPTelemetry()
    try:
        while not telemetry.is_connected():
            telemetry.connect()
        CCOUNT = 10
        while CCOUNT > 0:
            print("-----------------------------------")
            telemetry.listen()
            print("-----------------------------------")
            CCOUNT -= 1
    except Exception as e:
        print(e)
    telemetry.disconnect()
