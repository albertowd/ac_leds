"""
Fuck
"""
import os
import sys

sys.path.append(os.getcwd())

from ac_leds.ac.udp_telemetry import UDPTelemetry
from ac_leds.aura.api import AuraAPI
from ac_leds.aura.bgr_color import BGRColor
from ac_leds.aura.device_color import AuraDeviceColor
from ac_leds.aura.keyboard import ROGFunctionKeys, ROG_NPAD_GEARS

if __name__ == "__main__":
    api = AuraAPI()
    telemetry = UDPTelemetry()
    try:
        while not telemetry.is_connected():
            telemetry.connect()
        telemetry.start_listening()
    except Exception as e:
        print(e)

    try:
        if api.connect():
            api.get_devices()
            if api.has_device_type('Keyboard'):
                max_rpm: float = 1.0
                while True:
                    car_info = telemetry.get_lastest_car_info()
                    current_rpm = max(1.0, car_info.engine_rpm)
                    max_rpm = max(max_rpm, current_rpm)
                    rpm_perc = current_rpm / max_rpm
                    print(f"RPM: {current_rpm}\tMAX RPM: {max_rpm}\tPERC: {rpm_perc}\tTotal Keys:{int(rpm_perc * 12)}")
                    gear_codes = [str(k) for k in ROG_NPAD_GEARS[car_info.gear]]
                    key_codes = [str(k.value) for k in ROGFunctionKeys][:int(rpm_perc * 12)]
                    #print(key_codes)
                    reset_colors = AuraDeviceColor(apply = False, color = BGRColor(0x00, 0x00, 0x00))
                    rev_colors = AuraDeviceColor(apply = False, color = BGRColor(0x00, 0xFF, 0x00), key_codes=key_codes)
                    gear_colors = AuraDeviceColor(color = BGRColor(0x00, 0x00, 0xFF), key_codes=gear_codes)
                    api.set_colors([reset_colors, rev_colors, gear_colors])
                    #time.sleep(1)
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        pass

    telemetry.disconnect()
    api.shutdown()
