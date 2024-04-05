"""
Aura Device Color module
"""

from ac_leds.aura.bgr_color import BGRColor

class AuraDeviceColor:
    """
    Class to make device color definitions.
    """

    def __init__(self, apply: bool = True, color: BGRColor = BGRColor(), device: str = "Keyboard", key_codes: [str] = [], x: int = 0, y: int = 0):
        self.__apply = apply
        self.__color = color
        self.__device = device
        self.__key_codes = key_codes
        self.__x = x
        self.__y = y

    def to_rest(self) -> dict:
        """
        Converts the device color to the rest object being expected.
        """
        obj = {
            "apply": "true" if self.__apply else "false",
            "color": str(int(self.__color)),
            "device": self.__device,
            "range": "custom" if len(self.__key_codes) > 0 or self.__x > 0 or self.__y > 0 else "all"
        }
        if len(self.__key_codes) > 0:
            obj["keycode"] = self.__key_codes
        elif self.__x > 0 or self.__y > 0:
            obj["x"] = self.__x
            obj["y"] = self.__y
        return obj

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"AuraDeviceColor {self.__apply}(apply) {self.__color} {self.__device}(device) {self.__key_codes}(key_codes) {self.__x}(x) {self.__y}(y)"
