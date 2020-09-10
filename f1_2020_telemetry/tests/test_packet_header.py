import ctypes

from ..packets import PacketHeader


def test_packet_header():
    expected_header_size = ctypes.sizeof(PacketHeader)

    # Penalty 5, Infringement 27, lapNum 2, otherVehicleId = 255, placesGained = 0, time = 255, vehicleIdx = 14
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
