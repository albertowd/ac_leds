'''
Handles the pedals indicator leds.
'''
from openrgb.utils import RGBColor

from ac_leds.ac.udp_packs import CarInfo
from ac_leds.gauges.gauge import Gauge
from ac_leds.open_rgb.colors import BLACK, GREEN, RED, YELLOW

class Pedals(Gauge):
    '''
    Handles the pedals indicator leds.
    '''

    def __init__(self) -> None:
        super().__init__()
        self.__abs: bool = False
        self.__brake: float = 0.0
        #self.__clutch: float = 0.0
        self.__gas: float = 0.0
        self.__tc: bool = False

    def get_colors(self) -> [(RGBColor, [str])]:
        '''
        Calculate the colors and zones of the gauge at current value.
        '''
        #if self.__clutch > 0.5:
        #    return [
        #        (WHITE, ['Key: Down Arrow', 'Key: Up Arrow'])
        #    ]
        #else:
        return [
            (YELLOW if self.__tc else GREEN if self.__gas > 0.1 else BLACK, ['Key: Up Arrow']),
            (YELLOW if self.__abs else RED if self.__brake > 0.1 else BLACK, ['Key: Down Arrow'])
        ]

    def update(self, car_info: CarInfo) -> None:
        '''
        Updates internal gauge values.
        '''
        self.__abs = car_info.is_abs_in_action
        self.__brake = car_info.brake
        #self.__clutch = car_info.clutch
        self.__gas = car_info.gas
        self.__tc = car_info.is_tc_in_action
