'''
Steel Engine REST API module
'''
from openrgb import OpenRGBClient
from openrgb.orgb import Device
from openrgb.utils import DeviceType, RGBColor

class OpenRGBAPI:
    '''
    Class to interact with the OpenRGB service.
    '''

    def __init__(self, port: int = 6742):
        self.__client:OpenRGBClient = None
        self.__keyboards: [Device] = []
        self.__port = port

    def __str__(self) -> str:
        return f"Open RGB API: {self.__port}(port) {len(self.__keyboards)}(keyboards)"

    def connect(self) -> bool:
        '''
        Tries to connect to the service.
        '''
        if not self.is_connected():
            try:
                self.__client = OpenRGBClient(name="AC LEDS", port=self.__port)
                self.__client.clear()
                self.update()
            except Exception as exp:
                print(exp)
        return self.is_connected()

    def disconnect(self) -> bool:
        '''
        Tries to disconnect from the service.
        '''
        if self.is_connected():
            try:
                self.__client.disconnect()
                self.__client = None
            except Exception as exp:
                print(exp)
        return not self.is_connected()

    def is_connected(self) -> bool:
        '''
        Checks the service connection.
        '''
        return self.__client is not None and self.__client.comms.connected

    def is_ready(self) -> bool:
        '''
        Checks if there is supported devices to use.
        '''
        return len(self.__keyboards) > 0

    def set_color(self, color: RGBColor, leds: [str]) -> bool:
        '''
        Sets the color of filtered zones in a device (does not updates the hardware).
        '''
        if self.is_connected():
            for keyboard in self.__keyboards:
                filtered_ids = [led.id for led in keyboard.leds if led.name in leds]
                for led_id in filtered_ids:
                    keyboard.zones[0].colors[led_id] = color
        return self.is_connected()

    def show(self) -> None:
        '''
        Actualy updates the zone colors on hardware.
        '''
        for keyboard in self.__keyboards:
            #print(keyboard.zones[0].leds)
            keyboard.zones[0].show(True)

    def update(self) -> None:
        '''
        Updates supported devices.
        '''
        self.__keyboards = []
        if self.is_connected():
            try:
                self.__client.update()
                self.__keyboards = [device for device in self.__client.ee_devices if device.type == DeviceType.KEYBOARD]
                for keyboard in self.__keyboards:
                    print(f"Keybaord {keyboard.name} leds: {[led for led in keyboard.leds]} zones: {[zone.name for zone in keyboard.zones]}")
            except Exception as exp:
                print(exp)
