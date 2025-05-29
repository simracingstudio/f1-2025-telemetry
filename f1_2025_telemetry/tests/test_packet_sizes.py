"""
Test packet sizes
"""
import ctypes
from f1_2020_telemetry.packets import (
    PacketCarSetupData_V1,
    PacketCarStatusData_V1,
    PacketCarTelemetryData_V1,
    PacketEventData_V1,
    PacketFinalClassificationData_V1,
    PacketLapData_V1,
    PacketLobbyInfoData_V1,
    PacketMotionData_V1,
    PacketParticipantsData_V1,
    PacketSessionData_V1,
)


def test_packet_sizes():
    """Tests that each telemetry packet type has its expected size"""

    assert ctypes.sizeof(PacketMotionData_V1) == 1464
    assert ctypes.sizeof(PacketSessionData_V1) == 251
    assert ctypes.sizeof(PacketLapData_V1) == 1190
    assert ctypes.sizeof(PacketEventData_V1) == 35
    assert ctypes.sizeof(PacketParticipantsData_V1) == 1213
    assert ctypes.sizeof(PacketCarSetupData_V1) == 1102
    assert ctypes.sizeof(PacketCarTelemetryData_V1) == 1307
    assert ctypes.sizeof(PacketCarStatusData_V1) == 1344
    assert ctypes.sizeof(PacketFinalClassificationData_V1) == 839
    assert ctypes.sizeof(PacketLobbyInfoData_V1) == 1169
