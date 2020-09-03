#! /usr/bin/env python3

import time
import sys

from collections import namedtuple, Counter

from PyQt5.QtCore import QObject, pyqtSignal, QAbstractListModel, QVariant, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QLabel,
    QListView,
)
from PyQt5.QtNetwork import QAbstractSocket, QUdpSocket

from f1_2020_telemetry.packets import PacketID, unpack_udp_packet, UnpackError

IncomingPacket = namedtuple(
    "IncomingPacket", "timestamp, recv_port, src_address, src_port, packet"
)


class Session(QObject):
    def __init__(self, sessionUID, first_timestamp, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sessionUID = sessionUID
        self.first_timestamp = first_timestamp
        self.counter = 0
        self.cmap = Counter()

    def processIncomingPacket(self, incomingPacket):
        packet_id = PacketID(incomingPacket.packet.header.packetId)
        self.counter += 1
        self.cmap[packet_id] += 1
        # print(self.sessionUID, self.counter, self.cmap)
        if packet_id == PacketID.PARTICIPANTS:
            print(incomingPacket)


class SessionManager(QObject):

    updated = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sessions = {}
        self.session_list = []

    def processIncomingPacket(self, incomingPacket):
        sessionUID = incomingPacket.packet.header.sessionUID
        if sessionUID not in self.sessions:
            new_session = Session(sessionUID, incomingPacket.timestamp)
            self.sessions[sessionUID] = new_session
            self.session_list.append(new_session)
            self.updated.emit()
        self.sessions[sessionUID].processIncomingPacket(incomingPacket)

    def count(self):
        return len(self.session_list)

    def getSession(self, index):
        return self.session_list[index]


class SessionManagerListModel(QAbstractListModel):
    def __init__(self, sessionManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sessionManager = sessionManager
        self.sessionManager.updated.connect(self.reset)

    def rowCount(self, parent):
        if parent.isValid():
            print("YIKES!")
            return 0
        return self.sessionManager.count()

    def data(self, index, role):
        if role == Qt.DisplayRole:
            session = self.sessionManager.getSession(index.row())
            d = f"{session.sessionUID:016x}"
            return d
        return None

    def reset(self):
        self.beginResetModel()
        self.endResetModel()


class MyCentralWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QHBoxLayout()
        left = QListView()
        app = QApplication.instance()
        smlm = SessionManagerListModel(app.sessionManager)
        left.setModel(smlm)
        right = QLabel("Right")
        layout.addWidget(left)
        layout.addWidget(right)
        self.setLayout(layout)


class MyMainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        centralWidget = MyCentralWidget()
        self.setCentralWidget(centralWidget)


class UdpSocketMonitor(QObject):

    incomingPacket = pyqtSignal(IncomingPacket)

    def __init__(self, port, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.port = port

        # Bind mode: either QAbstractSocket.ShareAddress or QAbstractSocket.ReuseAddressHint.
        #
        # Linux ShareAddress           -- works
        # MacOS ShareAddress
        # Win10 ShareAddress
        #
        # Linux ReuseAddressHint
        # MacOS ReuseAddressHint
        # Win10 ReuseAddressHint

        self.sock = QUdpSocket()
        self.sock.bind(self.port, QAbstractSocket.ShareAddress)
        self.sock.readyRead.connect(self.readSocketData)

    def readSocketData(self):
        while self.sock.hasPendingDatagrams():
            timestamp = time.time()
            (datagram, address, port) = self.sock.readDatagram(2048)
            try:
                packet = unpack_udp_packet(datagram)
                incoming_packet = IncomingPacket(
                    timestamp, self.port, address.toString(), port, packet
                )
                self.incomingPacket.emit(incoming_packet)
            except UnpackError:
                pass


class NetworkMonitor(QObject):

    incomingPacket = pyqtSignal(IncomingPacket)

    def __init__(self, ports, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.udp_port_monitors = []
        for port in ports:
            udp_port_monitor = UdpSocketMonitor(port)
            udp_port_monitor.incomingPacket.connect(self.incomingPacket)
            self.udp_port_monitors.append(udp_port_monitor)


class MyApplication(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.networkMonitor = NetworkMonitor([20777])
        self.sessionManager = SessionManager()

        self.networkMonitor.incomingPacket.connect(
            self.sessionManager.processIncomingPacket
        )

        self.mainWindow = MyMainWindow()
        self.mainWindow.show()


app = None


def main():
    global app
    app = MyApplication(sys.argv)
    return QApplication.exec_()


if __name__ == "__main__":
    exitcode = main()
    sys.exit(exitcode)
