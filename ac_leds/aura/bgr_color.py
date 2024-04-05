"""
Module to handle BGR Colors
"""

B_MASK = 0xFF0000
G_MASK = 0x00FF00
R_MASK = 0x0000FF

class BGRColor:
    """
    Base class for the color.
    """

    def __init__(self, b: int = 0xFF, g: int = 0xFF, r: int = 0xFF) -> None:
        self.__b = b
        self.__g = g
        self.__r = r
        self.__int = int(self)

    def __index__(self) -> int:
        b: int = self.__b << 16
        g: int = self.__g << 8
        return b + g + self.__r

    def __str__(self) -> str:
        return f"BGRColor: {int(self)} | {hex(self)} | rgb({self.__r}, {self.__g}, {self.__b})"

    def __hex__(self) -> str:
        """
        Converts the values to the BGR string format.
        """
        return hex(self.__int)
