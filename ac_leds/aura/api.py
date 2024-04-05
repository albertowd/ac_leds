"""
Aura REST API module
"""
from requests import get, post, put, delete

from ac_leds.aura.device_color import AuraDeviceColor


class AuraAPI:
    """
    Class to interact with the Aura API service.
    """
    BASE_URL = "http://127.0.0.1:27339/AuraSDK"
    REQUEST_TIMEOUT = 10

    def __init__(self):
        self.__connected = False
        self.__devices = {}

    def __str__(self) -> str:
        return f"AuraAPI connected: {self.is_connected()} devices: {self.__devices}"

    def connect(self) -> bool:
        """
        Initializes the API control over the Aura service.
        """
        if not self.is_connected():
            try:
                response = post(AuraAPI.BASE_URL, json={"category": "SDK"}, timeout=AuraAPI.REQUEST_TIMEOUT)
                if response.status_code == 200:
                    result = int(response.json()['result'])
                    self.__connected = result == 0
            except Exception as e:
                print(e)

        return self.is_connected()

    def get_devices(self, force_update = False) -> dict:
        """
        Returns a list of devices found.
        """
        if self.is_connected() and (len(self.__devices) == 0 or force_update):
            self.update()
        return self.__devices

    def has_device_type(self, device_type: str) -> bool:
        """
        Checks if there is a device type available.
        """
        for dev_type in self.__devices:
            if dev_type == device_type:
                return True
        return False

    def is_connected(self) -> bool:
        """
        Checcks if its connected.
        """
        return self.__connected

    def set_colors(self, device_color: [AuraDeviceColor]) -> int:
        """
        Sets the color of all lights of a device.
        """
        if self.is_connected():
            response = put(f"{AuraAPI.BASE_URL}/AuraDevice", json={
                "data": list(map(lambda colors: colors.to_rest(), device_color))
            }, timeout=AuraAPI.REQUEST_TIMEOUT)
            if response.status_code == 200:
                return int(response.json()['result'])
        return -1

    def shutdown(self) -> bool:
        """
        Finalizes the API control over the Aura service.
        """
        try:
            response = delete(AuraAPI.BASE_URL, timeout=AuraAPI.REQUEST_TIMEOUT)
            if response.status_code == 200:
                self.__connected = False
        except Exception as e:
            print(e)
        return not self.is_connected()

    def update(self) -> None:
        """
        Updates the availabled cached device dict.
        """
        self.__devices.clear()
        try:
            response = get(f"{AuraAPI.BASE_URL}/AuraDevice", timeout=AuraAPI.REQUEST_TIMEOUT)
            if response.status_code == 200:
                devices = response.json()
                for key in devices:
                    if key not in ["count", "result"]:
                        self.__devices[key] = devices[key]
                self.update_layout()
        except Exception as e:
            print(e)

    def update_layout(self) -> None:
        """
        Updates the lights layout of a cached device.
        """
        for key, device in self.__devices.items():
            try:
                response = get(f"{AuraAPI.BASE_URL}/{key}/layout", timeout=AuraAPI.REQUEST_TIMEOUT)
                if response.status_code == 200:
                    device["layout"] = response.json()
                    del device["layout"]["result"]
            except Exception as e:
                print(e)
