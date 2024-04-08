'''
Handles the steer indicator leds.
'''
from openrgb.utils import RGBColor

from ac_leds.ac.udp_packs import CarInfo
from ac_leds.gauges.gauge import Gauge
from ac_leds.open_rgb.colors import BLACK, BLUE

class Steer(Gauge):
    '''
    Handles the steer indicator leds.
    '''

    def __init__(self) -> None:
        super().__init__()
        self.__steer: float = 0.0

    def get_colors(self) -> [(RGBColor, [str])]:
        '''
        Calculate the colors and zones of the gauge at current value.
        '''
        return [
            (BLUE if self.__steer < -0.1 else BLACK, ['Key: Left Arrow']),
            (BLUE if self.__steer > 0.1 else BLACK, ['Key: Right Arrow'])
        ]

    def update(self, car_info: CarInfo) -> None:
        '''
        Updates internal gauge values.
        '''
        self.__steer = car_info.steer
