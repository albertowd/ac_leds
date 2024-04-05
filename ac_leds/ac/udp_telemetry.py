"""
Module to handle AC udp telemetry.
"""
from socket import AF_INET, SOCK_DGRAM, socket
from threading import Lock, Thread

from ac_leds.ac.udp_packs import CarInfo, Handshake, HandshakeResponse, IdentifierID, OperationID

class UDPTelemetry:
    """
    Base class to keep data connection.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 9996) -> None:
        self.__host = host
        self.__lastest_car_info: CarInfo = None
        self.__lock = Lock()
        self.__port = port
        self.__response: HandshakeResponse = None
        self.__socket: socket = None

    def connect(self) -> bool:
        """
        If not cconnected, connects with the server.
        """
        if not self.is_connected():
            try:
                self.__socket: socket = socket(AF_INET, SOCK_DGRAM)
                self.__socket.connect((self.__host, self.__port))
                handshake: Handshake = Handshake(IdentifierID.ANDROID, OperationID.HANDSHAKE)
                print(handshake)
                self.__socket.sendall(handshake.pack())
                self.__response = HandshakeResponse(self.__socket.recv(HandshakeResponse.SIZE))
                print(self.__response)
                subscribe: Handshake = Handshake(IdentifierID.ANDROID, OperationID.SUBSCRIBE_UPDATE)
                print(subscribe)
                self.__socket.sendall(subscribe.pack())
            except Exception as e: # pylint: disable=broad-exception-caught
                print("Could not connect to the UDP server.")
                print(e)

        return self.is_connected()

    def disconnect(self) -> None:
        """
        If connected, disconnects from the server.
        """
        self.set_latest_car_info(None)
        self.__response = None
        if self.__socket is not None:
            handshake: Handshake = Handshake(IdentifierID.ANDROID, OperationID.DISMISS)
            print(handshake)
            self.__socket.sendall(handshake.pack())
            self.__socket.close()
            self.__socket = None

    def get_lastest_car_info(self) -> CarInfo:
        """
        Retrieves the latest car info from the thread.
        """
        with self.__lock:
            return self.__lastest_car_info

    def is_connected(self) -> bool:
        """
        Checks if there is connection.
        """
        return self.__socket is not None and self.__response is not None

    def listen(self) -> CarInfo:
        """
        Listens to new UDP updates.
        """
        while self.is_connected():
            self.set_latest_car_info(CarInfo(self.__socket.recv(CarInfo.SIZE)))
            #print()
            #print(self.get_lastest_car_info())
            #print()

    def set_latest_car_info(self, car_info: CarInfo) -> None:
        """
        Updates the latest car info received.
        """
        with self.__lock:
            self.__lastest_car_info = car_info

    def start_listening(self) -> None:
        """
        Starts a thread to be listening to UDP packets.
        If nos started, the packets will be delayed because
        the socket reads them in received order.
        """
        Thread(target=self.listen).start()
