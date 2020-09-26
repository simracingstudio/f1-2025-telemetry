"""
Test packet header size and features
"""
import ctypes
from f1_2020_telemetry.packets import PacketHeader


def test_packet_header_109():
    """Test version 1.09 packet header"""

    data = b"\xe4\x07\x01\t\x01\x03\xa3\x80\x9atC\xc0\x8e}:\x11\tD\xab\\\x00\x00\xff\xffPENA\x05\x07\x04\xff\xff\x05\x00"
    header = PacketHeader.from_buffer_copy(data)

    assert header.packetFormat == 2020
    assert header.gameMajorVersion == 1
    assert header.gameMinorVersion == 9


def test_packet_header():
    """Test packet header expected fields"""

    expected_header_size = ctypes.sizeof(PacketHeader)

    event_data = b"\xe4\x07\x01\x08\x01\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00PENA\x05\x1b\x0e\xff\xff\x02\x00"
    header = PacketHeader.from_buffer_copy(event_data)

    assert ctypes.sizeof(header) == expected_header_size

    assert header.packetFormat == 2020
    assert header.gameMajorVersion == 1
    assert header.gameMinorVersion == 8
    assert header.packetVersion == 1
    assert header.packetId == 3  # Event
    assert header.sessionUID == 0
    assert header.sessionTime == 0
    assert header.frameIdentifier == 0
    assert header.playerCarIndex == 0
    assert header.secondaryPlayerCarIndex == 0
