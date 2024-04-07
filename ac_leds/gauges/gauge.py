'''
Base class for led gauges.
'''
from openrgb.utils import RGBColor

from ac_leds.ac.udp_packs import CarInfo

class Gauge:
    '''
    Base class for led gauges.
    '''

    def get_colors(self) -> [(RGBColor, [str])]:
        '''
        Calculate the colors and zones of the gauge at current value.
        '''
        return []

    def update(self, car_info: CarInfo) -> None:
        '''
        Updates internal gauge values.
        '''
