"""
Module to handle AC udp telemetry.
"""

from enum import IntEnum
from struct import calcsize, pack, unpack

class IdentifierID(IntEnum):
    """
    App type identifier.
    """
    IPHONE = 0
    IPAD = 1
    ANDROID = 2
    ANDROID_TABLET = 3

class OperationID(IntEnum):
    """
    Handshake operation identifier.
    """
    HANDSHAKE = 0
    SUBSCRIBE_UPDATE = 1
    SUBSCRIBE_SPOT = 2
    DISMISS = 3

class Handshake:
    """
    Handshake structure.
    """
    FORMAT = "<iii"
    SIZE = calcsize(FORMAT)

    def __init__(self, identifier: IdentifierID, operation_id: OperationID, version: int = 1) -> None:
        self.__identifier: IdentifierID = identifier
        self.__operation_id: OperationID = operation_id
        self.__version: int = version

    def pack(self) -> bytes:
        """
        Packs the handshake to send it.
        """
        return pack(Handshake.FORMAT, self.__identifier, self.__version, self.__operation_id)

    def __str__(self) -> str:
        return f"AC UDP Handshake: {self.__identifier}(identifier) {self.__operation_id}(operation) {self.__version}(version)"

class HandshakeResponse:
    """
    Handshake response structure.
    """
    FORMAT: str = "<100s100sii100s100s"
    SIZE: int = calcsize(FORMAT)

    def __init__(self, data: bytes) -> None:
        (
            self.__car_name,
            self.__driver_name,
            self.__identifier,
            self.__version,
            self.__track_name,
            self.__track_config
        ) = unpack(HandshakeResponse.FORMAT, data)
        self.__parse_unpacked()

    def __parse_unpacked(self) -> None:
        self.__car_name = self.__car_name.decode("utf-16", errors='ignore').split("%")[0]
        self.__driver_name = self.__driver_name.decode("utf-16", errors='ignore').split("%")[0]
        self.__track_name = self.__track_name.decode("utf-16", errors='ignore').split("%")[0]
        self.__track_config = self.__track_config.decode("utf-16", errors='ignore').split("%")[0]

    def __str__(self) -> str:
        return f"AC UDP Handshake Response: {self.__car_name}(carName) {self.__driver_name}(driverName) {self.__identifier}(identifier) {self.__track_config}(trackConfig) {self.__track_name}(trackName) {self.__version} (version)"

class CarInfo:
    """
    Car info update structure.
    """
    FORMAT: str = "<4sifff??????2sfffiiiifffffiffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    SIZE: int = calcsize(FORMAT)

    def __init__(self, data: bytes) -> None:
        (
            self.identifier,
            self.size,

            self.speed_kmh,
            self.speed_mph,
            self.speed_ms,

            self.is_abs_enabled,
            self.is_abs_in_action,
            self.is_tc_in_action,
            self.is_tc_enabled,
            self.is_in_pit,
            self.is_engine_limiter_on,

            self.g_pad,
            self.g_vertical,
            self.g_horizontal,
            self.g_frontal,

            self.lap_time,
            self.last_lap,
            self.best_lap,
            self.lap_count,

            self.gas,
            self.brake,
            self.clutch,
            self.engine_rpm,
            self.steer,
            self.gear,
            self.height,

            self.wheel_angular_speed_fl,
            self.wheel_angular_speed_fr,
            self.wheel_angular_speed_rl,
            self.wheel_angular_speed_rr,

            self.splip_angle_fl,
            self.splip_angle_fr,
            self.splip_angle_rl,
            self.splip_angle_rr,

            self.splip_angle_contact_patch_fl,
            self.splip_angle_contact_patch_fr,
            self.splip_angle_contact_patch_rl,
            self.splip_angle_contact_patch_rr,

            self.slip_ratio_fl,
            self.slip_ratio_fr,
            self.slip_ratio_rl,
            self.slip_ratio_rr,

            self.tyre_slip_fl,
            self.tyre_slip_fr,
            self.tyre_slip_rl,
            self.tyre_slip_rr,

            self.nd_slip_fl,
            self.nd_slip_fr,
            self.nd_slip_rl,
            self.nd_slip_rr,

            self.load_fl,
            self.load_fr,
            self.load_rl,
            self.load_rr,

            self.dy_fl,
            self.dy_fr,
            self.dy_rl,
            self.dy_rr,

            self.mz_fl,
            self.mz_fr,
            self.mz_rl,
            self.mz_rr,

            self.tyre_dirt_level_fl,
            self.tyre_dirt_level_fr,
            self.tyre_dirt_level_rl,
            self.tyre_dirt_level_rr,

            self.camber_rad_fl,
            self.camber_rad_fr,
            self.camber_rad_rl,
            self.camber_rad_rr,

            self.tyre_radius_fl,
            self.tyre_radius_fr,
            self.tyre_radius_rl,
            self.tyre_radius_rr,

            self.tyre_loaded_radius_fl,
            self.tyre_loaded_radius_fr,
            self.tyre_loaded_radius_rl,
            self.tyre_loaded_radius_rr,

            self.suspension_height_fl,
            self.suspension_height_fr,
            self.suspension_height_rl,
            self.suspension_height_rr,

            self.car_position_normalized,
            self.car_slope,

            self.car_coordinates_x,
            self.car_coordinates_y,
            self.car_coordinates_z
        ) = unpack(CarInfo.FORMAT, data)
        self.identifier = self.identifier.decode("utf-16")

    def __str__(self) -> str:
        return f"AC Car Info: {self.__dict__}"
