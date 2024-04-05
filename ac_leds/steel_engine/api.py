"""
Steel Engine REST API module
"""
from json import load
from os import getenv, path
from threading import Thread
from requests import post

class SteelEngineAPI:
    """
    Class to interact with the Aura API service.
    """
    CORE_PROPS_WIN = path.join(getenv("PROGRAMDATA"), "SteelSeries", "SteelSeries Engine 3", "coreProps.json")
    CORE_PROPS_OSX = path.join("/Library", "Application Support", "SteelSeries Engine 3", "coreProps.json")
    REQUEST_TIMEOUT = 10

    def __init__(self):
        self.__base_url = None
        self.__bound = False
        try:
            with open(SteelEngineAPI.CORE_PROPS_WIN, encoding="utf-8") as file:
                core_props = load(file)
                self.__base_url = f"http://{core_props['address']}"
        except Exception as e:
            print(e)

        if self.__base_url is None:
            try:
                with open(SteelEngineAPI.CORE_PROPS_OSX, encoding="utf-8") as file:
                    core_props = load(file)
                    self.__base_url = f"http://{core_props['address']}"
            except Exception as e:
                print(e)
                raise e

    def __str__(self) -> str:
        return f"SteelEngineAPI: {self.__base_url}(url) {self.__bound}(bound)"

    def bind(self) -> bool:
        """
        Binds the API effect over the Steel Engine service.
        """
        if not self.is_bound() and self.__base_url is not None:
            try:
                response = post(f"{self.__base_url}/bind_game_event", json={
                    "event": "RPM_BAR",
                    "game": "ASSETTO_CORSA",
                    "handlers": [
                        {
                            "device-type": "rgb-per-key-zones",
                            "color": {
                                "blue": 0,
                                "green": 255,
                                "red": 0
                            },
                            "mode": "percent",
                            "zone": "function-keys"
                        }
                    ],
                    "icon_id": 5, # Explosion icon
                    "max_value": 100,
                    "min_value": 0
                }, timeout=SteelEngineAPI.REQUEST_TIMEOUT)
                if response.status_code == 200:
                    self.__bound = True
            except Exception as e:
                print(e)

        return self.is_bound()

    def heart_beat(self) -> bool:
        """
        Sends a heart beat to the API so the service do not stop it while inactive.
        """
        if self.is_bound():
            try:
                response = post(f"{self.__base_url}/game_heartbeat", json={"game": "ASSETTO_CORSA"}, timeout=SteelEngineAPI.REQUEST_TIMEOUT)
                return response.status_code == 200
            except Exception as e:
                print(e)
        return False

    def is_bound(self) -> bool:
        """
        Checcks if its bound to the API.
        """
        return self.__bound

    def register(self) -> None:
        """
        Registers the game metatada on the API service.
        """
        if self.is_bound():
            try:
                response = post(f"{self.__base_url}/game_metadata", json={
                    "developer": "Alberto Wollmann Dietrich",
                    "game": "ASSETTO_CORSA",
                    "game_display_name": "Assetto Corsa",
                }, timeout=SteelEngineAPI.REQUEST_TIMEOUT)
                return response.status_code == 200
            except Exception as e:
                print(e)
        return False

    def send_event(self, value: int) -> bool:
        """
        Sets the color of all lights of a device.
        """
        if self.is_bound():
            response = post(f"{self.__base_url}/game_event", json={
                "data": {
                    "value": value
                },
                "event": "RPM_BAR",
                "game": "ASSETTO_CORSA"
            }, timeout=SteelEngineAPI.REQUEST_TIMEOUT)
            return response.status_code == 200
        return False

    def start_heart_beat(self) -> None:
        """
        Starts a thread to send the heart beat event.
        """
        Thread(target=self.heart_beat).start()
