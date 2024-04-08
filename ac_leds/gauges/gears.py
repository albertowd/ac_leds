'''
Handles the gear indicator leds.
'''
from openrgb.utils import RGBColor

from ac_leds.ac.udp_packs import CarInfo
from ac_leds.gauges.gauge import Gauge
from ac_leds.open_rgb.colors import BLACK, WHITE

class Gears(Gauge):
    '''
    Handles the gear indicator leds.
    '''

    KEYS = [
        ['Key: `', 'Key: Number Pad -'],
        ['Key: 0', 'Key: Number Pad 0'],
        ['Key: 1', 'Key: Number Pad 1'],
        ['Key: 2', 'Key: Number Pad 2'],
        ['Key: 3', 'Key: Number Pad 3'],
        ['Key: 4', 'Key: Number Pad 4'],
        ['Key: 5', 'Key: Number Pad 5'],
        ['Key: 6', 'Key: Number Pad 6'],
        ['Key: 7', 'Key: Number Pad 7'],
        ['Key: 8', 'Key: Number Pad 8'],
    ]

    def __init__(self) -> None:
        super().__init__()
        self.__gear: int = 1

    def get_colors(self) -> [(RGBColor, [str])]:
        '''
        Calculate the colors and zones of the gauge at current value.
        '''
        blacks = []
        for index, keys in enumerate(Gears.KEYS):
            if index != self.__gear:
                blacks = blacks + keys
        return [
            (BLACK, blacks),
            (WHITE, Gears.KEYS[self.__gear])
        ]

    def update(self, car_info: CarInfo) -> None:
        '''
        Updates internal gauge values.
        '''
        self.__gear = car_info.gear
