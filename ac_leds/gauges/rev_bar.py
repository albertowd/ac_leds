'''
Handles the rev indicator leds.
'''
from openrgb.utils import RGBColor

from ac_leds.ac.udp_packs import CarInfo
from ac_leds.gauges.gauge import Gauge
from ac_leds.open_rgb.colors import BLACK, BLUE, GREEN, RED

class RevBar(Gauge):
    '''
    Handles the rev indicator leds.
    '''

    GRB = [
        GREEN,
        GREEN,
        GREEN,
        GREEN,
        RED,
        RED,
        RED,
        RED,
        BLUE,
        BLUE,
        BLUE,
        BLUE
    ]

    RB = [
        RED,
        RED,
        RED,
        RED,
        RED,
        RED,
        BLUE,
        BLUE,
        BLUE,
        BLUE,
        BLUE,
        BLUE
    ]

    KEYS = [
        'Key: F1',
        'Key: F2',
        'Key: F3',
        'Key: F4',
        'Key: F5',
        'Key: F6',
        'Key: F7',
        'Key: F8',
        'Key: F9',
        'Key: F10',
        'Key: F11',
        'Key: F12'
    ]

    def __init__(self) -> None:
        super().__init__()
        self.__current_rpm = 1.0
        self.__max_rpm = self.__current_rpm

    def get_colors(self) -> [(RGBColor, [str])]:
        '''
        Calculate the colors and zones of the gauge at current value.
        '''
        rpm_perc = self.__current_rpm / self.__max_rpm
        filter_lights = int(rpm_perc * 11.0)
        return [(color, [RevBar.KEYS[index]]) for index, color in enumerate(RevBar.GRB)] + [(BLACK, RevBar.KEYS[filter_lights + 1:])]

    def update(self, car_info: CarInfo) -> None:
        '''
        Updates internal gauge values.
        '''
        self.__current_rpm = max(1.0, car_info.engine_rpm)
        self.__max_rpm = max(self.__max_rpm, self.__current_rpm)
