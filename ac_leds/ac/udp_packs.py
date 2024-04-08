'''
Module to handle AC udp telemetry.
'''

from enum import IntEnum
from struct import calcsize, pack, unpack

class IdentifierID(IntEnum):
    '''
    App type identifier.
    '''
    IPHONE = 0
    IPAD = 1
    ANDROID = 2
    ANDROID_TABLET = 3

class OperationID(IntEnum):
    '''
    Handshake operation identifier.
    '''
    HANDSHAKE = 0
    SUBSCRIBE_UPDATE = 1
    SUBSCRIBE_SPOT = 2
    DISMISS = 3

class Handshake:
    '''
    Handshake structure.
    '''
    FORMAT = '<iii'
    SIZE = calcsize(FORMAT)

    def __init__(self, identifier: IdentifierID, operation_id: OperationID, version: int = 1) -> None:
        self.__identifier: IdentifierID = identifier
        self.__operation_id: OperationID = operation_id
        self.__version: int = version

    def pack(self) -> bytes:
        '''
        Packs the handshake to send it.
        '''
        return pack(Handshake.FORMAT, self.__identifier, self.__version, self.__operation_id)

    def __str__(self) -> str:
        return f'AC UDP Handshake: {self.__identifier}(identifier) {self.__operation_id}(operation) {self.__version}(version)'

class HandshakeResponse:
    '''
    Handshake response structure.
    '''
    FORMAT: str = '<100s100sii100s100s'
    SIZE: int = calcsize(FORMAT)

    def __init__(self, data: bytes) -> None:
        self.__car_name: str
        self.__driver_name: str
        self.__identifier: int
        self.__version: int
        self.__track_name: str
        self.__track_config: str

        (
            self.__car_name, # char x 100
            self.__driver_name, # char x 100
            self.__identifier, # int
            self.__version, # int
            self.__track_name, # char x 100
            self.__track_config # char x 100
        ) = unpack(HandshakeResponse.FORMAT, data)
        self.__parse_unpacked()

    def __parse_unpacked(self) -> None:
        self.__car_name = self.__car_name.decode('utf-16', errors='ignore').split('%')[0]
        self.__driver_name = self.__driver_name.decode('utf-16', errors='ignore').split('%')[0]
        self.__track_name = self.__track_name.decode('utf-16', errors='ignore').split('%')[0]
        self.__track_config = self.__track_config.decode('utf-16', errors='ignore').split('%')[0]

    def __str__(self) -> str:
        return f'AC UDP Handshake Response: {self.__car_name}(carName) {self.__driver_name}(driverName) {self.__identifier}(identifier) {self.__track_config}(trackConfig) {self.__track_name}(trackName) {self.__version} (version)'

class CarInfo:
    '''
    Car info update structure.
    '''
    FORMAT: str = '<4sifff??????2sfffiiiifffffiffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
    SIZE: int = calcsize(FORMAT)

    def __init__(self, data: bytes) -> None:
        self.data = data

        self.identifier: str
        self.size: int

        self.speed_kmh: float
        self.speed_mph: float
        self.speed_ms: float

        self.is_abs_enabled: bool
        self.is_abs_in_action: bool
        self.is_tc_in_action: bool
        self.is_tc_enabled: bool
        self.is_in_pit: bool
        self.is_engine_limiter_on: bool

        self.g_pad: str
        self.g_vertical: float
        self.g_horizontal: float
        self.g_frontal: float

        self.lap_time: int
        self.last_lap: int
        self.best_lap: int
        self.lap_count: int

        self.gas: float
        self.brake: float
        self.clutch: float
        self.engine_rpm: float
        self.steer: float
        self.gear: int
        self.height: float

        self.wheel_angular_speed_fl: float
        self.wheel_angular_speed_fr: float
        self.wheel_angular_speed_rl: float
        self.wheel_angular_speed_rr: float

        self.splip_angle_fl: float
        self.splip_angle_fr: float
        self.splip_angle_rl: float
        self.splip_angle_rr: float

        self.splip_angle_contact_patch_fl: float
        self.splip_angle_contact_patch_fr: float
        self.splip_angle_contact_patch_rl: float
        self.splip_angle_contact_patch_rr: float

        self.slip_ratio_fl: float
        self.slip_ratio_fr: float
        self.slip_ratio_rl: float
        self.slip_ratio_rr: float

        self.tyre_slip_fl: float
        self.tyre_slip_fr: float
        self.tyre_slip_rl: float
        self.tyre_slip_rr: float

        self.nd_slip_fl: float
        self.nd_slip_fr: float
        self.nd_slip_rl: float
        self.nd_slip_rr: float

        self.load_fl: float
        self.load_fr: float
        self.load_rl: float
        self.load_rr: float

        self.dy_fl: float
        self.dy_fr: float
        self.dy_rl: float
        self.dy_rr: float

        self.mz_fl: float
        self.mz_fr: float
        self.mz_rl: float
        self.mz_rr: float

        self.tyre_dirt_level_fl: float
        self.tyre_dirt_level_fr: float
        self.tyre_dirt_level_rl: float
        self.tyre_dirt_level_rr: float

        self.camber_rad_fl: float
        self.camber_rad_fr: float
        self.camber_rad_rl: float
        self.camber_rad_rr: float

        self.tyre_radius_fl: float
        self.tyre_radius_fr: float
        self.tyre_radius_rl: float
        self.tyre_radius_rr: float

        self.tyre_loaded_radius_fl: float
        self.tyre_loaded_radius_fr: float
        self.tyre_loaded_radius_rl: float
        self.tyre_loaded_radius_rr: float

        self.suspension_height_fl: float
        self.suspension_height_fr: float
        self.suspension_height_rl: float
        self.suspension_height_rr: float

        self.car_position_normalized: float
        self.car_slope: float

        self.car_coordinates_x: float
        self.car_coordinates_y: float
        self.car_coordinates_z: float

        (
            self.identifier, #char x 2
            self.size, # int

            self.speed_kmh, # float
            self.speed_mph, # float
            self.speed_ms, # float

            self.is_abs_enabled, # boll
            self.is_abs_in_action, # boll
            self.is_tc_in_action, # boll
            self.is_tc_enabled, # boll
            self.is_in_pit, # boll
            self.is_engine_limiter_on, # boll

            self.g_pad, # unknown
            self.g_vertical, # float
            self.g_horizontal, # float
            self.g_frontal, # float

            self.lap_time, # int
            self.last_lap, # int
            self.best_lap, # int
            self.lap_count, # int

            self.gas, # float
            self.brake, # float
            self.clutch, # float
            self.engine_rpm, # float
            self.steer, # float
            self.gear, # int
            self.height, # float

            self.wheel_angular_speed_fl, # float
            self.wheel_angular_speed_fr, # float
            self.wheel_angular_speed_rl, # float
            self.wheel_angular_speed_rr, # float

            self.splip_angle_fl, # float
            self.splip_angle_fr, # float
            self.splip_angle_rl, # float
            self.splip_angle_rr, # float

            self.splip_angle_contact_patch_fl, # float
            self.splip_angle_contact_patch_fr, # float
            self.splip_angle_contact_patch_rl, # float
            self.splip_angle_contact_patch_rr, # float

            self.slip_ratio_fl, # float
            self.slip_ratio_fr, # float
            self.slip_ratio_rl, # float
            self.slip_ratio_rr, # float

            self.tyre_slip_fl, # float
            self.tyre_slip_fr, # float
            self.tyre_slip_rl, # float
            self.tyre_slip_rr, # float

            self.nd_slip_fl, # float
            self.nd_slip_fr, # float
            self.nd_slip_rl, # float
            self.nd_slip_rr, # float

            self.load_fl, # float
            self.load_fr, # float
            self.load_rl, # float
            self.load_rr, # float

            self.dy_fl, # float
            self.dy_fr, # float
            self.dy_rl, # float
            self.dy_rr, # float

            self.mz_fl, # float
            self.mz_fr, # float
            self.mz_rl, # float
            self.mz_rr, # float

            self.tyre_dirt_level_fl, # float
            self.tyre_dirt_level_fr, # float
            self.tyre_dirt_level_rl, # float
            self.tyre_dirt_level_rr, # float

            self.camber_rad_fl, # float
            self.camber_rad_fr, # float
            self.camber_rad_rl, # float
            self.camber_rad_rr, # float

            self.tyre_radius_fl, # float
            self.tyre_radius_fr, # float
            self.tyre_radius_rl, # float
            self.tyre_radius_rr, # float

            self.tyre_loaded_radius_fl, # float
            self.tyre_loaded_radius_fr, # float
            self.tyre_loaded_radius_rl, # float
            self.tyre_loaded_radius_rr, # float

            self.suspension_height_fl, # float
            self.suspension_height_fr, # float
            self.suspension_height_rl, # float
            self.suspension_height_rr, # float

            self.car_position_normalized, # float
            self.car_slope, # float

            self.car_coordinates_x, # float
            self.car_coordinates_y, # float
            self.car_coordinates_z # float
        ) = unpack(CarInfo.FORMAT, data)
        self.identifier = self.identifier.decode('utf-16', errors='ignore')

    def __str__(self) -> str:
        return f'AC Car Info: {self.__dict__}'
