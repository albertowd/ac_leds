"""
Fuck
"""
import os
import sys

sys.path.append(os.getcwd())

from ac_leds.ac.udp_telemetry import UDPTelemetry
from ac_leds.steel_engine.api import SteelEngineAPI

if __name__ == "__main__":
    api = SteelEngineAPI()
    telemetry = UDPTelemetry()
    try:
        while not telemetry.is_connected():
            telemetry.connect()
        telemetry.start_listening()
    except Exception as e:
        print(e)

    try:
        if api.bind():
            max_rpm: float = 1.0
            api.register()
            while True:
                car_info = telemetry.get_lastest_car_info()
                current_rpm = max(1.0, car_info.engine_rpm)
                max_rpm = max(max_rpm, current_rpm)
                rpm_perc = current_rpm / max_rpm
                print(f"{car_info.engine_rpm}\tRPM: {current_rpm}\tMAX RPM: {max_rpm}\tPERC: {rpm_perc}%\tPERC_INT: {int(rpm_perc * 100.0)}")
                api.send_event(int(rpm_perc * 100.0))
                #time.sleep(1)
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        pass

    telemetry.disconnect()
